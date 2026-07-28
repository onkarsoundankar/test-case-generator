"""
jira_client.py
----------------
Optional: fetch a user story directly from Jira by issue key (e.g. "PROJ-123")
instead of pasting the text manually. Requires JIRA_URL, JIRA_EMAIL, and
JIRA_API_TOKEN to be set in your .env file.
"""

import os
import requests


def fetch_story_from_jira(issue_key: str):
    jira_url = os.environ.get("JIRA_URL")
    jira_email = os.environ.get("JIRA_EMAIL")
    jira_token = os.environ.get("JIRA_API_TOKEN")

    if not all([jira_url, jira_email, jira_token]):
        raise EnvironmentError(
            "Jira credentials missing. Set JIRA_URL, JIRA_EMAIL, and JIRA_API_TOKEN in your .env file."
        )

    url = f"{jira_url.rstrip('/')}/rest/api/3/issue/{issue_key}"

    response = requests.get(
        url,
        auth=(jira_email, jira_token),
        headers={"Accept": "application/json"},
    )

    response.raise_for_status()

    data = response.json()

    fields = data.get("fields", {})
    summary = fields.get("summary", "")

    # Jira Cloud stores description as Atlassian Document Format (ADF)
    description = fields.get("description")
    description_text = (
        _extract_text_from_adf(description)
        if description
        else ""
    )

    story = f"{summary}\n\n{description_text}".strip()

    acceptance = ""

    if "Acceptance Criteria:" in story:
        story, acceptance = story.split(
            "Acceptance Criteria:",
            1
        )

    return {
        "story": story.strip(),
        "acceptance": acceptance.strip()
    }


def _extract_text_from_adf(node):
    """Recursively pull plain text out of Atlassian Document Format JSON."""

    if node is None:
        return ""

    text_parts = []

    if isinstance(node, dict):

        if node.get("type") == "text":
            text_parts.append(node.get("text", ""))

        for child in node.get("content", []):
            text_parts.append(_extract_text_from_adf(child))

    elif isinstance(node, list):

        for child in node:
            text_parts.append(_extract_text_from_adf(child))

    return " ".join(t for t in text_parts if t)