"""
main.py
--------
CLI entrypoint. Ties together retrieval + generation.

Examples:
    python src/main.py --story "As a user, I want to..." --test-types functional,edge,negative
    python src/main.py --story-file my_story.txt
    python src/main.py --jira-key PROJ-123
"""

import argparse
import os
import sys
from datetime import datetime

from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(__file__))

from retriever import retrieve_similar_stories
from generator import generate_test_cases, generate_test_cases_mock, print_manual_prompt
from jira_client import fetch_story_from_jira

load_dotenv()

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "output")


def parse_args():
    parser = argparse.ArgumentParser(description="AI-powered test case generator from user stories.")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--story", type=str, help="User story text directly on the command line.")
    source.add_argument("--story-file", type=str, help="Path to a text file containing the user story.")
    source.add_argument("--jira-key", type=str, help="Jira issue key to fetch the story from, e.g. PROJ-123.")

    parser.add_argument(
        "--acceptance-criteria",
        type=str,
        default="",
        help="Optional: semicolon-separated acceptance criteria, e.g. 'AC1;AC2;AC3'",
    )
    parser.add_argument(
        "--test-types",
        type=str,
        default="functional,edge,negative",
        help="Comma-separated test types to generate: smoke, regression, exploratory, functional, edge, negative",
    )
    parser.add_argument("--top-k", type=int, default=3, help="Number of similar past examples to retrieve.")
    parser.add_argument("--output", type=str, default=None, help="Output file path (.feature). Auto-named if omitted.")
    parser.add_argument(
        "--mock",
        action="store_true",
        help="FREE mode: skip the Claude API entirely and generate template-based output. No cost, no API key needed.",
    )
    parser.add_argument(
        "--print-prompt",
        action="store_true",
        help="FREE mode: instead of calling the API, print a ready-to-copy prompt you can paste into claude.ai for free.",
    )

    return parser.parse_args()


def get_story_text(args):
    if args.story:
        return args.story
    if args.story_file:
        with open(args.story_file, "r") as f:
            return f.read()
    if args.jira_key:
        print(f"Fetching story {args.jira_key} from Jira...")
        return fetch_story_from_jira(args.jira_key)


def main():
    args = parse_args()
    story_text = get_story_text(args)
    acceptance_criteria = [ac.strip() for ac in args.acceptance_criteria.split(";") if ac.strip()]
    test_types = [t.strip() for t in args.test_types.split(",") if t.strip()]

    print("\n--- Step 1: Retrieving similar past stories (RAG retrieval) ---")
    similar = retrieve_similar_stories(story_text, top_k=args.top_k)
    for ex in similar:
        print(f"  Matched: {ex['title']}  (similarity: {ex['similarity_score']:.2f})")

    if args.print_prompt:
        print_manual_prompt(story_text, acceptance_criteria, similar, test_types)
        print("Paste the block above into https://claude.ai, then save the reply yourself. No file was written.")
        return

    if args.mock:
        print("\n--- Step 2: Generating MOCK test cases (no API call, $0 cost) ---")
        result = generate_test_cases_mock(
            story_text=story_text,
            acceptance_criteria=acceptance_criteria,
            retrieved_examples=similar,
            test_types=test_types,
        )
    else:
        print("\n--- Step 2: Generating test cases with Claude (uses paid API credits) ---")
        result = generate_test_cases(
            story_text=story_text,
            acceptance_criteria=acceptance_criteria,
            retrieved_examples=similar,
            test_types=test_types,
        )

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    if args.output:
        output_path = args.output
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(OUTPUT_DIR, f"test_cases_{timestamp}.feature")

    with open(output_path, "w") as f:
        f.write(result)

    print(f"\n--- Done. Test cases saved to: {output_path} ---\n")
    print(result)


if __name__ == "__main__":
    main()
