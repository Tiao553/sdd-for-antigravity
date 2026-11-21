---
name: validate
description: Multi-agent quality gate for AgentSpec SDD Phase 3.5. Orchestrates four specialized CrewAI crews (SpecCrew, CodeCrew, DeliveryCrew, CouncilCrew) to validate that an implemented feature matches its DEFINE requirements and DESIGN intent.
---

# Validate Skill (`/validate`)

> **Phase 3.5 Quality Gate** — Multi-Agent Consensus Verification before Production Delivery (`/ship`).

---

## 1. Purpose & Overview

The `/validate` skill executes a rigorous, multi-agent consensus audit on newly implemented features. It bridges the gap between **Phase 3 (`/build`)** and **Phase 4 (`/ship`)**, verifying that:

1. **The code actually fulfills the business intent** documented in `DEFINE_{FEATURE}.md` (SpecCrew).
2. **The code adheres to architecture blueprints and technical best practices** documented in `DESIGN_{FEATURE}.md` (CodeCrew).
3. **The code is operationally sound, observable, idempotent, and backfill-ready** (DeliveryCrew).
4. **All findings are aggregated, arbitrated, and scored** into a formal quality gate verdict (CouncilCrew).

---

## 2. Architecture of the 4 Crews

```text
 ┌────────────────────────────────────────────────────────┐
 │             Immutable ValidateContext                  │
 │  (DEFINE.md + DESIGN.md + BUILD_REPORT.md + Code Diff) │
 └───────────┬────────────────────────────────┬───────────┘
             │                                │
             ▼                                ▼
   ┌───────────────────┐            ┌───────────────────┐
   │     SpecCrew      │            │     CodeCrew      │
   │   (Weight: 40%)   │            │   (Weight: 35%)   │
   │  - User Stories   │            │  - Architecture   │
   │  - FR Coverage    │            │  - SQL Pruning    │
   │  - Acceptance GWT │            │  - Typing / Lint  │
   │  - Edge Cases     │            │  - Data Quality   │
   └─────────┬─────────┘            └─────────┬─────────┘
             │                                │
             └────────────────┬───────────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │   DeliveryCrew    │
                    │   (Weight: 25%)   │
                    │  - Runbook & Docs │
                    │  - Observability  │
                    │  - Backfill Plan  │
                    │  - Rollback / SRE │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │    CouncilCrew    │
                    │ (Chief Arbitrator)│
                    │  - Weighted Score │
                    │  - Blocker Check  │
                    │  - PASS / BLOCKED │
                    └───────────────────┘
```

---

## 3. Usage & CLI Invocations

### Standard Chat Invocation
```bash
/validate <FEATURE_NAME>
/validate ORDERS_PIPELINE
/validate AUTH_SERVICE
```

### Direct Terminal Invocation
```bash
python skills/validate/scripts/main.py <FEATURE_NAME> [OPTIONS]
```

#### Supported Options & Flags
- `--mock`: Runs validation using deterministic mock evaluation data (useful in CI/CD without LLM API keys).
- `--strict`: Treats WARNING-level issues as BLOCKERS (enforces 100% perfection).
- `--output-dir <PATH>`: Custom directory for reports (defaults to `.agents/sdd/reports/`).
- `--skip-delivery`: Validates only Spec and Code (useful for rapid internal feature development).

---

## 4. Environment & Prerequisites

The validate crew can use either direct OpenRouter, OpenAI, or Gemini API keys for running the CrewAI autonomous agents:

```bash
# Option A: OpenRouter (Recommended for multi-model evaluation)
export OPENAI_API_KEY='sk-or-v1-...'
export OPENAI_API_BASE='https://openrouter.ai/api/v1'

# Option B: Direct OpenAI
export OPENAI_API_KEY='sk-proj-...'

# Option C: Google Gemini via OpenAI-compatible endpoint
export OPENAI_API_KEY='AIzaSy...'
export OPENAI_API_BASE='https://generativelanguage.googleapis.com/v1beta/openai/'
```

---

## 5. Output Artifacts & Gate Decisions

Upon conclusion of the 4-crew audit, CouncilCrew emits the following deterministic outputs:

| Composite Score | Blocker Count | Official Verdict | Produced Artifacts | Next SDD Action |
| :---: | :---: | :---: | :--- | :--- |
| **$\ge 85.0$** | 0 Critical | **PASS** | `VALIDATION_REPORT_{FEATURE}.md`<br/>`RUNBOOK_{FEATURE}.md` | Unlocks Phase 4: `/ship {FEATURE}` |
| **$70.0 - 84.9$** | 0 Critical | **CONDITIONAL** | `VALIDATION_REPORT_{FEATURE}.md`<br/>`ROADMAP_{FEATURE}.md` | Requires team review of remediation items. |
| **$< 70.0$** | $\ge 1$ Critical | **BLOCKED** | `VALIDATION_REPORT_{FEATURE}.md` | Exits with code 1. Re-invoke `/build`. |

---

## 6. Directory Structure & Implementation Files

```text
skills/validate/
├── SKILL.md               # Skill definition and reference guide
└── scripts/               # Core execution scripts
    ├── __init__.py        # Python package initialization
    ├── main.py            # Typer CLI application entry point
    ├── schemas.py         # Pydantic v2 data models (ValidateContext, reports)
    ├── tools.py           # File readers, ruff/mypy subprocess drivers
    ├── llm.py             # LLM configuration and OpenRouter bindings
    └── crews/             # CrewAI specialized multi-agent implementations
        ├── __init__.py
        ├── spec_crew.py   # Hierarchical crew (4 agents: MGR, ARC, ENG, SWE)
        ├── code_crew.py   # Hierarchical crew (4 agents: MGR, SWE, ENG, OPS)
        ├── delivery_crew.py # Sequential crew (2 agents: CMP, GAP)
        └── council_crew.py  # Sequential arbitrator crew (3 agents: JDG, RPT, PRD)
```

---

## 7. Troubleshooting & Recovery

| Issue | Root Cause | Solution |
| :--- | :--- | :--- |
| **`FileNotFoundError: DEFINE_...`** | Phase 1 was skipped or feature name misspelled. | Run `/define <FEATURE>` first or verify spelling in `.agents/sdd/features/`. |
| **`APIConnectionError`** | Invalid or missing `OPENAI_API_KEY`. | Set valid API key in environment or use `--mock` for offline lint checks. |
| **Gate Stalled on Blocker** | Genuine bug or missing acceptance criterion. | Check Section 3 of `VALIDATION_REPORT`, apply fix in code, and re-run `/validate`. |
