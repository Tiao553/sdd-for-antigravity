# Dashboard Composition

## Core Layout Principles

### Visual Hierarchy
Place the most important metric top-left (F-pattern reading) or top-center (Z-pattern). Supporting metrics and charts follow in descending importance.

- **Level 1** — KPI cards / Big Numbers (headline metrics)
- **Level 2** — Primary charts (trend, comparison)
- **Level 3** — Detail tables, filters, drilldowns

### Grid Systems
- Use a consistent grid (12-column is common)
- Align chart edges — misalignment signals disorder
- Leave whitespace between sections; avoid chart walls

### Filter Placement
- Global filters (date range, region) → top bar or left sidebar
- Page-level filters → right sidebar or inline
- Chart-level filters → tooltip or drill-through, not visible by default

## Platform-Specific Patterns

### Power BI
- **Canvas size** — 1280×720 (16:9) default; use 1920×1080 for large screens
- **Snap to grid** — enable for consistent alignment
- **Themes** — use JSON theme files, not manual color per visual
- **Bookmark navigation** — replaces tab navigation for report pages
- **Tooltip pages** — custom tooltips as report pages (set page type to "Tooltip")
- Escalate to `power-bi-developer` for DAX measures and data model questions

### Tableau
- **Layout containers** — use tiled containers, not floating objects
- **Padding** — inner/outer padding on containers instead of blank objects
- **Device designer** — phone, tablet, desktop layouts in one workbook
- **Dashboard actions** — filter, highlight, URL for interactivity

### Evidence.dev
- Pages = Markdown files in `pages/` directory
- **Grid layout** — CSS Grid via `<Grid cols=3>` component
- **Section** — `<Details>` for collapsible sections
- Composition is code: treat layout as Markdown + component props
- See `modern-stack` KB for full Evidence.dev setup patterns

## Anti-Patterns

| Anti-pattern | Why it hurts | Fix |
|-------------|-------------|-----|
| Chart wall | Cognitive overload | Group into sections with headers |
| Traffic light everywhere | Loses meaning | Reserve red/yellow/green for true status |
| Too many colors | Distracts | ≤7 colors; use one accent color for highlights |
| Unlabeled axes | Forces guessing | Always label with unit |
| Default chart titles | "Sum of Revenue" | Write conclusion titles: "North region grew 18% YoY" |
