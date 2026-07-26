"""Deployable FastAPI dashboard for the mcp-scan leaderboard.

Run locally:
    pip install "mcp-scan[web]"
    MCP_SCAN_TARGETS=./examples/good_server,./examples/bad_server \
        uvicorn mcp_scan.webapp:app --reload

Deploy: any platform that runs a Python web app (Fly.io / Render / Railway).
Set MCP_SCAN_TARGETS to a comma-separated list of repo paths or git URLs.
"""
from __future__ import annotations

import os

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from .leaderboard import DEFAULT_REPOS, build_leaderboard, to_html

app = FastAPI(title="mcp-scan leaderboard", version="0.3.0")
_cache: dict = {"data": None}


def _targets() -> list:
    env = os.environ.get("MCP_SCAN_TARGETS")
    if env:
        return [t.strip() for t in env.split(",") if t.strip()]
    return DEFAULT_REPOS


def _board() -> dict:
    if _cache["data"] is None:
        _cache["data"] = build_leaderboard(_targets())
    return _cache["data"]


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    return to_html(_board())


@app.get("/api/leaderboard")
def api() -> dict:
    return _board()


@app.post("/api/refresh")
def refresh() -> dict:
    _cache["data"] = None
    return {"refreshed": True, "count": _board()["count"]}


@app.get("/healthz")
def healthz() -> dict:
    return {"ok": True}
