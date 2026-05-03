# Round 2: Advanced CSS & HTML Techniques for Stunning Visualizations

> Compiled 2026-02-25. Every snippet is self-contained and production-ready.

---

## 1. CSS-Only Techniques

### 1.1 Scroll-Snap Presentation (Slide Deck)

```html
<div class="deck">
  <section class="slide" style="--bg: #1a1a2e">
    <h1>Slide One</h1>
    <p>Full-screen scroll-snap presentation</p>
  </section>
  <section class="slide" style="--bg: #16213e">
    <h1>Slide Two</h1>
    <p>Each section snaps into view</p>
  </section>
  <section class="slide" style="--bg: #0f3460">
    <h1>Slide Three</h1>
    <p>No JavaScript required</p>
  </section>
</div>

<style>
.deck {
  height: 100vh;
  overflow-y: scroll;
  scroll-snap-type: y mandatory;
}
.slide {
  height: 100vh;
  scroll-snap-align: start;
  display: grid;
  place-content: center;
  text-align: center;
  background: var(--bg);
  color: #fff;
  font-family: system-ui;
}
.slide h1 {
  font-size: clamp(2rem, 5vw, 4rem);
  margin: 0 0 .5em;
}
</style>
```

### 1.2 Conic-Gradient Pie Chart

```html
<div class="pie-chart" style="--s1: 35; --s2: 25; --s3: 20; --s4: 20;">
  <div class="legend">
    <span style="--c: #e63946">Revenue 35%</span>
    <span style="--c: #457b9d">Costs 25%</span>
    <span style="--c: #2a9d8f">Growth 20%</span>
    <span style="--c: #e9c46a">Other 20%</span>
  </div>
</div>

<style>
.pie-chart {
  --c1: #e63946; --c2: #457b9d; --c3: #2a9d8f; --c4: #e9c46a;
  width: 250px; height: 250px;
  border-radius: 50%;
  background: conic-gradient(
    var(--c1) 0% calc(var(--s1) * 1%),
    var(--c2) calc(var(--s1) * 1%) calc((var(--s1) + var(--s2)) * 1%),
    var(--c3) calc((var(--s1) + var(--s2)) * 1%) calc((var(--s1) + var(--s2) + var(--s3)) * 1%),
    var(--c4) calc((var(--s1) + var(--s2) + var(--s3)) * 1%) 100%
  );
  position: relative;
  margin: 2rem;
}
/* Donut hole */
.pie-chart::after {
  content: '';
  position: absolute;
  inset: 25%;
  background: #fff;
  border-radius: 50%;
}
.legend {
  position: absolute;
  top: 110%; left: 0;
  display: flex; flex-wrap: wrap; gap: .5rem;
}
.legend span::before {
  content: '';
  display: inline-block;
  width: 12px; height: 12px;
  background: var(--c);
  border-radius: 2px;
  margin-right: 4px;
  vertical-align: middle;
}
</style>
```

### 1.3 CSS Counters for Auto-Numbering

```html
<ol class="fancy-list">
  <li>Define your strategy</li>
  <li>Gather the data</li>
  <li>Build the prototype</li>
  <li>Ship it</li>
</ol>

<style>
.fancy-list {
  counter-reset: steps;
  list-style: none;
  padding: 0;
}
.fancy-list li {
  counter-increment: steps;
  padding: 1rem 1rem 1rem 4rem;
  position: relative;
  margin-bottom: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
}
.fancy-list li::before {
  content: counter(steps, decimal-leading-zero);
  position: absolute;
  left: 1rem; top: 50%;
  transform: translateY(-50%);
  font-size: 1.5rem;
  font-weight: 800;
  color: #e63946;
  font-family: system-ui;
}
</style>
```

### 1.4 Container Queries

```html
<div class="card-container">
  <article class="card">
    <img src="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' width='400' height='200'><rect fill='%23457b9d' width='400' height='200'/></svg>" alt="">
    <div class="card-body">
      <h3>Responsive Card</h3>
      <p>This card adapts to its container width, not the viewport.</p>
    </div>
  </article>
</div>

<style>
.card-container {
  container-type: inline-size;
  container-name: card-wrap;
}
.card {
  display: grid;
  gap: 1rem;
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 12px;
}
.card img { width: 100%; border-radius: 8px; }

@container card-wrap (min-width: 500px) {
  .card {
    grid-template-columns: 200px 1fr;
    align-items: center;
  }
}
@container card-wrap (min-width: 800px) {
  .card {
    grid-template-columns: 300px 1fr;
    padding: 2rem;
  }
  .card h3 { font-size: 1.5rem; }
}
</style>
```

