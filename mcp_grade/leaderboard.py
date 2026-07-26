"""Leaderboard engine + CLI: scan many MCP servers and rank them A–F.

Usage:
    mcp-grade-leaderboard                          # scan the curated default list
    mcp-grade-leaderboard ./serverA ./serverB      # scan specific paths/URLs
    mcp-grade-leaderboard --from-file repos.txt --html leaderboard.html --json lb.json
"""
from __future__ import annotations

import json
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional, Tuple

import typer
from rich.console import Console
from rich.table import Table

from .scanner import scan

# Curated, real, popular standalone MCP servers to seed the leaderboard.
# (modelcontextprotocol/servers is a monorepo — scan its src/* subdirs individually.)
DEFAULT_REPOS = [
    "https://github.com/microsoft/playwright-mcp",
    "https://github.com/github/github-mcp-server",
    "https://github.com/upstash/context7-mcp",
    "https://github.com/sooperset/mcp-atlassian",
    "https://github.com/modelcontextprotocol/inspector",
]

GRADE_COLOR = {"A": "green", "B": "green", "C": "yellow", "D": "yellow", "F": "red"}
console = Console()


def _resolve(target: str) -> Tuple[str, str]:
    """Return (local_path, display_label). Clones git URLs to a temp dir."""
    if target.startswith(("http://", "https://", "git@")):
        dest = tempfile.mkdtemp(prefix="mcp-grade-lb-")
        subprocess.run(["git", "clone", "--depth", "1", target, dest],
                       check=True, capture_output=True, timeout=180)
        return dest, target
    return str(Path(target).expanduser().resolve()), target


def build_leaderboard(targets: List[str], live: bool = False) -> dict:
    rows = []
    for t in targets:
        try:
            path, label = _resolve(t)
            rep = scan(path, live=live)
            rows.append({
                "name": label,
                "grade": rep.grade,
                "score": rep.overall,
                "categories": {c.category: c.score for c in rep.categories},
                "error": None,
            })
        except Exception as e:  # a clone/scan failure shouldn't kill the board
            rows.append({"name": t, "grade": None, "score": None, "categories": {},
                         "error": f"{type(e).__name__}: {e}"[:240]})
    rows.sort(key=lambda r: (r["score"] is not None, r["score"] or 0), reverse=True)
    for i, r in enumerate(rows, 1):
        r["rank"] = i
    return {"generated_at": datetime.now(timezone.utc).isoformat(), "count": len(rows), "servers": rows}


def to_markdown(lb: dict) -> str:
    lines = ["# 🏆 mcp-grade leaderboard", "",
             f"_Generated {lb['generated_at']} · {lb['count']} servers_", "",
             "| # | Grade | Score | Server |", "|---|---|---|---|"]
    for s in lb["servers"]:
        g = s.get("grade") or "—"
        score = f"{s['score']:.0f}" if isinstance(s.get("score"), (int, float)) else "—"
        err = f" _(error: {s['error']})_" if s.get("error") else ""
        lines.append(f"| {s['rank']} | **{g}** | {score} | `{s['name']}`{err} |")
    lines += ["", "---", "_Ranked by [mcp-grade](https://github.com/lipon101/mcp-grade)._"]
    return "\n".join(lines)


