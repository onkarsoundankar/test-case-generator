"""
AI Test Case Generator
----------------------

Local:
- Ollama Local AI
- Groq Cloud AI

Streamlit Cloud:
- Groq Cloud AI only
"""


import os
import sys
import tempfile
from datetime import datetime


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
# Environment Detection
# -----------------------------

running_on_cloud = (
    os.getenv("STREAMLIT_SHARING_MODE") == "1"
    or
    "STREAMLIT_RUNTIME" in os.environ
)


# -----------------------------
# Load Environment Variables
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

from report_utils import (
    generate_report,
)

from pdf_report import (
    create_pdf_report
)


from retriever import (
    retrieve_similar_stories
)


from generator_groq import (
    generate_test_cases_groq
)


from jira_client import (
    fetch_story_from_jira
)


# -----------------------------
# Initialize ChromaDB
# -----------------------------

@st.cache_resource
def load_database():

    initialize_chromadb()


load_database()



# -----------------------------
# Import Ollama Only Locally
# -----------------------------

ollama_available = False


if not running_on_cloud:

    try:

        from generator_ollama import (
            generate_test_cases_ollama
        )

        ollama_available = True


    except Exception:

        ollama_available = False



# -----------------------------
# Page Setup
# -----------------------------

st.set_page_config(
    page_title="AI Test Case Generator",
    page_icon="🧪",
    layout="wide"
)



# -----------------------------
# Session State
# -----------------------------

if "story" not in st.session_state:

    st.session_state["story"] = ""


if "acceptance" not in st.session_state:

    st.session_state["acceptance"] = ""



# -----------------------------
# CSS
# -----------------------------

st.markdown(
"""
<style>

.title {

font-size:42px;
font-weight:700;
text-align:center;

}


.subtitle {

text-align:center;
color:gray;
font-size:18px;

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
<div class="title">
🧪 AI Test Case Generator
</div>

<div class="subtitle">
RAG + LLM powered BDD Test Case Generation
</div>

""",
unsafe_allow_html=True
)



# -----------------------------
# Sidebar
# -----------------------------

with st.sidebar:


    st.header(
        "⚙ Settings"
    )


    if running_on_cloud:


        model = "Groq Cloud AI"


        st.info(
            "Running on Streamlit Cloud\n\nUsing Groq AI only"
        )


    else:


        available_models = [
            "Groq Cloud AI"
        ]


        if ollama_available:

            available_models.insert(
                0,
                "Ollama Local AI"
            )


        model = st.radio(

            "Select AI Model",

            available_models

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


    if jira_issue_key.strip():

        try:


            jira_data = fetch_story_from_jira(

                jira_issue_key.strip()

            )


            st.session_state["story"] = jira_data["story"]

            st.session_state["acceptance"] = jira_data["acceptance"]


            st.success(

                f"{jira_issue_key} imported successfully!"

            )


        except Exception as e:


            st.error(

                f"Unable to fetch Jira story.\n\n{e}"

            )



# -----------------------------
# Input Area
# -----------------------------


col1, col2 = st.columns(2)



with col1:


    st.subheader(
        "📝 User Story"
    )


    story = st.text_area(

        "Enter User Story",

        value=st.session_state["story"],

        height=220

    )



with col2:


    st.subheader(
        "📋 Acceptance Criteria"
    )


    acceptance = st.text_area(

        "Enter Acceptance Criteria",

        value=st.session_state["acceptance"],

        height=220

    )



generate = st.button(

    "🚀 Generate Test Cases",

    use_container_width=True

)