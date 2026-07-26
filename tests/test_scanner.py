"""End-to-end tests against the bundled good/bad fixtures."""
from pathlib import Path

from mcp_grade.scanner import scan

EXAMPLES = Path(__file__).resolve().parent.parent / "examples"


def test_good_server_scores_well():
    rep = scan(str(EXAMPLES / "good_server"))
    assert rep.grade in {"A", "B"}, f"good_server graded {rep.grade} ({rep.overall})"
    assert rep.overall >= 80


def test_bad_server_scores_poorly():
    rep = scan(str(EXAMPLES / "bad_server"))
    assert rep.grade in {"D", "F"}, f"bad_server graded {rep.grade} ({rep.overall})"
    assert rep.overall < 65


def test_bad_server_flags_secrets():
    rep = scan(str(EXAMPLES / "bad_server"))
    sec = {r.check: r for cat in rep.categories for r in cat.results if cat.category == "security"}
    assert sec["security.no_hardcoded_secrets"].status.value == "fail"
    assert sec["security.env_hygiene"].status.value == "fail"


def test_good_server_passes_security():
    rep = scan(str(EXAMPLES / "good_server"))
    sec = {r.check: r for cat in rep.categories for r in cat.results if cat.category == "security"}
    assert sec["security.no_hardcoded_secrets"].status.value == "pass"


def test_json_dict_shape():
    from mcp_grade.report import to_dict

    rep = scan(str(EXAMPLES / "good_server"))
    d = to_dict(rep)
    assert d["grade"] in {"A", "B"}
    assert {"target", "grade", "overall", "generated_at", "categories"} <= set(d.keys())
    assert len(d["categories"]) == 5
    assert all({"category", "score", "weight", "checks"} <= set(c.keys()) for c in d["categories"])
    assert all(
        {"check", "status", "score", "weight", "message"} <= set(ch.keys())
        for c in d["categories"] for ch in c["checks"]
    )