_HTML_TEMPLATE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>mcp-grade leaderboard</title>
<style>
  :root { color-scheme: light; }
  body { font-family: -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif;
         margin: 0; background: #f6f8fa; color: #1f2328; }
  .wrap { max-width: 840px; margin: 40px auto; padding: 0 20px; }
  h1 { font-size: 26px; margin-bottom: 4px; }
  .meta { color: #656d76; font-size: 13px; margin-bottom: 24px; }
  table { width: 100%; border-collapse: collapse; background: #fff;
          border: 1px solid #d0d7de; border-radius: 8px; overflow: hidden; }
  th, td { padding: 10px 14px; text-align: left; border-bottom: 1px solid #eaeef2; font-size: 14px; }
  th { background: #f6f8fa; font-weight: 600; }
  tr:last-child td { border-bottom: none; }
  .rank { color: #656d76; width: 40px; }
  .score { font-variant-numeric: tabular-nums; width: 70px; }
  .name { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }
  .badge { color: #fff; font-weight: 700; padding: 2px 10px; border-radius: 12px; font-size: 13px; }
  .err { color: #cf222e; font-size: 12px; }
  footer { margin-top: 20px; color: #656d76; font-size: 13px; }
  a { color: #0969da; }
</style></head>
<body><div class="wrap">
  <h1>🏆 mcp-grade leaderboard</h1>
  <div class="meta">Generated __GENERATED__ · __COUNT__ servers · graded A–F on security, liveness, protocol, usability, docs</div>
  <table><thead><tr><th>#</th><th>Grade</th><th>Score</th><th>Server</th></tr></thead>
  <tbody>
__BODY__
  </tbody></table>
  <footer>Ranked by <a href="https://github.com/lipon101/mcp-grade">mcp-grade</a> — Lighthouse for MCP servers.</footer>
</div></body></html>"""


def to_html(lb: dict) -> str:
    badge = {"A": "#1a7f37", "B": "#1a7f37", "C": "#9a6700", "D": "#9a6700", "F": "#cf222e"}
    rows = []
    for s in lb["servers"]:
        g = s.get("grade") or "—"
        color = badge.get(s.get("grade"), "#6e7781")
        score = f"{s['score']:.0f}" if isinstance(s.get("score"), (int, float)) else "—"
        name = str(s["name"]).replace("<", "&lt;")
        err = f' <span class="err">({s["error"]})</span>' if s.get("error") else ""
        rows.append(
            f'<tr><td class="rank">{s["rank"]}</td>'
            f'<td><span class="badge" style="background:{color}">{g}</span></td>'
            f'<td class="score">{score}</td><td class="name">{name}{err}</td></tr>')
    return (_HTML_TEMPLATE
            .replace("__GENERATED__", str(lb["generated_at"]))
            .replace("__COUNT__", str(lb["count"]))
            .replace("__BODY__", "\n".join(rows)))


app = typer.Typer(add_completion=False, help="Generate an mcp-grade leaderboard ranking MCP servers A–F.")


@app.command()
def main(
    targets: Optional[List[str]] = typer.Argument(None, help="Repo paths or git URLs. Defaults to a curated list."),
    live: bool = typer.Option(False, "--live", help="Also run live handshakes (slow; needs the [live] extra)."),
    from_file: Optional[Path] = typer.Option(None, "--from-file", help="Read targets (one per line; # comments ok) from a file."),
    json_out: Optional[Path] = typer.Option(None, "--json", help="Write leaderboard JSON to this path."),
    md_out: Optional[Path] = typer.Option(None, "--md", help="Write leaderboard Markdown to this path."),
    html_out: Optional[Path] = typer.Option(None, "--html", help="Write a static leaderboard HTML page to this path."),
) -> None:
    if from_file:
        targets = [ln.strip() for ln in from_file.read_text().splitlines()
                   if ln.strip() and not ln.strip().startswith("#")]
    if not targets:
        targets = DEFAULT_REPOS
        console.print(f"[dim]No targets given — scanning {len(targets)} curated repos (cloning…)[/dim]")

    lb = build_leaderboard(targets, live=live)

    t = Table(title=f"mcp-grade leaderboard ({lb['count']} servers)")
    t.add_column("#", justify="right")
    t.add_column("Grade")
    t.add_column("Score", justify="right")
    t.add_column("Server")
    for s in lb["servers"]:
        g = s.get("grade") or "—"
        score = f"{s['score']:.0f}" if isinstance(s.get("score"), (int, float)) else "—"
        style = GRADE_COLOR.get(s.get("grade"), "dim")
        t.add_row(str(s["rank"]), f"[{style}]{g}[/{style}]", score, s["name"])
    console.print(t)

    if json_out:
        json_out.write_text(json.dumps(lb, indent=2), encoding="utf-8")
        console.print(f"[dim]JSON written to {json_out}[/dim]")
    if md_out:
        md_out.write_text(to_markdown(lb), encoding="utf-8")
        console.print(f"[dim]Markdown written to {md_out}[/dim]")
    if html_out:
        html_out.write_text(to_html(lb), encoding="utf-8")
        console.print(f"[dim]HTML written to {html_out}[/dim]")


def entrypoint() -> None:
    app()


if __name__ == "__main__":
    entrypoint()
