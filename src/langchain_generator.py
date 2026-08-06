"""
langchain_generator.py
----------------------
LangChain based test case generator.
"""

from langchain_core.output_parsers import StrOutputParser

from langchain_prompt import gherkin_prompt
from langchain_llm import get_llm



def generate_test_cases(
        story,
        acceptance,
        similar_stories,
        coverage,
        model_type
):

    """
    Generates Gherkin test cases
    using LangChain pipeline.
    """


    llm = get_llm(
        model_type
    )


    chain = (
        gherkin_prompt
        |
        llm
        |
        StrOutputParser()
    )


    response = chain.invoke(
        {
            "story": story,
            "acceptance": acceptance,
            "similar_stories": similar_stories,
            "coverage": coverage
        }
    )


    return response