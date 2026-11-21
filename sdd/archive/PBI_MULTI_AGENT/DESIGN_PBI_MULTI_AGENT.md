# DESIGN: PBI Multi-Agent PBIP Generator

> Technical design for implementing the PBI Multi-Agent PBIP Generator

## Metadata

| Attribute | Value |
|-----------|-------|
| **Feature** | PBI_MULTI_AGENT |
| **Date** | 2026-04-25 |
| **Author** | design-agent |
| **DEFINE** | [DEFINE_PBI_MULTI_AGENT.md](./DEFINE_PBI_MULTI_AGENT.md) |
| **Status** | ✅ Shipped |
| **Shipped Date** | 2026-04-27 |

---

## Architecture Overview

┌───────────────────────────────────────────────────────────────────────┐
│                          SYSTEM DIAGRAM                                │
├───────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  [User Prompt]                                                         │
│        │                                                               │
│        ▼                                                               │
│  ┌───────────────────────── LangGraph ──────────────────────────────┐  │
│  │                                                                  │  │
│  │  1. [Requirement Analyst] → 2. [Schema Mapper]                   │  │
│  │                                       │                          │  │
│  │                                       ▼                          │  │
│  │        [YAML Schemas] ←────── 3. [TMDL Builder]                  │  │
│  │                                       │                          │  │
│  │                                       ▼                          │  │
│  │                          4. [TMDL Validator] ──(retry)──┐        │  │
│  │                                       │                 │        │  │
│  │                                       ▼                 │        │  │
│  │                             5. [DAX Specialist]         │        │  │
│  │                                       │                 │        │  │
│  │                                       ▼                 │        │  │
│  │                    6. [Shadow Traffic Configurator]     │        │  │
│  │                                       │                 │        │  │
│  │           ┌───────────────────────────┴─────────────┐   │        │  │
│  │           │                                         │   │        │  │
│  │           ▼                                         ▼   │        │  │
│  │   [Docker: Shadow Traffic]                  7. [Layout Designer] │  │
│  │           │                                         │   │        │  │
│  │           ▼                                         │   │        │  │
│  │   [Supabase: Postgres] ◄────────────────────────────┘   │        │  │
│  │                                                         │        │  │
│  │                                       ▼                 │        │  │
│  │                           8. [PBIP Assembler]           │        │  │
│  └───────────────────────────────────────┬──────────────────────────┘  │
│                                          │                             │
│                                          ▼                             │
│                                  [PBIP Directory]                      │
└───────────────────────────────────────────────────────────────────────┘

---

## Components

| Component | Purpose | Technology |
|-----------|---------|------------|
| **Orchestrator** | Manages state, transitions, and retries | LangGraph |
| **Agents** | Specific LLM personas executing distinct tasks | LangChain + OpenRouter |
| **Validators** | Checks syntax and structure of generated artifacts | Python custom logic |
| **Templates** | Base structures for PBIP files | Jinja2 |
| **CLI** | User entry point | Typer |
| **State** | Shared memory between agents | Python `TypedDict` |

---

## Key Decisions

### Decision 1: LangGraph for Orchestration

| Attribute | Value |
|-----------|-------|
| **Status** | Accepted |
| **Date** | 2026-04-25 |

**Context:** The pipeline needs sequential execution with conditional retry loops (e.g., if TMDL is invalid, retry the TMDL Builder up to 3 times).
**Choice:** Use `langgraph` StateGraph.
**Rationale:** Provides typed state, visualizable graphs, and native integration with LangChain. Perfect for cyclic workflows (retries).
**Alternatives Rejected:**
1. Simple Python functions - rejected because managing retries and state passing becomes messy.
2. Airflow - rejected because it's too heavy for a local synchronous CLI tool.
**Consequences:** Requires users to install `langgraph`. Excellent maintainability.

### Decision 2: YAML Schema Catalog

| Attribute | Value |
|-----------|-------|
| **Status** | Accepted |
| **Date** | 2026-04-25 |

**Context:** The LLM needs context on what data is available to generate valid reports without connecting to a live DB.
**Choice:** Use YAML files to represent the dimensional models (tables, columns, types, relationships).
**Rationale:** Easily readable by both humans and LLMs. Can be injected into the `Schema Mapper` prompt efficiently.
**Alternatives Rejected:** SQL DDLs - rejected because they are harder to parse programmatically and less compact than YAML.

