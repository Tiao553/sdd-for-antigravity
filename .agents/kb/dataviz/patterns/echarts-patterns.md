# ECharts Patterns

## Option Object Structure

Every ECharts chart is configured via a single `option` object:

```javascript
const option = {
  title:   { text: "Monthly Revenue" },
  tooltip: { trigger: "axis" },
  legend:  { data: ["2023", "2024"] },
  xAxis:   { type: "category", data: months },
  yAxis:   { type: "value", name: "USD" },
  series:  [
    { name: "2023", type: "bar", data: data2023 },
    { name: "2024", type: "bar", data: data2024 },
  ],
};
chart.setOption(option);
```

## Common Chart Recipes

### Line with area fill
```javascript
series: [{
  type: "line",
  data: values,
  smooth: true,
  areaStyle: { opacity: 0.15 },
  lineStyle: { width: 2.5 },
}]
```

### Stacked bar
```javascript
series: [
  { name: "A", type: "bar", stack: "total", data: dataA },
  { name: "B", type: "bar", stack: "total", data: dataB },
]
```

### Scatter with visual map
```javascript
{
  visualMap: { min: 0, max: 100, dimension: 2, inRange: { color: ["#50a3ba", "#eac736", "#d94e5d"] } },
  series: [{ type: "scatter", data: [[x, y, size], ...] }]
}
```

### Pie / Donut
```javascript
series: [{
  type: "pie",
  radius: ["40%", "70%"],   // donut: inner radius > 0
  data: [{ value: 400, name: "North" }, { value: 300, name: "South" }],
  label: { formatter: "{b}: {d}%" },
}]
```

## Dataset Binding (declarative data)

```javascript
{
  dataset: { source: [["month", "revenue", "cost"], ["Jan", 400, 250], ["Feb", 520, 310]] },
  xAxis: { type: "category" },
  yAxis: {},
  series: [
    { type: "bar", encode: { x: "month", y: "revenue" } },
    { type: "line", encode: { x: "month", y: "cost" } },
  ]
}
```

## Toolbox and Interactivity

```javascript
toolbox: {
  feature: {
    dataZoom: { yAxisIndex: "none" },  // zoom slider
    saveAsImage: {},                    // PNG download
    magicType: { type: ["line", "bar"] }, // type toggle
  }
},
dataZoom: [{ type: "inside" }, { type: "slider" }],
```

## Responsive Grid

```javascript
grid: { left: "3%", right: "4%", bottom: "3%", containLabel: true }

// Resize on container change
window.addEventListener("resize", () => chart.resize());
```

## Event Handlers

```javascript
chart.on("click", (params) => {
  console.log(params.name, params.value);
});
```
