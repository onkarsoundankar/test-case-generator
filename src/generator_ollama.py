"""
generator_ollama.py
-------------------
Local LLM generator using Ollama.
Uses Qwen 2.5 running locally.
"""

import ollama


def generate_test_cases_ollama(
        story,
        acceptance_criteria,
        similar_stories,
        test_types
):

    prompt = f"""
You are a senior QA automation engineer.

Your task is to generate detailed BDD Gherkin test cases.

User Story:
{story}


Acceptance Criteria:
{acceptance_criteria}


Similar Past Test Cases:
{similar_stories}


Test Types Required:
{test_types}


Generate test cases with:

Feature:
Scenario:
Given:
When:
Then:


Requirements:

1. Generate positive test cases
2. Generate negative test cases
3. Generate edge cases
4. Include validations and error scenarios
5. Follow proper Gherkin syntax
6. Make test cases detailed enough for automation engineers
"""


    response = ollama.chat(
        model="qwen2.5:7b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )


    return response["message"]["content"]