### Decision 3: Shadow Traffic + Supabase for High-Fidelity Data

| Attribute | Value |
|-----------|-------|
| **Status** | Accepted |
| **Date** | 2026-04-26 |

**Context:** Reports need realistic data structure and Supabase integration was requested for advanced querying and data persistence.
**Choice:** Use Shadow Traffic (via Docker) to generate data into a Supabase/Postgres instance.
**Rationale:** Shadow Traffic generates high-fidelity data from JSON schemas. Supabase provides a real Postgres backend for the PBIP to connect to, ensuring 100% compatibility with Power BI's native Postgres connector.
**Alternatives Rejected:**
1. Inline M Expressions - rejected because it's limited for complex relational scenarios and doesn't support the requested Supabase flow.
2. Manual CSV generation - rejected because it lacks the high-fidelity randomization of Shadow Traffic.

---

## File Manifest

| # | File | Action | Purpose | Agent | Dependencies |
|---|------|--------|---------|-------|--------------|
| 1 | `pyproject.toml` | Create | Dependencies | (general) | None |
| 2 | `.env.example` | Create | Environment template | (general) | None |
| 3 | `README.md` | Create | Documentation | (general) | None |
| 4 | `.gitignore` | Create | Git ignores | (general) | None |
| 5 | `src/pbi_agent/config.py` | Create | Pydantic settings | @python-developer | None |
| 6 | `src/pbi_agent/state.py` | Create | PBIPState TypedDict | @python-developer | None |
| 7 | `src/pbi_agent/llm.py` | Create | OpenRouter factory | @genai-architect | 5 |
| 8 | `src/pbi_agent/schemas/vendas.yaml` | Create | Sales catalog | @schema-designer | None |
| 9 | `src/pbi_agent/validators/tmdl_validator.py` | Create | TMDL syntax check | @python-developer | None |
| 10 | `src/pbi_agent/validators/pbip_validator.py` | Create | PBIP structure check | @python-developer | None |
| 11 | `src/pbi_agent/agents/requirement_analyst.py` | Create | Node | @genai-architect | 6, 7 |
| 12 | `src/pbi_agent/agents/schema_mapper.py` | Create | Node | @genai-architect | 6, 7 |
| 13 | `src/pbi_agent/agents/tmdl_builder.py` | Create | Node | @genai-architect | 6, 7 |
| 14 | `src/pbi_agent/agents/dax_specialist.py` | Create | Node | @genai-architect | 6, 7 |
| 15 | `src/pbi_agent/agents/layout_designer.py` | Create | Node | @genai-architect | 6, 7 |
| 16 | `src/pbi_agent/agents/shadow_traffic_config.py` | Create | Node | @genai-architect | 6, 7 |
| 17 | `src/pbi_agent/agents/pbip_assembler.py` | Create | Node | @python-developer | 6 |
| 18 | `src/pbi_agent/graph.py` | Create | LangGraph workflow | @pipeline-architect | 6, 9, 11-17 |
| 19 | `src/pbi_agent/cli.py` | Create | Typer CLI | @python-developer | 5, 18 |
| 20 | `src/pbi_agent/templates/tmdl/dataset.tmdl.j2` | Create | Jinja2 template | @schema-designer | None |
| 21 | `src/pbi_agent/templates/pbir/report.pbir.j2` | Create | Jinja2 template | @schema-designer | None |
| 22 | `docker-compose.yml` | Create | Shadow Traffic infra | @python-developer | None |
| 23 | `src/pbi_agent/utils/db.py` | Create | Supabase/Postgres helpers | @python-developer | None |
| 24 | `tests/conftest.py` | Create | Pytest fixtures | @test-generator | None |
| 25 | `tests/test_agents.py` | Create | Agent logic tests | @test-generator | 11-16 |
| 26 | `tests/test_graph.py` | Create | LangGraph tests | @test-generator | 18 |

**Total Files:** 24

---

## Implementation Chunks

