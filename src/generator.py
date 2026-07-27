"""
generator.py
-------------
Uses Ollama (local Qwen model) instead of Anthropic.

Completely FREE.
No API key required.
"""

import json
import requests

MODEL_NAME = "qwen2.5:7b"

TEST_TYPE_TEMPLATES = {
    "smoke": "Focus on 2-4 critical happy-path scenarios.",
    "regression": "Generate comprehensive positive, negative, validation and edge test cases.",
    "exploratory": "Generate creative exploratory scenarios."
}

SYSTEM_PROMPT = """
You are a Senior QA Automation Engineer.

Generate ONLY valid Gherkin.

Rules:

- Output only Feature and Scenario blocks.
- No markdown.
- No explanations.
- Cover positive scenarios.
- Cover negative scenarios.
- Cover validation scenarios.
- Cover edge cases.
- Use realistic test data.
"""


def build_user_prompt(
    story_text,
    acceptance_criteria,
    retrieved_examples,
    test_types
):
    prompt = []

    prompt.append("USER STORY")
    prompt.append(story_text)

    if acceptance_criteria:
        prompt.append("\nACCEPTANCE CRITERIA")
        for ac in acceptance_criteria:
            prompt.append(f"- {ac}")

    if retrieved_examples:

        prompt.append("\nSIMILAR STORIES")

        for item in retrieved_examples:

            prompt.append(
                f"\nTitle: {item['title']}"
            )

            prompt.append(item["document"])

            if "test_cases" in item:
                prompt.append("\nExisting Test Cases:")
                prompt.extend(item["test_cases"])

    if test_types:

        prompt.append("\nTEST TYPES")

        for t in test_types:
            if t in TEST_TYPE_TEMPLATES:
                prompt.append(TEST_TYPE_TEMPLATES[t])

    prompt.append(
        "\nGenerate a complete professional Gherkin feature file."
    )

    return "\n".join(prompt)


def generate_test_cases(
    story_text,
    acceptance_criteria,
    retrieved_examples,
    test_types,
    api_key=None
):

    prompt = build_user_prompt(
        story_text,
        acceptance_criteria,
        retrieved_examples,
        test_types,
    )

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": MODEL_NAME,
            "system": SYSTEM_PROMPT,
            "prompt": prompt,
            "stream": False,
        },
    )

    data = response.json()

    return data["response"]


def generate_test_cases_mock(
    story_text,
    acceptance_criteria,
    retrieved_examples,
    test_types
):
    return generate_test_cases(
        story_text,
        acceptance_criteria,
        retrieved_examples,
        test_types,
    )