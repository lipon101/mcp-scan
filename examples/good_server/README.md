# weather-mcp (example "good" server)

Get current weather for any city from one MCP tool — a clean, well-packaged reference server.

## Install

```bash
pip install weather-mcp
```

## Usage / quickstart

Add it to your Claude Desktop config, then ask "What's the weather in Dhaka?"

```json
{
  "mcpServers": {
    "weather": {
      "command": "weather-mcp",
      "transport": "stdio"
    }
  }
}
```

```python
# Or call the tool directly
from weather_mcp.server import mcp
```

## Configuration

Set your API key via environment (never commit it):

```bash
export WEATHER_API_KEY=...   # see .env.example
```

## Permissions

This server only makes outbound HTTPS calls to the weather API and reads the
`WEATHER_API_KEY` environment variable. It does not touch the filesystem.

## Transport

Runs over **stdio**. See `examples/` for more.
