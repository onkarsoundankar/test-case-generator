from prompt import PROMPT_TEMPLATE

prompt = PROMPT_TEMPLATE.invoke(
    {
        "story": "User Login",
        "acceptance_criteria": "User logs in with valid credentials.",
        "similar_stories": "Login story from database.",
        "test_types": "Functional, Negative"
    }
)

print(prompt.text)