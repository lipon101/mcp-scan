"""A well-structured example MCP server (used as mcp-grade's 'good' fixture)."""
import os

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("weather")

# Read secrets from the environment — never hardcode them.
API_KEY = os.environ.get("WEATHER_API_KEY", "")


@mcp.tool()
def get_weather(city: str) -> str:
    """Return the current weather for a city."""
    if not API_KEY:
        return "WEATHER_API_KEY is not set."
    # (pretend we call a weather API here)
    return f"Sunny, 28°C in {city}"


@mcp.tool()
def list_cities() -> list[str]:
    """List supported cities."""
    return ["Dhaka", "London", "Tokyo"]


if __name__ == "__main__":
    mcp.run()
