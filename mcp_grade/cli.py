"""Command-line interface for mcp-grade."""
from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from . import report as report_mod
from .scanner import scan

app = typer.Typer(
    add_completion=False,
    help="mcp-grade — Lighthouse/ESLint for MCP servers. Grade any MCP server A–F from one command.",
)
console = Console()

_GRADE_ORDER = ["F", "D", "C", "B", "A"]


@app.command()
def main(
    target: str = typer.Argument(..., help="Path to an MCP server repo, or a git URL to clone & scan."),
    report: bool = typer.Option(False, "--report", help="Write a Markdown report card (mcp-grade-report.md)."),
    badge: bool = typer.Option(False, "--badge", help="Print a shields.io badge for the grade."),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Write the Markdown report to this path."),
    json_out: Optional[Path] = typer.Option(None, "--json", help="Write a machine-readable JSON summary to this path."),
    live: bool = typer.Option(False, "--live", help="Actually launch the server and verify the MCP handshake (needs `pip install mcp-grade[live]`)."),
    command: Optional[str] = typer.Option(None, "--command", help="Command to launch the server for --live (default: auto-detect server.py)."),
    fail_under: Optional[str] = typer.Option(None, "--fail-under", help="Exit non-zero below this grade (A/B/C/D). Great for CI."),
) -> None:
    """Scan an MCP server and print an A–F quality report card."""
    if target.startswith(("http://", "https://", "git@")):
        target = _clone(target)

    rep = scan(target, live=live, command=command)
    report_mod.render_terminal(rep, console)

    if badge:
        console.print(report_mod.badge_markdown(rep))

    if report or output:
        dest = output or Path("mcp-grade-report.md")
        dest.write_text(report_mod.to_markdown(rep), encoding="utf-8")
        console.print(f"[dim]Markdown report written to {dest}[/dim]")

    # Written before the fail-under gate so the JSON exists even when the gate fails.
    if json_out:
        json_out.write_text(json.dumps(report_mod.to_dict(rep), indent=2), encoding="utf-8")
        console.print(f"[dim]JSON summary written to {json_out}[/dim]")

    if fail_under:
        wanted = fail_under.upper()
        if wanted not in _GRADE_ORDER:
            console.print(f"[red]--fail-under must be one of A/B/C/D/F (got {fail_under!r})[/red]")
            raise typer.Exit(code=2)
        if _GRADE_ORDER.index(rep.grade) < _GRADE_ORDER.index(wanted):
            console.print(f"[red]Grade {rep.grade} is below --fail-under {wanted} → failing (exit 1).[/red]")
            raise typer.Exit(code=1)
        console.print(f"[green]Grade {rep.grade} meets --fail-under {wanted}.[/green]")


def _clone(url: str) -> str:
    dest = tempfile.mkdtemp(prefix="mcp-grade-")
    console.print(f"[dim]Cloning {url} …[/dim]")
    subprocess.run(["git", "clone", "--depth", "1", url, dest], check=True)
    return dest


def entrypoint() -> None:
    app()


if __name__ == "__main__":
    entrypoint()
