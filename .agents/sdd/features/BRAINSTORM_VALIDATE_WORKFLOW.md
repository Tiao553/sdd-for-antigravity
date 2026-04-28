# BRAINSTORM: /validate — Pre-Ship Council Validation Workflow

> Exploratory session to clarify intent and approach before requirements capture

## Metadata

| Attribute | Value |
|-----------|-------|
| **Feature** | VALIDATE_WORKFLOW |
| **Date** | 2026-04-27 |
| **Author** | brainstorm-agent |
| **Status** | Ready for Define |

---

## Initial Idea

**Raw Input:** Build a `/validate` phase that sits between `/build` and `/ship` — a CrewAI-based multi-crew council that reads all SDD artifacts (BRAINSTORM, DEFINE, DESIGN) and the built project, validates intent-to-delivery traceability, runs quality checks, generates a detailed gap report, and if production-ready produces a runbook and deployment roadmap.

**Context Gathered:**
- Current SDD workflow has 5 phases: brainstorm → define → design → build → ship. No validation gate exists between build and ship.
- `/build` already runs ruff/mypy/pytest as per BUILD_REPORT but this is developer-level, not council-level.
- The framework has a `skills/` directory pattern (visual-explainer, excalidraw-diagram) for reusable capability packs invoked by workflow commands.
- Existing agents (data-architect, data-engineer, software-engineer concepts) exist in `.agents/rules/` but are not organized into an executable crew.
- No VALIDATION_REPORT artifact type exists in the current SDD template system.

**Technical Context Observed (for Define):**

| Aspect | Observation | Implication |
|--------|-------------|-------------|
| Skill location | `.agents/skills/` | Skill lives at `.agents/skills/validate/` |
| Workflow location | `.agents/workflows/sdd-workflow/` | New `validate.md` alongside build.md and ship.md |
| Agent rules | `.agents/rules/` by category | Crew agents inherit patterns from existing specialists |
| SDD templates | `.agents/sdd/templates/` | New VALIDATION_REPORT template needed |
| Report output | `.agents/sdd/reports/` | VALIDATION_REPORT_{FEATURE}.md stored here |

---

## Discovery Questions & Answers

| # | Question | Answer | Impact |
|---|----------|--------|--------|
| 1 | What is the primary artifact the council evaluates? | Both SDD documents AND built code — full traceability from intent to implementation | Full cross-validation scope: BRAINSTORM → DEFINE → DESIGN → code → tests |
| 2 | What crew topology? | Hybrid B outer (multi-crew) + C inner (Manager LLM per crew) | Two parallel ingestion crews (Spec + Code), each with internal LLM-driven routing |
| 3 | Inter-agent communication model? | Hybrid B+C — multi-crew contracts at the outer layer, Manager LLM within each crew | Each crew outputs a structured JSON report; a DeliveryCrew consumes both outputs |
| 4 | Should there be a comparison layer before the council? | Yes — a new DeliveryCrew sits between the parallel flows and the CouncilCrew | DeliveryCrew generates `delivery_delta.json` (intent vs. delivery) as council input |
| 5 | Validation scoring model? | D — weighted dimensions + hard stops for CRITICAL issues | Score 0-100 across 5 dimensions; any CRITICAL blocks runbook generation |
| 6 | How should `/validate` be packaged? | A — first-class SDD workflow command; skill at `.agents/skills/validate/` | New `validate.md` workflow + `validate-agent.md` rule + skill directory |

---

## Sample Data Inventory

> Samples improve LLM accuracy through in-context learning and few-shot prompting.

| Type | Location | Count | Notes |
|------|----------|-------|-------|
| Existing BUILD_REPORT | `.agents/sdd/reports/` | Multiple | Source of truth for what was built; crew reads these |
| DEFINE documents | `.agents/sdd/features/` | Multiple | Requirements to validate against |
| DESIGN documents | `.agents/sdd/features/` | Multiple | Architecture spec to cross-check |
| Built code artifacts | Project tree (per feature) | Variable | Subject of CodeCrew analysis |
| ruff/mypy/pytest results | Generated at runtime | — | CodeCrew executes and reads these |

---

## Approaches Explored

### Approach A: Single Flat CrewAI Crew
**Description:** One crew, all agents share context, sequential/parallel process.
**Pros:** Simple to build, native CrewAI support.
**Cons:** No context isolation, context bloat with large projects, poor scalability.
**Verdict:** Rejected — insufficient for multi-domain projects.

---

