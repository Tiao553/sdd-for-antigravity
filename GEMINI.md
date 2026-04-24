# AgentSpec Development

> Spec-Driven Development framework for Data Engineering on Antigravity

---

## Project Context

**What is AgentSpec?** An Antigravity plugin that provides structured AI-assisted development through a 5-phase SDD workflow, specialized for data engineering with 63 agents, 34 commands, 25 KB domains, and 2 skills.

**Current Status:** v3.0.0 — Antigravity plugin distribution complete. Linear is the project tracker (source of truth).

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

- Specific trigger conditions
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
