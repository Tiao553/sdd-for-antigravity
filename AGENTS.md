# AgentSpec Agents (Antigravity Migration)

AgentSpec deploys **63 specialized agents** across **8 categories**, each built on a **three-tier template system** with mandatory **KB-First knowledge resolution**. Every agent carries a cognitive framework that enforces structured confidence scoring, provenance tracking, and explicit stop conditions -- turning raw LLM capability into disciplined, auditable domain expertise.

`63 agents | 8 categories | 3 tiers (T1/T2/T3) | 25 KB domains | 100% template compliance`

---

## How Agents Work (Cognitive Architecture)

AgentSpec agents are not raw LLM prompts. They operate through a three-layer cognitive architecture that separates routing, reasoning, and domain knowledge.

### Layer 1: Antigravity Orchestrator (Router)

The orchestrator is Antigravity itself. It reads all 58 agent description fields from frontmatter, pattern-matches user messages to agent capabilities, and launches the best-fit agent. The orchestrator:

- Maintains memory, tasks, and plans across messages
- Selects agents based on trigger phrases, file types, and context
- Receives structured responses with confidence scores
- Is a **generalist** -- it knows WHO to call, not HOW to do the work

### Layer 2: Agent Template (Cognitive Framework)

Every agent inherits from `.agents/rules/default.md`, which defines structured thinking:

- **KB-First Resolution** -- check local knowledge before external sources
- **Agreement Matrix** -- structured confidence scoring (KB vs Tool alignment)
- **Impact Tiers** -- CRITICAL/IMPORTANT/STANDARD/ADVISORY with thresholds
- **Stop Conditions** -- agents know when to REFUSE or ESCALATE
- **Provenance** -- every response cites confidence score and sources

### Layer 3: Agent Instance (Domain Specialist)

Each agent adds domain-specific knowledge, capabilities, quality gates, and anti-patterns on top of the template framework. This layer carries the expertise -- dbt, Spark, Fabric, Airflow, and so on.

### Request Flow

```text
User
  |
  v
Orchestrator (Antigravity)
  |-- reads agent descriptions from `.agents/rules/`
  |-- pattern-matches message to capabilities
  |-- selects best-fit agent
  v
Agent Instance
  |-- KB-First: read .agents/kb/{domain}/
  |-- Agreement Matrix: calculate confidence
  |-- Impact Tier: check threshold for task type
  |-- Execute (confidence met) or Stop (below threshold)
  v
Response with Provenance
  |-- confidence score
  |-- sources cited (KB file, Tool query, codebase path)
```

---

## Agent Tiers (T1 / T2 / T3)

Every agent declares a tier in frontmatter (`tier: T1|T2|T3`). The tier governs which template sections are required and sets a line budget.

| Tier | Name | Lines | Use For |
|------|------|-------|---------|
| **T1** | Utility | 80-150 | Single-purpose tools, orchestrators, lightweight helpers |
| **T2** | Domain Expert | 150-350 | Domain specialists with KB domains, complex decision-making |
| **T3** | Platform Specialist | 350-600 | Agents with tool dependencies, live instance access, deep platform expertise |

### Section-by-Tier Matrix

| Section | T1 | T2 | T3 |
|---------|:--:|:--:|:--:|
| Identity | Required | Required | Required |
| Knowledge Resolution | Compact | Full + Agreement Matrix | Full + Sources + Decision Tree |
| Capabilities | 2-4 | 3-5 | 3-6 |
| Constraints | -- | Required | Required |
| Stop Conditions | -- | Required | Required |
| Quality Gate | 3-5 items | 5-8 items | Multi-section |
| Response Format | Single | Standard + Below-threshold | 4-tier (high/medium/low/conflict) |
| Anti-Patterns | 3-5 rows | 5+ rows + Warning Signs | Full + Warning Signs |
| Error Recovery | -- | -- | Required |
| Extension Points | -- | -- | Required |
| Changelog | -- | -- | Required |
| Remember | Required | Required | Required |

### Current Distribution

- **T1 (11 agents):** genai-architect, medallion-architect, aws-data-architect, gcp-data-architect, ai-prompt-specialist, python-developer, lakeflow-specialist, spark-performance-analyzer, spark-troubleshooter, prompt-crafter, chart-architect
- **T2 (32 agents):** data-platform-engineer, kb-architect, lakehouse-architect, pipeline-architect, schema-designer, the-planner, ai-data-engineer-gcp, code-cleaner, code-documenter, code-reviewer, data-contracts-engineer, data-quality-analyst, test-generator, ai-data-engineer, dbt-specialist, spark-engineer, spark-specialist, sql-optimizer, streaming-engineer, codebase-explorer, meeting-analyst, shell-script-specialist, brainstorm-agent, build-agent, define-agent, design-agent, iterate-agent, ship-agent, dashboard-designer, power-bi-developer, storytelling-analyst, viz-code-generator
- **T3 (20 agents):** ai-data-engineer-cloud, ai-prompt-specialist-gcp, aws-deployer, aws-lambda-architect, ci-cd-specialist, lambda-builder, supabase-specialist, fabric-ai-specialist, fabric-architect, fabric-cicd-specialist, fabric-logging-specialist, fabric-pipeline-developer, fabric-security-specialist, llm-specialist, airflow-specialist, lakeflow-architect, lakeflow-expert, lakeflow-pipeline-builder, qdrant-specialist, spark-streaming-architect

