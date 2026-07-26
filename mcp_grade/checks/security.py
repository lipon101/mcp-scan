"""Security checks: hardcoded secrets, eval/exec, dependency & env hygiene."""
from __future__ import annotations

import re
from pathlib import Path
from typing import List

from ..models import CheckResult, Status
from ._util import iter_files, read_text

CATEGORY = "security"

SECRET_PATTERNS = [
    ("AWS access key", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("OpenAI-style secret key", re.compile(r"\bsk-[A-Za-z0-9]{20,}\b")),
    ("GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b")),
    ("Slack token", re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}")),
    ("Private key block", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA |PGP )?PRIVATE KEY-----")),
    ("Generic secret assignment", re.compile(
        r"(?i)\b(api[_-]?key|secret|password|passwd|token|auth)\b\s*[:=]\s*['\"][A-Za-z0-9_\-]{16,}['\"]")),
]

SCAN_EXTS = {".py", ".js", ".ts", ".json", ".env", ".sh", ".yaml", ".yml", ".toml", ".txt", ".cfg", ".ini"}


def run(path: Path) -> List[CheckResult]:
    out: List[CheckResult] = []
    findings = []
    eval_files = []

    for f in iter_files(path):
        if f.suffix.lower() not in SCAN_EXTS:
            continue
        txt = read_text(f)
        rel = f.relative_to(path)
        for name, pat in SECRET_PATTERNS:
            if pat.search(txt):
                findings.append(f"{name} in {rel}")
        if f.suffix == ".py" and re.search(r"\b(eval|exec)\s*\(", txt):
            eval_files.append(str(rel))

    clean = not findings
    out.append(CheckResult(
        "security.no_hardcoded_secrets", CATEGORY,
        Status.PASS if clean else Status.FAIL,
        1.0 if clean else 0.0, 4,
        "No hardcoded secrets detected" if clean else f"{len(findings)} potential secret(s) found",
        detail="; ".join(findings[:8]),
    ))

    out.append(CheckResult(
        "security.no_eval_exec", CATEGORY,
        Status.PASS if not eval_files else Status.WARN,
        1.0 if not eval_files else 0.4, 1,
        "No eval()/exec() usage" if not eval_files else f"eval/exec in {len(eval_files)} file(s)",
        detail=", ".join(eval_files[:6]),
    ))

    manifest = any((path / m).exists() for m in
                   ["pyproject.toml", "requirements.txt", "setup.py", "package.json", "Cargo.toml", "go.mod"])
    out.append(CheckResult(
        "security.declared_dependencies", CATEGORY,
        Status.PASS if manifest else Status.WARN,
        1.0 if manifest else 0.4, 2,
        "Dependency manifest present (auditable)" if manifest else "No dependency manifest found",
    ))

    env_example = (path / ".env.example").exists() or (path / ".env.sample").exists()
    has_env = (path / ".env").exists()
    if has_env:
        status, score, msg = Status.FAIL, 0.1, "Committed .env file detected — secrets may be exposed!"
    elif env_example:
        status, score, msg = Status.PASS, 1.0, "Uses .env.example (secrets kept out of the repo)"
    else:
        status, score, msg = Status.WARN, 0.6, "No .env.example guidance for configuring secrets"
    out.append(CheckResult("security.env_hygiene", CATEGORY, status, score, 2, msg))

    return out
