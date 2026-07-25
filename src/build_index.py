"""
build_index.py
----------------
Reads the corpus of past user stories + test cases, converts each story
into a numeric vector (an "embedding") using a local embedding model,
and stores those vectors in a FAISS index for fast similarity search.

Run this once (or whenever you update the corpus):
    python src/build_index.py
"""

import json
import os
import pickle

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

CORPUS_PATH = os.path.join(os.path.dirname(__file__), "corpus", "sample_stories.json")
INDEX_DIR = os.path.join(os.path.dirname(__file__), "..", "vector_index")
INDEX_PATH = os.path.join(INDEX_DIR, "stories.index")
METADATA_PATH = os.path.join(INDEX_DIR, "stories_metadata.pkl")

EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"  # small, fast, runs fine on M1 CPU


def build_index():
    os.makedirs(INDEX_DIR, exist_ok=True)

    with open(CORPUS_PATH, "r") as f:
        corpus = json.load(f)

    print(f"Loaded {len(corpus)} stories from corpus.")
    print(f"Loading embedding model '{EMBEDDING_MODEL_NAME}' (first run downloads it, ~80MB)...")
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)

    # Combine title + story + acceptance criteria into one text block per story,
    # since that's what we want to match against new incoming stories.
    texts = []
    for item in corpus:
        combined = (
            item["title"]
            + ". "
            + item["story"]
            + " Acceptance criteria: "
            + " ".join(item["acceptance_criteria"])
        )
        texts.append(combined)

    print("Encoding stories into vectors...")
    embeddings = model.encode(texts, show_progress_bar=True, normalize_embeddings=True)
    embeddings = np.array(embeddings).astype("float32")

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)  # inner product on normalized vectors = cosine similarity
    index.add(embeddings)

    faiss.write_index(index, INDEX_PATH)
    with open(METADATA_PATH, "wb") as f:
        pickle.dump(corpus, f)

    print(f"Index built with {index.ntotal} vectors.")
    print(f"Saved index to: {INDEX_PATH}")
    print(f"Saved metadata to: {METADATA_PATH}")


if __name__ == "__main__":
    build_index()
