"""
build_chromadb.py
-----------------
Reads the corpus of user stories and stores them in ChromaDB.

Run:
    python3 src/build_chromadb.py
"""

import json
import os
import shutil

import chromadb
from chromadb.utils import embedding_functions

# --------------------------------------------------
# Paths
# --------------------------------------------------

CORPUS_PATH = os.path.join(
    os.path.dirname(__file__),
    "corpus",
    "sample_stories.json"
)

import tempfile

CHROMA_DB_PATH = os.path.join(
    tempfile.gettempdir(),
    "chroma_db"
)


def build_chromadb():
    """Creates and populates the ChromaDB database."""

    # Start fresh
    if os.path.exists(CHROMA_DB_PATH):
        shutil.rmtree(CHROMA_DB_PATH)

    os.makedirs(CHROMA_DB_PATH, exist_ok=True)

    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)

    embedding_function = embedding_functions.DefaultEmbeddingFunction()

    collection = client.get_or_create_collection(
        name="sample_stories",
        embedding_function=embedding_function
    )

    with open(CORPUS_PATH, "r") as f:
        corpus = json.load(f)

    print(f"Loaded {len(corpus)} stories")

    for item in corpus:

        document = f"""
Title:
{item['title']}

Story:
{item['story']}

Acceptance Criteria:
{' '.join(item['acceptance_criteria'])}
"""

        collection.upsert(
            ids=[item["id"]],
            documents=[document],
            metadatas=[
                {
                    "title": item["title"],
                    "story": item["story"],
                    "acceptance_criteria": "\n".join(item["acceptance_criteria"]),
                    "test_cases": "\n\n".join(item["test_cases"])
                }
            ]
        )

    print("=" * 50)
    print("Successfully built ChromaDB")
    print(f"Collection contains {collection.count()} stories")
    print("=" * 50)


if __name__ == "__main__":
    build_chromadb()