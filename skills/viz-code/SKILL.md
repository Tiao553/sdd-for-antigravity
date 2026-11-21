---
name: viz-code
description: Visualization code generation — delegates to viz-code-generator agent
---

# Viz Code Command

> Generate production-ready chart code for Plotly, ECharts, Evidence.dev, or Vega-Altair

## Usage

```bash
/viz-code <library> <chart-type> <data-description>
```

## Examples

```bash
/viz-code plotly "grouped bar chart — monthly sales by region, data in DataFrame with columns: month, region, revenue"
/viz-code echarts "line chart with area fill — daily active users over 90 days"
/viz-code evidence "bar chart + trend line — weekly orders, Evidence.dev page connected to Postgres"
/viz-code vega-altair "scatter plot with interactive brush selection — ad_spend vs conversions by campaign"
```

---

## What This Command Does

1. Invokes the **viz-code-generator** agent
2. Confirms data shape and target library
3. Loads KB patterns from `dataviz`, `modern-stack`, and `sql-patterns` domains
4. Generates:
   - Complete, runnable code with imports
   - Theming and layout configuration
   - How to run or render the output
   - One optional customization tip (interactivity, export, theming)

## Agent Delegation

| Agent | Role |
|-------|------|
| `viz-code-generator` | Primary — chart code generation |
| `chart-architect` | Escalation — if chart type is uncertain |
| `storytelling-analyst` | Escalation — if narrative/annotations are needed |

## KB Domains Used

- `dataviz` — plotly, echarts, evidence-dev, vega-altair patterns
- `modern-stack` — Evidence.dev project setup and DuckDB integration
- `sql-patterns` — SQL for Evidence.dev query blocks

## Output

Complete, runnable code for the specified library. Use `/chart` first if unsure which chart type to use.
