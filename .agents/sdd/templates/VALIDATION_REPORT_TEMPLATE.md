# VALIDATION REPORT: {FEATURE_NAME}

> Evidence-based quality gate verdict for SDD Phase 3.5.

## Document Control

| Attribute | Value |
|-----------|-------|
| Feature | {FEATURE_NAME} |
| Generated At | {YYYY-MM-DD} |
| Validation Score | **{SCORE}/100** |
| Verdict | **{VERDICT}** |
| Recommended Artifact | {RECOMMENDED_ARTIFACT} |
| Gate Owner | {GATE_OWNER} |
| Source Artifacts | `DEFINE_{FEATURE_NAME}.md`, `DESIGN_{FEATURE_NAME}.md`, `BUILD_REPORT_{FEATURE_NAME}.md` |

---

## Executive Summary

{EXECUTIVE_SUMMARY}

### Decision

| Decision Item | Result |
|---------------|--------|
| Production readiness | {PRODUCTION_READINESS_DECISION} |
| Runbook eligibility | {RUNBOOK_ELIGIBILITY} |
| Roadmap eligibility | {ROADMAP_ELIGIBILITY} |
| Blocking issues | {BLOCKING_ISSUE_COUNT} |

---

## Gate Criteria

| Gate | Pass Condition | Result | Evidence |
|------|----------------|--------|----------|
| Specification alignment | DEFINE requirements are traceable to implementation evidence | {SPEC_GATE_RESULT} | See scoring breakdown and gap catalog |
| Architecture fidelity | Implementation follows DESIGN decisions and boundaries | {ARCH_GATE_RESULT} | See architecture fidelity score |
| Code quality | Lint, type, test, and maintainability findings are acceptable | {CODE_GATE_RESULT} | See code quality score |
| Security and DevOps | Secrets, CI/CD, dependencies, and operational controls are acceptable | {DEVOPS_GATE_RESULT} | See security and DevOps score |
| Production readiness | Delivery gaps are non-blocking and rollback/observability are defined | {READINESS_GATE_RESULT} | See production readiness score |

---

## Scoring Breakdown

| Dimension | Weight | Score | Gate | Notes |
|-----------|--------|-------|------|-------|
{SCORING_ROWS}

### Formula

```text
score = (Spec Alignment * 0.30)
      + (Code Quality * 0.25)
      + (Architecture Fidelity * 0.20)
      + (Security and DevOps * 0.15)
      + (Production Readiness * 0.10)
```

---

## Critical Issues

If this section contains any real issue, RUNBOOK generation is blocked.

| ID | Issue | Domain | Recommendation |
|----|-------|--------|----------------|
{CRITICAL_ISSUE_ROWS}

---

## Gap Catalog

| ID | Missing Requirement / Defect | Severity |
|----|------------------------------|----------|
{GAP_ROWS}

---

## Evidence Register

| Evidence Type | Expected Source | Status | Notes |
|---------------|-----------------|--------|-------|
| Requirements | `DEFINE_{FEATURE_NAME}.md` | {DEFINE_EVIDENCE_STATUS} | Requirement IDs should map to implementation evidence |
| Architecture | `DESIGN_{FEATURE_NAME}.md` | {DESIGN_EVIDENCE_STATUS} | Design decisions should be reflected in code structure |
| Build output | `BUILD_REPORT_{FEATURE_NAME}.md` | {BUILD_EVIDENCE_STATUS} | Build/test evidence should be current |
| Code tree | Implemented files under feature scope | {CODE_TREE_STATUS} | Unexpected and missing files should be reviewed |
| Validation JSON | `ValidationReport.artifact_plan` | Present | Crews return JSON guidance only; documents are rendered by the skill |

---

## Follow-up Actions

| Priority | Action | Owner | Due | Exit Criteria |
|----------|--------|-------|-----|---------------|
| P1 | Resolve all CRITICAL findings before production promotion | {GATE_OWNER} | TBD | Critical issue count is zero |
| P2 | Address HIGH and MEDIUM gap catalog items | {DELIVERY_OWNER} | TBD | Validation score is at least 90 |
| P3 | Re-run `/validate {FEATURE_NAME}` after remediation | {GATE_OWNER} | TBD | New validation report supersedes this document |

---

## Audit Notes

- This report is generated from structured validation output.
- The Validation Council provides JSON guidance only.
- Markdown artifacts are rendered by the validate skill using repository templates.
- Treat this document as a point-in-time gate result, not as a permanent approval.
