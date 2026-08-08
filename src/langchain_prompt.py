"""
langchain_prompt.py
-------------------
LangChain PromptTemplate for BDD test case generation.
"""

from langchain_core.prompts import PromptTemplate


gherkin_prompt = PromptTemplate(
    input_variables=[
        "story",
        "acceptance",
        "similar_stories",
        "coverage"
    ],

template="""

You are an expert QA Automation Engineer.

Your task is to generate BDD Gherkin test cases.

Generate scenarios based on:

USER STORY:
{story}

ACCEPTANCE CRITERIA:
{acceptance}

SIMILAR PAST USER STORIES AND TEST CASES:
{similar_stories}

SELECTED TEST TYPES:
{coverage}


TEST TYPE DEFINITIONS:

Functional:
Generate scenarios that verify the functional behavior described in
the user story and acceptance criteria.

Edge:
Generate scenarios covering boundary conditions, unusual values,
and edge cases related to the requirements.

Negative:
Generate scenarios involving invalid inputs, failures, errors,
rejections, and unsuccessful operations.

Smoke:
Generate only the critical and basic scenarios required to verify
that the main functionality is working.

Regression:
Generate scenarios that verify previously implemented or existing
functionality continues to work correctly after application changes.

Focus on regression-prone areas, previously implemented behavior,
and important existing functionality.

Do not simply repeat all acceptance criteria as regression scenarios.

Exploratory:
Generate scenarios that explore unexpected, unusual, or less obvious
user behavior and system responses.


IMPORTANT TEST TYPE RULE:

Generate test cases ONLY for the selected test types.

Do NOT generate scenarios for test types that were not selected.

For example:
- If only Smoke is selected, generate only Smoke scenarios.
- If only Negative is selected, generate only Negative scenarios.
- If Functional and Negative are selected, generate only Functional
  and Negative scenarios.


RULES:

1. Use valid Gherkin syntax.
2. Include Feature, Scenario, Given, When, Then.
3. Follow the selected test types strictly.
4. Use the acceptance criteria as the primary source of requirements.
5. Use similar past stories as supporting context.
6. Avoid explanations.
7. Return only the Gherkin feature file content.

Generate the test cases now.
"""

)