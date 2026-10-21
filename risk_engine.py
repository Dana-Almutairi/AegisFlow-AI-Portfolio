
import math


def evaluate_release(test_passed, vulnerabilities, coverage):
    # Validate input types and values
    if type(test_passed) is not bool:
        return "BLOCKED: Invalid test status"

    if type(vulnerabilities) is not int or vulnerabilities < 0:
        return "BLOCKED: Invalid vulnerability count"

    if (
        type(coverage) not in (int, float)
        or not math.isfinite(coverage)
        or not 0 <= coverage <= 100
    ):
        return "BLOCKED: Invalid coverage value"

    # Evaluate release safety
    if not test_passed:
        return "BLOCKED: Tests failed"

    if vulnerabilities > 0:
        return "BLOCKED: Security vulnerabilities detected"

    if coverage < 80:
        return "REVIEW: Test coverage is below 80%"

    return "APPROVED: Ready for deployment"


if __name__ == "__main__":
    result = evaluate_release(
        test_passed=True,
        vulnerabilities=0,
        coverage=95
    )

    print(result)
