# AgentSpec Development

> Spec-Driven Development framework for Data Engineering on Antigravity

---

## Project Context

**What is AgentSpec?** An Antigravity plugin that provides structured AI-assisted development through a 5-phase SDD workflow, specialized for data engineering with 63 agents, 34 commands, 25 KB domains, and 2 skills.

**Current Status:** v3.0.0 — Antigravity plugin distribution complete. Linear is the project tracker (source of truth).

---

## Orchestration Rules

These rules govern how Antigravity behaves in this workspace. They replace the need for a global `~/.gemini/GEMINI.md`.

### 1. Agent Invocation Disclosure (MANDATORY)

At the start of **EVERY** response, explicitly state which agent or role is handling the task:

```
> [!IMPORTANT]
> Invoking Specialist: [Agent Name] (Path: .agents/rules/[category]/[agent].md)
```

If no specialist matches, state:
```
> [!IMPORTANT]
> Invoking Specialist: Orchestrator (Direct)
> Reason: [why no specialist matched]
```

### 2. Automatic Agent Routing

1. **Identify Need:** The orchestrator identifies the need using the agent's `description` trigger (max 250 chars). When a task involves a specific domain, consult **`.agents/rules/routing.json`** for the matching specialist.
2. **Dynamic Discovery:** The orchestrator will automatically discover and hot-reload new or modified rule files in `.agents/rules/` without needing a manual `routing.json` update.
3. **Assign in Plan:** Every `implementation_plan.md` MUST include an **Agent Assignments** table mapping tasks to specialist agents.
4. **Just-In-Time Persona:** Before executing a specialist task:
   - Read the specialist's rule file at the path specified in `routing.json` or dynamically discovered.
   - Adopt its "Identity", "Resolution Order", and "Quality Gate"
   - Use its specific `kb_domains`
5. **Sequential Execution (Pipelines):** When a user requests a multi-step intent that maps to a pipeline in `routing.json` (e.g., `framework-migration`), the orchestrator MUST invoke the listed agents in the exact sequence, passing the output of the previous agent as context for the next.
6. **Judge Node (Agent Negotiation):** If a user intent is highly ambiguous and matches multiple specialists, act as the Judge Node. Request a brief "bid" or execution plan from the top 3 matching agents, then select the most appropriate agent to execute the task.

### 3. Middleware Stack Protocol

The Orchestrator MUST execute these middleware hooks automatically during the lifecycle of a task:
- **Pre-hook (Context Pruning):** Before passing a massive conversation context to an agent, invoke the `context-optimizer` to summarize conversational history older than 5 turns, explicitly retaining technical specs.
- **Pre-hook (Security):** Route all external/destructive operations through the `security-auditor` agent first.
- **Post-hook (Confidence Validator):** After an agent finishes its work, the orchestrator MUST intercept the response. If the agent's self-reported Confidence Score is below its Tier's Threshold (e.g., < 0.85 for T2), the orchestrator MUST pause and ask the user for confirmation before proceeding to the next agent or concluding the task.

### 4. Planning Protocol

- **Small tasks** (single file, quick fix): Execute directly.
- **Medium tasks** (2-5 files): Provide a brief plan, then execute.
- **Large tasks** (6+ files, new features): Generate `implementation_plan.md` with Agent Assignments table before executing.

### 4. KB-First Resolution

Every agent follows this mandatory knowledge resolution order:

```text
1. KB CHECK       Read .agents/kb/{domain}/index.md — scan headings only (~20 lines)
2. ON-DEMAND LOAD Read specific pattern/concept file matching the task (one file, not all)
3. TOOL FALLBACK  Single tool query if KB insufficient (max 3 tool calls per task)
4. CONFIDENCE     Calculate from Agreement Matrix (never self-assess)
```

#### Agreement Matrix

```text
                 | TOOL AGREES    | TOOL DISAGREES | TOOL SILENT    |
-----------------+----------------+----------------+----------------+
KB HAS PATTERN   | HIGH (0.95)    | CONFLICT(0.50) | MEDIUM (0.75)  |
                 | -> Execute     | -> Investigate | -> Proceed     |
-----------------+----------------+----------------+----------------+
KB SILENT        | TOOL-ONLY(0.85)| N/A            | LOW (0.50)     |
                 | -> Proceed     |                | -> Ask User    |
```

#### Impact Tiers

| Tier | Threshold | Action if Below | Examples |
|------|-----------|-----------------|----------|
| CRITICAL | 0.95 | REFUSE + explain | Schema migrations, production DDL, delete ops |
| IMPORTANT | 0.90 | ASK user first | Model creation, pipeline config, access control |
| STANDARD | 0.85 | PROCEED + caveat | Code generation, documentation |
| ADVISORY | 0.75 | PROCEED freely | Explanations, comparisons |

### 5. Execution Style

- Auto-execute safe commands without asking.
- For destructive operations, always confirm first.
- Prefer concise responses — summarize at the end.

### 6. Response Quality

