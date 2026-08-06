"""
chain.py
--------
Main LangChain workflow for generating BDD test cases.
"""

from retriever import retrieve_similar_stories
from prompt import PROMPT_TEMPLATE
from llm import get_llm


def _format_similar_stories(similar_stories):
    """
    Convert retrieved stories into prompt-friendly text.
    """

    if not similar_stories:
        return "No similar stories found."

    formatted = []

    for i, story in enumerate(similar_stories, start=1):
        formatted.append(
            f"""
Story {i}

Title:
{story["title"]}

User Story:
{story["story"]}

Acceptance Criteria:
{chr(10).join(story["acceptance_criteria"])}

----------------------------------------
"""
        )

    return "\n".join(formatted)


def generate_test_cases(
    story,
    acceptance_criteria,
    test_types,
    similar_stories=None,
    top_k=3,
):
    """
    Generate BDD Gherkin test cases using LangChain.
    """

    # Retrieve similar stories only if not provided
    if similar_stories is None:
        similar_stories = retrieve_similar_stories(
            story,
            top_k,
        )

    # Convert retrieved stories into prompt-friendly text
    context = _format_similar_stories(similar_stories)

    # Get configured LLM
    llm = get_llm()

    # Build LangChain pipeline
    chain = PROMPT_TEMPLATE | llm

    # Execute pipeline
    response = chain.invoke(
        {
            "story": story,
            "acceptance_criteria": acceptance_criteria,
            "similar_stories": context,
            "test_types": test_types,
        }
    )

    # Return generated Gherkin
    return response.content