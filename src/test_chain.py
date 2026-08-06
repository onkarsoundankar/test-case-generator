from chain import generate_test_cases

story = """
As a registered user,
I want to log in using my email and password,
so that I can access my account.
"""

acceptance_criteria = """
Given valid credentials
When the user logs in
Then the dashboard is displayed.
"""

test_cases = generate_test_cases(
    story=story,
    acceptance_criteria=acceptance_criteria,
    test_types="Functional, Negative",
    top_k=3,
)

print(test_cases)