- **Extreme Depth & Detail (MANDATORY):** Every output produced by Antigravity MUST be extensive, deep, and extremely detailed. Avoid "lazy" or "minimum viable" responses. Do NOT summarize or truncate technical explanations unless explicitly requested. Provide comprehensive reasoning, edge-case analysis, and detailed code implementations. If a task feels too large, break it down but maintain extreme depth in each part.
- Use Portuguese (pt-BR) when the user writes in Portuguese.
- Use English when the user writes in English.
- Always cite confidence and sources when using KB-First resolution.
- Format responses in GitHub-style markdown.

### 7. Stop Conditions

- **Ambiguity:** If intent is unclear, ASK — don't assume.
- **Destructive operations:** Always confirm before `DELETE`, `DROP`, `rm -rf`, `git push --force`.
- **Pre-flight Security Hook:** (Enforced via Middleware Stack).
- **Low confidence (<0.75):** (Enforced via Post-hook Confidence Validator).
- **No specialist match:** If no agent matches in `routing.json`, STOP and ask the user.
- **Context bloat:** Do not read all agent files at once. Read ONLY the one needed for the current task.

### 8. Build Workflow & Agent Instantiation

- **Contextual Specialization:** During the **Build Phase**, the Orchestrator MUST explicitly instantiate the relevant specialist agent and its rules into the active context for EVERY activity.
- **Rules Overrides:** The rules of the specialist agent take precedence over the general orchestrator rules for that specific activity.
- **Traceability:** Every activity in a build must start with the Invoking Specialist banner (`> [!IMPORTANT] Invoking Specialist: [Agent Name]`).

### 9. Telemetry Logging Protocol

To ensure framework observability, the Orchestrator MUST track the following for every task:
- **Agent Invoked:** The ID of the agent that handled the task.
- **Token Usage:** Estimated tokens consumed (Input/Output).
- **Execution Time:** Wall-clock time for the task.
- **Outcome:** Success, Failure, or User Interception.

Summary of telemetry SHOULD be saved to `.agents/reports/telemetry.jsonl` periodically or on task conclusion.

---

## Repository Structure

```text
sdd-for-antigravity/
├── GEMINI.md                # Main Antigravity context and system prompt
├── AGENTS.md                # Antigravity agent routing and escalation map
├── .agents/                 # Antigravity agent configuration
│   ├── rules/               # Agent entrypoints and templates
│   │   ├── default.md       # Antigravity default entrypoint baseline
│   │   ├── architect/       # 8 system-level design agents
│   │   ├── cloud/           # 10 AWS, GCP, cloud services, CI/CD
│   │   ├── platform/        # 6 Microsoft Fabric specialists
│   │   ├── python/          # 6 Python dev, code quality, prompts
│   │   ├── test/            # 3 testing, data quality, contracts
│   │   ├── data-engineering/ # 15 DE implementation specialists
│   │   ├── data-viz/         # 5 visualization specialists
│   │   ├── dev/             # 4 developer tools & productivity
│   │   └── workflow/        # 6 SDD phase agents
│   │
│   ├── commands/            # 34 slash commands
│   │   ├── workflow/        # SDD commands (7)
│   │   ├── data-engineering/ # DE commands (8)
│   │   ├── data-viz/         # Data visualization commands (4)
│   │   ├── core/            # Utility commands (5)
│   │   ├── knowledge/       # KB commands (1)
│   │   ├── review/          # Review commands (1)
│   │   └── visual-explainer/ # Visual documentation commands (8)
│   │
│   ├── skills/              # Reusable capability packs
│   │   ├── visual-explainer/ # HTML page generation
│   │   └── excalidraw-diagram/ # Excalidraw JSON generation
│   │
│   ├── sdd/                 # SDD framework
│   │   ├── architecture/    # WORKFLOW_CONTRACTS.yaml, ARCHITECTURE.md
│   │   ├── templates/       # 5 document templates (DE-aware)
│   │   ├── features/        # Active development
│   │   ├── reports/         # Build reports
│   │   └── archive/         # Shipped features
│   │
│   └── kb/                  # Knowledge Base (23 domains)
│       ├── _templates/      # 7 KB domain templates
│       ├── _index.yaml      # Domain registry
│       ├── dbt/             # dbt patterns and concepts
│       └── ...              # 22 other domains
│
├── docs/                    # Documentation
│   ├── getting-started/     # Installation and first pipeline
│   ├── concepts/            # SDD pillars through DE lens
│   ├── tutorials/           # dbt, star schema, Spark, streaming tutorials
│   └── reference/           # Full catalog: agents, commands, KB domains
│
├── CHANGELOG.md             # Version history
├── CONTRIBUTING.md          # Contribution guide
├── SECURITY.md              # Security policy
└── README.md                # Project overview
```

---

## Development Workflow

Use AgentSpec's own SDD workflow to develop AgentSpec on Antigravity:

```bash
# Explore an enhancement idea
/brainstorm "Add Judge layer for spec validation"

# Capture requirements
/define JUDGE_LAYER

# Design the architecture
/design JUDGE_LAYER

# Build it
/build JUDGE_LAYER

# Ship when complete
/ship JUDGE_LAYER
```

Data engineering example:

```bash
# Design a star schema
/schema "Star schema for e-commerce analytics"

# Scaffold a pipeline
/pipeline "Daily orders ETL from Postgres to Snowflake"

# Generate quality checks
/data-quality models/staging/stg_orders.sql
```

