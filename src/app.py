"""
AI Test Case Generator

Local:
- Ollama Local AI
- Groq Cloud AI

Streamlit Cloud:
- Groq Cloud AI only
"""

import os
import sys
import tempfile


# -----------------------------
# Path setup
# -----------------------------

sys.path.insert(
    0,
    os.path.dirname(__file__)
)


import streamlit as st
from dotenv import load_dotenv


# -----------------------------
# Page Config
# MUST be first Streamlit command
# -----------------------------

st.set_page_config(
    page_title="AI Test Case Generator",
    page_icon="🧪",
    layout="wide"
)


# -----------------------------
# Detect Streamlit Cloud
# -----------------------------

running_on_cloud = False

try:

    running_on_cloud = (
        st.secrets.get(
            "STREAMLIT_CLOUD",
            "false"
        )
        == "true"
    )

except Exception:

    running_on_cloud = False



# -----------------------------
# Environment
# -----------------------------

load_dotenv(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        ".env"
    )
)



# -----------------------------
# Imports
# -----------------------------

from init_chromadb import initialize_chromadb

from report_utils import generate_report

from pdf_report import create_pdf_report

from retriever import retrieve_similar_stories

from generator_groq import generate_test_cases_groq

from jira_client import fetch_story_from_jira



# -----------------------------
# Initialize ChromaDB
# -----------------------------

@st.cache_resource
def load_database():

    initialize_chromadb()


load_database()



# -----------------------------
# Local Ollama
# -----------------------------

ollama_available = False


if not running_on_cloud:

    try:

        from generator_ollama import generate_test_cases_ollama

        ollama_available = True


    except Exception:

        ollama_available = False



# -----------------------------
# Session State
# -----------------------------

if "story" not in st.session_state:

    st.session_state.story = ""


if "acceptance" not in st.session_state:

    st.session_state.acceptance = ""



# -----------------------------
# Header
# -----------------------------

st.markdown(
    """
    <h1 style="text-align:center">
    🧪 AI Test Case Generator
    </h1>

    <p style="text-align:center;color:gray">
    RAG + LLM powered BDD Test Case Generation
    </p>
    """,
    unsafe_allow_html=True
)



# -----------------------------
# Sidebar
# -----------------------------

with st.sidebar:

    st.header("⚙ Settings")


    if running_on_cloud:

        model = "Groq Cloud AI"

        st.success(
            "☁ Streamlit Cloud\n\n"
            "Using Groq Cloud AI only"
        )


    else:

        models = [
            "Groq Cloud AI"
        ]


        if ollama_available:

            models.insert(
                0,
                "Ollama Local AI"
            )


        model = st.radio(
            "Select AI Model",
            models
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



# -----------------------------
# Jira Import
# -----------------------------

st.subheader(
    "📥 Import User Story from Jira"
)


jira_issue_key = st.text_input(
    "Enter Jira Issue Key",
    placeholder="Example: KAN-6"
)



if st.button("📥 Fetch from Jira"):

    try:

        jira_data = fetch_story_from_jira(
            jira_issue_key.strip()
        )


        st.session_state.story = jira_data["story"]

        st.session_state.acceptance = jira_data["acceptance"]


        st.success(
            "Jira story imported successfully"
        )


    except Exception as e:

        st.error(e)



# -----------------------------
# Input
# -----------------------------

col1, col2 = st.columns(2)



with col1:

    story = st.text_area(
        "📝 User Story",
        value=st.session_state.story,
        height=220
    )



with col2:

    acceptance = st.text_area(
        "📋 Acceptance Criteria",
        value=st.session_state.acceptance,
        height=220
    )



generate = st.button(
    "🚀 Generate Test Cases",
    use_container_width=True
)



# -----------------------------
# Generate
# -----------------------------

if generate:


    if not story.strip():

        st.error(
            "Please enter user story"
        )

        st.stop()



    criteria_list = [

        x.strip()

        for x in acceptance.splitlines()

        if x.strip()

    ]



    with st.spinner(
        "🔎 Searching similar stories..."
    ):


        similar = retrieve_similar_stories(
            story,
            top_k
        )



    st.subheader(
        "🔎 Similar Stories"
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



    with st.spinner(
        "🤖 Generating test cases..."
    ):

        try:


            if (
                model == "Ollama Local AI"
                and ollama_available
            ):


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


        except Exception as e:

            st.error(e)

            st.stop()



    st.success(
        "Generated successfully"
    )


    st.subheader(
        "🧪 Generated Gherkin"
    )


    st.code(
        result,
        language="gherkin"
    )



    # -----------------------------
    # Evaluation
    # -----------------------------

    report = generate_report(

        story_title="User Story",

        manual_test_cases=criteria_list,

        generated_test_cases=result

    )



    st.subheader(
        "📊 Evaluation"
    )


    c1, c2, c3 = st.columns(3)


    c1.metric(
        "Manual Cases",
        report["manual_test_cases"]
    )


    c2.metric(
        "Generated",
        report["generated_scenarios"]
    )


    c3.metric(
        "Coverage",
        f'{report["coverage_percent"]}%'
    )



    pdf = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    )



    create_pdf_report(
        evaluation_result=report,
        output_path=pdf.name
    )



    with open(pdf.name, "rb") as f:

        st.download_button(

            "📄 Download PDF Report",

            f,

            file_name="evaluation_report.pdf",

            mime="application/pdf"

        )