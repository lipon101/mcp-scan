"""Protocol checks: detectable MCP server, declared tools, valid manifest, documented transport."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import List

from ..models import CheckResult, Status
from ._util import find_readme, iter_files, read_text

CATEGORY = "protocol"

SERVER_HINTS = [
    r"\bFastMCP\b", r"from\s+mcp\b", r"import\s+mcp\b", r"\bServer\s*\(",
    r"@mcp\.tool", r"@server\.tool", r"list_tools", r"modelcontextprotocol",
    r"createSdkMcpServer", r"McpServer",
]
TOOL_HINTS = [
    r"@[\w.]*tool\b", r"list_tools", r"\"tools\"\s*:", r"'tools'\s*:",
    r"register_tool", r"add_tool", r"@[\w.]*resource\b",
]
MANIFEST_NAMES = ["mcp.json", "server.json", "manifest.json", ".mcp.json", "claude_desktop_config.json"]


def run(path: Path) -> List[CheckResult]:
    out: List[CheckResult] = []

    code_text = ""
    for f in iter_files(path):
        if f.suffix.lower() in {".py", ".js", ".ts", ".jsx", ".tsx"}:
            code_text += "\n" + read_text(f)

    is_server = any(re.search(h, code_text) for h in SERVER_HINTS)
    out.append(CheckResult(
        "protocol.detectable_server", CATEGORY,
        Status.PASS if is_server else Status.WARN,
        1.0 if is_server else 0.4, 3,
        "MCP server entrypoint detected" if is_server else "Could not detect an MCP server entrypoint",
    ))

    has_tools = any(re.search(h, code_text) for h in TOOL_HINTS)
    out.append(CheckResult(
        "protocol.declares_tools", CATEGORY,
        Status.PASS if has_tools else Status.WARN,
        1.0 if has_tools else 0.4, 2,
        "Tool/resource registration detected" if has_tools else "No tool declarations found",
    ))

    manifest = next((path / n for n in MANIFEST_NAMES if (path / n).exists()), None)
    if manifest is not None:
        try:
            data = json.loads(read_text(manifest))
            ok = isinstance(data, (dict, list))
            out.append(CheckResult(
                "protocol.valid_manifest", CATEGORY,
                Status.PASS if ok else Status.FAIL, 1.0 if ok else 0.2, 2,
                f"{manifest.name} parses as valid JSON",
            ))
        except Exception as e:
            out.append(CheckResult(
                "protocol.valid_manifest", CATEGORY, Status.FAIL, 0.0, 2,
                f"{manifest.name} is invalid JSON", detail=str(e),
            ))
    else:
        out.append(CheckResult(
            "protocol.valid_manifest", CATEGORY, Status.WARN, 0.5, 2,
            "No machine-readable manifest (e.g. mcp.json) found",
        ))

    readme = find_readme(path)
    rtxt = read_text(readme).lower() if readme else ""
    transport = any(t in rtxt for t in ["stdio", "http", "sse", "streamable"])
    out.append(CheckResult(
        "protocol.transport_documented", CATEGORY,
        Status.PASS if transport else Status.WARN,
        1.0 if transport else 0.5, 1,
        "Transport (stdio/http/sse) documented" if transport else "Transport not documented in README",
    ))

    return out