### 1.5 Scroll-Driven Animations

```html
<div class="scroll-container">
  <div class="progress-bar"></div>
  <article class="content">
    <h1>Scroll-Driven Progress Bar</h1>
    <p>Lorem ipsum dolor sit amet... (repeat for scrollable content)</p>
    <!-- Add enough content to scroll -->
  </article>
</div>

<style>
@keyframes grow-progress {
  from { transform: scaleX(0); }
  to   { transform: scaleX(1); }
}

.scroll-container {
  height: 100vh;
  overflow-y: scroll;
}

.progress-bar {
  position: sticky;
  top: 0;
  height: 4px;
  background: #e63946;
  transform-origin: left;
  animation: grow-progress linear;
  animation-timeline: scroll();
}
</style>
```

### 1.6 View Transitions API (requires JS trigger, CSS defines the animation)

```html
<style>
/* Define custom view transition animations */
::view-transition-old(slide-it) {
  animation: slide-out 0.4s ease-in both;
}
::view-transition-new(slide-it) {
  animation: slide-in 0.4s ease-out both;
}

@keyframes slide-out {
  to { transform: translateX(-100%); opacity: 0; }
}
@keyframes slide-in {
  from { transform: translateX(100%); opacity: 0; }
}

.main-content {
  view-transition-name: slide-it;
}
</style>

<script>
// Trigger: call this when swapping content
function navigate(newHTML) {
  if (!document.startViewTransition) {
    document.querySelector('.main-content').innerHTML = newHTML;
    return;
  }
  document.startViewTransition(() => {
    document.querySelector('.main-content').innerHTML = newHTML;
  });
}
</script>
```

---

## 2. SVG Animation

### 2.1 Stroke Drawing Animation (stroke-dasharray)

```html
<svg viewBox="0 0 200 200" width="200" height="200">
  <path class="draw-path"
    d="M 10,100 Q 50,10 100,100 T 190,100"
    fill="none" stroke="#e63946" stroke-width="3"
    stroke-linecap="round" />
</svg>

<style>
.draw-path {
  stroke-dasharray: 400;
  stroke-dashoffset: 400;
  animation: draw 2s ease forwards;
}
@keyframes draw {
  to { stroke-dashoffset: 0; }
}
</style>
```

### 2.2 SVG Morphing with CSS (using d: path())

```html
<svg viewBox="0 0 200 200" width="200">
  <path class="morph" fill="#2a9d8f"
    d="M100,10 L190,70 L160,170 L40,170 L10,70 Z" />
</svg>

<style>
.morph {
  transition: d 0.6s ease-in-out;
}
.morph:hover {
  d: path("M100,10 C155,10 190,55 190,100 C190,145 155,190 100,190 C45,190 10,145 10,100 C10,55 45,10 100,10 Z");
}
</style>
```

### 2.3 Animated SVG Spinner

```html
<svg class="spinner" viewBox="0 0 50 50" width="50" height="50">
  <circle cx="25" cy="25" r="20"
    fill="none" stroke="#457b9d" stroke-width="4"
    stroke-linecap="round"
    stroke-dasharray="90 150"
    stroke-dashoffset="0">
    <animateTransform attributeName="transform"
      type="rotate" from="0 25 25" to="360 25 25"
      dur="1s" repeatCount="indefinite"/>
  </circle>
</svg>
```

### 2.4 Animated SVG Line Chart

