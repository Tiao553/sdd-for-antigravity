# Data Visualization Commands

> Four commands covering the full dataviz workflow: chart selection → code generation → dashboard design → storytelling

## Commands

| Command | Agent | Purpose |
|---------|-------|---------|
| `/chart` | `chart-architect` | Recommend the right chart type before writing code |
| `/dashboard` | `dashboard-designer` | Design dashboard layout, visual hierarchy, and page structure |
| `/viz-code` | `viz-code-generator` | Generate code for Plotly, ECharts, Evidence.dev, or Vega-Altair |
| `/dataviz-story` | `storytelling-analyst` | Create SCR narrative, chart titles, and annotation text |

## Typical Workflow

```bash
# 1. Decide what chart to use
/chart "monthly revenue over 2 years, want to show growth trend"

# 2. Generate the code
/viz-code plotly "line chart — month on x, revenue on y"

# 3. Write the narrative
/dataviz-story "Revenue grew 23% YoY — need exec narrative and chart annotations"

# 4. Design a full dashboard
/dashboard "Power BI sales dashboard — date filter, regional breakdown, KPIs"
```

## Agents Used

| Agent | Tier | Specialty |
|-------|------|-----------|
| `chart-architect` | T1 | Chart type selection via decision tree |
| `dashboard-designer` | T2 | Multi-platform layout and composition |
| `power-bi-developer` | T2 | DAX, semantic model, RLS (sub-agent of dashboard-designer) |
| `viz-code-generator` | T2 | Plotly, ECharts, Evidence.dev, Vega-Altair code |
| `storytelling-analyst` | T2 | SCR narrative, annotations, insight bullets |
