"""Live protocol probing — actually launch an MCP server and verify the handshake.

Optional and OFF by default so mcp-scan stays fast and works offline. Enable with
`mcp-scan <target> --live`. Requires the MCP SDK: `pip install mcp-scan[live]`.

A server that *runs and answers* is worth more than one that merely looks correct,
so live evidence is folded into the Protocol category when enabled.
"""
from __future__ import annotations

import asyncio
import shlex
import sys
import time
from pathlib import Path
from typing import List, Optional

from .models import CheckResult, Status

CATEGORY = "protocol"
DEFAULT_TIMEOUT = 20.0


def _find_entrypoint(path: Path) -> Optional[List[str]]:
    """Best-effort guess at how to launch the server as a stdio subprocess."""
    for name in ["server.py", "main.py", "app.py", "__main__.py"]:
        if (path / name).exists():
            return [sys.executable, name]
    return None


async def _handshake(command: str, args: List[str], cwd: str, timeout: float):
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    params = StdioServerParameters(command=command, args=args, cwd=cwd)
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            init = await asyncio.wait_for(session.initialize(), timeout=timeout)
            tools = await asyncio.wait_for(session.list_tools(), timeout=timeout)
            tool_names = [t.name for t in tools.tools]
            return init, tool_names


def probe(path: Path, command: Optional[str] = None, timeout: float = DEFAULT_TIMEOUT) -> List[CheckResult]:
    """Run live checks. Never raises — every path returns CheckResults."""
    out: List[CheckResult] = []

    parts = shlex.split(command) if command else _find_entrypoint(path)
    if not parts:
        out.append(CheckResult(
            "protocol.live_launchable", CATEGORY, Status.WARN, 0.4, 2,
            "No entrypoint found to launch (pass --command 'python server.py')"))
        return out

    try:
        import mcp  # noqa: F401
    except Exception:
        out.append(CheckResult(
            "protocol.live_sdk", CATEGORY, Status.WARN, 0.5, 1,
            "MCP SDK not installed — `pip install mcp-scan[live]` to enable live probing"))
        return out

    t0 = time.time()
    try:
        init, tool_names = asyncio.run(_handshake(parts[0], parts[1:], str(path), timeout))
        latency = int((time.time() - t0) * 1000)
        server_name = getattr(getattr(init, "serverInfo", None), "name", None) or "?"
        out.append(CheckResult(
            "protocol.live_handshake", CATEGORY, Status.PASS, 1.0, 3,
            f"Server '{server_name}' initialized over stdio in {latency} ms"))
        if tool_names:
            out.append(CheckResult(
                "protocol.live_lists_tools", CATEGORY, Status.PASS, 1.0, 2,
                f"Listed {len(tool_names)} tool(s)", detail=", ".join(tool_names[:12])))
        else:
            out.append(CheckResult(
                "protocol.live_lists_tools", CATEGORY, Status.WARN, 0.5, 2,
                "Server responded but exposed 0 tools"))
    except Exception as e:
        out.append(CheckResult(
            "protocol.live_handshake", CATEGORY, Status.FAIL, 0.0, 3,
            f"Live handshake failed: {type(e).__name__}", detail=str(e)[:240]))
    return out