```html
<svg viewBox="0 0 400 200" width="400" style="background:#1a1a2e;border-radius:8px;padding:10px">
  <!-- Grid lines -->
  <g stroke="#ffffff15" stroke-width="0.5">
    <line x1="0" y1="50" x2="400" y2="50"/>
    <line x1="0" y1="100" x2="400" y2="100"/>
    <line x1="0" y1="150" x2="400" y2="150"/>
  </g>
  <!-- Data line -->
  <polyline class="chart-line"
    points="20,160 70,140 120,90 170,120 220,60 270,80 320,30 370,50"
    fill="none" stroke="#e63946" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
  <!-- Area fill -->
  <polygon
    points="20,160 70,140 120,90 170,120 220,60 270,80 320,30 370,50 370,180 20,180"
    fill="url(#area-grad)" opacity="0.3"/>
  <defs>
    <linearGradient id="area-grad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#e63946"/>
      <stop offset="100%" stop-color="transparent"/>
    </linearGradient>
  </defs>
</svg>

<style>
.chart-line {
  stroke-dasharray: 600;
  stroke-dashoffset: 600;
  animation: draw-line 1.5s ease forwards;
}
@keyframes draw-line {
  to { stroke-dashoffset: 0; }
}
</style>
```

---

## 3. Modern CSS Features

### 3.1 @layer (Cascade Layers)

```css
/* Control specificity without !important wars */
@layer reset, base, components, utilities;

@layer reset {
  *, *::before, *::after { box-sizing: border-box; margin: 0; }
}

@layer base {
  body { font-family: system-ui; line-height: 1.6; color: #333; }
  h1, h2, h3 { line-height: 1.2; }
}

@layer components {
  .btn {
    padding: .75em 1.5em;
    border: none;
    border-radius: 8px;
    background: #457b9d;
    color: #fff;
    cursor: pointer;
    font-weight: 600;
  }
}

@layer utilities {
  .text-center { text-align: center; }
  .mt-1 { margin-top: 1rem; }
}
```

### 3.2 :has() — The Parent Selector

```css
/* Card with image gets different layout */
.card:has(img) {
  display: grid;
  grid-template-columns: 200px 1fr;
}

/* Form group highlights when child input is focused */
.form-group:has(input:focus) {
  outline: 2px solid #457b9d;
  border-radius: 8px;
}

/* Hide placeholder when sibling has content */
.wrapper:has(.list:empty) .empty-state {
  display: block;
}
```

### 3.3 color-mix() and OKLCH Colors

```css
:root {
  /* OKLCH: perceptually uniform, great for design systems */
  --primary: oklch(55% 0.25 260);        /* vibrant blue */
  --primary-light: oklch(75% 0.15 260);
  --primary-dark: oklch(35% 0.25 260);

  /* Generate hover states with color-mix */
  --btn-hover: color-mix(in oklch, var(--primary) 85%, white);
  --btn-active: color-mix(in oklch, var(--primary) 85%, black);

  /* Semi-transparent from any color */
  --overlay: color-mix(in srgb, var(--primary) 50%, transparent);
}

.badge {
  /* Automatic tints */
  --badge-bg: color-mix(in oklch, var(--badge-color, #e63946) 20%, white);
  background: var(--badge-bg);
  color: var(--badge-color, #e63946);
  padding: .25em .75em;
  border-radius: 999px;
  font-weight: 600;
}
```

### 3.4 Subgrid

```html
<div class="grid-parent">
  <article class="grid-child">
    <h3>Title</h3>
    <p>Description that might be long</p>
    <footer>Action</footer>
  </article>
  <article class="grid-child">
    <h3>Short</h3>
    <p>Brief</p>
    <footer>Action</footer>
  </article>
</div>

<style>
.grid-parent {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1.5rem;
  /* Define the row template children align to */
  grid-template-rows: subgrid; /* only works in explicit grid */
}

/* Practical subgrid: cards with aligned rows */
.grid-child {
  display: grid;
  grid-template-rows: auto 1fr auto;
  gap: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 12px;
  padding: 1.5rem;
}
.grid-child footer {
  align-self: end;
}
</style>
```

### 3.5 Anchor Positioning

```html
<button id="trigger" class="anchor-btn">Hover me</button>
<div class="tooltip" popover>I'm anchored to the button!</div>

<style>
.anchor-btn {
  anchor-name: --my-anchor;
  padding: .75em 1.5em;
  background: #457b9d;
  color: white;
  border: none;
  border-radius: 8px;
}

.tooltip {
  position: fixed;
  position-anchor: --my-anchor;
  top: anchor(bottom);
  left: anchor(center);
  translate: -50% 8px;
  background: #1a1a2e;
  color: white;
  padding: .5em 1em;
  border-radius: 6px;
  font-size: .875rem;
  margin: 0;
  border: none;
}

.anchor-btn:hover + .tooltip {
  display: block;
}
</style>
```

