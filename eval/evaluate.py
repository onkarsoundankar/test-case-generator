"""
evaluate.py
------------
Simple evaluation comparing AI-generated test cases against a manually-written
reference set. This uses lightweight text-overlap heuristics (not a substitute
for human review, but useful as a quick coverage signal).

Usage:
    python eval/evaluate.py --generated output/test_cases_20260101_120000.feature --manual manual_reference.feature
"""

import argparse
import re


def extract_scenarios(feature_text: str):
    """Pull out scenario titles and their step lines from a .feature file's text."""
    scenarios = []
    current_title = None
    current_steps = []
    for line in feature_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("Scenario"):
            if current_title:
                scenarios.append({"title": current_title, "steps": current_steps})
            current_title = stripped.split(":", 1)[-1].strip()
            current_steps = []
        elif stripped.startswith(("Given", "When", "Then", "And", "But")):
            current_steps.append(stripped)
    if current_title:
        scenarios.append({"title": current_title, "steps": current_steps})
    return scenarios


def keyword_set(text: str):
    words = re.findall(r"[a-zA-Z]{4,}", text.lower())
    stopwords = {"given", "when", "then", "should", "user", "with", "that", "this", "have"}
    return set(w for w in words if w not in stopwords)


def evaluate(generated_path: str, manual_path: str):
    with open(generated_path, "r") as f:
        generated_text = f.read()
    with open(manual_path, "r") as f:
        manual_text = f.read()

    generated_scenarios = extract_scenarios(generated_text)
    manual_scenarios = extract_scenarios(manual_text)

    print(f"Generated test cases: {len(generated_scenarios)} scenarios")
    print(f"Manual test cases:    {len(manual_scenarios)} scenarios\n")

    # Coverage: what fraction of manual scenario "topics" (keywords) appear
    # somewhere in the generated set.
    manual_keywords = set()
    for s in manual_scenarios:
        manual_keywords |= keyword_set(s["title"] + " " + " ".join(s["steps"]))

    generated_keywords = set()
    for s in generated_scenarios:
        generated_keywords |= keyword_set(s["title"] + " " + " ".join(s["steps"]))

    if manual_keywords:
        coverage = len(manual_keywords & generated_keywords) / len(manual_keywords)
    else:
        coverage = 0.0

    # Precision proxy: what fraction of generated keywords are also present in
    # manual reference (rough signal for "on-topic-ness", not true precision).
    if generated_keywords:
        precision_proxy = len(manual_keywords & generated_keywords) / len(generated_keywords)
    else:
        precision_proxy = 0.0

    print(f"Estimated coverage (manual topics found in AI output):  {coverage:.0%}")
    print(f"Estimated precision proxy (AI output on-topic):          {precision_proxy:.0%}")
    print("\nNote: These are rough heuristics based on keyword overlap, meant to flag")
    print("obvious gaps quickly. Always have a human reviewer sanity-check the output.")

    missing_keywords = manual_keywords - generated_keywords
    if missing_keywords:
        print(f"\nPossible gaps (topics in manual tests not seen in AI output):")
        print(", ".join(sorted(missing_keywords)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compare AI-generated vs manual test cases.")
    parser.add_argument("--generated", required=True, help="Path to AI-generated .feature file")
    parser.add_argument("--manual", required=True, help="Path to manually-written .feature file")
    args = parser.parse_args()
    evaluate(args.generated, args.manual)
