"""
retriever.py
-------------
Retrieves similar user stories from ChromaDB.

This file is a drop-in replacement for the old FAISS retriever.
It returns the SAME structure so the rest of the application
(generator.py, app.py) does not need any changes.
"""

import os

import chromadb
from chromadb.utils import embedding_functions

import tempfile

CHROMA_DB_PATH = os.path.join(
    tempfile.gettempdir(),
    "chroma_db"
)

_client = None
_collection = None


def _load():
    global _client, _collection

    if _client is None:
        _client = chromadb.PersistentClient(path=CHROMA_DB_PATH)

    if _collection is None:
        embedding_function = embedding_functions.DefaultEmbeddingFunction()

        _collection = _client.get_collection(
            name="sample_stories",
            embedding_function=embedding_function
        )


def retrieve_similar_stories(new_story_text: str, top_k: int = 3):
    """
    Returns the same structure as the old FAISS retriever.
    """

    _load()

    results = _collection.query(
        query_texts=[new_story_text],
        n_results=top_k
    )

    stories = []

    for i in range(len(results["ids"][0])):

        metadata = results["metadatas"][0][i]

        stories.append(
            {
                "id": results["ids"][0][i],
                "title": metadata["title"],
                "story": metadata["story"],
                "acceptance_criteria": metadata["acceptance_criteria"].split("\n"),
                "test_cases": metadata["test_cases"].split("\n\n"),
                "similarity_score": float(results["distances"][0][i]),
            }
        )

    return stories