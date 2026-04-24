---
name: dataviz-story
description: Data storytelling and narrative generation — delegates to storytelling-analyst agent
---

# Dataviz Story Command

> Transform data summaries and charts into structured narratives with insights and annotations

## Usage

```bash
/dataviz-story <data-summary-or-chart-description>
```

## Examples

```bash
/dataviz-story "Revenue dropped 18% in March after growing 8% MoM for 6 months — need exec narrative"
/dataviz-story "Line chart showing churn acceleration — need title, annotation text, and slide bullets"
/dataviz-story "Sales by region dashboard — Southeast underperforming vs target, build the story"
/dataviz-story metrics/q1-summary.md
```

---

## What This Command Does

1. Invokes the **storytelling-analyst** agent
2. Extracts the key insight and structures it using the SCR framework
3. Loads KB patterns from the `dataviz` domain
4. Produces:
   - SCR narrative (Situation / Complication / Resolution)
   - Chart annotation package (title, subtitle, callout, footer)
   - Slide bullets (lead with the number, cause, implication)
   - "So what" framing for the audience

## Agent Delegation

| Agent | Role |
|-------|------|
| `storytelling-analyst` | Primary — narrative, annotations, insight extraction |
| `viz-code-generator` | Escalation — if chart code is also needed |
| `chart-architect` | Escalation — if chart type selection is still open |

## KB Domains Used

- `dataviz` — data-storytelling concepts (SCR, progressive disclosure, anti-patterns)

## Output

Text artifacts: narrative structure, chart title, annotation text, and slide bullets. Does not generate code — use `/viz-code` for that.
