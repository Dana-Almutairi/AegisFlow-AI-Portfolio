
from risk_engine import evaluate_release


def test_approved_release():
    result = evaluate_release(True, 0, 95)
    assert result == "APPROVED: Ready for deployment"


def test_failed_tests():
    result = evaluate_release(False, 0, 95)
    assert result == "BLOCKED: Tests failed"


def test_security_issue():
    result = evaluate_release(True, 2, 95)
    assert result == "BLOCKED: Security vulnerabilities detected"


def test_low_coverage():
    result = evaluate_release(True, 0, 60)
    assert result == "REVIEW: Test coverage is below 80%"
