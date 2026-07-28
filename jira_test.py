import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

JIRA_URL = os.getenv("JIRA_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")

ISSUE_KEY = "KAN-6"  # Change this if your issue key is different

url = f"{JIRA_URL}/rest/api/3/issue/{ISSUE_KEY}"

response = requests.get(
    url,
    auth=HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN),
    headers={
        "Accept": "application/json"
    }
)

print("=" * 50)
print("Status Code:", response.status_code)
print("=" * 50)

if response.status_code == 200:
    issue = response.json()

    print("Issue Key :", issue["key"])
    print("Summary   :", issue["fields"]["summary"])
    print("Status    :", issue["fields"]["status"]["name"])
else:
    print(response.text)