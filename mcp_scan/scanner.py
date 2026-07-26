"""Orchestrates all checks against a target path and builds a ScanReport."""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from .checks import run_all
from .grading import build_report
from .models import ScanReport


def scan(target: str, live: bool = False, command: Optional[str] = None) -> ScanReport:
    path = Path(target).expanduser().resolve()
    results = run_all(path)
    if live:
        from .live import probe
        results.extend(probe(path, command=command))
    report = build_report(str(path), results)
    report.generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    return report
