# VALIDATION REPORT: {Feature Name}

> Final verdict from the Validation Council

## Metadata

| Attribute | Value |
|-----------|-------|
| **Feature** | {FEATURE_NAME} |
| **Date** | {YYYY-MM-DD} |
| **Score** | **{XX}/100** |
| **Verdict** | {Approved for Prod / Remediation Required} |

---

## Executive Summary

{Brief summary of the validation results, including highlights and major concerns.}

---

## Scoring Breakdown

| Dimension | Weight | Score | Notes |
|-----------|--------|-------|-------|
| Spec Alignment | 30% | {X}/100 | {Notes on DEFINE coverage} |
| Code Quality | 25% | {X}/100 | {Notes on lint/tests/types} |
| Architecture Fidelity | 20% | {X}/100 | {Notes on DESIGN adherence} |
| Security & DevOps | 15% | {X}/100 | {Notes on CI/CD and secrets} |
| Production Readiness | 10% | {X}/100 | {Notes on observability} |

---

## Critical Issues (Hard Stops)

*If this section is not empty, RUNBOOK generation is blocked.*

| ID | Issue | Domain | Recommendation |
|----|-------|--------|----------------|
| CRIT-01 | {Description} | {Spec/Code/Ops} | {How to fix} |

---

## Gap Catalog

| ID | Missing Requirement / Defect | Severity |
|----|------------------------------|----------|
| GAP-01 | {Description} | {MAJOR/MINOR} |
| GAP-02 | {Description} | {MAJOR/MINOR} |
