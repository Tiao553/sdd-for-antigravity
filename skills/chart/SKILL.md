---
name: chart
description: Chart type recommendation — delegates to chart-architect agent
---

# Chart Command

> Get the right chart type for your data before writing a single line of code

## Usage

```bash
/chart <data-description-or-question>
```

## Examples

```bash
/chart "monthly revenue over 2 years, want to show growth trend"
/chart "market share across 8 product segments"
/chart "correlation between ad spend and conversions"
/chart "sales funnel from lead to close — 5 stages"
```

---

## What This Command Does

1. Invokes the **chart-architect** agent
2. Analyzes the data relationship you want to show (trend, comparison, composition, distribution, flow, correlation)
3. Loads KB patterns from the `dataviz` domain
4. Produces:
   - Recommended chart type with rationale
   - Alternatives considered and why rejected
   - Required data shape (columns, aggregations)
   - Suggested chart title (conclusion, not description)
   - Next step: suggested `/viz-code` invocation

## Agent Delegation

| Agent | Role |
|-------|------|
| `chart-architect` | Primary — chart type selection |
| `viz-code-generator` | Escalation — when user wants implementation code |

## KB Domains Used

- `dataviz` — chart-selection decision tree, anti-patterns

## Output

A chart recommendation with rationale, not code. Use `/viz-code` after this to generate implementation.
