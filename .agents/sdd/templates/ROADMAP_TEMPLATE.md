# ROADMAP: {FEATURE_NAME} Remediation

> Prioritized plan to move a feature from validation warning/failure to production readiness.

## Document Control

| Attribute | Value |
|-----------|-------|
| Feature | {FEATURE_NAME} |
| Generated At | {YYYY-MM-DD} |
| Current Score | {CURRENT_SCORE}/100 |
| Target Score | 90/100 or higher |
| Current Verdict | {CURRENT_VERDICT} |
| Remediation Owner | {REMEDIATION_OWNER} |
| Related Validation | `VALIDATION_REPORT_{FEATURE_NAME}.md` |

---

## Remediation Summary

{REMEDIATION_SUMMARY}

### Target Outcome

The feature is ready to ship when:

- validation score is at least 90/100;
- critical issue count is zero;
- all P1 remediation items are complete;
- remaining P2/P3 items are explicitly accepted or scheduled;
- `/validate {FEATURE_NAME}` produces a new report with no blocking findings.

---

## Priority Backlog

| Priority | ID | Task | Estimated Effort | Suggested Assignee |
|----------|----|------|------------------|--------------------|
{ROADMAP_ROWS}

---

## Workstreams

| Workstream | Objective | Owner | Exit Criteria |
|------------|-----------|-------|---------------|
| Specification alignment | Close requirement coverage gaps between DEFINE and implementation | {REMEDIATION_OWNER} | Every requirement has evidence or a documented deferral |
| Architecture fidelity | Correct deviations from DESIGN boundaries and decisions | {ARCHITECTURE_OWNER} | Architecture score is at least 90 |
| Code quality | Resolve lint, type, test, and maintainability issues | {DELIVERY_OWNER} | Code quality score is at least 90 |
| Security and DevOps | Resolve secrets, dependency, CI/CD, and operational control gaps | {OPERATIONS_OWNER} | Security and DevOps score is at least 90 |
| Production readiness | Add missing operational evidence, rollback, and observability coverage | {OPERATIONS_OWNER} | Production readiness score is at least 90 |

---

## Execution Plan

| Phase | Scope | Entry Criteria | Exit Criteria |
|-------|-------|----------------|---------------|
| 1. Stabilize | Resolve CRITICAL and P1 blockers | Validation report reviewed | No CRITICAL findings remain |
| 2. Complete | Resolve HIGH/MEDIUM implementation and evidence gaps | Phase 1 complete | Score is at least 90 in local validation |
| 3. Harden | Improve monitoring, rollback, and operational evidence | Phase 2 complete | Runbook can be generated from validation |
| 4. Revalidate | Re-run the quality gate and publish superseding artifacts | All remediation merged | New validation report approves or clearly scopes remaining work |

---

## Acceptance Criteria

| Criterion | Verification |
|-----------|--------------|
| All CRITICAL findings resolved | `VALIDATION_REPORT_{FEATURE_NAME}.md` shows zero critical issues |
| Score reaches target | `/validate {FEATURE_NAME}` reports score at least 90 |
| Runbook eligible | `runbook_eligible` is true in validation JSON |
| Evidence is current | DEFINE, DESIGN, BUILD_REPORT, and code tree reflect the same implementation |
| Residual risks accepted | Remaining non-blocking risks have owner and due date |

---

## Risk Register

| Risk | Impact | Likelihood | Mitigation | Owner |
|------|--------|------------|------------|-------|
| Remediation changes introduce regressions | High | Medium | Add or update tests before revalidation | {DELIVERY_OWNER} |
| Missing operational evidence blocks runbook | Medium | Medium | Update monitoring, rollback, and deployment evidence before revalidation | {OPERATIONS_OWNER} |
| Requirement ambiguity delays closure | Medium | Low | Clarify DEFINE and document accepted scope changes | {REMEDIATION_OWNER} |

---

## Revalidation Checklist

- [ ] P1 items are complete and linked to commits or evidence.
- [ ] P2 items are complete or explicitly accepted by owner.
- [ ] Tests and quality checks have been re-run.
- [ ] `BUILD_REPORT_{FEATURE_NAME}.md` has been updated.
- [ ] `/validate {FEATURE_NAME}` has been re-run.
- [ ] Superseded validation artifacts are archived or clearly marked.

---

## Notes

- This roadmap is generated from structured validation output.
- It should be treated as the active remediation plan until a newer validation report replaces it.
- Do not use this document as production approval; production approval requires a runbook-eligible validation result.
