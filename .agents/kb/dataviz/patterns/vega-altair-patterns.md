# Vega-Altair Patterns

## Core Grammar

```python
import altair as alt
import pandas as pd

chart = (
    alt.Chart(df)
    .mark_bar()
    .encode(
        x=alt.X("month:T", title="Month"),
        y=alt.Y("revenue:Q", title="Revenue (USD)"),
        color="region:N",
        tooltip=["month:T", "revenue:Q", "region:N"],
    )
    .properties(title="Revenue by Region", width=600, height=300)
)
chart.save("chart.html")
```

## Data Type Shorthands

| Shorthand | Type | Example |
|-----------|------|---------|
| `:Q` | Quantitative (numeric) | `revenue:Q` |
| `:N` | Nominal (categorical) | `region:N` |
| `:O` | Ordinal (ordered categories) | `rating:O` |
| `:T` | Temporal (date/time) | `date:T` |

## Common Marks

```python
.mark_bar()        # bar chart
.mark_line()       # line chart
.mark_point()      # scatter plot
.mark_area()       # area chart
.mark_text()       # text labels
.mark_rule()       # reference line
.mark_rect()       # heatmap (binned)
.mark_arc()        # pie / donut
```

## Layering

```python
# Base chart reused across layers
base = alt.Chart(df).encode(x="month:T")

line  = base.mark_line().encode(y="revenue:Q")
point = base.mark_point(size=60).encode(y="revenue:Q")
rule  = alt.Chart(pd.DataFrame({"y": [1_000_000]})).mark_rule(color="red", strokeDash=[6,3]).encode(y="y:Q")

chart = (line + point + rule).properties(title="Revenue vs Target")
```

## Faceting (small multiples)

```python
# Wrap into grid by category
chart = (
    alt.Chart(df)
    .mark_line()
    .encode(x="month:T", y="revenue:Q")
    .facet(facet="region:N", columns=3)
)
```

## Interactive Selections

```python
# Brush selection on scatter
brush = alt.selection_interval()

points = (
    alt.Chart(df)
    .mark_point()
    .encode(
        x="ad_spend:Q",
        y="revenue:Q",
        color=alt.condition(brush, "segment:N", alt.value("lightgray")),
    )
    .add_params(brush)
)

# Dropdown filter
input_dropdown = alt.binding_select(options=["North", "South", "East", "West"], name="Region ")
selection = alt.selection_point(fields=["region"], bind=input_dropdown)

chart = (
    alt.Chart(df)
    .mark_bar()
    .encode(x="month:T", y="revenue:Q")
    .add_params(selection)
    .transform_filter(selection)
)
```

## Conditional Encoding (highlight pattern)

```python
highlight = alt.selection_point(on="mouseover", fields=["region"])

color = alt.condition(
    highlight,
    alt.Color("region:N"),
    alt.value("lightgray"),
)

chart = alt.Chart(df).mark_bar().encode(x="month:T", y="revenue:Q", color=color).add_params(highlight)
```

## Configuration and Theming

```python
alt.themes.enable("fivethirtyeight")  # built-in theme

# Custom config
chart = chart.configure_axis(
    grid=False, labelFontSize=12, titleFontSize=13
).configure_view(
    strokeWidth=0
).configure_title(
    fontSize=16, anchor="start"
)
```
