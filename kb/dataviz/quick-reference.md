# Dataviz Quick Reference

## Chart Type Decision Tree

| Data relationship | Best chart |
|-------------------|-----------|
| Comparison across categories | Bar / Column |
| Trend over time | Line / Area |
| Part-of-whole | Pie (≤5 slices), Treemap (many), Stacked bar |
| Distribution | Histogram, Box plot, Violin |
| Correlation between two metrics | Scatter plot |
| Flow / Sankey | Sankey, Alluvial |
| Geo / spatial | Choropleth, Bubble map |
| Single KPI vs target | Gauge, Bullet chart |
| Many metrics at once | Radar / Spider (use sparingly) |

## Library Comparison

| Concern | Plotly | ECharts | Vega-Altair | Evidence.dev |
|---------|--------|---------|-------------|--------------|
| Language | Python / React | JavaScript | Python | Markdown + SQL |
| Interactivity | High | High | Medium | Medium |
| Learning curve | Low (`px`) | Medium | Medium | Low |
| Best for | Notebooks, Dash apps | Web dashboards | Research, publications | SQL-first analytics |
| Theming | `update_layout` | `theme` object | `alt.themes` | CSS variables |

## Power BI DAX Quick Lookup

| Pattern | DAX |
|---------|-----|
| Basic measure | `Sales = SUM(Orders[Amount])` |
| Filter override | `CALCULATE([Sales], Region[Name] = "North")` |
| Remove all filters | `CALCULATE([Sales], ALL(Orders))` |
| YTD | `TOTALYTD([Sales], 'Date'[Date])` |
| Prior year | `CALCULATE([Sales], SAMEPERIODLASTYEAR('Date'[Date]))` |
| % of total | `DIVIDE([Sales], CALCULATE([Sales], ALL(Orders)))` |

## Evidence.dev Component Cheat Sheet

```markdown
```sql orders
SELECT month, SUM(revenue) AS revenue FROM sales GROUP BY 1
```

<LineChart data={orders} x=month y=revenue />
<BarChart data={orders} x=month y=revenue />
<DataTable data={orders} />
<BigValue data={orders} value=revenue />
```

## Storytelling Structure (SCR)
1. **Situation** — What is the context?
2. **Complication** — What changed or is wrong?
3. **Resolution** — What should happen next?
