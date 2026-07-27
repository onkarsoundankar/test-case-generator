"""
build_chromadb.py
-----------------
Reads the corpus of user stories and stores them in ChromaDB.

Run:
    python3 src/build_chromadb.py
"""

import json
import os

import chromadb
from chromadb.utils import embedding_functions

# ----------------------------
# Paths
# ----------------------------

CORPUS_PATH = os.path.join(
    os.path.dirname(__file__),
    "corpus",
    "sample_stories.json"
)

CHROMA_DB_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "chroma_db"
)

# ----------------------------
# Create Chroma Client
# ----------------------------

client = chromadb.PersistentClient(path=CHROMA_DB_PATH)

embedding_function = embedding_functions.DefaultEmbeddingFunction()

collection = client.get_or_create_collection(
    name="sample_stories",
    embedding_function=embedding_function
)

# ----------------------------
# Read Corpus
# ----------------------------

with open(CORPUS_PATH, "r") as f:
    corpus = json.load(f)

print(f"Loaded {len(corpus)} stories")

# ----------------------------
# Insert Stories
# ----------------------------

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
        metadatas=[{
            "title": item["title"]
        }]
    )

print("================================")
print("Successfully built ChromaDB")
print("Collection:", collection.count())
print("================================")