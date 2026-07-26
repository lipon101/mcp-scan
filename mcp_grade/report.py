"""Rendering: rich terminal report card + Markdown export + shields badge + JSON."""
from __future__ import annotations

from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from . import __version__
from .models import ScanReport, Status

GRADE_COLOR = {"A": "green", "B": "green", "C": "yellow", "D": "yellow", "F": "red"}
BADGE_COLOR = {"A": "brightgreen", "B": "green", "C": "yellow", "D": "orange", "F": "red"}
STATUS_ICON = {Status.PASS: "✅", Status.WARN: "⚠️ ", Status.FAIL: "❌"}
CAT_LABEL = {
    "security": "🔒 Security",
    "liveness": "🫀 Liveness",
    "protocol": "🔌 Protocol",
    "usability": "🧰 Usability",
    "docs": "📚 Docs & Maintenance",
}


def render_terminal(report: ScanReport, console: Optional[Console] = None) -> None:
    console = console or Console()
    color = GRADE_COLOR.get(report.grade, "white")

    header = Text()
    header.append(f"  {report.grade}  ", style=f"bold white on {color}")
    header.append(f"  Score {report.overall:.0f}/100    ", style="bold")
    header.append(report.target, style="dim")
    console.print(Panel(header, title="mcp-grade report card", border_style=color, expand=False))

    for cat in report.categories:
        title = f"{CAT_LABEL.get(cat.category, cat.category)}  —  {cat.score:.0f}/100  (weight {int(cat.weight * 100)}%)"
        t = Table(title=title, title_justify="left", expand=False, pad_edge=False)
        t.add_column("", width=3, no_wrap=True)
        t.add_column("Check", style="bold", no_wrap=True)
        t.add_column("Message")
        for r in cat.results:
            t.add_row(STATUS_ICON[r.status], r.check.split(".")[-1], r.message)
        console.print(t)

    console.print(f"\n[dim]Generated {report.generated_at} · mcp-grade {__version__} · run with --report for a Markdown card[/dim]\n")


def to_markdown(report: ScanReport) -> str:
    icon = {"pass": "✅", "warn": "⚠️", "fail": "❌"}
    lines = [
        f"# mcp-grade report card — Grade {report.grade} ({report.overall:.0f}/100)",
        "",
        f"**Target:** `{report.target}`  ",
        f"**Generated:** {report.generated_at}",
        "",
        "| Category | Score | Weight |",
        "|---|---|---|",
    ]
    for cat in report.categories:
        lines.append(f"| {cat.category} | {cat.score:.0f}/100 | {int(cat.weight * 100)}% |")
    lines.append("")
    for cat in report.categories:
        lines.append(f"## {cat.category} — {cat.score:.0f}/100")
        for r in cat.results:
            lines.append(f"- {icon[r.status.value]} **{r.check.split('.')[-1]}** — {r.message}")
            if r.detail:
                lines.append(f"  - _{r.detail}_")
        lines.append("")
    lines += [
        "---",
        "_Scanned with [mcp-grade](https://github.com/lipon101/mcp-grade) — Lighthouse for MCP servers._",
    ]
    return "\n".join(lines)


def to_dict(report: ScanReport) -> dict:
    """Machine-readable summary for CI, dashboards, and the GitHub Action."""
    return {
        "target": report.target,
        "grade": report.grade,
        "overall": report.overall,
        "generated_at": report.generated_at,
        "categories": [
            {
                "category": c.category,
                "score": c.score,
                "weight": c.weight,
                "checks": [
                    {
                        "check": r.check,
                        "status": r.status.value,
                        "score": r.score,
                        "weight": r.weight,
                        "message": r.message,
                        "detail": r.detail,
                    }
                    for r in c.results
                ],
            }
            for c in report.categories
        ],
    }


def badge_markdown(report: ScanReport) -> str:
    color = BADGE_COLOR.get(report.grade, "lightgrey")
    url = f"https://img.shields.io/badge/mcp--grade-{report.grade}_{int(report.overall)}-{color}"
    return f"![mcp-grade grade]({url})"
