"""Check registry. Each module exposes CATEGORY and run(path) -> list[CheckResult]."""
from __future__ import annotations

from pathlib import Path
from typing import List

from ..models import CheckResult, Status
from . import docs, liveness, protocol, security, usability

ALL_CHECK_MODULES = [security, liveness, protocol, usability, docs]


def run_all(path: Path) -> List[CheckResult]:
    results: List[CheckResult] = []
    for mod in ALL_CHECK_MODULES:
        try:
            results.extend(mod.run(path))
        except Exception as e:  # a broken check must never kill the whole scan
            results.append(
                CheckResult(
                    check=f"{mod.__name__.split('.')[-1]}.error",
                    category=getattr(mod, "CATEGORY", "unknown"),
                    status=Status.WARN,
                    score=0.5,
                    weight=0.0,
                    message=f"check module errored: {e}",
                )
            )
    return results