---

## Active Development Tasks

| Task | Status | Description |
|------|--------|-------------|
| Data engineering pivot | Done | 25 KB domains, 63 agents (9 categories), 34 commands |
| Adapt existing agents for DE | Done | code-reviewer, code-cleaner, test-generator, design, define, build |
| Adapt SDD templates for DE | Done | BRAINSTORM, DEFINE, DESIGN, BUILD_REPORT templates |
| Documentation overhaul | Done | Getting started, concepts, tutorials, reference, README |
| Migrate Claude to Antigravity | Active | Adapt CLAUDE.md to GEMINI.md, `.agents/rules/` and `AGENTS.md` |
| Create GEMINI.md.template | Pending | Template for user projects |
| Implement Judge layer | Planned | Spec validation via external LLM |
| Add telemetry | Planned | Local usage tracking |

---

## Coding Standards

### Markdown Files

- ATX-style headers (`#`, `##`, `###`)
- Fenced code blocks with language identifiers
- Tables properly aligned

### Agent Prompts

- Specific trigger conditions in the `description` field (max 250 chars)
- Clear capabilities list
- Concrete examples
- Defined output format
- `kb_domains` field for DE agents

### KB Domains

- `index.md` - Domain overview
- `quick-reference.md` - Cheat sheet
- `concepts/` - 3-6 concept files
- `patterns/` - 3-6 pattern files with code examples

---

## Commands Available

### SDD Workflow (7)

| Command | Purpose |
|---------|---------|
| `/brainstorm` | Explore ideas (Phase 0) |
| `/define` | Capture requirements (Phase 1) |
| `/design` | Create architecture (Phase 2) |
| `/build` | Execute implementation (Phase 3) |
| `/ship` | Archive completed work (Phase 4) |
| `/iterate` | Update existing docs (Cross-phase) |
| `/create-pr` | Create pull request |

### Data Engineering (8)

| Command | Purpose |
|---------|---------|
| `/pipeline` | DAG/pipeline scaffolding |
| `/schema` | Interactive schema design |
| `/data-quality` | Quality rules generation |
| `/lakehouse` | Table format + catalog guidance |
| `/sql-review` | SQL-specific code review |
| `/ai-pipeline` | RAG/embedding scaffolding |
| `/data-contract` | Contract authoring (ODCS) |
| `/migrate` | Legacy ETL migration |
| `/chart` | Chart type recommendation |
| `/dashboard` | Dashboard layout design |
| `/viz-code` | Visualization code generation |
| `/dataviz-story` | Data storytelling narrative |

### Core & Utilities (7)

| Command | Purpose |
|---------|---------|
| `/status` | Project status report |
| `/create-kb` | Create KB domain |
| `/review` | Code review |
| `/meeting` | Meeting transcript analysis |
| `/memory` | Save session insights |
| `/sync-context` | Update GEMINI.md |
| `/readme-maker` | Generate README |

### Visual Explainer (8)

| Command | Purpose |
|---------|---------|
| `/generate-web-diagram` | Standalone HTML diagram |
| `/generate-slides` | Magazine-quality slide deck as HTML |
| `/generate-visual-plan` | Visual implementation plan |
| `/diff-review` | Before/after architecture comparison |
| `/plan-review` | Current codebase vs. proposed plan |
| `/project-recap` | Project state and cognitive debt |
| `/fact-check` | Verify document accuracy against codebase |
| `/share` | Share HTML page via Vercel |

---

## Key Files to Know

| File | Purpose |
|------|---------|
| `GEMINI.md` | Primary Antigravity system prompt and context |
| `AGENTS.md` | Agent routing, categories, and escalation map |
| `.agents/rules/default.md` | Baseline template/entrypoint for Antigravity agents |
| `.agents/sdd/architecture/WORKFLOW_CONTRACTS.yaml` | Phase transition rules |
| `.agents/sdd/templates/*.md` | Document templates (DE-aware) |
| `.agents/kb/_templates/*.template` | KB domain templates |
| `.agents/kb/_index.yaml` | KB domain registry (25 domains) |
| `.agents/rules/data-engineering/` | DE implementation specialists |
| `.agents/rules/data-viz/` | Data visualization specialists |
| `.agents/rules/architect/` | System-level design agents (schema, pipeline, lakehouse) |
| `.agents/rules/cloud/` | AWS, GCP, CI/CD, deployment agents |
| `.agents/rules/platform/` | Microsoft Fabric specialists |
| `.agents/rules/python/` | Python dev, code quality, prompt engineering |
| `.agents/rules/test/` | Testing, data quality, data contracts |
| `.agents/rules/dev/` | Prompt crafter, codebase explorer, shell scripts, meeting analyst |
| `.agents/skills/visual-explainer/` | HTML generation skill (templates, CSS patterns, scripts) |
| `.agents/skills/excalidraw-diagram/` | Excalidraw JSON generation skill |

---

## Version

- **Version:** 3.0.0 (Antigravity Migration)
- **Status:** Release
- **Last Updated:** 2026-04-23