---

## Core Principle: KB-First Resolution

Every agent follows this mandatory knowledge resolution order. Agents that skip KB and go straight to execution tools are violating the architecture.

### Resolution Order

```text
1. KB CHECK       Read .agents/kb/{domain}/index.md -- scan headings only (~20 lines)
2. ON-DEMAND LOAD Read specific pattern/concept file matching the task (one file, not all)
3. TOOL FALLBACK  Single tool query if KB insufficient (max 3 tool calls per task)
4. CONFIDENCE     Calculate from Agreement Matrix (never self-assess)
```

### Agreement Matrix

```text
                 | TOOL AGREES    | TOOL DISAGREES | TOOL SILENT    |
-----------------+----------------+----------------+----------------+
KB HAS PATTERN   | HIGH (0.95)    | CONFLICT(0.50) | MEDIUM (0.75)  |
                 | -> Execute     | -> Investigate | -> Proceed     |
-----------------+----------------+----------------+----------------+
KB SILENT        | TOOL-ONLY(0.85)| N/A            | LOW (0.50)     |
                 | -> Proceed     |                | -> Ask User    |
```

### Impact Tiers

| Tier | Threshold | Action if Below | Examples |
|------|-----------|-----------------|----------|
| CRITICAL | 0.95 | REFUSE + explain | Schema migrations, production DDL, delete ops |
| IMPORTANT | 0.90 | ASK user first | Model creation, pipeline config, access control |
| STANDARD | 0.85 | PROCEED + caveat | Code generation, documentation |
| ADVISORY | 0.75 | PROCEED freely | Explanations, comparisons |

---

## Agent Categories

*(See complete list in full documentation. Core categories map across 8 domains: Architect, Cloud, Platform, Python, Test, Data Engineering, Dev, and Workflow).*

---

## Escalation Map

Agents are not isolated. When a task crosses domain boundaries, agents escalate to the appropriate specialist.

```text
Workflow <-> Data Engineering:
  build-agent -> dbt-specialist, spark-engineer, pipeline-architect
  design-agent -> schema-designer, pipeline-architect
  define-agent -> data-contracts-engineer, data-quality-analyst

Python <-> Data Engineering:
  code-reviewer -> sql-optimizer, data-quality-analyst
  test-generator -> data-quality-analyst, dbt-specialist

Data Engineering <-> Data Engineering:
  dbt-specialist <-> spark-engineer
  pipeline-architect <-> streaming-engineer
  lakehouse-architect <-> data-platform-engineer

Cloud <-> Data Engineering:
  aws-data-architect -> pipeline-architect, spark-engineer
  fabric-architect -> medallion-architect, lakehouse-architect

Architect <-> Data Engineering:
  genai-architect -> ai-data-engineer, streaming-engineer

Dev <-> All:
  prompt-crafter -> any agent
  codebase-explorer -> python-developer, pipeline-architect
```

---

## Creating Custom Agents

### Step-by-Step

1. **Check the "When NOT to Create" criteria**
2. **Choose a tier** -- T1 for simple tools, T2 for domain experts, T3 for platform specialists
3. **Copy `.agents/rules/default.md`** to the appropriate category folder
4. **Fill in frontmatter** -- all required fields for your tier
5. **Write sections** required for your tier
6. **Place in the correct category folder**
7. **Verify compliance**

### Frontmatter Schema

**Required (all tiers):**

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Agent identifier (kebab-case, matches filename) |
| `description` | string (max 250 chars) | Activation trigger for Model Decision mode ("Apply this rule when...") |
| `tools` | list | Available tools |
| `kb_domains` | list | KB domains this agent reads (empty `[]` if none) |
| `color` | string | UI color |
| `tier` | string | T1, T2, or T3 |

**Required for T2+ only:**

| Field | Type | Description |
|-------|------|-------------|
| `stop_conditions` | list | Conditions that cause the agent to halt or refuse |
| `escalation_rules` | list | Trigger/target/reason rules for cross-agent routing |

---

## Template Reference

All Antigravity agents inherit from `.agents/rules/default.md`. The template defines 12 sections:

| # | Section | Purpose |
|---|---------|---------|
| 1 | **Frontmatter** | Name, description, tools, KB domains, tier, color |
| 2 | **Identity** | Purpose, domain, threshold |
| 3 | **Knowledge Resolution** | KB-First order, Agreement Matrix, Sources |
| 4 | **Capabilities** | When/Process/Output for each capability |
| 5 | **Constraints** | Domain boundaries and resource limits |
| 6 | **Stop Conditions** | Hard stops, escalation rules, retry limits |
| 7 | **Quality Gate** | Pre-flight checklist scaled to tier |
| 8 | **Response Format** | Standard + below-threshold + conflict/low-confidence |
| 9 | **Anti-Patterns** | Never Do / Why / Instead table + Warning Signs |
| 10 | **Error Recovery** | Error/recovery/fallback table |
| 11 | **Extension Points** | How to extend capabilities, KB, Tools |
| 12 | **Remember** | Motto, mission, core principle |
