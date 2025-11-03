# backend/index_documents.py
import os, json, math
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import pdfplumber

# Path relative to project root (2 levels up from backend/)
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
INDEX_PATH = os.path.join(os.path.dirname(__file__), "..", "embeddings", "resume.index")
META_PATH = os.path.join(os.path.dirname(__file__), "..", "embeddings", "resume_meta.json")
os.makedirs(os.path.dirname(INDEX_PATH), exist_ok=True)

# Simple PDF -> text
def pdf_to_text(path):
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def read_documents(data_dir=DATA_DIR):
    docs = []
    for fname in os.listdir(data_dir):
        path = os.path.join(data_dir, fname)
        if fname.lower().endswith(".pdf"):
            txt = pdf_to_text(path)
            docs.append({"source": fname, "text": txt})
        elif fname.lower().endswith((".txt", ".md")):
            with open(path, "r", encoding="utf-8") as f:
                docs.append({"source": fname, "text": f.read()})
    return docs

# Simple chunker: split by sentences/paragraphs into approx chunk_size words
def chunk_text(text, chunk_size=300, overlap=50):
    if not text or not text.strip():
        return []
    words = text.split()
    chunks = []
    i = 0
    idx = 0
    while i < len(words):
        end = min(i + chunk_size, len(words))
        chunk = " ".join(words[i:end])
        chunks.append({"id": idx, "text": chunk})
        idx += 1
        # Prevent infinite loop: ensure we always advance
        next_i = end - overlap
        if next_i <= i:
            next_i = i + 1
        i = next_i
        # Safety check
        if i >= len(words):
            break
    return chunks

def build_index(chunks, model_name="all-MiniLM-L6-v2"):
    model = SentenceTransformer(model_name)
    texts = [c["text"] for c in chunks]
    embeddings = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)
    # normalize for cosine similarity
    faiss.normalize_L2(embeddings)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)
    faiss.write_index(index, INDEX_PATH)

    # save meta
    meta = [{"id": c["id"], "text": c["text"]} for c in chunks]
    with open(META_PATH, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    print("Index saved to", INDEX_PATH)
    print("Meta saved to", META_PATH)

if __name__ == "__main__":
    print("Reading documents...")
    docs = read_documents()
    print(f"Found {len(docs)} document(s)")
    all_chunks = []
    for d in docs:
        print(f"Processing {d['source']}...")
        chunks = chunk_text(d["text"], chunk_size=300, overlap=50)
        print(f"  Created {len(chunks)} chunks")
        # add source in meta
        for c in chunks:
            c["source"] = d["source"]
        all_chunks.extend(chunks)
    print(f"Total chunks: {len(all_chunks)}")
    print("Building index (this may take a while)...")
    build_index(all_chunks)
    print("Done!")

