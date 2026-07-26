# mcp-scan report card — Grade A (96/100)

**Target:** `/home/user/mcp-scan/examples/good_server`  
**Generated:** 2026-07-26 04:03 UTC

| Category | Score | Weight |
|---|---|---|
| security | 100/100 | 25% |
| liveness | 81/100 | 20% |
| protocol | 100/100 | 20% |
| usability | 100/100 | 20% |
| docs | 100/100 | 15% |

## security — 100/100
- ✅ **no_hardcoded_secrets** — No hardcoded secrets detected
- ✅ **no_eval_exec** — No eval()/exec() usage
- ✅ **declared_dependencies** — Dependency manifest present (auditable)
- ✅ **env_hygiene** — Uses .env.example (secrets kept out of the repo)

## liveness — 81/100
- ✅ **project_exists** — Project directory exists and is non-empty
- ⚠️ **vcs_present** — No .git — cannot verify history/activity
- ⚠️ **recent_activity** — Skipped (no git history available)
- ✅ **not_deprecated** — No deprecation markers in README

## protocol — 100/100
- ✅ **detectable_server** — MCP server entrypoint detected
- ✅ **declares_tools** — Tool/resource registration detected
- ✅ **valid_manifest** — mcp.json parses as valid JSON
- ✅ **transport_documented** — Transport (stdio/http/sse) documented

## usability — 100/100
- ✅ **has_readme** — README present
- ✅ **install_instructions** — Install / getting-started instructions present
- ✅ **quickstart_example** — Runnable usage example present
- ✅ **clear_value_prop** — Concise opening line / value prop
- ✅ **config_example** — Configuration example present

## docs — 100/100
- ✅ **has_license** — LICENSE file present
- ✅ **readme_substantive** — README is substantive (845 chars)
- ✅ **has_examples** — Examples present
- ✅ **has_changelog** — Changelog present
- ✅ **has_contributing** — Contributing guide present

---
_Scanned with [mcp-scan](https://github.com/lipon101/mcp-scan) — Lighthouse for MCP servers._

![mcp-scan grade](https://img.shields.io/badge/mcp--scan-A_96-brightgreen)
