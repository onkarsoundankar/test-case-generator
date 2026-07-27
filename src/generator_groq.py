"""
generator_groq.py
-----------------
Cloud LLM generator using Groq API
"""

import os
from dotenv import load_dotenv
from groq import Groq


# Load .env from project root
load_dotenv(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        ".env"
    )
)


def generate_test_cases_groq(
        story,
        acceptance_criteria,
        similar_stories,
        test_types
):

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise Exception(
            "GROQ_API_KEY not found. Check your .env file."
        )


    client = Groq(
        api_key=api_key
    )


    prompt = f"""
You are a senior QA automation engineer.

Generate BDD Gherkin test cases.

User Story:

{story}

Acceptance Criteria:

{acceptance_criteria}

Similar Past Stories:

{similar_stories}

Test Types:

{test_types}

Generate:

- Positive scenarios
- Negative scenarios
- Edge cases
- Validation scenarios
- Security scenarios if applicable

Format:

Feature: Feature name

Scenario: Scenario name

Given
When
Then

Output only Gherkin.
"""


    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )


    return response.choices[0].message.content