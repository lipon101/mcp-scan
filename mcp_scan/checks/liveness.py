"""Liveness checks: project exists, VCS present, recent activity, not deprecated."""
from __future__ import annotations

import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import List

from ..models import CheckResult, Status
from ._util import find_readme, read_text

CATEGORY = "liveness"


def run(path: Path) -> List[CheckResult]:
    out: List[CheckResult] = []

    non_empty = path.is_dir() and any(path.iterdir())
    out.append(CheckResult(
        "liveness.project_exists", CATEGORY,
        Status.PASS if non_empty else Status.FAIL,
        1.0 if non_empty else 0.0, 3,
        "Project directory exists and is non-empty" if non_empty else "Target is empty or not a directory",
    ))

    git = (path / ".git").exists()
    out.append(CheckResult(
        "liveness.vcs_present", CATEGORY,
        Status.PASS if git else Status.WARN,
        1.0 if git else 0.5, 1,
        "Git repository present" if git else "No .git — cannot verify history/activity",
    ))

    score, status, msg = 0.5, Status.WARN, "Skipped (no git history available)"
    if git:
        try:
            last = subprocess.run(
                ["git", "-C", str(path), "log", "-1", "--format=%ct"],
                capture_output=True, text=True, timeout=10,
            )
            ts = int(last.stdout.strip())
            age_days = (datetime.now(timezone.utc).timestamp() - ts) / 86400
            if age_days <= 180:
                score, status, msg = 1.0, Status.PASS, f"Active — last commit {int(age_days)} days ago"
            elif age_days <= 365:
                score, status, msg = 0.6, Status.WARN, f"Stale — last commit {int(age_days)} days ago"
            else:
                score, status, msg = 0.2, Status.FAIL, f"Likely abandoned — last commit {int(age_days)} days ago"
        except Exception:
            pass
    out.append(CheckResult("liveness.recent_activity", CATEGORY, status, score, 2, msg))

    readme = find_readme(path)
    txt = read_text(readme).lower() if readme else ""
    deprecated = any(k in txt[:2000] for k in
                     ["deprecated", "archived", "no longer maintained", "abandoned", "unmaintained"])
    out.append(CheckResult(
        "liveness.not_deprecated", CATEGORY,
        Status.FAIL if deprecated else Status.PASS,
        0.0 if deprecated else 1.0, 2,
        "README signals deprecated/archived" if deprecated else "No deprecation markers in README",
    ))

    return out
