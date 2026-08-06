"""
generator.py
-------------
Takes the new user story + retrieved similar examples, builds a prompt,
and calls the Claude API to generate structured BDD/Gherkin test cases.
"""

import os

import anthropic

MODEL_NAME = "claude-sonnet-4-6"

TEST_TYPE_TEMPLATES = {
    "smoke": "Focus on 2-4 critical happy-path scenarios that verify the core feature works at all.",
    "regression": "Focus on a broad, thorough set of scenarios covering functional, edge, and negative cases, "
                  "similar to what a full regression suite would need.",
    "exploratory": "Focus on unusual, creative, boundary-pushing scenarios a tester might explore manually "
                   "(unexpected inputs, race conditions, unusual user flows).",
}

SYSTEM_PROMPT = """You are a senior QA engineer who writes precise, professional test cases in BDD/Gherkin format.

Rules:
- Output ONLY valid Gherkin syntax (Feature, Scenario, Given/When/Then/And).
- Always include a mix of: functional (happy path), edge cases, and negative/error cases, unless the requested
  test type says otherwise.
- Base your test cases on the acceptance criteria provided. Do not invent requirements that contradict them.
- Use the retrieved past examples only as a style/structure reference, not as content to copy verbatim.
- Be specific and concrete (use realistic example data where helpful).
- Do not include any commentary, explanations, or markdown headers outside of the Gherkin itself.
"""


def build_user_prompt(story_text: str, acceptance_criteria: list, retrieved_examples: list, test_types: list):
    prompt_parts = []

    prompt_parts.append("## New User Story\n" + story_text.strip())

    if acceptance_criteria:
        prompt_parts.append(
            "## Acceptance Criteria\n" + "\n".join(f"- {ac}" for ac in acceptance_criteria)
        )

    if retrieved_examples:
        prompt_parts.append("## Reference Examples From Similar Past Stories (style/structure reference only)")
        for i, ex in enumerate(retrieved_examples, 1):
            prompt_parts.append(
                f"### Example {i}: {ex['title']} (similarity: {ex['similarity_score']:.2f})\n"
                + "\n".join(ex["test_cases"])
            )

    type_instructions = []
    for t in test_types:
        if t in TEST_TYPE_TEMPLATES:
            type_instructions.append(f"- {t}: {TEST_TYPE_TEMPLATES[t]}")
    if type_instructions:
        prompt_parts.append("## Requested Test Types\n" + "\n".join(type_instructions))

    prompt_parts.append(
        "## Task\nGenerate a complete Gherkin '.feature' file with a Feature block and multiple "
        "Scenario blocks covering the requested test types. Cover functional, edge, and negative cases."
    )

    return "\n\n".join(prompt_parts)


def generate_test_cases(story_text: str, acceptance_criteria: list, retrieved_examples: list,
                         test_types: list, api_key: str = None):
    client = anthropic.Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))

    user_prompt = build_user_prompt(story_text, acceptance_criteria, retrieved_examples, test_types)

    response = client.messages.create(
        model=MODEL_NAME,
        max_tokens=2000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}],
    )

    text_blocks = [block.text for block in response.content if block.type == "text"]
    return "\n".join(text_blocks)


def generate_test_cases_mock(story_text: str, acceptance_criteria: list, retrieved_examples: list,
                              test_types: list):
    """
    FREE mode — does not call any API or cost any money.

    Builds a template-based set of Gherkin test cases by adapting the
    single most similar retrieved example. It's much less intelligent than
    the real Claude-generated version (it can't truly understand your new
    story), but it lets you see the whole pipeline (retrieval -> formatting
    -> saving a .feature file) working end to end for free.
    """
    feature_title = story_text.strip().splitlines()[0][:60]
    lines = [f"Feature: {feature_title}", ""]

    lines.append("  # NOTE: This is MOCK output (no AI call was made, $0 cost).")
    lines.append("  # It is adapted from the most similar past example below as a placeholder.")
    lines.append("  # For real AI-written test cases tailored to your exact story, either:")
    lines.append("  #   1) add Anthropic API credits and re-run without --mock, or")
    lines.append("  #   2) copy the prompt printed below into https://claude.ai for free.")
    lines.append("")

    if acceptance_criteria:
        lines.append("  # Acceptance criteria considered:")
        for ac in acceptance_criteria:
            lines.append(f"  #   - {ac}")
        lines.append("")

    if retrieved_examples:
        best_match = retrieved_examples[0]
        for i, scenario_block in enumerate(best_match["test_cases"], 1):
            lines.append(f"  {scenario_block}")
            lines.append("")
    else:
        lines.append("  Scenario: Placeholder scenario (no similar examples found)")
        lines.append("    Given a precondition related to the story")
        lines.append("    When the user performs the main action")
        lines.append("    Then the expected result occurs")
        lines.append("")

    return "\n".join(lines)


def print_manual_prompt(story_text: str, acceptance_criteria: list, retrieved_examples: list, test_types: list):
    """
    Prints a ready-to-copy prompt the user can paste into the free claude.ai
    chat interface to get real AI-generated test cases without any API billing.
    """
    prompt = build_user_prompt(story_text, acceptance_criteria, retrieved_examples, test_types)
    print("\n" + "=" * 70)
    print("COPY EVERYTHING BELOW THIS LINE, PASTE INTO https://claude.ai (free):")
    print("=" * 70)
    print(SYSTEM_PROMPT)
    print(prompt)
    print("=" * 70)
    print("COPY EVERYTHING ABOVE THIS LINE")
    print("=" * 70 + "\n")
