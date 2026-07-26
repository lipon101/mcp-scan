"""Scoring + grading logic (Lighthouse-style weighted categories)."""
from __future__ import annotations

from typing import Dict, List

from .models import CategoryScore, CheckResult, ScanReport

# Category weights — must sum to 1.0. Security is weighted highest on purpose:
# a server that leaks secrets should never score well, no matter how pretty its README.
CATEGORY_WEIGHTS: Dict[str, float] = {
    "security": 0.25,
    "liveness": 0.20,
    "protocol": 0.20,
    "usability": 0.20,
    "docs": 0.15,
}

# (min_score, grade) — checked high to low.
GRADE_BREAKPOINTS = [
    (90, "A"),
    (80, "B"),
    (65, "C"),
    (50, "D"),
    (0, "F"),
]


def grade_from_score(score: float) -> str:
    for threshold, grade in GRADE_BREAKPOINTS:
        if score >= threshold:
            return grade
    return "F"


def _category_score(results: List[CheckResult]) -> float:
    total_w = sum(r.weight for r in results)
    if total_w == 0:
        return 0.0
    weighted = sum(r.score * r.weight for r in results)
    return round(100.0 * weighted / total_w, 1)


def build_report(target: str, results: List[CheckResult]) -> ScanReport:
    by_cat: Dict[str, List[CheckResult]] = {}
    for r in results:
        by_cat.setdefault(r.category, []).append(r)

    categories: List[CategoryScore] = []
    overall = 0.0
    for cat, weight in CATEGORY_WEIGHTS.items():
        res = by_cat.get(cat, [])
        score = _category_score(res)
        categories.append(CategoryScore(category=cat, score=score, weight=weight, results=res))
        overall += score * weight

    overall = round(overall, 1)
    return ScanReport(
        target=target,
        categories=categories,
        overall=overall,
        grade=grade_from_score(overall),
    )
