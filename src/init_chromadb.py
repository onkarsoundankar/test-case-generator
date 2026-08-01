import os
import chromadb
from chromadb.utils import embedding_functions

from build_chromadb import build_chromadb


CHROMA_DB_PATH = "chroma_db"


def initialize_chromadb():

    print(f"Using ChromaDB path: {CHROMA_DB_PATH}")

    client = chromadb.PersistentClient(
        path=CHROMA_DB_PATH
    )

    embedding_function = (
        embedding_functions.DefaultEmbeddingFunction()
    )

    collections = [
        c.name for c in client.list_collections()
    ]

    if "sample_stories" in collections:

        print("✓ ChromaDB collection already exists.")

    else:

        print("Collection missing. Building ChromaDB...")

        build_chromadb()

        print("✓ ChromaDB initialized.")