---

## 4. Print CSS Mastery

### 4.1 Complete Print Stylesheet

```css
@media print {
  /* Page setup */
  @page {
    size: A4 portrait;
    margin: 2cm 2.5cm;

    @top-center {
      content: "Company Report 2026";
      font-size: 9pt;
      color: #999;
    }
    @bottom-right {
      content: "Page " counter(page) " of " counter(pages);
      font-size: 9pt;
      color: #999;
    }
  }

  @page :first {
    @top-center { content: none; } /* No header on first page */
    margin-top: 4cm;
  }

  /* Clean up for print */
  body {
    font-size: 11pt;
    line-height: 1.5;
    color: #000;
    background: #fff;
  }

  /* Hide non-print elements */
  nav, .sidebar, .no-print, button, .interactive {
    display: none !important;
  }

  /* Page break control */
  h1, h2, h3 {
    break-after: avoid;   /* Don't break right after a heading */
    page-break-after: avoid;
  }

  table, figure, .chart {
    break-inside: avoid;  /* Keep tables/figures together */
    page-break-inside: avoid;
  }

  section {
    break-before: page;   /* Each section starts a new page */
  }

  /* Make links visible */
  a[href^="http"]::after {
    content: " (" attr(href) ")";
    font-size: 9pt;
    color: #666;
  }

  /* Force backgrounds to print */
  .chart, .badge, .highlight {
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }

  /* Table styling for print */
  table {
    width: 100%;
    border-collapse: collapse;
  }
  th, td {
    border: 0.5pt solid #ccc;
    padding: 6pt 8pt;
    text-align: left;
  }
  thead {
    display: table-header-group; /* Repeat header on each page */
  }
}
```

### 4.2 Print-Specific Page Types

```css
@page cover {
  margin: 0;
  @top-center { content: none; }
  @bottom-right { content: none; }
}

@page landscape {
  size: A4 landscape;
}

.cover-page { page: cover; }
.wide-table-page { page: landscape; }
```

---

## 5. Micro-Interactions

### 5.1 Magnetic Hover Button

```html
<button class="mag-btn">
  <span>Get Started</span>
</button>

<style>
.mag-btn {
  --x: 0; --y: 0;
  position: relative;
  padding: 1em 2.5em;
  background: #1a1a2e;
  color: #fff;
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  overflow: hidden;
  transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1); /* spring */
}

.mag-btn::before {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(
    circle at var(--x, 50%) var(--y, 50%),
    rgba(255,255,255,0.15) 0%,
    transparent 60%
  );
  opacity: 0;
  transition: opacity 0.3s;
}

.mag-btn:hover::before { opacity: 1; }

.mag-btn:hover {
  transform: translateY(-2px) scale(1.02);
  box-shadow: 0 10px 30px rgba(0,0,0,0.2);
}

.mag-btn:active {
  transform: translateY(0) scale(0.98);
  transition-duration: 0.1s;
}
</style>

<script>
document.querySelector('.mag-btn').addEventListener('mousemove', e => {
  const r = e.target.getBoundingClientRect();
  e.target.style.setProperty('--x', ((e.clientX - r.left) / r.width * 100) + '%');
  e.target.style.setProperty('--y', ((e.clientY - r.top) / r.height * 100) + '%');
});
</script>
```

### 5.2 Spring Animation with CSS

```css
/* Spring-like bounce via cubic-bezier overshoot */
.spring-pop {
  transition: transform 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.spring-pop:hover {
  transform: scale(1.1);
}

/* Multi-step spring with keyframes */
@keyframes spring-in {
  0%   { transform: scale(0); opacity: 0; }
  50%  { transform: scale(1.12); }
  70%  { transform: scale(0.95); }
  85%  { transform: scale(1.03); }
  100% { transform: scale(1); opacity: 1; }
}

.spring-enter {
  animation: spring-in 0.6s ease both;
}
```

### 5.3 Staggered Card Reveal

