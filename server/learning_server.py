"""Basic FastMCP server exposing programming learning capabilities."""

from fastmcp import FastMCP

mcp = FastMCP("Programming Learning Server")


if __name__ == "__main__":
    mcp.run()
