import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()

api_base_url = "https://rb-tracker.bosch.com/tracker19"

# Use single quotes inside f-strings to avoid quoting issues
auth_headers = {"Authorization": f"Bearer {os.getenv('ACCESS_TOKEN')}"}

def get_jira_issue() -> str:
    """Fetch JIRA issues and return a JSON array string matching the requested format.

    Returned JSON format:
    [
        {"Issue": "key", "summary": "summary", "status": "status", "link": "link"},
        ...
    ]
    """
    jira_url = (
        f"{api_base_url}/rest/agile/1.0/board/71043/issue"
        "?jql=assignee=NRS1FE+and+status+IN+(%22In+Progress%22)"
        "&fields=summary,description,status&orderBy=+updated"
    )
    response = requests.get(jira_url, headers=auth_headers)

    # On non-200 responses return a JSON object with error details
    if response.status_code != 200:
        return json.dumps({
            "error": True,
            "status_code": response.status_code,
            "message": response.text,
        })

    issues = response.json().get("issues", [])
    if not issues:
        return json.dumps([])

    issue_list = []
    for issue in issues:
        key = issue.get("key")
        summary = issue.get("fields", {}).get("summary")
        status = issue.get("fields", {}).get("status", {}).get("name")
        description = issue.get("fields", {}).get("description", "")
        issue_list.append({
            "Issue": key,
            "summary": summary,
            "description":description,
            "status": status,
            "link": f"{api_base_url}/browse/{key}"
        })

    return json.dumps(issue_list)


def get_jira_issue_details(issue_key: str) -> str:
    """Fetch detailed information for a specific JIRA issue.

    Args:
        issue_key (str): The key of the JIRA issue to fetch.
    Returns:
        str: A JSON string containing detailed information about the issue.
    """ 
    jira_url = f"{api_base_url}/rest/api/2/issue/{issue_key}"
    response = requests.get(jira_url, headers=auth_headers)

    if response.status_code != 200:
        return json.dumps({
            "error": True,
            "status_code": response.status_code,
            "message": response.text,
        })

    issue = response.json()
    key = issue.get("key")
    fields = issue.get("fields", {})
    summary = fields.get("summary")
    description = fields.get("description", "")
    status = fields.get("status", {}).get("name")
    assignee = fields.get("assignee", {}).get("displayName", "Unassigned")
    reporter = fields.get("reporter", {}).get("displayName", "Unknown")
    created = fields.get("created")
    updated = fields.get("updated")

    issue_details = {
        "Issue": key,
        "summary": summary,
        "description": description,
        "status": status,
        "assignee": assignee,
        "reporter": reporter,
        "created": created,
        "updated": updated,
        "link": f"{api_base_url}/browse/{key}"
    }

    return json.dumps(issue_details)

    
def update_jira_issue_content(issue_key: str, new_description: str,new_title:str) -> str:
    """Update the description of a JIRA issue.

    Args:
        issue_key (str): The key of the JIRA issue to update.
        new_description (str): The new description content.
        new_title (str): The new title content.
    Returns:
        str: A message indicating success or failure.
    """
    jira_url = f"{api_base_url}/rest/api/2/issue/{issue_key}"
    payload = {
        "fields": {
            "description": new_description,
            "summary": new_title
        }
    }
    response = requests.put(jira_url, headers={**auth_headers, "Content-Type": "application/json"}, json=payload)

    if response.status_code == 204:
        return f"Issue {issue_key} updated successfully."
    else:
        return f"Failed to update issue {issue_key}. Status code: {response.status_code}, Message: {response.text}"
    

def add_jira_comment_to_issue(issue_key: str, comment: str) -> str:
    """Add a comment to a JIRA issue.

    Args:
        issue_key (str): The key of the JIRA issue to comment on.
        comment (str): The comment text to add.
    Returns:
        str: A message indicating success or failure.
    """
    jira_url = f"{api_base_url}/rest/api/2/issue/{issue_key}/comment"
    payload = {
        "body": comment
    }
    response = requests.post(jira_url, headers={**auth_headers, "Content-Type": "application/json"}, json=payload)

    if response.status_code == 201:
        return f"Comment added to issue {issue_key} successfully."
    else:
        return f"Failed to add comment to issue {issue_key}. Status code: {response.status_code}, Message: {response.text}"
    
def create_jira_issue(summary: str, description: str, issue_type: str = "Task") -> str:
    """Create a new JIRA issue.

    Args:
        summary (str): The summary/title of the issue.
        description (str): The description/content of the issue.
        issue_type (str): The type of the issue (default is "Task").
    Returns:
        str: A message indicating success or failure.
    """
    jira_url = f"{api_base_url}/rest/api/2/issue"
    payload = {
        "fields": {
            "project": {
                "key": "TFA"  # Replace with your project key
            },
            "summary": summary,
            "description": description,
            "issuetype": {
                "name": issue_type
            }
        }
    }
    response = requests.post(jira_url, headers={**auth_headers, "Content-Type": "application/json"}, json=payload)

    if response.status_code == 201:
        issue_key = response.json().get("key")
        return f"Issue {issue_key} created successfully."
    else:
        return f"Failed to create issue. Status code: {response.status_code}, Message: {response.text}"