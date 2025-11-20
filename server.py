from fastmcp import FastMCP
from jira import get_jira_issue, get_jira_issue_details, update_jira_issue_content, add_jira_comment_to_issue, create_jira_issue


mcp = FastMCP("Tracker and Release Assistant")


@mcp.tool()
def get_my_open_issues() -> str:
    """
    Fetch JIRA issues and return a JSON array string matching the requested format.
    Returned JSON format:
    [
        {"Issue": "key", "summary": "summary", "status": "status", "link": "link"},
        ...
    ]
    """
    return get_jira_issue()


@mcp.tool()
def issue_details(issue_key: str) -> str:
    """
    Fetch detailed information for a specific JIRA issue.

    Args:
        issue_key (str): The key of the JIRA issue to fetch.
    Returns:
        str: A JSON string containing detailed information about the issue.
    """
    return get_jira_issue_details(issue_key)


@mcp.tool()
def update_issue_content(issue_key: str, new_content: str, new_titel: str) -> str:
    """
    Update the content of a specific JIRA issue.

    Args:
        issue_key (str): The key of the JIRA issue to update.
        new_content (str): The new content to set for the issue.
        new_titel (str): The new title to set for the issue.
    Returns:
        str: A JSON string indicating success or failure of the update operation.
    """
    return update_jira_issue_content(issue_key, new_content, new_titel)


@mcp.tool()
def add_comment(issue_key: str, comment: str) -> str:
    """
    Add a comment to a specific JIRA issue.

    Args:
        issue_key (str): The key of the JIRA issue to comment on.
        comment (str): The comment text to add.
    Returns:
        str: A JSON string indicating success or failure of the comment operation.
    """
    return add_jira_comment_to_issue(issue_key, comment)

@mcp.tool()
def create_issue(summary: str, description: str, issue_type: str = "Task") -> str:
    """
    Create a new JIRA issue.

    Args:
        summary (str): The summary/title of the issue.
        description (str): The detailed description of the issue.
        issue_type (str): The type of the issue (default is "Task").
    Returns:
        str: A JSON string indicating success or failure of the create operation.
    """
    return create_jira_issue(summary, description, issue_type)


if __name__ == "__main__":
    mcp.run()
