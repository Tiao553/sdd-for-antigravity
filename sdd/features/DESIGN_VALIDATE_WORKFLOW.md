# DESIGN: /validate — Pre-Ship Council Validation Workflow

> Technical design for implementing the multi-crew CrewAI validation framework.

## Metadata

| Attribute | Value |
|-----------|-------|
| **Feature** | VALIDATE_WORKFLOW |
| **Date** | 2026-04-28 |
| **Author** | design-agent |
| **DEFINE** | [DEFINE_VALIDATE_WORKFLOW.md](./DEFINE_VALIDATE_WORKFLOW.md) |
| **Status** | Ready for Build |

---

## Architecture Overview

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        VALIDATION SYSTEM                                │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  [Validate Orchestrator] ← Reads DEFINE, DESIGN, BUILD_REPORT + Code   │
│             │                                                          │
│     ┌───────┴───────┐   (Parallel Execution)                           │
│     ▼               ▼                                                  │
│ [SpecCrew]      [CodeCrew]                                             │
│ (Hierarchical)  (Hierarchical)                                         │
│     │               │                                                  │
│     └───────┬───────┘   (JSON Contracts)                               │
│             ▼                                                          │
│      [DeliveryCrew] ← Diffs intent vs. delivery (Sequential)           │
│             │                                                          │
│             ▼                                                          │
│      [CouncilCrew] ← Computes 5-dimension score & gaps (Sequential)    │
│             │                                                          │
│     ┌───────┼──────────────────┐                                       │
│     ▼       ▼                  ▼                                       │
│ [REPORT]  [ROADMAP] (≥70)   [RUNBOOK] (≥90)                            │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

---

## Components

| Component | Purpose | Technology |
|-----------|---------|------------|
| Orchestrator | Coordinates the 4 crews and manages file I/O | Python, Typer (CLI) |
| SpecCrew | Analyzes SDD documents using hierarchical routing | CrewAI, LangChain |
| CodeCrew | Runs/parses quality tools and analyzes codebase | CrewAI, Subprocess |
| DeliveryCrew | Compares planned spec vs. code implementation | CrewAI (Sequential) |
| CouncilCrew | Scores the project and generates final artifacts | CrewAI (Sequential) |
| SDD Templates | Templates for formatting the final output files | Markdown / Jinja2 |

---

## Key Decisions

### Decision 1: Inner Crew Routing Strategy

| Attribute | Value |
|-----------|-------|
| **Status** | Accepted |
| **Date** | 2026-04-28 |

**Context:** SpecCrew and CodeCrew need to analyze various domains (Data Eng, SWE, DevOps) without hard-coding which agent analyzes which file.

**Choice:** Use CrewAI's `Process.hierarchical` with a Manager LLM for SpecCrew and CodeCrew.

**Rationale:** Allows the LLM to dynamically delegate tasks to the appropriate domain specialist based on the content of the files.

**Alternatives Rejected:**
1. Sequential routing - Rejected because it forces all agents to run even if their domain isn't present in the project.

**Consequences:**
- Slight increase in LLM calls (Manager overhead).
- Highly adaptable to any project type.

---

### Decision 2: Inter-Crew Communication

| Attribute | Value |
|-----------|-------|
| **Status** | Accepted |
| **Date** | 2026-04-28 |

**Context:** The 4 crews need to pass complex findings to each other.

**Choice:** Output structured JSON files (`spec_report.json`, `code_report.json`, `delivery_delta.json`) between crews.

**Rationale:** Ensures deterministic parsing by the downstream crews and prevents context window hallucination.

**Alternatives Rejected:**
1. Passing plain text context - Rejected because it's prone to losing specific gap IDs or severity flags.

**Consequences:**
- Requires strict Pydantic output schemas for the Crew tasks.

---

## File Manifest

| # | File | Action | Purpose | Agent | Dependencies |
|---|------|--------|---------|-------|--------------|
| 1 | `.agents/rules/workflow/validate-agent.md` | Create | System instructions for the orchestrator | @prompt-crafter | None |
| 2 | `.agents/workflows/sdd-workflow/validate.md` | Create | User-facing workflow documentation | @code-documenter | None |
| 3 | `.agents/skills/validate/main.py` | Create | CLI entry point and orchestration logic | @python-developer | None |
| 4 | `.agents/skills/validate/schemas.py` | Create | Pydantic models for JSON contracts | @python-developer | None |
| 5 | `.agents/skills/validate/tools.py` | Create | Tools to read SDD files, run `ruff`/`mypy` | @python-developer | None |
| 6 | `.agents/skills/validate/crews/spec_crew.py` | Create | Hierarchical SpecCrew definition | @ai-data-engineer | 4 |
| 7 | `.agents/skills/validate/crews/code_crew.py` | Create | Hierarchical CodeCrew definition | @ai-data-engineer | 4, 5 |
| 8 | `.agents/skills/validate/crews/delivery_crew.py` | Create | Sequential DeliveryCrew definition | @ai-data-engineer | 4 |
| 9 | `.agents/skills/validate/crews/council_crew.py` | Create | Sequential CouncilCrew definition | @ai-data-engineer | 4 |

