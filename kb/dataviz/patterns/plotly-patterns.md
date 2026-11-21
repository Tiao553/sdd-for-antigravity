# Plotly Patterns

## px vs go

Use `plotly.express` (`px`) for standard charts with a DataFrame — it's one line. Drop to `plotly.graph_objects` (`go`) when you need fine-grained control or custom traces.

```python
import plotly.express as px
import plotly.graph_objects as go

# px: fast path
fig = px.bar(df, x="month", y="revenue", color="region", title="Revenue by Region")

# go: full control
fig = go.Figure()
fig.add_trace(go.Bar(x=df["month"], y=df["revenue"], name="Revenue"))
```

## Common Chart Recipes

### Line chart with markers
```python
fig = px.line(df, x="date", y="value", markers=True,
              title="Revenue grew 18% YoY",
              labels={"value": "Revenue (USD)", "date": ""})
fig.update_traces(line_width=2.5)
```

### Grouped vs stacked bar
```python
# Grouped
fig = px.bar(df, x="month", y="sales", color="segment", barmode="group")

# Stacked
fig = px.bar(df, x="month", y="sales", color="segment", barmode="stack")
```

### Scatter with trendline
```python
fig = px.scatter(df, x="ad_spend", y="revenue", trendline="ols",
                 hover_data=["campaign"])
```

### Subplots (multiple charts in grid)
```python
from plotly.subplots import make_subplots

fig = make_subplots(rows=1, cols=2, subplot_titles=("Revenue", "Units"))
fig.add_trace(go.Bar(x=df["month"], y=df["revenue"]), row=1, col=1)
fig.add_trace(go.Bar(x=df["month"], y=df["units"]), row=1, col=2)
```

## Layout and Theming

```python
fig.update_layout(
    template="plotly_white",       # clean background
    font_family="Inter, sans-serif",
    title_font_size=16,
    legend=dict(orientation="h", yanchor="bottom", y=1.02),
    margin=dict(l=40, r=20, t=60, b=40),
    plot_bgcolor="white",
    paper_bgcolor="white",
)

# Reference line (target / benchmark)
fig.add_hline(y=1_000_000, line_dash="dot", annotation_text="Target")

# Annotation callout
fig.add_annotation(x="2024-11", y=1_200_000,
                   text="Black Friday peak", showarrow=True, arrowhead=2)
```

## Export

```python
fig.write_html("chart.html")           # interactive
fig.write_image("chart.png", scale=2)  # static (requires kaleido)
fig.show()                             # notebook / Dash inline
```

## Dash Integration Snippet
```python
from dash import Dash, dcc, html
import plotly.express as px

app = Dash(__name__)
fig = px.line(df, x="date", y="revenue")
app.layout = html.Div([dcc.Graph(figure=fig)])
```
