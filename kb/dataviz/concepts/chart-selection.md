# Chart Selection

## Decision Framework

Chart selection follows four questions in order:

1. **What is the data type?** — categorical, temporal, quantitative, relational
2. **What relationship do you want to show?** — comparison, trend, distribution, composition, flow, correlation
3. **Who is the audience?** — executive (simple), analyst (detailed), technical (dense)
4. **What is the medium?** — dashboard, slide, notebook, report

## By Relationship

### Comparison
- **Bar chart** — compare values across discrete categories; horizontal when labels are long
- **Bullet chart** — compare actual vs target for a single metric
- **Grouped bar** — compare subcategories side-by-side
- Avoid pie charts for comparison; humans judge angles poorly

### Trend Over Time
- **Line chart** — default for time series; use for continuous data
- **Area chart** — emphasize magnitude, not just direction; stacked area for composition over time
- **Slope chart** — compare two time points across multiple series
- Use consistent date granularity on the X axis

### Distribution
- **Histogram** — frequency of a single continuous variable
- **Box plot** — median, quartiles, outliers; good for comparing distributions
- **Violin plot** — richer distribution shape than box plot
- Avoid bar charts for distributions; they hide shape

### Composition (Part-of-whole)
- **Pie chart** — only when ≤5 categories and proportions matter more than values
- **Treemap** — when many categories and hierarchy exists
- **Stacked bar** — composition change over time or across categories
- **Waterfall** — show how components add up to a total

### Correlation
- **Scatter plot** — relationship between two quantitative variables
- **Bubble chart** — scatter with a third quantitative dimension (size)
- **Heatmap** — correlation matrix or cross-tab frequency

### Flow
- **Sankey diagram** — flows between nodes with magnitude
- **Funnel chart** — conversion steps (sales pipeline, user onboarding)

## When NOT to Use

| Chart | Avoid when |
|-------|-----------|
| Pie | More than 5 categories, need to compare absolute values |
| 3D charts | Always — depth distorts perception |
| Dual Y-axis | Audiences can misread scale; prefer two charts |
| Radar/Spider | More than 6 variables; hard to read accurately |
| Gauge | When trend or comparison matters more than current value |

## Escalation

If the user asks for code after chart selection → hand off to `viz-code-generator`.
