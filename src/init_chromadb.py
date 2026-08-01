import os
import tempfile

import chromadb
from chromadb.errors import NotFoundError
from chromadb.utils import embedding_functions

from build_chromadb import build_chromadb

# Use writable temp directory
CHROMA_DB_PATH = os.path.join(
    tempfile.gettempdir(),
    "chroma_db"
)


def initialize_chromadb():
    """
    Creates ChromaDB only if the collection does not exist.
    """

    print(f"Using ChromaDB path: {CHROMA_DB_PATH}")

    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)

    embedding_function = embedding_functions.DefaultEmbeddingFunction()

    try:
        client.get_collection(
            name="sample_stories",
            embedding_function=embedding_function
        )

        print("✓ ChromaDB collection already exists.")

    except NotFoundError:

        print("Collection not found. Building ChromaDB...")

        build_chromadb()

        print("✓ ChromaDB successfully initialized.")