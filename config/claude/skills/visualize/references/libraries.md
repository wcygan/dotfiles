# CDN Library Reference

Preferred CDN libraries and when to use them. Always use jsDelivr for consistent, fast loading.

## Table of Contents
- [Motion](#motion) ⭐ (animations — included in skeleton)
- [Chart.js](#chartjs)
- [D3.js](#d3js)
- [Three.js](#threejs)
- [Mermaid](#mermaid)
- [Reveal.js](#revealjs)
- [Leaflet](#leaflet)

---

## Motion

**Best for:** ALL animations. Spring physics, scroll-triggered reveals, staggered entrances, number counters, hover micro-interactions. Replaces raw CSS @keyframes and IntersectionObserver.

```html
<script src="https://cdn.jsdelivr.net/npm/motion@12/dist/motion.js"></script>
```

**Included in the mandatory skeleton.** Exposes global `Motion` object.

```javascript
// Spring-animated card entrance
Motion.animate('.card',
  { opacity: [0, 1], y: [40, 0], scale: [0.95, 1] },
  { delay: Motion.stagger(0.08), duration: 0.5, ease: Motion.spring({ stiffness: 200, damping: 22 }) }
);

// Scroll-triggered reveal
Motion.inView('.section', (info) => {
  Motion.animate(info.target, { opacity: 1, y: 0 }, { duration: 0.6 });
});
```

See [animations.md](animations.md) for complete API reference and recipes (~15KB gzipped).

---

## Chart.js

**Best for:** Standard charts with beautiful defaults. Bar, line, pie, doughnut, radar, polar area, scatter, bubble.

```html
<script src="https://cdn.jsdelivr.net/npm/chart.js@4"></script>
```

### When to Use
- Quick data visualization with minimal config
- Standard chart types (bar, line, pie, doughnut, radar)
- When you want great defaults without deep customization
- Responsive, animated charts out of the box

### Pattern
```html
<canvas id="myChart"></canvas>
<script>
new Chart(document.getElementById('myChart'), {
  type: 'bar', // line, pie, doughnut, radar, polarArea, scatter, bubble
  data: {
    labels: ['Jan', 'Feb', 'Mar'],
    datasets: [{
      label: 'Revenue',
      data: [12, 19, 3],
      backgroundColor: 'hsla(220, 80%, 55%, 0.7)',
      borderColor: 'hsl(220, 80%, 55%)',
      borderWidth: 2,
      borderRadius: 6,
    }]
  },
  options: {
    responsive: true,
    plugins: {
      legend: { position: 'bottom' },
      title: { display: true, text: 'Monthly Revenue' }
    },
    scales: { y: { beginAtZero: true } }
  }
});
</script>
```

### Tips
- Use `borderRadius` for rounded bar charts
- `tension: 0.4` on line datasets for smooth curves
- Combine chart types: `{ type: 'bar', datasets: [{ type: 'line', ... }, { ... }] }`

---

## D3.js

**Best for:** Custom, complex, or unconventional data visualizations. Force-directed graphs, geographic maps, treemaps, sunbursts.

```html
<script src="https://cdn.jsdelivr.net/npm/d3@7"></script>
```

### When to Use
- Custom visualizations Chart.js can't handle
- Force-directed network graphs
- Geographic/map visualizations (with topojson)
- Treemaps, sunbursts, chord diagrams
- When you need full SVG control

### Pattern
```html
<div id="viz"></div>
<script>
const data = [30, 86, 168, 281, 303, 365];
const width = 600, height = 400, margin = { top: 20, right: 20, bottom: 30, left: 40 };

const svg = d3.select('#viz').append('svg')
  .attr('viewBox', `0 0 ${width} ${height}`);

const x = d3.scaleBand()
  .domain(data.map((_, i) => i))
  .range([margin.left, width - margin.right])
  .padding(0.2);

const y = d3.scaleLinear()
  .domain([0, d3.max(data)])
  .range([height - margin.bottom, margin.top]);

svg.selectAll('rect').data(data).join('rect')
  .attr('x', (_, i) => x(i))
  .attr('y', d => y(d))
  .attr('width', x.bandwidth())
  .attr('height', d => y(0) - y(d))
  .attr('rx', 4)
  .attr('fill', 'hsl(220, 80%, 55%)');
</script>
```

---

## Three.js

**Best for:** 3D visualizations, immersive data displays, architectural/spatial representations.

```html
<script src="https://cdn.jsdelivr.net/npm/three@0.170/build/three.module.min.js" type="module"></script>
```

### When to Use
- 3D data visualization (3D scatter, terrain)
- Product/architectural visualization
- Immersive, impressive hero visuals
- When 2D isn't enough to convey the concept

---

## Mermaid

**Best for:** Diagrams from text definitions. Flowcharts, sequence diagrams, Gantt charts, ER diagrams, class diagrams.

```html
<script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>
<script>mermaid.initialize({ startOnLoad: true, theme: 'neutral' });</script>
```

### When to Use
- Quick flowcharts and process diagrams
- Sequence diagrams for API/system interactions
- Gantt charts for project timelines
- When diagram accuracy matters more than custom styling

### Pattern
```html
<pre class="mermaid">
graph TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Action 1]
    B -->|No| D[Action 2]
    C --> E[End]
    D --> E
</pre>
```

### Tips
- Use `%%` for comments in Mermaid syntax
- Themes: `default`, `neutral`, `dark`, `forest`
- Custom styles: `style A fill:#f9f,stroke:#333`

---

## Reveal.js

**Best for:** Full-featured slide decks when you need more than the basic template.

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5/dist/reveal.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5/dist/theme/white.css">
<script src="https://cdn.jsdelivr.net/npm/reveal.js@5/dist/reveal.js"></script>
```

### When to Use
- Complex presentations with nested slides (vertical + horizontal)
- Markdown-based slide content
- Built-in speaker notes, PDF export, overview mode
- When the basic slide template isn't enough

### Tips
- Themes: `white`, `black`, `league`, `beige`, `moon`, `night`, `serif`, `simple`, `solarized`
- Fragments for step-by-step reveals
- Code highlighting with highlight.js plugin

---

## Leaflet

**Best for:** Interactive maps with markers, polygons, heatmaps.

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/leaflet@1/dist/leaflet.css">
<script src="https://cdn.jsdelivr.net/npm/leaflet@1/dist/leaflet.js"></script>
```

### When to Use
- Location data visualization
- Geographic comparisons
- Travel/route visualization
- Any data with lat/lng coordinates

### Pattern
```html
<div id="map" style="height: 500px; border-radius: 12px;"></div>
<script>
const map = L.map('map').setView([37.5, -122.3], 10);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '© OpenStreetMap'
}).addTo(map);
L.marker([37.5, -122.3]).addTo(map).bindPopup('Location');
</script>
```
