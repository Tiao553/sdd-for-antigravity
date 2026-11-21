# DEFINE: /validate — Pre-Ship Council Validation Workflow

> A multi-crew CrewAI council that sits between `/build` and `/ship` to validate intent-to-delivery traceability and production readiness.

## Metadata

| Attribute | Value |
|-----------|-------|
| **Feature** | VALIDATE_WORKFLOW |
| **Date** | 2026-04-28 |
| **Author** | define-agent |
| **Status** | Ready for Design |
| **Clarity Score** | 15/15 |

---

## Problem Statement

The current SDD workflow lacks a structured, automated quality gate between the `/build` phase and `/ship` archival. Without this, developers might ship features that have unvalidated spec alignment, undetected code quality regressions, or missing production readiness criteria, leading to technical debt and deployment risks.

---

## Target Users

| User | Role | Pain Point |
|------|------|------------|
| Data Engineer | Developer | Has no structured way to verify their implementation matches DEFINE requirements before shipping. |
| Tech Lead | Reviewer | Lacks an automated quality council or comprehensive gap report before approving production deployment. |
| AgentSpec Contributor | Architect | Needs a reusable skill pattern for building multi-crew, multi-agent validation workflows. |

---

## Goals

What success looks like (prioritized):

| Priority | Goal |
|----------|------|
| **MUST** | `/validate <feature>` command is invocable from the CLI after `/build` completes. |
| **MUST** | SpecCrew and CodeCrew run in parallel, producing structured JSON reports. |
| **MUST** | DeliveryCrew consumes parallel reports + original context to generate `delivery_delta.json`. |
| **MUST** | CouncilCrew produces a `VALIDATION_REPORT_{FEATURE}.md` with a weighted score across 5 dimensions. |
| **MUST** | Any CRITICAL issue must trigger a hard stop, blocking runbook generation and logging an explicit catalog in the report. |
| **MUST** | Skill lives at `.agents/skills/validate/` as a self-contained CrewAI project. |
| **MUST** | `RUNBOOK_{FEATURE}.md` is generated only when the final score is ≥ 90 and there are zero CRITICAL issues. |
| **MUST** | `ROADMAP_{FEATURE}.md` is generated when the final score is between 70–89 and there are zero CRITICAL issues. |

**Priority Guide:**
- **MUST** = MVP fails without this
- **SHOULD** = Important, but workaround exists
- **COULD** = Nice-to-have, cut first if needed

---

## Success Criteria

Measurable outcomes (must include numbers):

- [ ] Command `/validate` executes completely and outputs `VALIDATION_REPORT_{FEATURE}.md`.
- [ ] 2 parallel crews (SpecCrew and CodeCrew) execute and generate intermediate JSON artifacts.
- [ ] Final score is calculated across exactly 5 dimensions: Spec Alignment (30%), Code Quality (25%), Architecture Fidelity (20%), Security & DevOps (15%), Production Readiness (10%).
- [ ] Score calculation handles CRITICAL flags correctly (1 or more CRITICALs strictly prevents runbook generation).

---

## Acceptance Tests

| ID | Scenario | Given | When | Then |
|----|----------|-------|------|------|
| AT-001 | Happy path (Score ≥ 90) | A completed build with no critical issues | `/validate feature` runs | Generates Validation Report, Runbook, and Roadmap. |
| AT-002 | Remediation required | A build with 1 CRITICAL issue in Code Quality | `/validate feature` runs | Generates Validation Report with CRITICAL catalog; no Runbook or Roadmap is produced. |
| AT-003 | Partial success (Score 80) | A build with score 80 and 0 CRITICAL issues | `/validate feature` runs | Generates Validation Report and Roadmap, but no Runbook. |

---

## Out of Scope

Explicitly NOT included in this feature:

- Domain-specific plugin crews (e.g., dbt, Spark, Kafka validators).
- LLM-driven code execution (the council only reads existing test/lint results).
- Automatic PR creation or automatically triggering the `/ship` command.
- Validation history dashboard or long-term persistence layer.
- Multi-project or cross-feature validation logic.

---

## Constraints

| Type | Constraint | Impact |
|------|------------|--------|
| Technical | Must use CrewAI as the multi-agent framework. | Dictates the project structure and agent orchestration inside the skill. |
| Workflow | Must be invocable independently of `/ship`. | Preserves user agency; `/ship` does not automatically trigger validation. |
| Data | JSON contracts between crews must follow a defined schema. | Required for robust parsing by the DeliveryCrew and CouncilCrew. |
| Execution | Quality tools (ruff, mypy, pytest) invoked via shell, not re-implemented in Python. | CodeCrew Manager LLM must be able to run and parse shell commands. |

---

## Technical Context

> Essential context for Design phase - prevents misplaced files and missed infrastructure needs.

| Aspect | Value | Notes |
|--------|-------|-------|
| **Deployment Location** | `.agents/skills/validate/` & `.agents/workflows/sdd-workflow/validate.md` | The skill logic and its CLI trigger location. |
| **KB Domains** | `crewai`, `python` | For building multi-crew systems and hierarchical routing. |
| **IaC Impact** | None | This is a local CLI workflow tool. |

**Why This Matters:**

- **Location** → Design phase uses correct project structure, prevents misplaced files
- **KB Domains** → Design phase pulls correct patterns from `.agents/kb/`
- **IaC Impact** → Triggers infrastructure planning, avoids "works locally" failures

---

## Assumptions

Assumptions that if wrong could invalidate the design:

| ID | Assumption | If Wrong, Impact | Validated? |
|----|------------|------------------|------------|
| A-001 | CrewAI hierarchical process can accurately route findings to specialists based on LLM decisions. | Would need to build hard-coded deterministic routing instead. | [ ] |
| A-002 | Agent context windows can handle combining BRAINSTORM, DEFINE, DESIGN, and BUILD_REPORT contents. | DeliveryCrew might OOM or lose instructions; would require a context pruning hook. | [ ] |

---

## Clarity Score Breakdown

| Element | Score (0-3) | Notes |
|---------|-------------|-------|
| Problem | 3 | Clear pain point regarding missing quality gate before shipping. |
| Users | 3 | Explicit personas defined with precise needs. |
| Goals | 3 | Strict MUSTs covering multi-crew topology and outputs. |
| Success | 3 | Quantitative criteria based on the 5 scoring dimensions and output artifacts. |
| Scope | 3 | In and out-of-scope explicitly locked. |
| **Total** | **15/15** | |

**Scoring Guide:**
- 0 = Missing entirely
- 1 = Vague or incomplete
- 2 = Clear but missing details
- 3 = Crystal clear, actionable

**Minimum to proceed: 12/15**

---

## Open Questions

None - ready for Design.

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-04-28 | define-agent | Initial version from BRAINSTORM_VALIDATE_WORKFLOW.md |

---

## Next Step

**Ready for:** `/design .agents/sdd/features/DEFINE_VALIDATE_WORKFLOW.md`
