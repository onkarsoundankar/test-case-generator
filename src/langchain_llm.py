"""
langchain_llm.py
----------------
Creates LangChain compatible LLM clients.
Supports:
- Ollama (local)
- Groq (cloud)
"""


import os



def get_llm(model_type):

    """
    Returns LangChain LLM object.
    """

    if model_type == "ollama":

        from langchain_ollama import ChatOllama


        llm = ChatOllama(
            model="qwen2.5:7b",
            temperature=0.2
        )


        return llm



    elif model_type == "groq":

        from langchain_groq import ChatGroq


        llm = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0.2,
            api_key=os.getenv(
                "GROQ_API_KEY"
            )
        )


        return llm



    else:

        raise ValueError(
            f"Unsupported model type: {model_type}"
        )