```html
<div class="card-grid">
  <div class="reveal-card" style="--i:0">Card 1</div>
  <div class="reveal-card" style="--i:1">Card 2</div>
  <div class="reveal-card" style="--i:2">Card 3</div>
  <div class="reveal-card" style="--i:3">Card 4</div>
</div>

<style>
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1.5rem;
}

@keyframes fade-up {
  from { opacity: 0; transform: translateY(30px); }
  to   { opacity: 1; transform: translateY(0); }
}

.reveal-card {
  animation: fade-up 0.5s cubic-bezier(0.34, 1.56, 0.64, 1) both;
  animation-delay: calc(var(--i) * 0.1s);
  padding: 2rem;
  background: #f8f9fa;
  border-radius: 12px;
  text-align: center;
  font-weight: 600;
}
</style>
```

### 5.4 Ripple Effect (CSS + minimal JS)

```html
<button class="ripple-btn" onclick="ripple(event)">Click Me</button>

<style>
.ripple-btn {
  position: relative;
  overflow: hidden;
  padding: 1em 2em;
  background: #2a9d8f;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
}

.ripple-btn .ripple-circle {
  position: absolute;
  border-radius: 50%;
  background: rgba(255,255,255,0.4);
  transform: scale(0);
  animation: ripple-anim 0.6s ease-out;
  pointer-events: none;
}

@keyframes ripple-anim {
  to { transform: scale(4); opacity: 0; }
}
</style>

<script>
function ripple(e) {
  const btn = e.currentTarget;
  const c = document.createElement('span');
  c.classList.add('ripple-circle');
  const r = btn.getBoundingClientRect();
  const d = Math.max(r.width, r.height);
  c.style.width = c.style.height = d + 'px';
  c.style.left = (e.clientX - r.left - d/2) + 'px';
  c.style.top = (e.clientY - r.top - d/2) + 'px';
  btn.appendChild(c);
  c.addEventListener('animationend', () => c.remove());
}
</script>
```

---

## 6. Data Visualization Without Libraries

### 6.1 Pure CSS Bar Chart

```html
<div class="bar-chart" style="--max: 100">
  <div class="bar" style="--val: 85; --c: #e63946">
    <span class="label">Q1</span>
    <span class="value">85%</span>
  </div>
  <div class="bar" style="--val: 62; --c: #457b9d">
    <span class="label">Q2</span>
    <span class="value">62%</span>
  </div>
  <div class="bar" style="--val: 94; --c: #2a9d8f">
    <span class="label">Q3</span>
    <span class="value">94%</span>
  </div>
  <div class="bar" style="--val: 71; --c: #e9c46a">
    <span class="label">Q4</span>
    <span class="value">71%</span>
  </div>
</div>

<style>
.bar-chart {
  display: flex;
  align-items: flex-end;
  gap: 1.5rem;
  height: 250px;
  padding: 1rem 2rem;
  border-left: 2px solid #ddd;
  border-bottom: 2px solid #ddd;
}

.bar {
  flex: 1;
  height: calc(var(--val) / var(--max) * 100%);
  background: var(--c);
  border-radius: 8px 8px 0 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-end;
  padding-bottom: 0.5rem;
  position: relative;
  transition: height 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
  min-width: 60px;
}

.bar .value {
  position: absolute;
  top: -1.5rem;
  font-weight: 700;
  font-size: 0.875rem;
  color: var(--c);
}

.bar .label {
  position: absolute;
  bottom: -2rem;
  font-size: 0.8rem;
  color: #666;
  font-weight: 600;
}
</style>
```

### 6.2 CSS Horizontal Bar Chart (Data Table Hybrid)

```html
<table class="h-bar-chart">
  <tr><th>React</th><td style="--val: 92"><span>92%</span></td></tr>
  <tr><th>Vue</th><td style="--val: 67"><span>67%</span></td></tr>
  <tr><th>Svelte</th><td style="--val: 54"><span>54%</span></td></tr>
  <tr><th>Angular</th><td style="--val: 48"><span>48%</span></td></tr>
</table>

<style>
.h-bar-chart {
  width: 100%;
  border-collapse: collapse;
  font-family: system-ui;
}
.h-bar-chart th {
  text-align: right;
  padding: .75rem 1rem;
  width: 100px;
  font-weight: 600;
  color: #333;
}
.h-bar-chart td {
  padding: .75rem 0;
  position: relative;
}
.h-bar-chart td::before {
  content: '';
  display: block;
  height: 32px;
  width: calc(var(--val) * 1%);
  background: linear-gradient(90deg, #457b9d, #2a9d8f);
  border-radius: 0 6px 6px 0;
  transition: width 1s ease;
}
.h-bar-chart td span {
  position: absolute;
  left: calc(var(--val) * 1% + 8px);
  top: 50%;
  transform: translateY(-50%);
  font-size: .8rem;
  font-weight: 700;
  color: #457b9d;
}
</style>
```

