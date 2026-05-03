# Visualization Type Patterns

Detailed patterns for each visualization type. Load only the section relevant to the current task.

## Table of Contents
- [Slide Deck](#slide-deck)
- [Infographic](#infographic)
- [Dashboard](#dashboard)
- [Flowchart / Diagram](#flowchart--diagram)
- [Timeline](#timeline)
- [Comparison](#comparison)
- [Data Visualization](#data-visualization)
- [One-Pager](#one-pager)
- [Mind Map](#mind-map)
- [Kanban Board](#kanban-board)

---

## Slide Deck

### Structure
```html
<div class="deck">
  <section class="slide" data-notes="Speaker notes here">
    <!-- slide content -->
  </section>
</div>
```

### Navigation Pattern
```javascript
// Keyboard: ← → arrows, Space, Enter
// Click: left third = prev, right two-thirds = next
// Touch: swipe left/right
// URL hash: #slide-3 for direct linking
```

### Slide Types
1. **Title Slide** — big title, subtitle, optional author/date. Centered. Impactful.
2. **Content Slide** — heading + bullets or heading + visual. Never both walls of text AND a visual.
3. **Section Divider** — full-bleed color/gradient with section title. Breaks up the flow.
4. **Image/Visual Slide** — full-bleed image or large SVG diagram with minimal text.
5. **Two-Column** — split layout for comparisons, text+image, or code+explanation.
6. **Quote Slide** — large pull quote with attribution. Elegant typography.
7. **Data Slide** — chart/graph with one key insight called out.
8. **Closing Slide** — CTA, contact info, or summary. Memorable.

### Best Practices
- First slide hooks attention — bold statement or question
- One idea per slide
- Use progressive reveal within slides (CSS animation delays) for builds
- Consistent positioning: titles always same spot, content always same region
- Slide transitions: `transform: translateX()` with `transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1)`

---

## Infographic

### Structure
- Single long-scroll page
- Clear visual hierarchy with sections
- Use icons (inline SVG) to break up text
- Number callouts for statistics
- Color-coded sections

### Layout Pattern
```
┌─────────────────────────┐
│      HERO / TITLE       │
├─────────────────────────┤
│   Key Stat  │  Key Stat │
├─────────────────────────┤
│     Section 1           │
│  ┌────┐ ┌────┐ ┌────┐  │
│  │Icon│ │Icon│ │Icon│  │
│  │Text│ │Text│ │Text│  │
│  └────┘ └────┘ └────┘  │
├─────────────────────────┤
│     Chart / Visual      │
├─────────────────────────┤
│     Section 2           │
│     Timeline/Flow       │
├─────────────────────────┤
│     CTA / Source        │
└─────────────────────────┘
```

### Best Practices
- Max width 800px, centered
- Use scroll-triggered animations (IntersectionObserver)
- Big numbers: 48px+ font size, bold, accent color
- Source citations at bottom
- Shareable: looks good when screenshotted

---

## Dashboard

### Structure
- CSS Grid layout with cards
- Header with title + date/time
- KPI cards at top (3-5 key metrics)
- Charts/tables below in grid
- Optional sidebar for filters

### KPI Card Pattern
```html
<div class="kpi-card">
  <span class="kpi-label">Revenue</span>
  <span class="kpi-value">$1.2M</span>
  <span class="kpi-change positive">↑ 12.3%</span>
</div>
```

### Chart Patterns (SVG)
- **Bar chart**: `<rect>` elements with CSS transitions on height
- **Line chart**: `<polyline>` or `<path>` with stroke-dasharray animation
- **Donut chart**: `<circle>` with stroke-dasharray/stroke-dashoffset
- **Sparkline**: tiny `<polyline>` in KPI cards

### Best Practices
- Use CSS Grid with `auto-fit` and `minmax()` for responsive cards
- Subtle card shadows, no borders
- Color-code positive (green) and negative (red) changes
- Tooltips on hover for data points
- Auto-refresh indicator (even if static — sells the "live" feel)

---

## Flowchart / Diagram

### Approach
Use SVG for the diagram. Position nodes with CSS Grid or absolute positioning within an SVG viewBox.

### Node Types
```svg
<!-- Rounded rectangle (process) -->
<rect rx="8" />
<!-- Diamond (decision) -->
<polygon points="50,0 100,50 50,100 0,50" />
<!-- Circle (start/end) -->
<circle />
<!-- Parallelogram (input/output) -->
<polygon points="20,0 100,0 80,50 0,50" />
```

### Connection Lines
- Use `<path>` with cubic bezier curves for smooth connections
- Arrow markers: `<marker>` element with `<polygon>` arrowhead
- Elbow connectors for orthogonal layouts

### Best Practices
- Left-to-right or top-to-bottom flow
- Consistent node sizes
- Labels centered in nodes
- Color-code different paths (success=green, error=red)
- Keep it simple: max 15-20 nodes before splitting into sub-diagrams

---

## Timeline

### Layout Options
1. **Vertical** — line down the center, events alternate left/right
2. **Horizontal** — scrollable timeline for fewer events
3. **Compact** — single column with dots and lines

### Vertical Timeline Pattern
```
     ┌──────────┐
     │ Event 1  │──── ●
     └──────────┘     │
                      │
          ● ────┌──────────┐
                │ Event 2  │
                └──────────┘
                      │
     ┌──────────┐     │
     │ Event 3  │──── ●
     └──────────┘
```

### Best Practices
- Alternating sides for visual balance
- Dates prominently displayed
- Color/icon differentiation for event types
- Scroll-triggered entrance animations
- "Now" marker for roadmaps

---

## Comparison

### Layout Options
1. **Side-by-side cards** — 2-3 options in columns
2. **Feature matrix** — rows = features, columns = options, checkmarks/values
3. **Before/After** — split screen

### Feature Matrix Pattern
- Sticky header row
- Alternating row backgrounds
- ✓ / ✗ icons (SVG) instead of text
- Highlight recommended option with accent border/badge

### Best Practices
- Max 4 comparison columns (more = overwhelming)
- Highlight key differentiators
- Use icons for quick scanning
- Color-code to guide toward recommended option (subtle, not pushy)

---

## Data Visualization

### Chart Types (all SVG-based)
- **Bar**: vertical or horizontal, grouped or stacked
- **Line**: single or multi-series, area fills
- **Pie/Donut**: max 6 segments, label percentages
- **Scatter**: for correlations, size for third dimension
- **Heatmap**: grid of colored cells

### SVG Chart Essentials
- Always include axes with labels
- Grid lines: subtle (`stroke: #eee`, `stroke-dasharray: 4`)
- Legend: positioned consistently (top-right or bottom)
- Responsive viewBox: `viewBox="0 0 600 400"` with `preserveAspectRatio`
- Animate on load: stroke-dasharray for lines, scaleY for bars

### Best Practices
- Lead with the insight, not the data
- Annotate key data points directly on the chart
- Don't use 3D effects
- Start y-axis at 0 for bar charts (line charts can break this rule)
- Max 5-7 data series per chart

---

## One-Pager

### Structure
- Hero section with headline + subtext
- 3-4 content sections
- Clear CTA or conclusion
- Max viewport: feels complete without scrolling (or minimal scroll)

### Best Practices
- Large hero text (48px+)
- Icon + text pairs for features
- Centered layout, max-width 960px
- Professional but not boring — one bold design choice
- Works as a screenshot/PDF

---

## Mind Map

### Approach
- Central node with radiating branches
- SVG with `<path>` curved connections
- Color-code branches by category
- Nodes expand on click (optional interactivity)

### Layout Algorithm (simplified)
- Center node at viewBox center
- First-level nodes in a circle around center
- Second-level nodes branch outward from their parent
- Use polar coordinates for positioning

### Best Practices
- Max 2-3 levels deep for readability
- Curved, organic-looking connections (bezier)
- Node size reflects importance
- Hover to highlight a branch and dim others

---

## Kanban Board

### Structure
```html
<div class="board">
  <div class="column">
    <h3>To Do</h3>
    <div class="card">Task</div>
  </div>
  <div class="column">
    <h3>In Progress</h3>
    <div class="card">Task</div>
  </div>
  <div class="column">
    <h3>Done</h3>
    <div class="card">Task</div>
  </div>
</div>
```

### Best Practices
- 3-5 columns (horizontal scroll if needed)
- Cards with title, optional tags/labels (color-coded chips), optional assignee avatar
- Column headers with item count
- Subtle drag-handle visual (even if not functional)
- WIP limits indicator
- Column background colors (very subtle) to differentiate stages
