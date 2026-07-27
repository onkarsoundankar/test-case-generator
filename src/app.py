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


# -----------------------------
# Imports
# -----------------------------

from retriever import retrieve_similar_stories

from generator_groq import (
    generate_test_cases_groq
)


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


col1, col2 = st.columns(2)



with col1:


    st.subheader(
        "📝 User Story"
    )


    story = st.text_area(

        "Enter User Story",

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



            # Save output


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


            filepath = os.path.join(

                output_dir,

                filename

            )


            with open(

                filepath,

                "w"

            ) as file:


                file.write(result)



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