### 6.3 CSS Heatmap

```html
<div class="heatmap">
  <div class="cell" style="--v:0.1">M</div>
  <div class="cell" style="--v:0.4">T</div>
  <div class="cell" style="--v:0.8">W</div>
  <div class="cell" style="--v:0.6">T</div>
  <div class="cell" style="--v:0.95">F</div>
  <div class="cell" style="--v:0.3">S</div>
  <div class="cell" style="--v:0.1">S</div>
</div>

<style>
.heatmap {
  display: grid;
  grid-template-columns: repeat(7, 48px);
  gap: 4px;
}
.cell {
  aspect-ratio: 1;
  display: grid;
  place-content: center;
  border-radius: 6px;
  font-size: .75rem;
  font-weight: 600;
  /* Interpolate green heatmap via oklch */
  background: color-mix(
    in oklch,
    oklch(90% 0.05 145) calc((1 - var(--v)) * 100%),
    oklch(55% 0.2 145) calc(var(--v) * 100%)
  );
  color: color-mix(
    in oklch,
    oklch(30% 0.05 145) calc(var(--v) * 100%),
    oklch(50% 0.05 145) calc((1 - var(--v)) * 100%)
  );
}
</style>
```

### 6.4 CSS Sparkline (inline mini chart)

```html
<span class="sparkline" style="--d: polygon(0% 80%, 14% 60%, 28% 40%, 42% 70%, 57% 20%, 71% 35%, 85% 10%, 100% 30%, 100% 100%, 0% 100%)"></span>

<style>
.sparkline {
  display: inline-block;
  width: 80px;
  height: 24px;
  background: linear-gradient(to top, rgba(42,157,143,0.2), rgba(42,157,143,0.05));
  clip-path: var(--d);
  vertical-align: middle;
}
</style>
```

---

## 7. Typography Tricks

### 7.1 Fluid Type with clamp()

```css
:root {
  /* Fluid type scale — no media queries needed */
  --fs-sm: clamp(0.8rem, 0.7rem + 0.25vw, 0.9rem);
  --fs-base: clamp(1rem, 0.9rem + 0.35vw, 1.125rem);
  --fs-lg: clamp(1.25rem, 1rem + 0.75vw, 1.75rem);
  --fs-xl: clamp(1.75rem, 1.2rem + 1.5vw, 3rem);
  --fs-2xl: clamp(2.5rem, 1.5rem + 3vw, 5rem);
}

body { font-size: var(--fs-base); }
h1 { font-size: var(--fs-2xl); }
h2 { font-size: var(--fs-xl); }
h3 { font-size: var(--fs-lg); }
small { font-size: var(--fs-sm); }
```

### 7.2 Text Gradient

```css
.gradient-text {
  background: linear-gradient(135deg, #e63946, #457b9d, #2a9d8f);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  font-size: clamp(2rem, 5vw, 5rem);
  font-weight: 900;
  line-height: 1.1;
}
```

### 7.3 Variable Fonts

```css
@font-face {
  font-family: 'Inter';
  src: url('Inter-VariableFont.woff2') format('woff2-variations');
  font-weight: 100 900;
  font-style: normal;
  font-display: swap;
}

.variable-demo {
  font-family: 'Inter', system-ui;
  font-variation-settings: 'wght' 400, 'slnt' 0;
  transition: font-variation-settings 0.3s ease;
}

.variable-demo:hover {
  font-variation-settings: 'wght' 800, 'slnt' -10;
}

/* Animating weight */
@keyframes breathe {
  0%, 100% { font-variation-settings: 'wght' 300; }
  50%      { font-variation-settings: 'wght' 800; }
}

.text-breathe {
  animation: breathe 3s ease-in-out infinite;
}
```

### 7.4 Optical Sizing & Kerning

```css
.refined-type {
  font-kerning: auto;
  font-feature-settings: 'kern' 1, 'liga' 1, 'calt' 1;
  font-optical-sizing: auto;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  letter-spacing: -0.02em; /* tighten display type */
  text-wrap: balance; /* modern balanced wrapping */
}
```

