# Changelog

## [1.0.0] - 2026-07-26
### Changed
- **Renamed the package** from `mcp-scan` to **`mcp-grade`** to take a unique PyPI name (the previous name was already owned by an unrelated package).
  - Install: `pipx install mcp-grade`
  - Commands: `mcp-grade` and `mcp-grade-leaderboard`
  - Import module: `mcp_grade`
- First stable release — ready for the GitHub Marketplace.


## [0.3.0] - 2026-07-26
### Added
- **Live protocol probing** (`--live`): actually launches the server over stdio and verifies the MCP handshake (`initialize` + `list_tools`) using the MCP SDK. Folded into the Protocol category; off by default. Needs `pip install mcp-grade[live]`.
- `--command` to control how `--live` launches a server (default: auto-detect `server.py`).
- **Leaderboard engine + CLI** (`mcp-grade-leaderboard`): scan many servers (paths or git URLs), rank them A–F, and emit JSON / Markdown / a static HTML page. Seeds with a curated list of popular real MCP servers.
- **Web dashboard** (`mcp_grade/webapp.py`): a deployable FastAPI app serving the leaderboard HTML + `/api/leaderboard` JSON. Needs `pip install mcp-grade[web]`.
- Scheduled `.github/workflows/leaderboard.yml` to regenerate the leaderboard weekly.
### Changed
- `scanner.scan()` accepts `live=` and `command=`.

## [0.2.0] - 2026-07-26
### Added
- **GitHub Action** (`action.yml`): composite action that installs mcp-grade and grades a repo in CI, with `grade`/`score` outputs, a `fail-under` gate, and an uploaded report-card artifact.
- `--json PATH` flag: machine-readable JSON summary for CI and dashboards.
- Repo CI workflow (`.github/workflows/ci.yml`) that runs the tests and dogfoods the gate on the good/bad examples.
### Changed
- Report-card footer now reports the real package version.

## [0.1.0] - 2026-07-26
### Added
- Initial release.
- Five check categories: security, liveness, protocol, usability, docs.
- Rich terminal report card with A–F grading.
- Markdown report export (`--report`) and shields badge (`--badge`).
- CI gate via `--fail-under`.
- Scan local paths or clone & scan git URLs.
