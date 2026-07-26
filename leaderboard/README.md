# 🏆 mcp-scan leaderboard

A ranked scoreboard of MCP servers, graded A–F by `mcp-scan`.

## Generate it

```bash
# Scan the curated list of popular servers (clones each, ~1 min)
mcp-scan-leaderboard --html leaderboard.html --json leaderboard.json --md leaderboard.md

# Or scan your own targets / a file of repos
mcp-scan-leaderboard --from-file leaderboard/repos.txt --html leaderboard.html

# Add live handshakes (slower, needs the [live] extra)
mcp-scan-leaderboard --from-file leaderboard/repos.txt --live --html leaderboard.html
```

Edit `repos.txt` to control which servers are ranked (one repo per line).

## Serve it live (web dashboard)

```bash
pip install "mcp-scan[web]"
MCP_SCAN_TARGETS="https://github.com/microsoft/playwright-mcp,https://github.com/github/github-mcp-server" \
    uvicorn mcp_scan.webapp:app --host 0.0.0.0 --port 8000
```

- `GET /` — the leaderboard HTML page
- `GET /api/leaderboard` — JSON
- `POST /api/refresh` — force a re-scan
- `GET /healthz` — health check

**Deploy** to Fly.io / Render / Railway: point the start command at
`uvicorn mcp_scan.webapp:app --host 0.0.0.0 --port $PORT` and set `MCP_SCAN_TARGETS`.

## Automate it

`.github/workflows/leaderboard.yml` regenerates the leaderboard weekly (Mondays 06:00 UTC)
and on demand (`workflow_dispatch`), uploading JSON/HTML/Markdown as workflow artifacts.
Publish those to GitHub Pages for a zero-host scoreboard.
