import json
from pathlib import Path

from retriever import retrieve_similar_stories
from generator_groq import generate_test_cases_groq

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
BENCHMARK_DIR = PROJECT_ROOT / "evaluation" / "benchmark"
GENERATED_DIR = PROJECT_ROOT / "evaluation" / "generated"

GENERATED_DIR.mkdir(exist_ok=True)

benchmark_files = list(BENCHMARK_DIR.glob("*.json"))

print(f"Found {len(benchmark_files)} benchmark file(s).\n")

for file in benchmark_files:

    print(f"Processing: {file.name}")

    with open(file, "r") as f:
        story = json.load(f)

    # Retrieve similar stories using ChromaDB
    similar = retrieve_similar_stories(
        story["user_story"]
    )

    print(f"Retrieved {len(similar)} similar stories")

    # Generate test cases using the same pipeline as Streamlit
    generated = generate_test_cases_groq(
        story=story["user_story"],
        acceptance_criteria=story["acceptance_criteria"],
        similar_stories=similar,
        test_types=["Regression"]
    )

    output = {
        "story_id": story["story_id"],
        "title": story["title"],
        "user_story": story["user_story"],
        "acceptance_criteria": story["acceptance_criteria"],
        "manual_test_cases": story["manual_test_cases"],
        "generated_test_cases": generated
    }

    output_file = GENERATED_DIR / file.name

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4)

    print(f"Saved: {output_file.name}")
    print("-" * 60)

print("\nBenchmark generation completed successfully.")