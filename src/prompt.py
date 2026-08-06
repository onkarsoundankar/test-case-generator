from langchain_core.prompts import PromptTemplate


PROMPT_TEMPLATE = PromptTemplate.from_template(
    """
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
)