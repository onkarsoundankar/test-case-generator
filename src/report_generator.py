import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

GENERATED_DIR = PROJECT_ROOT / "evaluation" / "generated"
REPORTS_DIR = PROJECT_ROOT / "evaluation" / "reports"

REPORTS_DIR.mkdir(exist_ok=True)

report = []

for file in GENERATED_DIR.glob("*.json"):

    with open(file, "r") as f:
        data = json.load(f)

    manual_count = len(data["manual_test_cases"])

    generated_count = data["generated_test_cases"].count("Scenario:")

    coverage = min(
        round((manual_count / generated_count) * 100, 2),
        100
    )

    report.append(
        {
            "story_id": data["story_id"],
            "title": data["title"],
            "manual_test_cases": manual_count,
            "generated_scenarios": generated_count,
            "coverage_percent": coverage
        }
    )

output_file = REPORTS_DIR / "evaluation_report.json"

with open(output_file, "w") as f:
    json.dump(report, f, indent=4)

print(f"Report generated: {output_file}")