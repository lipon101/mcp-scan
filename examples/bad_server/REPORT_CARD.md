# mcp-grade report card — Grade F (46/100)

**Target:** `/home/user/mcp-grade/examples/bad_server`  
**Generated:** 2026-07-26 04:03 UTC

| Category | Score | Weight |
|---|---|---|
| security | 16/100 | 25% |
| liveness | 81/100 | 20% |
| protocol | 44/100 | 20% |
| usability | 66/100 | 20% |
| docs | 29/100 | 15% |

## security — 16/100
- ❌ **no_hardcoded_secrets** — 2 potential secret(s) found
  - _OpenAI-style secret key in server.py; Generic secret assignment in server.py_
- ⚠️ **no_eval_exec** — eval/exec in 1 file(s)
  - _server.py_
- ⚠️ **declared_dependencies** — No dependency manifest found
- ❌ **env_hygiene** — Committed .env file detected — secrets may be exposed!

## liveness — 81/100
- ✅ **project_exists** — Project directory exists and is non-empty
- ⚠️ **vcs_present** — No .git — cannot verify history/activity
- ⚠️ **recent_activity** — Skipped (no git history available)
- ✅ **not_deprecated** — No deprecation markers in README

## protocol — 44/100
- ⚠️ **detectable_server** — Could not detect an MCP server entrypoint
- ⚠️ **declares_tools** — No tool declarations found
- ⚠️ **valid_manifest** — No machine-readable manifest (e.g. mcp.json) found
- ⚠️ **transport_documented** — Transport not documented in README

## usability — 66/100
- ✅ **has_readme** — README present
- ⚠️ **install_instructions** — No clear install instructions
- ⚠️ **quickstart_example** — No runnable example found
- ✅ **clear_value_prop** — Concise opening line / value prop
- ⚠️ **config_example** — No configuration example

## docs — 29/100
- ❌ **has_license** — No LICENSE — unclear reuse rights
- ⚠️ **readme_substantive** — README too short (26 chars)
- ⚠️ **has_examples** — No examples directory/section
- ⚠️ **has_changelog** — No changelog
- ⚠️ **has_contributing** — No contributing guide

---
_Scanned with [mcp-grade](https://github.com/lipon101/mcp-grade) — Lighthouse for MCP servers._

![mcp-grade grade](https://img.shields.io/badge/mcp--grade-F_46-red)