> **Chunking Topology:** Minimized number of chunks. Chunk 1 establishes the runnable foundation. Subsequent chunks deploy complete feature blocks.

### Chunk 1: Environment & Foundation
- **Files:** 1-10
- **Verification:** Environment runs, Pydantic models validate correctly, schemas are loaded.
- **Why:** Scaffolding, settings, state, LLM clients, and validators have no external logic dependencies and establish the base project.

### Chunk 2: Core Logic & Orchestration
- **Files:** 11-21
- **Verification:** CLI executes end-to-end (even with mocked inputs) without crashing.
- **Why:** Groups all LLM agents, LangGraph orchestration, Jinja2 templates, and CLI entry point into a single functional slice.

### Chunk 3: Testing & Polish
- **Files:** 22-24
- **Verification:** `pytest` passes with 100% success rate on critical paths.
- **Why:** Ensures the implemented pipeline is robust against the acceptance criteria.

---

## Agent Assignment Rationale

> Agents discovered from `.agents/rules/` - Build phase invokes matched specialists.

| Agent | Files Assigned | Why This Agent |
|-------|----------------|----------------|
| @python-developer | 5, 6, 9, 10, 17, 19 | Core Python app code, Pydantic models, CLI, validation logic |
| @genai-architect | 7, 11-16 | LLM integration patterns, structured JSON generation prompts, agent node logic |
| @schema-designer | 8, 20, 21 | YAML schema design, TMDL/PBIR template structures |
| @pipeline-architect | 18 | LangGraph orchestration, retries, and conditional edge routing |
| @test-generator | 22, 23, 24 | Pytest fixtures and unit/integration testing |
| (general) | 1, 2, 3, 4 | Scaffolding and simple text files |

---

## Code Patterns

### Pattern 1: LangGraph State Definition

```python
from typing import TypedDict, List, Dict

class PBIPState(TypedDict):
    user_prompt: str
    target_schema: str | None
    requirements: Dict[str, Any]
    schema_definition: Dict[str, Any]
    tmdl_dataset: str
    tmdl_valid: bool
    validation_errors: List[str]
    current_retry: int
    dax_measures: Dict[str, Any]
    shadow_data: Dict[str, Any]
    pbir_layout: Dict[str, Any]
    final_output_path: str
```

### Pattern 2: Conditional Edge Routing

```python
def tmdl_route(state: PBIPState) -> str:
    """Conditional routing based on validation."""
    if not state.get("validation_errors"):
        return "dax_specialist"
    if state.get("current_retry", 0) >= 3:
        return "fail"
    return "tmdl_builder"
```

---

## Data Flow

```text
1. User provides prompt via CLI
   │
   ▼
2. Graph initiated with PBIPState
   │
   ▼
3. Requirement Analyst (Extracts entities/metrics)
   │
   ▼
4. Schema Mapper (Maps to YAML catalog)
   │
   ▼
5. TMDL Builder (Generates dataset structure)
   │
   ▼
6. TMDL Validator (Validates syntax -> Retry loop if invalid)
   │
   ▼
7. DAX Specialist (Generates measures)
   │
   ▼
8. Shadow Data Generator (Generates M expressions)
   │
   ▼
9. Layout Designer (Generates PBIR JSON)
   │
   ▼
10. PBIP Assembler (Writes files to disk)
```

---

## Testing Strategy

| Test Type | Scope | Files | Tools | Coverage Goal |
|-----------|-------|-------|-------|---------------|
| Unit | Agents | `test_agents.py` | pytest + responses mock | 80% |
| Unit | State Machine | `test_graph.py` | pytest | Validate routing logic |
| Integration | CLI | `test_integration.py` | typer.testing | Happy path E2E |

---

## Configuration

| Config Key | Type | Default | Description |
|------------|------|---------|-------------|
| `OPENROUTER_API_KEY` | string | `None` | API key for LLM calls |
| `OUTPUT_DIR` | string | `./output` | Where PBIP folders are created |
| `MAX_RETRIES` | int | `3` | Maximum retry loop count for validation |

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-04-25 | design-agent | Initial version with minimized chunking topology (3 chunks) |

---

## Next Step

**Ready for:** `/build .agents/sdd/features/DESIGN_PBI_MULTI_AGENT.md`
