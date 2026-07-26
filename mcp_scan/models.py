"""Data models for mcp-scan."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List


class Status(str, Enum):
    PASS = "pass"
    WARN = "warn"
    FAIL = "fail"


@dataclass
class CheckResult:
    """Result of a single check."""
    check: str            # dotted id, e.g. "security.no_hardcoded_secrets"
    category: str         # liveness | security | protocol | usability | docs
    status: Status
    score: float          # 0.0 .. 1.0
    weight: float         # relative weight within its category
    message: str          # short human summary
    detail: str = ""      # optional longer explanation


@dataclass
class CategoryScore:
    category: str
    score: float          # 0..100
    weight: float         # category weight in the overall grade
    results: List[CheckResult] = field(default_factory=list)


@dataclass
class ScanReport:
    target: str
    categories: List[CategoryScore] = field(default_factory=list)
    overall: float = 0.0          # 0..100
    grade: str = "?"
    generated_at: str = ""
