---
name: validate
description: >
  Multi-agent quality gate for AgentSpec SDD Phase 3.5.
  Orchestrates four specialized CrewAI crews (SpecCrew, CodeCrew, DeliveryCrew, CouncilCrew)
  to validate that an implemented feature matches its DEFINE requirements and DESIGN intent.
  Produces a weighted validation score, a final report, and optionally RUNBOOK or ROADMAP artifacts.
entrypoint: scripts/main.py
tools:
  - run_command
---

# Validate Skill

## Purpose

This skill executes the `/validate` multi-agent quality gate. It reads SDD artifacts from disk,
builds an immutable `ValidateContext`, and passes it through a four-crew pipeline.

## Directory Structure

```
.agents/skills/validate/
├── skill.md               ← This file (skill descriptor)
└── scripts/               ← All executable code lives here
    ├── __init__.py        ← ValidateSkill entry class
    ├── main.py            ← CLI entry point (Typer)
    ├── schemas.py         ← Pydantic contracts (ValidateContext, reports)
    ├── tools.py           ← SDD file readers, ruff/mypy wrappers
    ├── spec_crew.py       ← (legacy flat file, superseded by crews/)
    ├── code_crew.py       ← (legacy flat file, superseded by crews/)
    └── crews/
        ├── __init__.py
        ├── spec_crew.py   ← Hierarchical · 4 agents (MGR, ARC, ENG, SWE)
        ├── code_crew.py   ← Hierarchical · 4 agents (MGR, SWE, ENG, OPS)
        ├── delivery_crew.py ← Sequential · 2 agents (CMP, GAP)
        └── council_crew.py  ← Sequential · 3 agents (JDG, RPT, PRD)
```

## Invocation

The skill is invoked by the `/validate` workflow. The workflow calls:

```bash
python3 .agents/skills/validate/scripts/main.py <FEATURE_NAME>
```

Where `<FEATURE_NAME>` is the feature identifier (e.g. `VALIDATE_WORKFLOW`).

## Required Environment Variables

| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | LLM provider API key (OpenRouter, OpenAI, etc.) |
| `OPENAI_API_BASE` | Optional: Override base URL (e.g. `https://openrouter.ai/api/v1`) |

## Crew Pipeline

```
ValidateContext (built from DEFINE + DESIGN + BUILD_REPORT + code_tree)
       │
       ├──[parallel]── SpecCrew  → SpecReport  (alignment_score, architecture_score)
       │                            Hierarchical · 4 agents
       │
       └──[parallel]── CodeCrew  → CodeReport  (quality_score, devops_score)
                                    Hierarchical · 4 agents
                  │
                  ▼
            DeliveryCrew → DeliveryDelta (missing_files, requirement_map, delta_score)
                           Sequential · 2 agents
                  │
                  ▼
            CouncilCrew  → ValidationReport (final score, runbook_eligible, roadmap_eligible)
                           Sequential · 3 agents
```

## Scoring Formula

| Dimension | Weight | Source |
|-----------|--------|--------|
| Spec Alignment | 30% | `SpecReport.alignment_score` |
| Code Quality | 25% | `CodeReport.quality_score` |
| Architecture Fidelity | 20% | `SpecReport.architecture_score` |
| Security & DevOps | 15% | `CodeReport.devops_score` |
| Production Readiness | 10% | `DeliveryDelta.delta_score` |

## Artifact Eligibility

| Score | No CRITICAL Issues | Artifact Generated |
|-------|-------------------|-------------------|
| ≥ 90 | ✅ | `RUNBOOK_{FEATURE}.md` |
| 70–89 | ✅ | `ROADMAP_{FEATURE}.md` |
| < 70 | Any | No artifact, Exit code 1 |
