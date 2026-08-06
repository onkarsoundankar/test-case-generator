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


REQUIRED TEST COVERAGE:
{coverage}


Rules:
1. Use valid Gherkin syntax.
2. Include Feature, Scenario, Given, When, Then.
3. Cover positive scenarios.
4. Cover negative scenarios.
5. Cover edge cases.
6. Avoid explanations.
7. Return only the Gherkin feature file content.


Generate the test cases now.
"""
)