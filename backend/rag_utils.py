# backend/rag_utils.py
import os, json
import numpy as np
# NOTE: sentence_transformers and faiss imports are kept at top level for type checking
# but actual heavy lifting is moved to lazy loader
from sentence_transformers import SentenceTransformer
import faiss

# Path relative to project root (2 levels up from backend/)
BASE = os.path.join(os.path.dirname(__file__), "..")
INDEX_PATH = os.path.join(BASE, "embeddings", "resume.index")
META_PATH = os.path.join(BASE, "embeddings", "resume_meta.json")

# ============================================================================
# MEMORY OPTIMIZATION: Singleton Lazy Loading
# We moved AWAY from module-level globals because they cause OOM at startup
# before the port opens on Render.
# ============================================================================

class RAGComponents:
    """
    Singleton class to hold RAG components.
    Initialized ONLY when first needed, not at startup.
    """
    _instance = None
    
    def __init__(self):
        print("🔄 Initializing RAG components (Lazy Load)...")
        
        # 1. Load Embedding Model
        print("   - Loading SentenceTransformer...")
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")
        
        # 2. Load FAISS Index
        print("   - Loading FAISS index...")
        if not os.path.exists(INDEX_PATH):
            raise FileNotFoundError(f"FAISS index not found at {INDEX_PATH}")
        self.index = faiss.read_index(INDEX_PATH)
        
        # 3. Load Metadata
        print("   - Loading metadata...")
        if not os.path.exists(META_PATH):
            raise FileNotFoundError(f"Metadata not found at {META_PATH}")
        with open(META_PATH, "r", encoding="utf-8") as f:
            self.meta = json.load(f)
            
        print("✓ RAG components ready!")

    @classmethod
    def get_instance(cls):
        """Get the singleton instance, creating it if it doesn't exist."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

# ============================================================================

def retrieve(query, top_k=2):  # MEMORY OPTIMIZATION: Keep k=2
    """
    Retrieve relevant contexts using lazy-loaded singleton.
    """
    # Get singleton instance (loads models if first time)
    rag = RAGComponents.get_instance()
    
    # Use the loaded components
    q_emb = rag.embedder.encode([query], convert_to_numpy=True)
    faiss.normalize_L2(q_emb)
    D, I = rag.index.search(q_emb, top_k)
    
    # Collect results
    results = []
    for idx in I[0]:
        results.append(rag.meta[idx])
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

