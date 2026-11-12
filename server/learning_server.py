"""Basic FastMCP server exposing programming learning capabilities."""

import json
from pathlib import Path

from fastmcp import FastMCP

mcp = FastMCP("Programming Learning Server")

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "topics.json"


def load_topics() -> list[dict]:
    """Load the programming topics stored in the local JSON dataset."""
    with DATA_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


@mcp.tool
def search_topics(query: str) -> list[dict]:
    """Search programming topics by title, summary, prerequisites, or key concepts.

    Args:
        query: Text used to find relevant programming topics.

    Returns:
        A list of matching topic summaries. Returns an empty list when no topic matches.
    """
    query = query.strip().lower()

    if not query:
        return []

    matching_topics = []

    for topic in load_topics():
        searchable_text = " ".join(
            [
                topic.get("title", ""),
                topic.get("summary", ""),
                " ".join(topic.get("prerequisites", [])),
                " ".join(topic.get("key_concepts", [])),
            ]
        ).lower()

        if query in searchable_text:
            matching_topics.append(
                {
                    "id": topic.get("id"),
                    "title": topic.get("title"),
                    "summary": topic.get("summary"),
                    "key_concepts": topic.get("key_concepts", []),
                }
            )

    return matching_topics


@mcp.tool
def get_topic_details(topic_id: str) -> dict:
    """Return the full information for a programming topic by its unique id.

    Args:
        topic_id: The unique identifier of the topic to retrieve.

    Returns:
        The full topic data when the id exists, or an error message when it does not.
    """
    topic_id = topic_id.strip()

    if not topic_id:
        return {
            "error": "Missing topic id.",
            "message": "Provide a valid topic id, for example 'python-decorators'.",
        }

    for topic in load_topics():
        if topic.get("id") == topic_id:
            return topic

    return {
        "error": "Topic not found.",
        "message": f"No topic found with id '{topic_id}'.",
    }


if __name__ == "__main__":
    mcp.run()
