"""
retriever.py
-------------
Given a NEW user story, this finds the most similar past stories
(and their existing test cases) from the vector index. These similar
examples are then handed to the AI as reference material ("retrieval-
augmented generation").
"""

import os
import pickle

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

INDEX_DIR = os.path.join(os.path.dirname(__file__), "..", "vector_index")
INDEX_PATH = os.path.join(INDEX_DIR, "stories.index")
METADATA_PATH = os.path.join(INDEX_DIR, "stories_metadata.pkl")

EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

_model = None
_index = None
_metadata = None


def _load():
    global _model, _index, _metadata
    if _model is None:
        _model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    if _index is None:
        if not os.path.exists(INDEX_PATH):
            raise FileNotFoundError(
                "Vector index not found. Run 'python src/build_index.py' first."
            )
        _index = faiss.read_index(INDEX_PATH)
    if _metadata is None:
        with open(METADATA_PATH, "rb") as f:
            _metadata = pickle.load(f)


def retrieve_similar_stories(new_story_text: str, top_k: int = 3):
    """
    Returns the top_k most similar past stories (with their test cases)
    to the given new story text.
    """
    _load()

    query_vec = _model.encode([new_story_text], normalize_embeddings=True)
    query_vec = np.array(query_vec).astype("float32")

    scores, indices = _index.search(query_vec, top_k)

    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx == -1:
            continue
        item = dict(_metadata[idx])
        item["similarity_score"] = float(score)
        results.append(item)

    return results
