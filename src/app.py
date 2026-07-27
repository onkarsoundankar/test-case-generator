"""
AI Test Case Generator UI
-------------------------
Streamlit Frontend

Features:
- RAG based similar story retrieval
- Ollama local LLM
- Groq Cloud LLM
- Download Gherkin feature file
"""

import os
import sys
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv


# -----------------------------
# Path setup
# -----------------------------

sys.path.insert(
    0,
    os.path.dirname(__file__)
)


# Load environment variables

load_dotenv(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        ".env"
    )
)


# Imports

from retriever import retrieve_similar_stories
from generator_ollama import generate_test_cases_ollama
from generator_groq import generate_test_cases_groq


# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="AI Test Case Generator",
    page_icon="🧪",
    layout="wide"
)


# -----------------------------
# Custom CSS
# -----------------------------

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        text-align: center;
        margin-bottom: 5px;
    }


    .subtitle {
        text-align:center;
        color:gray;
        font-size:18px;
        margin-bottom:30px;
    }


    .card {

        padding:20px;
        border-radius:12px;
        border:1px solid #ddd;
        margin-bottom:15px;

    }


    .stButton button {

        width:100%;
        height:45px;
        font-size:18px;
        font-weight:bold;

    }

    </style>
    """,
    unsafe_allow_html=True
)



# -----------------------------
# Header
# -----------------------------

st.markdown(
    """
    <div class="main-title">
    🧪 AI Test Case Generator
    </div>

    <div class="subtitle">
    Generate BDD Gherkin test cases using RAG + LLM
    </div>
    """,
    unsafe_allow_html=True
)



# -----------------------------
# Sidebar
# -----------------------------

with st.sidebar:


    st.header("⚙ Settings")


    model = st.radio(

        "Select AI Model",

        [
            "Ollama Local AI",
            "Groq Cloud AI"
        ]

    )


    st.divider()


    test_types = st.multiselect(

        "Test Coverage",

        [
            "Functional",
            "Negative",
            "Edge Cases",
            "Regression",
            "Smoke",
            "Security"
        ],

        default=[
            "Functional",
            "Negative",
            "Edge Cases"
        ]

    )


    top_k = st.slider(

        "Similar Stories",

        1,
        6,
        3

    )


    st.info(
        """
        Ollama:
        Free local AI model

        Groq:
        Fast cloud AI
        """
    )



# -----------------------------
# Input Section
# -----------------------------


col1, col2 = st.columns(
    2
)



with col1:

    st.subheader(
        "📝 User Story"
    )


    story = st.text_area(

        "Enter user story",

        placeholder=
        """
Example:

As a user,
I want to login using email and password
so that I can access my account.
""",

        height=220

    )



with col2:

    st.subheader(
        "📋 Acceptance Criteria"
    )


    criteria = st.text_area(

        "Enter acceptance criteria",

        placeholder=
        """
Example:

User can login with valid credentials.

Invalid password should show error.

Account locks after multiple failures.
""",

        height=220

    )



st.write("")

generate = st.button(
    "🚀 Generate Test Cases"
)



# -----------------------------
# Generation
# -----------------------------


if generate:


    if not story.strip():

        st.error(
            "Please enter user story"
        )


    else:


        criteria_list = [

            x.strip()

            for x in criteria.splitlines()

            if x.strip()

        ]


        # Retrieval

        with st.spinner(
            "🔎 Searching similar stories..."
        ):


            similar = retrieve_similar_stories(

                story,

                top_k=top_k

            )



        st.subheader(
            "🔎 Similar Stories Found"
        )


        for item in similar:


            with st.expander(

                item["title"]

            ):

                st.write(

                    item.get(
                        "story",
                        ""
                    )

                )

                st.write(

                    "Similarity Score:",

                    round(
                        item["similarity_score"],
                        2
                    )

                )



        # Generation

        with st.spinner(

            "🤖 Generating test cases..."

        ):


            try:


                if model == "Ollama Local AI":


                    result = generate_test_cases_ollama(

                        story,

                        criteria_list,

                        similar,

                        test_types

                    )


                else:


                    result = generate_test_cases_groq(

                        story,

                        criteria_list,

                        similar,

                        test_types

                    )



                st.success(
                    "Test cases generated successfully"
                )


                st.subheader(
                    "🧪 Generated Gherkin"
                )


                st.code(

                    result,

                    language="gherkin"

                )



                # Save file


                output_dir = os.path.join(

                    os.path.dirname(__file__),

                    "..",

                    "output"

                )


                os.makedirs(

                    output_dir,

                    exist_ok=True

                )


                timestamp = datetime.now().strftime(

                    "%Y%m%d_%H%M%S"

                )


                filename = (

                    f"test_cases_{timestamp}.feature"

                )


                path = os.path.join(

                    output_dir,

                    filename

                )


                with open(

                    path,

                    "w"

                ) as f:

                    f.write(result)



                st.download_button(

                    label="⬇ Download Feature File",

                    data=result,

                    file_name=filename,

                    mime="text/plain"

                )



            except Exception as e:


                st.error(

                    f"Generation failed: {e}"

                )