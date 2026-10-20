# AegisFlow AI – Security Analysis & Release Risk Assessment

- Issue: https://gitlab.com/gitlab-ai-hackathon/transcend-october-2026/43545252/aegisflow-ai/-/work_items/1
- Date: 2026-10-20
- Scope: `risk_engine.py`, `test_risk_engine.py`, `.gitlab-ci.yml`, CI pipeline results #1–#4 on `main`
- Method: static read, local execution of `risk_engine.py` with edge-case inputs, review of CI job logs.
  No existing project file was modified and nothing was deployed.

## Recommendation: REVIEW REQUIRED

Human approval is required before any release. The current evidence cannot support APPROVED:

- The "green" pipeline does not run any tests (F1).
- No vulnerability scanning other than secret detection exists, so "0 vulnerabilities" is not verifiable (F3).
- The release gate in `risk_engine.py` fails open on malformed input (F2).

If `evaluate_release()` is wired into an automated deployment gate as-is, treat the release as **BLOCKED** until F1 and F2 are fixed.

## Findings

| ID | Severity | Finding |
|----|----------|---------|
| F1 | High | CI runs **0 tests** and reports success |
| F2 | High | `evaluate_release()` fails open on invalid input |
| F3 | Medium | No SAST / dependency / container scanning; coverage is never measured |
| F4 | Medium | No approval gate, protected environment or deploy stage |
| F5 | Low | `secret_detection` job design weaknesses |
| F6 | Low | Pipeline hygiene: unpinned tooling, no `rules`, failed pipeline #3 has no job records |

### F1 – CI runs 0 tests (High)
`python_tests` runs `python -m unittest discover -p "test_*.py"`, but `test_risk_engine.py` contains
plain pytest-style functions, not `unittest.TestCase` classes. Job logs for pipelines #1 and #4 show
`Ran 0 tests ... OK`. I ran the 4 test functions manually and they pass, but CI never executes them.
The test stage therefore gives false assurance.

### F2 – `evaluate_release()` fails open (High)
Verified by running the function locally:

| Call | Result | Expected |
|------|--------|----------|
| `evaluate_release(True, 0, float("nan"))` | APPROVED | not approved (NaN comparison is always False) |
| `evaluate_release(True, -1, 95)` | APPROVED | invalid input rejected |
| `evaluate_release(True, 0, 150)` | APPROVED | invalid input rejected |
| `evaluate_release("no", 0, 95)` | APPROVED | `test_passed` should be a strict bool (any non-empty string is truthy) |
| `evaluate_release(True, None, 95)` | `TypeError` | explicit error (acceptable, but unhandled) |

A gate that approves on malformed or unexpected data is unsafe. Recommended fix: validate types and
ranges and default to BLOCKED. The inputs are also caller-supplied, so the function cannot tell
whether they come from real CI results.
Other gaps:
- `coverage == 80` is accepted (the boundary is untested).
- The REVIEW outcome has no escalation path.
- There are no tests for the invalid inputs above.

### F3 – Missing security scanning and measurement (Medium)
`.gitlab-ci.yml` only has secret detection. There is no SAST, dependency scanning, container scanning
or license compliance (for example the GitLab `Security/*.gitlab-ci.yml` templates). Test coverage is
never measured, so the `coverage` input has no source. The Vulnerability Report API returned an empty
list, which means "nothing scanned", not "no vulnerabilities".

### F4 – No human-approval control (Medium)
The README requires human approval for sensitive release decisions, but nothing enforces it: there is
no deploy job, `when: manual` gate, protected environment or approval rule. I could not read
protected-branch settings (the API token returned `insufficient_scope`), so branch protection and
merge approval rules are unverified. Pipelines #2–#4 ran with `source: push` directly on `main`.

### F5 – `secret_detection` job weaknesses (Low)
- `pip install detect-secrets` is unpinned (supply-chain and reproducibility risk).
- Pipeline #1 failed because of an invalid flag (`--fail-on-unaudited`); it was later fixed.
- The job regenerates `.secrets.baseline` on every run and counts all findings, so there is no audited baseline and no way to suppress false positives.
- The job produces no artifact or report.
- Result: pipeline #4 reported 0 potential secrets. No secrets were found in the tracked files I reviewed.

### F6 – Pipeline hygiene (Low)
- No `rules`/`workflow`, so jobs run on every push.
- Pipeline #3 shows `failed` with no job records, and its cause could not be determined from the available data.
- Image tags are floating (`python:3.11`).

## CI/CD evidence

| Pipeline | Status | Notes |
|----------|--------|-------|
| #1 (2967943117) | failed | `secret_detection`: unrecognized argument `--fail-on-unaudited`; `python_tests` "passed" with 0 tests |
| #2 | success | not inspected in detail |
| #3 (2968005004) | failed | no jobs listed, cause unknown |
| #4 (2968015836) | success | 0 tests run, 0 potential secrets |

## Missing information
- Protected branch, merge approval and environment settings (token lacked scope).
- Any SAST, dependency or container scan results (none configured).
- Real coverage numbers.
- The target deployment environment and the artifact being released. No application code beyond `risk_engine.py` exists.
- Cause of the failed pipeline #3.
- Pipeline #2 job details.

## Suggested next steps (not applied here, per the "do not modify project files" requirement)
1. Make CI run the tests (convert them to `unittest.TestCase`, or install and run pytest with coverage).
2. Harden `evaluate_release()`: strict validation, fail closed, and add tests for the cases above.
3. Add the GitLab SAST and dependency scanning templates.
4. Add a manual, protected-environment deploy job with required approvals.
5. Pin `detect-secrets` and the image versions.
