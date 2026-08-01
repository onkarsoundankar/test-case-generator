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
from datetime import datetime
from report_utils import generate_report, report_to_json
from init_chromadb import initialize_chromadb
import streamlit as st
from dotenv import load_dotenv

initialize_chromadb()
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


# -----------------------------
# Imports
# -----------------------------

from retriever import retrieve_similar_stories

from generator_groq import (
    generate_test_cases_groq
)

from jira_client import fetch_story_from_jira


# Import Ollama safely

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
# Detect Environment
# -----------------------------


running_on_cloud = (
    os.getenv(
        "STREAMLIT_SHARING_MODE"
    )
    or
    os.getenv(
        "IS_STREAMLIT_CLOUD"
    )
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
            "Running on Streamlit Cloud\n\nUsing Groq AI"
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
# Input
# -----------------------------

# -----------------------------
# Jira Import
# -----------------------------

st.subheader("📥 Import User Story from Jira")

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

col1, col2 = st.columns(2)



with col1:

    st.subheader(
        "📝 User Story"
    )

    story = st.text_area(
        "Enter User Story",
        value=st.session_state.get("story", ""),
        height=220,
        placeholder="""
Example:

As a user,
I want to login using email and password
so that I can access my account.
"""

    )



with col2:

    st.subheader(
        "📋 Acceptance Criteria"
    )

    acceptance = st.text_area(
        "Enter Acceptance Criteria",
        value=st.session_state.get(
            "acceptance",
            ""
        ),
        height=220,
        placeholder="""
Example:

User can login successfully.

Invalid password shows error.

Account locks after failed attempts.
"""
    )



st.write("")



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
            "Please enter a user story"
        )


        st.stop()



    criteria_list = [

        x.strip()

        for x in acceptance.splitlines()

        if x.strip()

    ]



    # Retrieval

    with st.spinner(
        "🔎 Finding similar stories..."
    ):


        similar = retrieve_similar_stories(

            story,

            top_k=top_k

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


            st.write(

                "Similarity:",

                round(

                    item[
                        "similarity_score"
                    ],

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

                "Generated successfully"

            )


            st.subheader(

                "🧪 Generated Gherkin"

            )


            st.code(

                result,

                language="gherkin"

            )


        except Exception as e:


            st.error(

                f"Generation failed: {e}"

            )


            st.stop()

    # -----------------------------
    # Evaluation Report
    # -----------------------------

    report = generate_report(

        story_title="User Story",

        manual_test_cases=criteria_list,

        generated_test_cases=result

    )


    st.subheader(
        "📊 Evaluation Summary"
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Manual Test Cases",
            report["manual_test_cases"]
        )


    with col2:

        st.metric(
            "Generated Scenarios",
            report["generated_scenarios"]
        )


    with col3:

        st.metric(
            "Coverage",
            f'{report["coverage_percent"]}%'
        )
                

    report_json = report_to_json(
        report
    )


    st.download_button(
        label="📥 Download Evaluation Report (JSON)",
        data=report_json,
        file_name="evaluation_report.json",
        mime="application/json"
    )


    # -----------------------------
    # Save Feature File
    # -----------------------------


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


    filename = f"test_cases_{timestamp}.feature"


    filepath = os.path.join(
        output_dir,
        filename
    )


    with open(filepath, "w") as file:

        file.write(result)



 import tempfile

from pdf_report import create_pdf_report

pdf_file = tempfile.NamedTemporaryFile(
    delete=False,
    suffix=".pdf"
)

create_pdf_report(
    evaluation_result=report,
    output_path=pdf_file.name
)

with open(pdf_file.name, "rb") as f:

    st.download_button(
        label="📄 Download Evaluation Report (PDF)",
        data=f,
        file_name="evaluation_report.pdf",
        mime="application/pdf",
    )