from retriever import retrieve_similar_stories

story = """
As a user,
I want to login using email and password
so that I can access my dashboard.
"""

results = retrieve_similar_stories(story)

for item in results:
    print("=" * 60)
    print("Title:", item["title"])
    print("Similarity:", item["similarity_score"])
    print()

    print("Story:")
    print(item["story"])
    print()

    print("Acceptance Criteria:")
    for ac in item["acceptance_criteria"]:
        print("-", ac)

    print()

    print("Test Cases:")
    for tc in item["test_cases"]:
        print(tc)
        print()