import os

import chromadb
from chromadb.errors import NotFoundError
from chromadb.utils import embedding_functions

from build_chromadb import build_chromadb

CHROMA_DB_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "chroma_db"
)


def initialize_chromadb():
    """
    Creates ChromaDB only if the collection does not exist.
    """

    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)

    embedding_function = embedding_functions.DefaultEmbeddingFunction()

    try:
        client.get_collection(
            name="sample_stories",
            embedding_function=embedding_function
        )
        print("ChromaDB collection already exists.")

    except NotFoundError:
        print("Collection not found. Building ChromaDB...")
        build_chromadb()