---

## 8. Design Trends in CSS

### 8.1 Glassmorphism

```html
<div class="glass-bg">
  <div class="glass-card">
    <h3>Glass Card</h3>
    <p>Frosted glass effect with backdrop-filter</p>
  </div>
</div>

<style>
.glass-bg {
  min-height: 300px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  display: grid;
  place-content: center;
  padding: 2rem;
}

.glass-card {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.25);
  border-radius: 16px;
  padding: 2rem 3rem;
  color: white;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}
</style>
```

### 8.2 Neumorphism

```html
<div class="neu-surface">
  <div class="neu-card">
    <div class="neu-inset">42</div>
    <p>Metric Value</p>
  </div>
</div>

<style>
.neu-surface {
  background: #e0e5ec;
  min-height: 300px;
  display: grid;
  place-content: center;
  padding: 2rem;
}

.neu-card {
  background: #e0e5ec;
  border-radius: 20px;
  padding: 2rem 3rem;
  text-align: center;
  box-shadow:
    8px 8px 16px #b8bec7,
    -8px -8px 16px #ffffff;
}

.neu-inset {
  background: #e0e5ec;
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 1rem;
  font-size: 2.5rem;
  font-weight: 800;
  color: #457b9d;
  box-shadow:
    inset 4px 4px 8px #b8bec7,
    inset -4px -4px 8px #ffffff;
}
</style>
```

### 8.3 Claymorphism

```css
.clay-card {
  background: linear-gradient(135deg, #f5e6ff, #e8d5f5);
  border-radius: 24px;
  padding: 2rem;
  box-shadow:
    8px 8px 16px rgba(0, 0, 0, 0.1),
    inset -4px -4px 8px rgba(0, 0, 0, 0.05),
    inset 4px 4px 8px rgba(255, 255, 255, 0.8);
  border: 2px solid rgba(255, 255, 255, 0.5);
}
```

---

## 9. Dark Mode Best Practices

### 9.1 Complete Dark Mode System

```css
:root {
  /* Light mode (default) */
  color-scheme: light dark;

  --surface-0: #ffffff;
  --surface-1: #f8f9fa;
  --surface-2: #e9ecef;
  --text-primary: #1a1a2e;
  --text-secondary: #6c757d;
  --border: #dee2e6;
  --accent: oklch(55% 0.25 260);
  --shadow: rgba(0, 0, 0, 0.1);

  /* Semantic tokens */
  --success: oklch(60% 0.2 145);
  --warning: oklch(75% 0.18 85);
  --danger: oklch(55% 0.22 25);
}

@media (prefers-color-scheme: dark) {
  :root {
    --surface-0: #0d1117;
    --surface-1: #161b22;
    --surface-2: #21262d;
    --text-primary: #e6edf3;
    --text-secondary: #8b949e;
    --border: #30363d;
    --accent: oklch(72% 0.18 260);
    --shadow: rgba(0, 0, 0, 0.4);

    --success: oklch(72% 0.16 145);
    --warning: oklch(80% 0.14 85);
    --danger: oklch(70% 0.18 25);
  }
}

/* Manual toggle override */
[data-theme="dark"] {
  --surface-0: #0d1117;
  --surface-1: #161b22;
  --surface-2: #21262d;
  --text-primary: #e6edf3;
  --text-secondary: #8b949e;
  --border: #30363d;
  --accent: oklch(72% 0.18 260);
  --shadow: rgba(0, 0, 0, 0.4);
}

/* Usage */
body {
  background: var(--surface-0);
  color: var(--text-primary);
}

.card {
  background: var(--surface-1);
  border: 1px solid var(--border);
  box-shadow: 0 2px 8px var(--shadow);
}
```

### 9.2 Dark Mode Image Handling

```css
/* Dim images slightly in dark mode */
@media (prefers-color-scheme: dark) {
  img:not([src*=".svg"]) {
    filter: brightness(0.85) contrast(1.1);
  }

  /* Invert diagrams/illustrations that are black-on-white */
  img.invertible {
    filter: invert(1) hue-rotate(180deg) brightness(0.9);
  }

  /* Reduce shadow intensity on elevated surfaces */
  .elevated {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
  }
}
```

