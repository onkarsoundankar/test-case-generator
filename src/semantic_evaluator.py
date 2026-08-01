import json
import re
from pathlib import Path

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

PROJECT_ROOT = Path(__file__).resolve().parent.parent

GENERATED_DIR = PROJECT_ROOT / "evaluation" / "generated"
REPORT_DIR = PROJECT_ROOT / "evaluation" / "reports"

REPORT_DIR.mkdir(exist_ok=True)

model = SentenceTransformer("all-MiniLM-L6-v2")

report = []

for file in GENERATED_DIR.glob("*.json"):

    with open(file, "r") as f:
        data = json.load(f)

    manual = data["manual_test_cases"]

    gherkin = data["generated_test_cases"]

    # Extract Scenario titles only
    generated = re.findall(r"Scenario:\s*(.*)", gherkin)

    generated_embeddings = model.encode(generated)

    covered = []

    missing = []

    similarities = []

    for tc in manual:

        tc_embedding = model.encode([tc])

        sim = cosine_similarity(
            tc_embedding,
            generated_embeddings
        )[0]

        best = float(max(sim))

        similarities.append(best)

        if best >= 0.75:
            covered.append(tc)
        else:
            missing.append(tc)

    coverage = round(
        len(covered) / len(manual) * 100,
        2
    )

    report.append(
        {
            "story": data["title"],
            "manual_test_cases": len(manual),
            "generated_scenarios": len(generated),
            "covered": len(covered),
            "missing": len(missing),
            "coverage_percent": coverage,
            "average_similarity": round(
                sum(similarities) / len(similarities),
                3
            )
        }
    )

output = REPORT_DIR / "semantic_report.json"

with open(output, "w") as f:
    json.dump(report, f, indent=4)

print("\nSemantic evaluation completed.\n")

for r in report:

    print(r)

print(f"\nReport saved to:\n{output}")