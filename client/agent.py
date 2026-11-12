"""Simple agent-like client that consumes the MCP server through MCP."""

import asyncio
from pathlib import Path

from fastmcp import Client
from fastmcp.client.transports import StdioTransport

OUTPUT_FILE = (
    Path(__file__).resolve().parent.parent / "output" / "sample_agent_response.md"
)

SAMPLE_QUESTION = "I want to study Python decorators. What should I review first?"


def format_response(topic: dict | None) -> str:
    """Format a student-facing response from MCP topic data."""
    if topic is None:
        return """# Study Recommendation

No matching programming topic was found.

Try another topic, such as Python functions, lists, dictionaries, decorators,
or C pointers.
"""

    prerequisites = "\n".join(
        f"- {item}" for item in topic.get("prerequisites", [])
    )
    key_concepts = "\n".join(
        f"- {item}" for item in topic.get("key_concepts", [])
    )
    common_mistakes = "\n".join(
        f"- {item}" for item in topic.get("common_mistakes", [])
    )

    return f"""# Study Recommendation

## Recommended topic

**{topic.get("title", "Unknown topic")}**

{topic.get("summary", "")}

## Why this topic is relevant

This topic matches your request. Reviewing it will help you understand the
concepts and avoid common mistakes related to **{topic.get("title", "this subject")}**.

## Prerequisites

{prerequisites or "- No prerequisites listed."}

## Key concepts

{key_concepts or "- No key concepts listed."}

## Practice idea

{topic.get("practice_idea", "No practice idea is available for this topic.")}

## Common mistakes to avoid

{common_mistakes or "- No common mistakes listed."}
"""


async def answer_question(question: str) -> str:
    """Answer a programming study question using the MCP server.

    The agent first searches for a matching topic, then retrieves its full
    details through the MCP server.
    """
    transport = StdioTransport(
        command="python3",
        args=["-m", "server.learning_server"],
    )

    async with Client(transport) as client:
        search_result = await client.call_tool(
            "search_topics",
            {"query": question},
        )

        results = search_result.data

        if not results:
            return format_response(None)

        topic_id = results[0]["id"]

        details_result = await client.call_tool(
            "get_topic_details",
            {"topic_id": topic_id},
        )

        return format_response(details_result.data)


async def main() -> None:
    """Run the agent with a sample student request."""
    response = await answer_question(SAMPLE_QUESTION)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(response, encoding="utf-8")

    print(response)


if __name__ == "__main__":
    asyncio.run(main())