**Total Files:** 9

---

## Implementation Chunks

> **Chunking Topology:** Limit chunks to 2-5 related files. Prioritize zero-dependency files in early chunks.

### Chunk 1: Foundation & Schemas
- **Files:** 1, 2, 4, 5
- **Verification:** Workflow docs exist, Pydantic schemas validate, `tools.py` can successfully run a shell command.

### Chunk 2: Parallel Crews (Spec & Code)
- **Files:** 6, 7
- **Verification:** Crews initialize correctly; mock execution produces valid JSON matching schemas.

### Chunk 3: Convergence Crews & Orchestration
- **Files:** 3, 8, 9
- **Verification:** Full end-to-end execution of `main.py` on a dummy feature outputs the three MD artifacts.

---

## Agent Assignment Rationale

| Agent | Files Assigned | Why This Agent |
|-------|----------------|----------------|
| @python-developer | 3, 4, 5 | Expert in Python CLI architecture, Pydantic schemas, and subprocess tools. |
| @ai-data-engineer | 6, 7, 8, 9 | Expert in CrewAI integration, agent prompting, and multi-crew data flows. |
| @prompt-crafter | 1 | Expert in formatting `.agents/rules/` markdown documents. |
| @code-documenter | 2 | Expert in creating user-facing workflow guides. |

---

## Code Patterns

### Pattern 1: Pydantic JSON Contract (schemas.py)

```python
from pydantic import BaseModel, Field
from typing import List

class GapItem(BaseModel):
    id: str = Field(..., description="Unique gap identifier (e.g., GAP-01)")
    description: str = Field(..., description="What is missing or misaligned")
    severity: str = Field(..., description="CRITICAL, MAJOR, or MINOR")
    domain: str = Field(..., description="Spec, Code, or Ops")

class CouncilVerdict(BaseModel):
    score: int = Field(..., ge=0, le=100)
    critical_count: int
    dimensions: dict[str, int]
    gaps: List[GapItem]
```

### Pattern 2: Crew Execution inside Orchestrator (main.py)

```python
# Run Spec and Code crews concurrently using ThreadPoolExecutor
with concurrent.futures.ThreadPoolExecutor() as executor:
    spec_future = executor.submit(spec_crew.kickoff, inputs=context)
    code_future = executor.submit(code_crew.kickoff, inputs=context)

    spec_report = spec_future.result()
    code_report = code_future.result()

# Pass results to Delivery Crew
delivery_delta = delivery_crew.kickoff(inputs={
    "spec_report": spec_report,
    "code_report": code_report,
    "original_context": context
})
```

---

## Data Flow

```text
1. CLI invoked: `/validate <feature>`
   │
   ▼
2. Tools read `.agents/sdd/features/*_<feature>.md` and `BUILD_REPORT`
   │
   ▼
3. SpecCrew and CodeCrew analyze context in parallel
   │
   ▼
4. DeliveryCrew diffs intended Spec vs actual Code reports
   │
   ▼
5. CouncilCrew scores the diff across 5 dimensions and flags CRITICALs
   │
   ▼
6. Jinja2 templates render `VALIDATION_REPORT`, `ROADMAP`, `RUNBOOK`
```

---

## Testing Strategy

| Test Type | Scope | Tools | Coverage Goal |
|-----------|-------|-------|---------------|
| Unit | Tools & Schemas | `pytest` | 90% |
| Integration | CrewAI Flows | `pytest` + mocked LLM | Valid JSON outputs |
| E2E | CLI Command | `typer.testing` | End-to-end artifact generation |

---

## Error Handling

| Error Type | Handling Strategy | Retry? |
|------------|-------------------|--------|
| Missing SDD file | Gracefully exit with error message pointing to `/define` | No |
| LLM parsing failure | CrewAI native Pydantic output parser retries | Yes (handled by CrewAI) |
| Tool execution fail | Subprocess captures `stderr`, CodeCrew analyzes the error | No |

---

## Security Considerations

- `tools.py` must only run whitelisted commands (`ruff check`, `mypy`, `pytest`).
- Avoid arbitrary code execution when analyzing the project tree.

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-04-28 | design-agent | Initial version |

---

## Next Step

**Ready for:** `/build .agents/sdd/features/DESIGN_VALIDATE_WORKFLOW.md`
