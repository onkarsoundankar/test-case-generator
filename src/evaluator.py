import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

GENERATED_DIR = PROJECT_ROOT / "evaluation" / "generated"

for file in GENERATED_DIR.glob("*.json"):

    print("=" * 70)

    print(file.name)

    with open(file, "r") as f:
        data = json.load(f)

    manual = data["manual_test_cases"]

    generated = data["generated_test_cases"]

    print(f"Manual Test Cases : {len(manual)}")

    scenario_count = generated.count("Scenario:")

    print(f"Generated Scenarios : {scenario_count}")

    print()