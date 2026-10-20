
def evaluate_release(test_passed, vulnerabilities, coverage):
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
