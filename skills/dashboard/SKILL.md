---
name: dashboard
description: Dashboard layout and composition design — delegates to dashboard-designer (escalates to power-bi-developer for DAX)
---

# Dashboard Command

> Design the layout, visual hierarchy, and structure of a dashboard before building it

## Usage

```bash
/dashboard <description-or-requirements>
```

## Examples

```bash
/dashboard "Power BI sales dashboard with filters by date, region, and product"
/dashboard "Evidence.dev page for monthly marketing metrics — CMO audience"
/dashboard "Tableau executive summary: 3 KPIs + trend + regional breakdown"
/dashboard requirements/dashboard-spec.md
```

---

## What This Command Does

1. Invokes the **dashboard-designer** agent
2. Analyzes your platform, audience, and metric requirements
3. Loads KB patterns from `dataviz` and `modern-stack` domains
4. Produces:
   - Page structure (rows, sections, visual list)
   - Filter hierarchy (global / page / visual level)
   - Visual type recommendations per section
   - Escalation notes for DAX measures (Power BI) or SQL blocks (Evidence.dev)

## Agent Delegation

| Agent | Role |
|-------|------|
| `dashboard-designer` | Primary — layout, composition, visual hierarchy |
| `power-bi-developer` | Escalation — DAX measures, semantic model, RLS |
| `viz-code-generator` | Escalation — Evidence.dev components or chart code |
| `chart-architect` | Escalation — chart type selection for individual visuals |

## KB Domains Used

- `dataviz` — dashboard-composition principles, platform patterns
- `modern-stack` — Evidence.dev project structure and components

## Output

A text-based wireframe and visual list with escalation notes. Use `/viz-code` for implementation and `/chart` for individual chart type decisions.
