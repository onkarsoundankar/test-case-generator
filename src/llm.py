import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq


# Load .env from project root
load_dotenv(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        ".env"
    )
)


def get_llm():

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise Exception(
            "GROQ_API_KEY not found. Check your .env file."
        )

    return ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.2,
        api_key=api_key,
    )