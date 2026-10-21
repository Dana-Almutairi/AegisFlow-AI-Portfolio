# AegisFlow AI

**Risk-Aware, Human-Supervised DevSecOps Automation Powered by GitLab Duo Agent Platform**

## Overview

AegisFlow AI is an AI-powered DevSecOps prototype that helps software teams assess security risks, review testing evidence, and make explainable software release decisions.

Built for the **GitLab Transcend Hackathon 2026 — Life After Code**, AegisFlow AI explores how AI-driven workflows can support software delivery beyond code generation.

## The Problem

Writing code is only one part of software development. Before releasing software, engineering teams must verify test results, investigate vulnerabilities, assess deployment risks, and decide whether a release is safe.

Incomplete evidence and disconnected workflows can make these decisions difficult.

## Our Solution

AegisFlow AI combines a Python release risk engine, GitLab CI/CD checks, and a custom GitLab Duo Agent Platform workflow.

Its central principle is simple:

**AI recommends. Humans remain in control.**

## Implemented Features

### 1. Release Risk Engine

The Python risk engine evaluates supplied release information and returns one of three decisions:

- **APPROVED:** Required conditions satisfy the configured policy.
- **REVIEW:** Coverage is below the required threshold.
- **BLOCKED:** Tests fail or vulnerabilities are reported.

The engine validates input types and ranges. Its current coverage threshold is 80%.

These decisions are based on supplied values; the engine does not independently collect CI/CD evidence.

### 2. Automated Testing and CI/CD

The repository includes:

- Python unit tests using pytest.
- A GitLab CI/CD testing stage.
- Secret detection using detect-secrets.
- A manual human-approval job.

A previous pipeline confirmed nine passing tests.

The current implementation does not automatically calculate test coverage or feed verified pipeline results into the release risk engine.

### 3. Custom AI Agents

Three custom agents have been configured in GitLab Duo Agent Platform:

- **AegisFlow Security Agent**
- **AegisFlow Testing Agent**
- **AegisFlow Release Decision Agent**

These agents represent the project's security, testing, and release-assessment responsibilities.

### 4. AegisFlow Release Guardian Workflow

A custom GitLab Duo Agent Platform Flow has been created and enabled.

Its configured stages are:

1. Security Analysis
2. Testing Analysis
3. Release Decision

The workflow uses specialized prompts to assess repository evidence and produce a human-supervised release recommendation.

The custom Flow uses its own configured agent components. Independent execution of the separately configured custom agents has not yet been verified.

### 5. Verified Workflow Execution

AegisFlow Release Guardian was triggered from GitLab Issue #1 using its service account.

**Execution evidence:**

- Session ID: `9819497`
- Status: `Finished`
- Final recommendation: `REVIEW REQUIRED`

The generated report identified release-readiness gaps, including missing verified execution evidence, incomplete coverage measurement, and opportunities to strengthen CI/CD security.

The report stated that no project files were modified and no deployment was performed.

**Final recommendation: REVIEW REQUIRED**

The workflow did not authorize a release. Human approval remains necessary before deployment.

## Architecture

```text
GitLab Issue / Trigger
         |
         v
AegisFlow Release Guardian
         |
         v
Security Analysis
         |
         v
Testing Analysis
         |
         v
Release Decision
         |
         v
APPROVED / REVIEW REQUIRED / BLOCKED
         |
         v
Human Review
```

The AI workflow currently provides advisory recommendations rather than automated deployment authorization.

## Technology Stack

- GitLab
- GitLab Duo Agent Platform
- GitLab CI/CD
- Python
- pytest
- detect-secrets
- YAML
- DevSecOps practices

## Current Limitations

The prototype currently has several limitations:

- Release risk inputs are not automatically populated from verified CI/CD results.
- Test coverage is not automatically measured.
- Dependency scanning and comprehensive SAST are not yet integrated.
- The manual approval job does not independently guarantee approval by a separate authorized reviewer.
- Automated deployment and incident monitoring are not implemented.
- The AI report requires validation against current repository and pipeline evidence.

## Future Improvements

- Integrate verified pipeline results into release decisions.
- Add measured test coverage and dependency vulnerability scanning.
- Strengthen approval permissions and protected environments.
- Extend support for code review and deployment monitoring.
- Improve agent evaluation and evidence traceability.

## Hackathon

**Event:** GitLab Transcend Hackathon 2026 — Life After Code

**Project:** AegisFlow AI

**Developer:** Dana Almutairi

## License

Licensed under the MIT License. See the LICENSE file for details.