### Approach B: Multiple Independent Crews
**Description:** Separate crew per domain, communicate via JSON contracts.
**Pros:** Full isolation, scales well, mirrors Antigravity routing.
**Cons:** Most complex to build, requires serialization contracts.
**Verdict:** Used as outer structure.

---

### Approach C: Single Crew + Manager LLM (Hierarchical) ⭐ Inner Pattern
**Description:** CrewAI `Process.hierarchical` — Manager LLM delegates dynamically.
**Pros:** Adaptive routing, simpler than full multi-crew, native CrewAI capability.
**Cons:** Non-deterministic routing, harder to audit.
**Verdict:** Used as inner routing pattern within each crew.

---

## Selected Approach

| Attribute | Value |
|-----------|-------|
| **Chosen** | Hybrid: B outer structure + C inner routing + DeliveryCrew delta layer |
| **User Confirmation** | 2026-04-27 |
| **Reasoning** | Multi-crew outer structure gives context isolation and scalability. Manager LLM inside each crew enables adaptive specialist routing without hard-coding domain dispatch. DeliveryCrew adds a structured comparison artifact that grounds the CouncilCrew's judgment in facts, not raw LLM inference. |

---

## Architecture: 4-Layer Crew Topology

```text
/validate <feature>
         │
         ▼
┌─────────────────────────┐
│  Validate Orchestrator   │  ← Entry point: reads all SDD artifacts + code tree
└────────────┬────────────┘
             │ spawns in parallel
    ┌────────┴────────┐
    ▼                 ▼
┌─────────┐     ┌─────────┐
│SpecCrew │     │CodeCrew │   ← Flow 1.1 and 1.2 run in parallel
│ Manager │     │ Manager │   ← Each has an internal Manager LLM (hierarchical)
│  LLM    │     │  LLM    │
│ ─────── │     │ ─────── │
│Architect│     │   SWE   │
│DataEngr │     │DataEngr │
│   SWE   │     │ DevOps  │
└────┬────┘     └────┬────┘
     │ spec_report   │ code_report
     └──────┬────────┘
            ▼
┌─────────────────────────┐
│      DeliveryCrew        │  ← NEW: receives original context + both reports
│  ┌─────────────────┐    │
│  │ Comparator      │    │  ← Diffs intent vs. delivery
│  │ Gap Mapper      │    │  ← Maps DEFINE requirements to implementation evidence
│  └─────────────────┘    │
│  output: delivery_delta.json │
└────────────┬────────────┘
             ▼
┌─────────────────────────┐
│       CouncilCrew        │  ← Reads delivery_delta.json + all reports
│  ┌─────────────────┐    │
│  │ Council Judge   │    │  ← Computes final score (0-100) across 5 dimensions
│  │ Report Writer   │    │  ← Generates VALIDATION_REPORT
│  │ Prod Readiness  │    │  ← Generates RUNBOOK if score qualifies
│  └─────────────────┘    │
└────────────┬────────────┘
             ▼
    Output Artifacts
    ├── VALIDATION_REPORT_{FEATURE}.md  (always)
    ├── ROADMAP_{FEATURE}.md            (score 70–89, zero CRITICALs)
    └── RUNBOOK_{FEATURE}.md            (score ≥ 90, zero CRITICALs)
```

---

## Scoring Model (D — Weighted + Hard Stops)

| Dimension | Weight | What It Measures |
|-----------|--------|-----------------|
| Spec Alignment | 30% | DEFINE requirements covered by implementation |
| Code Quality | 25% | ruff, mypy, pytest results, coverage, complexity |
| Architecture Fidelity | 20% | Implementation matches DESIGN spec |
| Security & DevOps | 15% | Secrets hygiene, CI/CD config, dependency audit |
| Production Readiness | 10% | Logging, error handling, observability, config externalization |

**Score → Output mapping:**

| Score | CRITICALs | Output |
|-------|-----------|--------|
| ≥ 90 | Zero | VALIDATION_REPORT + RUNBOOK + ROADMAP |
| 70–89 | Zero | VALIDATION_REPORT + ROADMAP |
| < 70 | Any | VALIDATION_REPORT only (remediation required) |
| Any | ≥ 1 | Hard stop — VALIDATION_REPORT with CRITICAL catalog |

---

## Key Decisions Made

