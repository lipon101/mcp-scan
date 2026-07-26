"""Usability checks: README, install steps, quickstart, value prop, config example."""
from __future__ import annotations

import re
from pathlib import Path
from typing import List

from ..models import CheckResult, Status
from ._util import find_readme, read_text

CATEGORY = "usability"


def run(path: Path) -> List[CheckResult]:
    out: List[CheckResult] = []
    readme = find_readme(path)
    txt = read_text(readme) if readme else ""
    low = txt.lower()

    out.append(CheckResult(
        "usability.has_readme", CATEGORY,
        Status.PASS if readme else Status.FAIL, 1.0 if readme else 0.0, 3,
        "README present" if readme else "No README found",
    ))

    install = ("```" in txt) and any(
        k in low for k in ["install", "pip install", "npm install", "pipx", "uv tool", "getting started", "setup"]
    )
    out.append(CheckResult(
        "usability.install_instructions", CATEGORY,
        Status.PASS if install else Status.WARN, 1.0 if install else 0.3, 3,
        "Install / getting-started instructions present" if install else "No clear install instructions",
    ))

    quickstart = txt.count("```") >= 2 and any(
        k in low for k in ["example", "usage", "quickstart", "quick start"]
    )
    out.append(CheckResult(
        "usability.quickstart_example", CATEGORY,
        Status.PASS if quickstart else Status.WARN, 1.0 if quickstart else 0.4, 2,
        "Runnable usage example present" if quickstart else "No runnable example found",
    ))

    first = next(
        (ln.strip() for ln in txt.splitlines()
         if ln.strip() and not ln.strip().startswith(("!", "[", "<", "#"))),
        "",
    )
    one_liner = 0 < len(first) <= 140
    out.append(CheckResult(
        "usability.clear_value_prop", CATEGORY,
        Status.PASS if one_liner else Status.WARN, 1.0 if one_liner else 0.5, 2,
        "Concise opening line / value prop" if one_liner else "Opening line missing or too long",
    ))

    config = ("```json" in low) or ("config" in low and "```" in txt) or (path / ".env.example").exists()
    out.append(CheckResult(
        "usability.config_example", CATEGORY,
        Status.PASS if config else Status.WARN, 1.0 if config else 0.5, 1,
        "Configuration example present" if config else "No configuration example",
    ))

    return out