---

## 10. Performance

### 10.1 CSS Containment

```css
/* Tell the browser this element is isolated — huge perf win for complex pages */
.widget {
  contain: layout style paint; /* or contain: strict for all */
  content-visibility: auto;    /* skip rendering when off-screen */
  contain-intrinsic-size: 0 500px; /* estimated size for content-visibility */
}

/* For repeated list items */
.list-item {
  contain: layout style;
  content-visibility: auto;
  contain-intrinsic-size: auto 80px;
}
```

### 10.2 will-change (Use Sparingly)

```css
/* Only apply will-change right before animation */
.animated-el {
  transition: transform 0.3s, opacity 0.3s;
}
.animated-el:hover {
  will-change: transform, opacity;
}
.animated-el.animating {
  will-change: transform, opacity;
}
/* Remove after animation completes via JS */

/* NEVER do this globally: */
/* * { will-change: transform; }  ← destroys performance */
```

### 10.3 Reducing Repaints

```css
/* Use transform/opacity for animations — they don't trigger layout/paint */
.good {
  /* ✅ GPU-composited, no repaints */
  transition: transform 0.3s, opacity 0.3s;
}
.good:hover {
  transform: translateY(-4px) scale(1.02);
  opacity: 0.9;
}

.bad {
  /* ❌ Triggers layout recalc + repaint */
  transition: top 0.3s, width 0.3s, margin 0.3s;
}

/* Use translate instead of positioning */
.slide-in {
  transform: translateX(-100%);
  transition: transform 0.4s ease;
}
.slide-in.active {
  transform: translateX(0);
}
```

### 10.4 Lazy Loading & Resource Hints

```html
<!-- Native lazy loading -->
<img src="hero.jpg" alt="Hero" loading="eager" fetchpriority="high">
<img src="below-fold.jpg" alt="" loading="lazy">

<!-- Preload critical resources -->
<link rel="preload" href="critical-font.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="hero.jpg" as="image" fetchpriority="high">

<!-- Preconnect to external origins -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="dns-prefetch" href="https://analytics.example.com">

<!-- Optimal font loading -->
<style>
@font-face {
  font-family: 'MyFont';
  src: url('myfont.woff2') format('woff2');
  font-display: swap; /* Show fallback immediately, swap when ready */
  unicode-range: U+0000-00FF; /* Only load Latin chars */
}
</style>
```

### 10.5 Critical CSS Pattern

```html
<head>
  <!-- Inline critical CSS for above-the-fold content -->
  <style>
    /* Only what's needed for first paint */
    body { margin: 0; font-family: system-ui; }
    .hero { min-height: 100vh; display: grid; place-content: center; }
  </style>

  <!-- Defer non-critical CSS -->
  <link rel="preload" href="full-styles.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
  <noscript><link rel="stylesheet" href="full-styles.css"></noscript>
</head>
```

---

## Bonus: Composable Utility Patterns

### Animation Composition

```css
/* Reusable timing functions */
:root {
  --ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1);
  --ease-out-expo: cubic-bezier(0.19, 1, 0.22, 1);
  --ease-in-out-circ: cubic-bezier(0.85, 0, 0.15, 1);
}

/* Stagger system */
[data-stagger] > * {
  --delay: calc(var(--i, 0) * 80ms);
  animation-delay: var(--delay) !important;
}

/* Reduced motion */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

### Complete Design Token System

```css
:root {
  /* Spacing scale */
  --space-xs: clamp(0.25rem, 0.2rem + 0.15vw, 0.375rem);
  --space-sm: clamp(0.5rem, 0.4rem + 0.3vw, 0.75rem);
  --space-md: clamp(1rem, 0.85rem + 0.5vw, 1.5rem);
  --space-lg: clamp(1.5rem, 1.2rem + 1vw, 2.5rem);
  --space-xl: clamp(2rem, 1.5rem + 2vw, 4rem);

  /* Border radius */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 16px;
  --radius-xl: 24px;
  --radius-full: 999px;

  /* Shadows (elevation system) */
  --shadow-sm: 0 1px 2px var(--shadow);
  --shadow-md: 0 4px 12px var(--shadow);
  --shadow-lg: 0 12px 32px var(--shadow);
  --shadow-xl: 0 24px 48px var(--shadow);
}
```