| # | Decision | Rationale | Alternative Rejected |
|---|----------|-----------|----------------------|
| 1 | DeliveryCrew as a separate crew (not an agent inside CouncilCrew) | Isolation: delta computation is a distinct concern from verdict rendering | Merged into CouncilCrew — too much responsibility per crew |
| 2 | Manager LLM pattern inside each crew | Enables adaptive routing without hard-coding domain specialists | Fixed sequential agent chain — inflexible for variable-domain projects |
| 3 | JSON contracts between crews | Structured, auditable, parseable by downstream crews | Free-form text passing — loses structure, harder to gap-detect |
| 4 | Three output artifacts vs. single report | Separates concerns: validation (always), remediation (conditional), deployment (conditional) | Single monolithic report — harder to consume selectively |
| 5 | First-class workflow command (not a ship gate) | User control: validate when ready, not forced on every /ship | Auto-gate in /ship — removes user agency, adds latency |

---

## Features Removed (YAGNI)

| Feature Suggested | Reason Removed | Can Add Later? |
|-------------------|----------------|----------------|
| Domain-specific plugins (dbt, Spark, Kafka) | Generic SWE/DataEng/DevOps agents cover MVP scope | Yes — skill extension points |
| LLM actually executing code at validate time | ruff/mypy/pytest already run during /build; CodeCrew reads results | Yes — post-MVP enhancement |
| Automatic PR creation on score ≥ 90 | /ship handles archiving; /validate scoped to reporting | Yes — /ship integration |
| Web dashboard for validation history | HTML report is sufficient for MVP | Yes — future observability layer |
| Multi-project cross-validation | Single feature scope is correct for MVP | Yes — enterprise edition |
| Real-time streaming progress to terminal | Batch report output is simpler and sufficient | Yes — UX enhancement |

---

## Incremental Validations

| Section | Presented | User Feedback | Adjusted? |
|---------|-----------|---------------|-----------|
| Scope (3 options) | ✅ | "C — both docs and code" | No |
| Crew topology (3 scenarios explained) | ✅ | "Hybrid B+C with DeliveryCrew layer" | Added DeliveryCrew |
| Architecture diagram (HTML visual) | ✅ | Confirmed — moved to docs/ | No |
| Scoring model | ✅ | "D — weighted + hard stops" | No |
| Packaging | ✅ | "A — first-class workflow command" | No |

---

## Suggested Requirements for /define

### Problem Statement (Draft)
The SDD workflow has no structured gate between `/build` completion and `/ship` archival — developers may ship features with unvalidated spec alignment, code quality regressions, or missing production readiness criteria.

### Target Users (Draft)

| User | Pain Point |
|------|------------|
| Data Engineer | No structured way to verify implementation matches DEFINE requirements before shipping |
| Tech Lead | No automated quality council or gap report before production deployment |
| AgentSpec Contributor | No skill pattern for multi-crew validation workflows |

### Success Criteria (Draft)
- [ ] `/validate <feature>` invocable from CLI after `/build` completes
- [ ] SpecCrew and CodeCrew run in parallel and produce structured JSON reports
- [ ] DeliveryCrew generates `delivery_delta.json` with intent-vs-delivery comparison
- [ ] CouncilCrew produces VALIDATION_REPORT with score across 5 dimensions
- [ ] RUNBOOK generated only when score ≥ 90 and zero CRITICALs
- [ ] ROADMAP generated when score 70–89 and zero CRITICALs
- [ ] Any CRITICAL issue triggers hard stop with explicit catalog in report
- [ ] Skill lives at `.agents/skills/validate/` as a self-contained CrewAI project
- [ ] Workflow command at `.agents/workflows/sdd-workflow/validate.md`
- [ ] Validate-agent rule at `.agents/rules/workflow/validate-agent.md`

### Constraints Identified
- Must use CrewAI as the multi-agent framework (consistent with existing skills direction)
- Must be invocable without modifying `/ship` (user agency preserved)
- JSON contracts between crews must follow a defined schema (auditable)
- All quality tools (ruff, mypy, pytest) invoked via shell, not re-implemented
- VALIDATION_REPORT must reference SDD artifact paths for traceability

### Out of Scope (Confirmed)
- Domain-specific plugin crews (dbt, Spark, Kafka validators)
- LLM-driven code execution beyond reading existing test results
- Automatic PR creation or /ship triggering
- Validation history dashboard or persistence layer
- Multi-project or cross-feature validation

---

## Session Summary

| Metric | Value |
|--------|-------|
| Questions Asked | 6 |
| Approaches Explored | 3 (A, B, C) + hybrid selected |
| Features Removed (YAGNI) | 6 |
| Validations Completed | 5 |
| Architecture Diagram | `docs/validate-crew-architecture.html` |

---

## Next Step

**Ready for:** `/define .agents/sdd/features/BRAINSTORM_VALIDATE_WORKFLOW.md`
