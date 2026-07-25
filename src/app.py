"""
app.py
-------
A simple browser-based demo of the pipeline (retrieval + generation),
so you don't need to type Terminal commands during a demo.

Run with:
    streamlit run src/app.py

This opens a local web page at http://localhost:8501 that you interact
with entirely through buttons and text boxes.
"""

import os
import sys
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(__file__))

from retriever import retrieve_similar_stories
from generator import generate_test_cases, generate_test_cases_mock, build_user_prompt, SYSTEM_PROMPT

load_dotenv()

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "output")

st.set_page_config(page_title="AI Test Case Generator", page_icon="🧪", layout="wide")

st.title("🧪 AI-Powered Test Case Generator")
st.caption("RAG pipeline: retrieves similar past stories, then generates BDD/Gherkin test cases.")

has_api_key = bool(os.environ.get("ANTHROPIC_API_KEY"))

with st.sidebar:
    st.header("Settings")

    if has_api_key:
        mode = st.radio(
            "Generation mode",
            ["Real AI (uses API credits)", "Free mock (no API call)", "Show prompt only (paste into claude.ai)"],
            index=0,
        )
    else:
        st.info("No ANTHROPIC_API_KEY found in .env — real AI generation is disabled.")
        mode = st.radio(
            "Generation mode",
            ["Free mock (no API call)", "Show prompt only (paste into claude.ai)"],
            index=0,
        )

    test_types = st.multiselect(
        "Test types to generate",
        ["functional", "edge", "negative", "smoke", "regression", "exploratory"],
        default=["functional", "edge", "negative"],
    )
    top_k = st.slider("Number of similar past examples to retrieve", 1, 6, 3)

st.subheader("1. Enter a user story")
story_text = st.text_area(
    "User story",
    placeholder="As a user, I want to reset my password via email so that I can regain access to my account.",
    height=100,
)
acceptance_criteria_raw = st.text_area(
    "Acceptance criteria (one per line, optional)",
    placeholder="User can request a reset link via email\nReset link expires after 30 minutes\nNew password must meet complexity rules",
    height=100,
)

generate_clicked = st.button("Generate Test Cases", type="primary", use_container_width=True)

if generate_clicked:
    if not story_text.strip():
        st.error("Please enter a user story first.")
    else:
        acceptance_criteria = [line.strip() for line in acceptance_criteria_raw.splitlines() if line.strip()]

        with st.spinner("Retrieving similar past stories..."):
            similar = retrieve_similar_stories(story_text, top_k=top_k)

        st.subheader("2. Retrieved similar past stories (RAG match)")
        for ex in similar:
            st.write(f"**{ex['title']}** — similarity: `{ex['similarity_score']:.2f}`")

        st.subheader("3. Generated test cases")

        if mode == "Show prompt only (paste into claude.ai)":
            prompt = build_user_prompt(story_text, acceptance_criteria, similar, test_types)
            full_prompt = SYSTEM_PROMPT + "\n\n" + prompt
            st.info("Copy the box below, paste it into https://claude.ai, then paste the reply back here manually.")
            st.code(full_prompt, language="text")

        elif mode == "Free mock (no API call)":
            with st.spinner("Generating mock test cases..."):
                result = generate_test_cases_mock(story_text, acceptance_criteria, similar, test_types)
            st.code(result, language="gherkin")

            os.makedirs(OUTPUT_DIR, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(OUTPUT_DIR, f"test_cases_{timestamp}.feature")
            with open(output_path, "w") as f:
                f.write(result)
            st.success(f"Saved to: {output_path}")
            st.download_button("Download .feature file", result, file_name=f"test_cases_{timestamp}.feature")

        else:  # Real AI
            with st.spinner("Calling Claude..."):
                try:
                    result = generate_test_cases(story_text, acceptance_criteria, similar, test_types)
                    st.code(result, language="gherkin")

                    os.makedirs(OUTPUT_DIR, exist_ok=True)
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    output_path = os.path.join(OUTPUT_DIR, f"test_cases_{timestamp}.feature")
                    with open(output_path, "w") as f:
                        f.write(result)
                    st.success(f"Saved to: {output_path}")
                    st.download_button("Download .feature file", result, file_name=f"test_cases_{timestamp}.feature")
                except Exception as e:
                    st.error(f"Generation failed: {e}")
