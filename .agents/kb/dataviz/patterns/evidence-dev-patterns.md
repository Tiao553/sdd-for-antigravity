# Evidence.dev Patterns

## Chart Components

Evidence.dev components consume a named SQL query result via `data={queryName}`.

```markdown
```sql monthly_revenue
SELECT 
  date_trunc('month', order_date) AS month,
  SUM(revenue)                    AS revenue,
  COUNT(*)                        AS orders
FROM orders
GROUP BY 1
ORDER BY 1
```

<LineChart data={monthly_revenue} x=month y=revenue title="Revenue Trend" />
<BarChart  data={monthly_revenue} x=month y=orders />
<DataTable data={monthly_revenue} />
```

## Common Component Props

### LineChart / BarChart / AreaChart
```markdown
<LineChart
  data={query_name}
  x=column_name
  y=column_name
  series=group_column      <!-- creates one line per group value -->
  title="Chart title"
  yAxisTitle="Revenue (USD)"
  yFmt=usd                 <!-- formatting: usd, pct, num, comma -->
  colorPalette={["#4e79a7","#f28e2b","#e15759"]}
/>
```

### BigValue (KPI card)
```markdown
<BigValue
  data={summary}
  value=total_revenue
  title="Total Revenue"
  fmt=usd
  comparison=prev_revenue
  comparisonTitle="vs last period"
/>
```

### DataTable with column formatting
```markdown
<DataTable data={orders} rows=20>
  <Column id=order_date fmt=date />
  <Column id=revenue fmt=usd align=right />
  <Column id=status contentType=colorscale />
</DataTable>
```

### ScatterPlot
```markdown
<ScatterPlot data={customers} x=ltv y=orders size=revenue series=segment />
```

## SQL Block Patterns

### Parameterized queries (inputs)
```markdown
<DateRangePicker name=date_range />

```sql filtered_sales
SELECT * FROM sales
WHERE order_date BETWEEN '${inputs.date_range.start}' AND '${inputs.date_range.end}'
```
```

### DuckDB local file
```markdown
```sql products
SELECT * FROM read_parquet('./sources/products.parquet')
```
```

### Aggregation with window function
```markdown
```sql running_total
SELECT
  order_date,
  SUM(revenue)                              AS daily_revenue,
  SUM(SUM(revenue)) OVER (ORDER BY order_date) AS cumulative_revenue
FROM orders
GROUP BY 1
ORDER BY 1
```
```

## Layout Components

```markdown
<Grid cols=3>
  <BigValue data={kpis} value=revenue title="Revenue" />
  <BigValue data={kpis} value=orders  title="Orders" />
  <BigValue data={kpis} value=aov     title="Avg Order Value" />
</Grid>

<Details title="Show detail table">
  <DataTable data={orders} />
</Details>
```

## Notes
- SQL blocks run at build time (static site) unless using a live database connection
- Component props use `=` not `=""` for column references; use `""` only for literal strings
- See `modern-stack` KB for full project setup, DuckDB integration, and deployment
