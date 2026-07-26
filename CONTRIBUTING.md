# Contributing to mcp-scan

Thanks for your interest! mcp-scan is intentionally small and opinionated.

## Adding a check

1. Create/edit a module in `mcp_scan/checks/` exposing `CATEGORY` and `run(path) -> list[CheckResult]`.
2. Register it in `mcp_scan/checks/__init__.py` (`ALL_CHECK_MODULES`).
3. Keep it fast and side-effect free — checks must never crash the scan (errors are caught and reported as a warning).
4. Add a test in `tests/` and, if useful, extend the `examples/good_server` / `examples/bad_server` fixtures.

## Development setup

```bash
pip install -e ".[dev]"
pytest -q
```

## Guidelines

- Security checks are weighted highest; don't dilute that.
- Prefer clear, actionable messages ("Committed .env file detected") over vague ones.
- One PR per concern, please.
