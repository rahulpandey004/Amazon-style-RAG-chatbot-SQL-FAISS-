import os
import re
import faiss
import pickle
import numpy as np
import nltk
from sentence_transformers import SentenceTransformer
from unstructured.partition.pdf import partition_pdf
from nltk.tokenize import sent_tokenize
# Setup
nltk.download("punkt", quiet=True)
VECTOR_DIR = "vector_store"
INDEX_PATH = os.path.join(VECTOR_DIR, "faiss.index")
META_PATH = os.path.join(VECTOR_DIR, "metadata.pkl")
DEBUG_FILE = "chunks_debug.txt" # The dummy txt file
os.makedirs(VECTOR_DIR, exist_ok=True)

embed_model = SentenceTransformer("all-MiniLM-L6-v2")
# ==========================================
# INDEXING ALGORITHMS (CALLABLE)
# ==========================================

def get_flat_index(dim: int):
    """Exact Brute Force search. 100% accuracy, slower on large data."""
    return faiss.IndexFlatIP(dim)

def get_hnsw_index(dim: int, m: int = 32, ef_cons: int = 128, ef_search: int = 64):
    """Fast Graph-based search. High speed, slightly lower accuracy."""
    index = faiss.IndexHNSWFlat(dim, m, faiss.METRIC_INNER_PRODUCT)
    index.hnsw.efConstruction = ef_cons
    index.hnsw.efSearch = ef_search
    return index

# ==========================================
# EXTRACTION & CHUNKING
# ==========================================

def extract_text_from_pdf(pdf_path: str) -> str:
    elements = partition_pdf(filename=pdf_path, strategy="fast")
    return "\n".join(el.text for el in elements if el.text)

def split_text_by_products(text: str):
    pattern = re.compile(r"^(.+Laptop\s+\d+)\s*$", re.MULTILINE)
    matches = list(pattern.finditer(text))
    return [text[m.start():matches[i+1].start() if i+1 < len(matches) else len(text)].strip() 
            for i, m in enumerate(matches)]

def semantic_chunk_text(text: str, max_tokens: int = 250):
    sentences = sent_tokenize(text)
    chunks, current_chunk, current_count = [], [], 0
    for s in sentences:
        words = s.split()
        if current_count + len(words) > max_tokens:
            chunks.append(" ".join(current_chunk))
            current_chunk, current_count = [s], len(words)
        else:
            current_chunk.append(s), (current_count := current_count + len(words))
    if current_chunk: chunks.append(" ".join(current_chunk))
    return chunks

# ==========================================
# INGESTION ENGINE
# ==========================================
def ingest_pdf(pdf_path: str, use_hnsw: bool = True):
    full_text = extract_text_from_pdf(pdf_path)
    # 1. Access index of each product section using enumerate
    product_sections = split_text_by_products(full_text)
    
    all_embeddings, all_metadata = [], []
    
    with open(DEBUG_FILE, "w", encoding="utf-8") as f:
        f.write(f"--- Chunk Export Log: {pdf_path} ---\n\n")

    # Use enumerate to track section_idx
    for section_idx, section in enumerate(product_sections):
        product_name_match = re.search(r"\b([A-Z][A-Za-z0-9 ]+ Laptop \d+)\b", section)
        product_name = product_name_match.group(1) if product_name_match else "UNKNOWN_LAPTOP"
        
        chunks = semantic_chunk_text(section)
        if not chunks: continue

        # Debug logging
        with open(DEBUG_FILE, "a", encoding="utf-8") as f:
            f.write(f"SECTION {section_idx} | PRODUCT: {product_name}\n")
            for i, chunk in enumerate(chunks):
                f.write(f"Chunk {i}:\n{chunk}\n\n")
            f.write("-" * 60 + "\n\n")

        # 2. Generate Embeddings
        embeddings = embed_model.encode(chunks).astype("float32")
        faiss.normalize_L2(embeddings)
        all_embeddings.append(embeddings)

        # 3. ADD DETAILED METADATA
        # Use enumerate to track chunk_id
        for chunk_id, chunk in enumerate(chunks):
            all_metadata.append({
                "product_name": product_name,
                "category": "Laptop",
                "chunk_id": chunk_id,
                "section_id": section_idx,
                "text": chunk
            })

    if not all_embeddings: 
        print("❌ No content found.")
        return

    # Finalize Indexing
    all_embeddings = np.vstack(all_embeddings)
    dim = all_embeddings.shape[1]
    
    index = get_hnsw_index(dim) if use_hnsw else get_flat_index(dim)
    index.add(all_embeddings)

    # Save
    faiss.write_index(index, INDEX_PATH)
    with open(META_PATH, "wb") as f:
        pickle.dump(all_metadata, f)
    
    print(f"✅ Ingested {len(all_metadata)} chunks with full metadata.")


def rag_search(query: str, k: int = 5):
    index = faiss.read_index(INDEX_PATH)
    with open(META_PATH, "rb") as f:
        metadata = pickle.load(f)

    query_emb = embed_model.encode([query]).astype("float32")
    faiss.normalize_L2(query_emb)

    _, indices = index.search(query_emb, k)
    return [metadata[i] for i in indices[0] if i != -1]

# ==========================================
# EXECUTION
# ==========================================

if __name__ == "__main__":
    # To use HNSW:
    ingest_pdf("docs/laptops.pdf", use_hnsw=True)
    
    # To use Flat Index (Comment out the above and use this):
    # ingest_pdf("docs/laptops.pdf", use_hnsw=False)
    
    # Test
    # for r in rag_search("Best battery life laptop"):
    #     print(f"\n[{r['product_name']}]: {r['text'][:100]}...")
