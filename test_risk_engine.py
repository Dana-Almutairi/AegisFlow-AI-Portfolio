
from risk_engine import evaluate_release


def test_nan_coverage_is_blocked():
    assert evaluate_release(True, 0, float("nan")).startswith("BLOCKED")


def test_negative_vulnerabilities_are_blocked():
    assert evaluate_release(True, -1, 95).startswith("BLOCKED")


def test_invalid_test_status_is_blocked():
    assert evaluate_release("False", 0, 95).startswith("BLOCKED")


def test_infinite_coverage_is_blocked():
    assert evaluate_release(True, 0, float("inf")).startswith("BLOCKED")


def test_coverage_above_100_is_blocked():
    assert evaluate_release(True, 0, 110).startswith("BLOCKED")
