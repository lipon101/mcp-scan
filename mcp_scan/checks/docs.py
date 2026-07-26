"""Docs & maintenance checks: license, substantive README, examples, changelog, contributing."""
from __future__ import annotations

from pathlib import Path
from typing import List

from ..models import CheckResult, Status
from ._util import find_readme, read_text

CATEGORY = "docs"


def run(path: Path) -> List[CheckResult]:
    out: List[CheckResult] = []

    license_present = any((path / n).exists() for n in ["LICENSE", "LICENSE.md", "LICENSE.txt", "COPYING"])
    out.append(CheckResult(
        "docs.has_license", CATEGORY,
        Status.PASS if license_present else Status.FAIL, 1.0 if license_present else 0.0, 3,
        "LICENSE file present" if license_present else "No LICENSE — unclear reuse rights",
    ))

    readme = find_readme(path)
    txt = read_text(readme) if readme else ""
    low = txt.lower()
    substantive = len(txt) >= 500
    out.append(CheckResult(
        "docs.readme_substantive", CATEGORY,
        Status.PASS if substantive else Status.WARN, 1.0 if substantive else 0.4, 2,
        f"README is substantive ({len(txt)} chars)" if substantive else f"README too short ({len(txt)} chars)",
    ))

    examples = (path / "examples").is_dir() or (path / "example").is_dir() or "example" in low
    out.append(CheckResult(
        "docs.has_examples", CATEGORY,
        Status.PASS if examples else Status.WARN, 1.0 if examples else 0.5, 1,
        "Examples present" if examples else "No examples directory/section",
    ))

    changelog = (path / "CHANGELOG.md").exists() or "changelog" in low
    out.append(CheckResult(
        "docs.has_changelog", CATEGORY,
        Status.PASS if changelog else Status.WARN, 1.0 if changelog else 0.5, 1,
        "Changelog present" if changelog else "No changelog",
    ))

    contributing = (path / "CONTRIBUTING.md").exists() or "contributing" in low
    out.append(CheckResult(
        "docs.has_contributing", CATEGORY,
        Status.PASS if contributing else Status.WARN, 1.0 if contributing else 0.5, 1,
        "Contributing guide present" if contributing else "No contributing guide",
    ))

    return out
