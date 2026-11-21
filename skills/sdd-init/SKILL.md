---
name: sdd-init
description: Initialize AgentSpec Spec-Driven Development (SDD) directory structure, document templates, and gitkeep files in the current workspace.
---

# SDD Init Skill (`/sdd-init`)

> **Workspace Bootstrapper** — Prepares any data engineering repository for AgentSpec's 5-phase SDD workflow.

---

## 1. Purpose & Overview

When working with AgentSpec as a global Antigravity plugin, you frequently open diverse client or internal data repositories (dbt projects, Spark repos, Dagster/Airflow DAG directories). 

The `/sdd-init` skill sets up the local governance infrastructure inside the target repository without needing manual directory creation. It initializes:
- `.agents/sdd/features/` — Staging ground for Phase 0 (`/brainstorm`), Phase 1 (`/define`), and Phase 2 (`/design`).
- `.agents/sdd/reports/` — Storage for Phase 3 (`BUILD_REPORT`) and Phase 3.5 (`VALIDATION_REPORT`).
- `.agents/sdd/archive/` — Historical immutable record for Phase 4 (`/ship`).
- `.agents/sdd/templates/` — Standardized templates for specifications, reports, runbooks, and roadmaps.

---

## 2. Usage

```bash
/sdd-init
```

### Options & Flags
- `/sdd-init --with-docs`: Also creates a `docs/architecture/` folder with starter architecture diagrams.
- `/sdd-init --force`: Overwrites existing templates if they have been updated in the global plugin.

---

## 3. Scaffolding Blueprint

Running `/sdd-init` creates the following directory structure in the current workspace root:

```text
<workspace-root>/
└── .agents/
    └── sdd/
        ├── features/
        │   └── .gitkeep
        ├── reports/
        │   └── .gitkeep
        ├── archive/
        │   └── .gitkeep
        └── templates/
            ├── BRAINSTORM_TEMPLATE.md
            ├── DEFINE_TEMPLATE.md
            ├── DESIGN_TEMPLATE.md
            ├── BUILD_REPORT_TEMPLATE.md
            ├── VALIDATION_REPORT_TEMPLATE.md
            ├── RUNBOOK_TEMPLATE.md
            └── ROADMAP_TEMPLATE.md
```

---

## 4. Execution Logic & Safety Guardrails

1. **Workspace Root Detection:** The skill inspects the active project root (searching for `.git`, `pyproject.toml`, `dbt_project.yml`, or workspace anchor).
2. **Non-Destructive Guarantee:** If `.agents/sdd/features/` already exists with active feature documents, `/sdd-init` **never** deletes or overwrites existing feature specs.
3. **Template Sync:** Copies the latest validated markdown templates from the plugin's `sdd/templates/` directory into the local workspace.
4. **Git Hygiene:** Places `.gitkeep` in empty folders so version control tracks the SDD directories even before the first spec is committed.

---

## 5. Next Steps After Initialization

Once initialized, start your development lifecycle:
1. **Phase 0:** `/brainstorm "Real-time fraud detection pipeline with PySpark"`
2. **Phase 1:** `/define FRAUD_DETECTION`
3. **Phase 2:** `/design FRAUD_DETECTION`
4. **Phase 3:** `/build FRAUD_DETECTION`
5. **Phase 3.5:** `/validate FRAUD_DETECTION`
6. **Phase 4:** `/ship FRAUD_DETECTION`
