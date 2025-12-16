# backend/rag_utils.py
import os, json
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

# Path relative to project root (2 levels up from backend/)
BASE = os.path.join(os.path.dirname(__file__), "..")
INDEX_PATH = os.path.join(BASE, "embeddings", "resume.index")
META_PATH = os.path.join(BASE, "embeddings", "resume_meta.json")

# ============================================================================
# MEMORY OPTIMIZATION: Load models once at module import (not per-request)
# This ensures models are shared across all requests and workers
# Critical for Render free tier memory limits
# ============================================================================

print("🔄 Loading embedding model (one-time at startup)...")
embedder = SentenceTransformer("all-MiniLM-L6-v2")
print("✓ Embedding model loaded")

print("🔄 Loading FAISS index...")
if not os.path.exists(INDEX_PATH):
    raise FileNotFoundError(f"FAISS index not found at {INDEX_PATH}. Run index_documents.py first.")
index = faiss.read_index(INDEX_PATH)
print("✓ FAISS index loaded")

print("🔄 Loading metadata...")
if not os.path.exists(META_PATH):
    raise FileNotFoundError(f"Metadata not found at {META_PATH}. Run index_documents.py first.")
with open(META_PATH, "r", encoding="utf-8") as f:
    meta = json.load(f)
print(f"✓ Metadata loaded ({len(meta)} chunks)")

# ============================================================================

def retrieve(query, top_k=2):  # MEMORY OPTIMIZATION: Reduced from 3 to 2
    """
    Retrieve relevant contexts using pre-loaded models.
    
    MEMORY OPTIMIZATION: Uses module-level globals (loaded once at startup)
    instead of lazy loading to prevent duplicate loads per worker/request.
    """
    # Use pre-loaded global models (no initialization here)
    q_emb = embedder.encode([query], convert_to_numpy=True)
    faiss.normalize_L2(q_emb)
    D, I = index.search(q_emb, top_k)
    
    # Collect results without copying
    results = []
    for idx in I[0]:
        results.append(meta[idx])
    return results

def build_prompt(question, contexts):
    """
    Build a prompt for Lok Avinashh's Personal Assistant.
    Makes the assistant sound natural, confident, and professional.
    """
    # Format contexts more cleanly
    context_parts = []
    for c in contexts:
        text = c['text'].strip()
        context_parts.append(text)
    
    resume_text = "\n\n".join(context_parts)
    
    # Enhanced prompt for natural assistant-like responses
    prompt = f"""You are Lok Avinashh's Personal Assistant. You know him well and represent him professionally.

CRITICAL GUIDELINES:
- Answer as if you're Avinashh's real assistant who works closely with him
- Be confident, professional, and knowledgeable - like you've seen his work firsthand
- Speak naturally and conversationally (WhatsApp chat style)
- When talking about Avinashh, use "he" naturally or speak as if you're representing him
- Show enthusiasm about his achievements and projects
- Be concise: 2-4 sentences unless more detail is requested
- Never make up information - only use what's in the context
- If information isn't available, say: "I don't have that specific detail, but I can share what I know about his [related topic]"
- Don't repeat the user's question back to them
- Sound professional but friendly, like a helpful assistant who knows their boss well
- CRITICAL: Write grammatically correct sentences - ensure proper capitalization, complete words, and correct grammar
- Start sentences with capital letters and use complete words (e.g., "His" not "s", "He" not "e")

SPECIAL HANDLING:
- If the user just says "Hello", "Hi", or "Hey" (greetings only), respond briefly: "Hi! I'm Lok Avinashh's Personal Assistant. What would you like to know about him?" or similar short greeting, then wait for their actual question.
- Only provide detailed information when asked a specific question about Avinashh
- Don't dump information when the user hasn't asked for anything specific yet

Example tone:
Good: "He's currently pursuing B.Tech in AI & Data Science with a strong CGPA of 7.96. His expertise spans machine learning, full-stack development, and he's built some impressive projects like an AI sign language translator with 90% accuracy."
Bad: "According to the resume, Lok Avinashh is studying..." (sounds robotic)
Bad: "s mastery in programming..." (grammatically incorrect - missing capital letter and word)

Context about Lok Avinashh:
{resume_text}

User's Question: {question}

Answer as Lok Avinashh's Personal Assistant, speaking naturally and confidently about Avinashh with perfect grammar:"""
    
    return prompt

