# Power BI DAX

## Evaluation Contexts

DAX operates in two contexts that every measure must account for:

- **Filter context** — the active filters on the report canvas (slicers, visual filters, row context from a table)
- **Row context** — exists inside calculated columns and iterator functions (SUMX, AVERAGEX); iterates row by row

`CALCULATE` is the only function that can **transition** row context into filter context.

## Core Functions

### CALCULATE
```dax
-- Override filter context
Sales North = CALCULATE([Total Sales], Region[Name] = "North")

-- Remove a dimension's filter
Sales All Regions = CALCULATE([Total Sales], ALL(Region))

-- Multiple filters combined (AND logic)
Sales North 2024 = CALCULATE([Total Sales], Region[Name] = "North", 'Date'[Year] = 2024)
```

### FILTER vs ALL
```dax
-- FILTER: returns a table of rows matching condition (use when you need row-by-row logic)
High Value Sales = CALCULATE([Total Sales], FILTER(Orders, Orders[Amount] > 1000))

-- ALL: removes filters from a column or table
Market Share = DIVIDE([Total Sales], CALCULATE([Total Sales], ALL(Orders)))

-- ALLEXCEPT: keep only specified column filters
Sales by Region = CALCULATE([Total Sales], ALLEXCEPT(Region, Region[Name]))
```

### Time Intelligence
```dax
-- Year-to-date (requires a marked Date table)
Sales YTD = TOTALYTD([Total Sales], 'Date'[Date])

-- Prior year same period
Sales PY = CALCULATE([Total Sales], SAMEPERIODLASTYEAR('Date'[Date]))

-- Year-over-year growth %
YoY % = DIVIDE([Total Sales] - [Sales PY], [Sales PY])

-- Rolling 3 months
Sales 3M = CALCULATE([Total Sales], DATESINPERIOD('Date'[Date], LASTDATE('Date'[Date]), -3, MONTH))
```

## Measures vs Calculated Columns

| | Measure | Calculated Column |
|--|---------|------------------|
| Evaluated | At query time (dynamic) | At refresh time (static) |
| Context | Respects filter context | Row context only |
| Storage | No storage cost | Adds to model size |
| Use for | KPIs, aggregations | Row-level flags, text concat, lookups |

## Date Table Requirements
Time intelligence functions require a **dedicated Date table** marked as such:
- Contiguous date range (no gaps)
- One row per day
- Marked via: `Table Tools > Mark as Date Table`
- Relate to fact tables via the date key

## Variables in DAX
```dax
YoY Growth =
VAR CurrentSales = [Total Sales]
VAR PriorSales = CALCULATE([Total Sales], SAMEPERIODLASTYEAR('Date'[Date]))
VAR Growth = DIVIDE(CurrentSales - PriorSales, PriorSales)
RETURN Growth
```
Variables improve readability and avoid recalculation.

## Common Mistakes
- Using `FILTER` when `ALL`/`CALCULATETABLE` is cleaner
- Forgetting to mark the Date table (breaks all time intelligence)
- Bidirectional relationships causing ambiguous filter paths
- Calculated columns when a measure would do (bloats model)
