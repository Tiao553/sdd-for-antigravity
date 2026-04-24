# Power BI Data Model Patterns

## Star Schema in Power BI

Apply dimensional modeling principles inside the Power BI semantic model:

```
         DimDate ──────┐
         DimProduct ───┤
         DimCustomer ──┼── FactSales (grain: one row per order line)
         DimRegion ────┘
```

- **Single-direction relationships** — filter flows from dimension to fact only
- **Integer surrogate keys** — use int keys, not natural string keys, for join performance
- **One active relationship per table pair** — use `USERELATIONSHIP()` in DAX for inactive paths

## Date Table Best Practices

```dax
-- Calculated table (simple, no Power Query needed)
DateTable =
ADDCOLUMNS(
    CALENDAR(DATE(2020,1,1), DATE(2026,12,31)),
    "Year",        YEAR([Date]),
    "Quarter",     "Q" & QUARTER([Date]),
    "Month",       FORMAT([Date], "MMM YYYY"),
    "MonthNumber", MONTH([Date]),
    "Weekday",     FORMAT([Date], "dddd"),
    "IsWeekend",   WEEKDAY([Date], 2) >= 6
)
```

Mark the table as a Date table via `Table Tools > Mark as Date Table > Date column`.

## Role-Playing Dimensions

When a fact table has multiple date foreign keys (order date, ship date, delivery date):

```dax
-- Create separate inactive relationships, activate per measure
Ship Date Sales = CALCULATE([Total Sales], USERELATIONSHIP(FactSales[ShipDate], DateTable[Date]))
```

## Avoiding Bidirectional Relationships

Bidirectional relationships cause ambiguous filter paths and unexpected results. Use them only for:
- Many-to-many bridge tables
- Role-playing workarounds where CROSSFILTER is explicitly needed

Prefer `CROSSFILTER()` in DAX over model-level bidirectional when possible.

## Row-Level Security (RLS)

```dax
-- Static RLS role: "North Region Only"
-- Table: DimRegion, Filter expression:
[RegionName] = "North"

-- Dynamic RLS (user-based)
-- Table: DimEmployee, Filter expression:
[Email] = USERPRINCIPALNAME()
```

Assign roles via `Modeling > Manage Roles`. Test with `View as role`.

## Calculated Table for Bridge (Many-to-Many)

```dax
-- Bridge table between Product and Category when M:M exists
ProductCategoryBridge = SUMMARIZE(FactSales, FactSales[ProductKey], FactSales[CategoryKey])
```

## Performance Guidelines

| Pattern | Recommendation |
|---------|---------------|
| Large text columns | Move to a separate dimension table; use integer key in fact |
| Calculated columns | Replace with Power Query transformations when possible |
| Implicit measures | Always create explicit measures; disable auto-aggregation |
| Relationships | Prefer star over snowflake; flatten dimensions in Power Query |
| Row count | Fact tables >10M rows → consider aggregations (composite model) |
