"""Tests for grading logic."""
from mcp_grade.grading import build_report, grade_from_score
from mcp_grade.models import CheckResult, Status


def test_grade_boundaries():
    assert grade_from_score(95) == "A"
    assert grade_from_score(90) == "A"
    assert grade_from_score(85) == "B"
    assert grade_from_score(70) == "C"
    assert grade_from_score(55) == "D"
    assert grade_from_score(20) == "F"


def _cr(cat, score, weight):
    return CheckResult(check=f"{cat}.x", category=cat, status=Status.PASS,
                       score=score, weight=weight, message="m")


def test_build_report_all_perfect():
    results = [_cr(cat, 1.0, 1) for cat in
               ["security", "liveness", "protocol", "usability", "docs"]]
    rep = build_report("t", results)
    assert rep.overall == 100.0
    assert rep.grade == "A"


def test_build_report_security_heavily_weighted():
    # Zero security but perfect everything else should still hurt a lot.
    results = [_cr("security", 0.0, 4)]
    results += [_cr(cat, 1.0, 1) for cat in
                ["liveness", "protocol", "usability", "docs"]]
    rep = build_report("t", results)
    assert rep.overall < 80  # cannot be an A/B with security zeroed
