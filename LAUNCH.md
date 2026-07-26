# 🚀 LAUNCH.md — ship `mcp-grade` (and the template)

A checklist to go from these files to a live, installable, discoverable project.

## 0. Make it yours (do this first)
Replace every `lipon101` with your GitHub handle:
- `mcp-grade`: `README.md`, `pyproject.toml` (`Homepage`/`Issues`), `report.py` footer link.
- `mcp-server-template`: `README.md`, `LICENSE`, and **`.github/workflows/mcp-grade.yml`** (`uses: lipon101/mcp-grade@v1`).

## 1. Push both repos to GitHub
```bash
# mcp-grade
cd mcp-grade && git init && git add -A && git commit -m "mcp-grade v0.2.0"
git branch -M main && git remote add origin https://github.com/<you>/mcp-grade.git && git push -u origin main

# mcp-server-template
cd ../mcp-server-template && git init && git add -A && git commit -m "MCP server template"
git branch -M main && git remote add origin https://github.com/<you>/mcp-server-template.git && git push -u origin main
```

## 2. Mark the template as a Template
On GitHub: `mcp-server-template` → **Settings** → check **"Template repository"**.
This enables the **"Use this template"** button — the one-click path that turns every
derived repo into a *dependent* of your Action.

## 3. Tag releases (so `@v1` resolves)
```bash
cd mcp-grade
git tag -a v0.2.0 -m "v0.2.0" && git push origin v0.2.0
git tag -a v1 -m "v1 (floating major)" && git push origin v1   # lets `uses: <you>/mcp-grade@v1` work
```

## 4. Publish `mcp-grade` to PyPI
**Option A — trusted publishing (recommended, no token):**
1. On PyPI → *Account settings → Publishing*, add a trusted publisher:
   Owner `<you>`, Repository `mcp-grade`, Workflow `publish.yml`, Environment `pypi`.
2. Create a GitHub **Release** (e.g. from the `v0.2.0` tag). `.github/workflows/publish.yml` builds and publishes automatically.

**Option B — manual:**
```bash
pip install --upgrade build twine
python -m build
twine upload dist/*
```
Verify: `pipx install mcp-grade && mcp-grade --help`.

## 5. Demo asset
`assets/demo.png` is a rendered terminal mockup you can use immediately. For maximum
impact, record a real 10-second GIF and replace it:
```bash
pipx install asciinema agg
asciinema rec demo.cast        # then run: mcp-grade ./examples/good_server --report  ; exit
agg demo.cast assets/demo.gif  # point the README at assets/demo.gif
```

## 6. The 48-hour launch (the window that matters)
- [ ] **Show HN** — Monday **00:00 UTC** (Sun 7pm ET); title leads with the *pain*, not the tech.
- [ ] **r/LocalLLaMA** right after (the channel that moves AI tools).
- [ ] **Product Hunt** + an **X** thread with the GIF.
- [ ] Submit to: **awesome-mcp-servers**, the **MCP Registry**, **awesome-actions**, and **GitHub Marketplace** (for the Action).
- [ ] Post the template in MCP Discord/forums as "the recommended way to start an MCP server."

## 7. After launch (the plateau)
- Reply to **every** issue/PR within 24h for two weeks.
- Ship **v0.3 within ~10 days** (live protocol probing + the public leaderboard).
- Keep a release cadence — the launch is a pulse; cadence is what keeps stars climbing.

## 8. Eligibility (Claude for Open Source)
Watch **GitHub → Insights → Dependents** (the Action's dependent repos) and PyPI downloads
(pepy.tech / pypistats.org). The 500-dependent-repos bar is a ~12–24 month target; once real
CI pipelines depend on `mcp-grade`, apply via the program's *"apply anyway if the ecosystem
quietly depends on it"* clause — even before hitting the hard number.
