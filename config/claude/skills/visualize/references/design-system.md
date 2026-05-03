## Design System

Apply these defaults. They are opinionated and tested — override only when user requests it.

### Design Notes
- **Use inline SVG for icons, NOT emojis.** Simple path-based SVGs for a professional look. See the Icons section above.
- **Chart.js charts MUST be destroyed and recreated on theme toggle** — not just CSS variable swaps. Colors are read at render time, so the chart must be rebuilt with new computed values.
- **Chart.js: DISABLE default animation** — Add `Chart.defaults.animation = false;` before creating charts. Default animations cause charts to appear blank/broken in screenshots, Playwright tests, and initial renders. This is a recurring bug that caused "broken charts" in rounds 13-25.
- **Chart.js: Use explicit color values** — Don't concatenate CSS variable values with hex alpha suffixes (e.g., `c.remote + '18'`). Use explicit `rgba()` values instead: `'rgba(12, 206, 107, 0.15)'`.
- **Chart.js: Don't use resetCanvas** — Just reuse the same canvas element. Destroy the old chart instance with `.destroy()` then create a new one on the same canvas.
- **Chart.js: Build after layout is stable** — Use `window.addEventListener('load', ...)` with a short `setTimeout(200)` and trigger `window.dispatchEvent(new Event('resize'))` after building.

### Typography
- **Primary font:** Inter via Google Fonts CDN — `https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap`
- **Professional letter-spacing (Apple/Stripe-inspired):**
  - **Hero headings (h1):** `letter-spacing: -0.03em` — tight like Apple keynote titles
  - **Section headings (h2-h3):** `letter-spacing: -0.02em`
  - **Body text:** `letter-spacing: -0.011em` for refined readability
  - **Labels/caps:** `letter-spacing: 0.05em` for small uppercase text
  - **Font features:** `font-feature-settings: 'cv11', 'ss01';` for Inter's stylistic alternates
- **Font-weight hierarchy (Stripe-inspired):**
  - **h1:** `font-weight: 700` (bold, not 800 — optically cleaner at large sizes)
  - **h2:** `font-weight: 600` (semibold)
  - **Card titles:** `font-weight: 600`
  - **Body text:** `font-weight: 400` (regular)
  - **Labels:** `font-weight: 500` (medium)
- **Text colors (Vercel-inspired):** Never pure white. Use `#ededed` or `var(--text)` which maps to `#f5f5f7` in dark mode. Secondary text at 60% opacity feel (`#888` or `var(--text-secondary)`)
- **NO gradient text on headings** — use solid colors only. Gradient text looks cheap at scale.
- **Multilingual support:** When content includes non-Latin text (Korean, Japanese, Chinese, etc.), add the appropriate Google Fonts:
  - **Korean:** Noto Sans KR — `https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;600;700;800;900&display=swap`
  - **Japanese:** Noto Sans JP — `https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;600;700;800;900&display=swap`
  - **Chinese (Simplified):** Noto Sans SC — `https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;600;700;800;900&display=swap`
  - **Arabic:** Noto Sans Arabic — `https://fonts.googleapis.com/css2?family=Noto+Sans+Arabic:wght@300;400;500;600;700;800;900&display=swap`
  - Set `font-family: 'Noto Sans KR', 'Inter', sans-serif;` (CJK font first, then Inter fallback for numbers/Latin)
  - Set `<html lang="ko">` (or appropriate language code)
- **Custom fonts:** When the user requests a specific font or vibe:
  - **Serif/editorial:** Lora, Playfair Display, Source Serif Pro
  - **Monospace/code:** JetBrains Mono, Fira Code, Source Code Pro
  - **Display/creative:** Space Grotesk, Outfit, Sora, Poppins
  - **Handwritten:** Caveat, Patrick Hand
  - Always load via Google Fonts CDN: `https://fonts.googleapis.com/css2?family=FONTNAME:wght@WEIGHTS&display=swap`
  - Update the `--font-primary` CSS var and `body { font-family: ... }` accordingly
- **Light mode text optimization:** Use softer text colors, not harsh black:
  - Primary text: `#1a1a1a` (not #000000) for better readability
  - Secondary text: `#666666` for proper hierarchy
  - Never pure black text on white backgrounds - it's too harsh
- **Font detection:** Infer the right font from context:
  - Korean/Japanese/Chinese content → auto-add Noto Sans KR/JP/SC
  - Code-heavy content (cheat sheets) → add JetBrains Mono for code blocks
  - Formal/editorial content → consider a serif font for headings
  - Playful/creative content → consider display fonts
- **Monospace:** JetBrains Mono or system `'SF Mono', 'Fira Code', 'Consolas', monospace`
- **Fallback:** `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`
- **Type scale (dramatic):** Make hero titles bigger, body should breathe more — 14 → 16 → 20 → 25 → 31 → 39 → 49px
- **Line-height:** 1.5–1.7 for body, 1.1 for headings (tight for professional feel)
- **Max line width:** 65–75 characters for readability
- Use `clamp()` for fluid responsive sizing: `clamp(1rem, 2.5vw, 1.25rem)`

### Modern CSS Techniques (Chrome 105+)

Use these cutting-edge CSS features where supported for better UX:

**Popover API** (Chrome 114+) — Zero-JS tooltips, info panels, and modals:
```html
<button popovertarget="info-panel">ℹ Details</button>
<div id="info-panel" popover>
  <h3>More Information</h3>
  <p>Details shown on click, no JS needed.</p>
</div>
```
```css
[popover] {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: 8px; padding: 16px; max-width: 320px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.2);
}
[popover]::backdrop { background: rgba(0,0,0,0.3); }
```
Use for: dashboard metric details, architecture node info, chart annotations.

**Exclusive `<details>` Accordion** (Chrome 120+) — Collapsible sections, no JS:
```html
<details name="faq" open><summary>Section 1</summary><p>Content</p></details>
<details name="faq"><summary>Section 2</summary><p>Content</p></details>
```
Same `name` attribute = only one open at a time. Use for: cheatsheets, process guides, FAQs, any content with collapsible groups.

**`::details-content` Styling** (Chrome 131+) — Animate accordion open/close:
```css
details { overflow: hidden; }
::details-content {
  transition: block-size 0.3s ease, opacity 0.3s ease;
  block-size: 0; opacity: 0;
}
details[open]::details-content {
  block-size: auto; opacity: 1;
}
```

**CSS Anchor Positioning** (Chrome 125+) — Position tooltips relative to elements:
```css
.node { anchor-name: --node-tooltip; }
.tooltip {
  position: fixed; position-anchor: --node-tooltip;
  position-area: block-start; margin-bottom: 8px;
}
```
Use for: architecture diagrams, org charts, any element needing positioned annotations.

**Container Queries** — Size elements based on their container, not viewport:
```css
.card-container {
  container-type: inline-size;
  container-name: card;
}
@container card (width > 400px) {
  .card-title { font-size: clamp(1.25rem, 4cqi, 2rem); }
}
```

**:has() Parent Selector** — Style elements based on their children:
```css
/* Style card if it contains an image */
.card:has(img) { padding-block: 2rem; }
/* Reduce spacing on headings followed by subheadings */
h1:has(+ h2) { margin-bottom: 0.25rem; }
```

**color-mix() Function** — Dynamic color generation:
```css
background: color-mix(in oklch, var(--accent), transparent 20%);
border-color: color-mix(in srgb, var(--text), var(--bg) 85%);
```

**light-dark() Function** (Chrome 123+) — Single-property theme switching:
```css
:root { color-scheme: light dark; }
background: light-dark(white, #1a1a1a);
color: light-dark(#333, #fff);
```

**@starting-style** (Chrome 117+) — Entry animations for new elements:
```css
.modal {
  opacity: 1; transform: scale(1);
  transition: opacity 0.3s, transform 0.3s;
  @starting-style {
    opacity: 0; transform: scale(0.8);
  }
}
```

### Color System (Class-Based Theming — NO @media prefers-color-scheme)

**CRITICAL: Do NOT use `@media (prefers-color-scheme)` for theme variables.** It fights with class-based `.theme-dark`/`.theme-light` and causes themes to break when OS mode differs from selected theme. Use ONLY class-based selectors on `html`:

```css
/* Theme via class on <html> — JS detects prefers-color-scheme on first load */
html.theme-dark {
  --bg: #0A0A0A;              /* near-black (Linear-inspired) */
  --surface: #141414;          /* barely lighter than bg */
  --surface-hover: #1C1C1C;
  --border: rgba(255,255,255,0.04);  /* nearly invisible borders */
  --text: #EDEDED;             /* not pure white */
  --text-secondary: #888888;
  --accent: #3b82f6;
  --accent-secondary: #8b5cf6;
  --positive: #10b981;
  --negative: #f43f5e;
  --warning: #f59e0b;
  --info: #06b6d4;             /* semantic info color */
  --muted: #0f0f0f;            /* subtle backgrounds */
}
html.theme-light {
  --bg: #FAFAF9;               /* warm off-white */
  --surface: #FFFFFF;
  --surface-hover: #F5F5F4;
  --border: #e5e5e5;           /* more visible than 0.06 opacity */
  --text: #1a1a1a;             /* softer than pure black */
  --text-secondary: #666666;   /* better contrast than #64748b */
  --accent: #2563eb;
  --accent-secondary: #7c3aed;
  --positive: #059669;
  --negative: #e11d48;
  --warning: #d97706;
  --info: #0ea5e9;             /* semantic info color */
  --muted: #f8fafc;            /* subtle backgrounds */
}
```

**JS theme init** detects OS preference on first visit, then uses localStorage override:
```javascript
var saved = localStorage.getItem('viz-theme');
var initial = saved || (window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark');
applyTheme(initial);
```

Chart color sequence: `#3b82f6, #8b5cf6, #ec4899, #f59e0b, #10b981, #06b6d4, #f43f5e`

### Semantic Color Usage (Professional Standards)

Use colors with semantic meaning, not decoration:

**Success/Positive Metrics** — `var(--positive)` (green):
- Revenue growth, user acquisition, completion rates
- Up arrows, positive percentages, "good" status indicators

**Warning/Caution** — `var(--warning)` (amber):
- Metrics approaching thresholds, pending statuses
- Neutral alerts, "attention needed" indicators

**Error/Negative Metrics** — `var(--negative)` (red):
- Declining metrics, failures, critical alerts
- Down arrows, negative percentages, error states

**Info/Primary Actions** — `var(--info)` (blue):
- Primary CTAs, informational highlights, process steps

**Accent Restraint Rules**:
- **KPI grids with 4+ cards:** Use at most 2 accent colors — `var(--accent)` for the single most important metric, `var(--text)` for others
- **Never colorize numbers randomly** — color must indicate semantic meaning
- **Delta indicators only:** Use `var(--positive)`/`var(--negative)` for arrows and percentages, not main values

### Professional Card System

Modern card styling beyond basic borders:

```css
.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;                    /* Larger than 8px for premium feel */
  box-shadow: 0 1px 3px rgba(0,0,0,0.05); /* Subtle depth in light mode */
  padding: 24px;                          /* Generous internal spacing */
  transition: all 0.15s ease;
}

/* Light mode: visible shadows */
.theme-light .card {
  box-shadow: 0 1px 3px rgba(0,0,0,0.05), 0 0 0 1px rgba(0,0,0,0.03);
}

/* Dark mode: border emphasis */
.theme-dark .card {
  box-shadow: 0 0 0 1px var(--border);
}

.card:hover {
  /* Light mode: deeper shadow */
  box-shadow: 0 4px 16px rgba(0,0,0,0.08), 0 0 0 1px rgba(0,0,0,0.03);
}

.theme-dark .card:hover {
  /* Dark mode: brighter border */
  box-shadow: 0 0 0 1px rgba(255,255,255,0.08);
}
```

**Key principles:**
- 12px border radius for premium feel (not 8px)
- Light mode emphasizes shadows, dark mode emphasizes borders
- Consistent 24px internal padding
- Hover states enhance the existing visual style

### Chart.js Professional Styling

Beyond library defaults — apply these to every chart:

```css
.chart-container {
  padding: 40px;          /* Breathing room around chart */
  min-height: 360px;      /* Substantial presence on dashboard */
  background: var(--surface);
  border-radius: 12px;
  border: 1px solid var(--border);
}

/* Remove excessive grid lines */
.chart-canvas {
  border-radius: 8px;     /* Inner chart gets smaller radius */
}
```

**Chart configuration enhancements:**
- Custom padding: `layout: { padding: { top: 30, right: 30, bottom: 30, left: 30 } }`
- Rounded corners on bars: `borderRadius: 4`
- Professional grid opacity: Light mode `rgba(0,0,0,0.04)`, Dark mode `rgba(255,255,255,0.02)`
- Thoughtful color palettes matching theme accent
- Axis label sizing: minimum 13px for readability
- Remove default animations: `Chart.defaults.animation = false`

### Spacing
- **8px grid** — all spacing in multiples: 4, 8, 12, 16, 24, 32, 48, 64, 96px
- **Generous padding** — `p-6` to `p-8` on cards, `px-8` on containers
- **Container:** `max-w-7xl mx-auto px-4 sm:px-6 lg:px-8`
- **Card gaps:** `gap-6` minimum

### Mobile Responsiveness (Critical)
**All visualizations must work flawlessly on mobile. No horizontal overflow allowed.**

```css
/* Required mobile breakpoints */
@media (max-width: 768px) {
  .dashboard-grid {
    grid-template-columns: 1fr; /* Single column on tablet */
    gap: 1rem; /* Reduced gap */
  }
  .chart-section {
    grid-template-columns: 1fr; /* Stack chart sections */
  }
  .container {
    padding: 1rem; /* Reduced container padding */
  }
}

@media (max-width: 375px) {
  .container {
    padding: 0.75rem; /* Minimal padding on small phones */
  }
  .kpi-card, .chart-card {
    padding: 1rem; /* Reduced card padding */
  }
  .filter-toolbar {
    flex-direction: column; /* Stack filters vertically */
    align-items: stretch;
  }
}
```

**Testing checklist:**
- ✅ No horizontal scrolling at 768px viewport
- ✅ No horizontal scrolling at 375px viewport  
- ✅ All text remains readable (min 16px)
- ✅ Touch targets are ≥44px
- ✅ Charts resize appropriately

### Card Hover Microinteractions
All cards should have subtle hover effects — shadow elevation ONLY, no transforms:
```css
.card, .stat-card, .kpi-card, .stat-item, .chart-container {
  transition: box-shadow 0.2s ease;
}
.card:hover, .stat-card:hover, .kpi-card:hover, .stat-item:hover {
  box-shadow: 0 0 0 1px var(--border), 0 8px 16px rgba(0,0,0,0.08);
}
```
- NO `translateY` or `scale` on card hover — it looks cheap
- Timeline items: subtle background highlight on hover
- Architecture nodes: subtle shadow elevation on hover
- List items: subtle background tint on hover, not translateX

### :focus-visible Standard
Every file MUST include:
```css
*:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
  border-radius: 4px;
}
```

### SVG Chart Hover Pattern
For inline SVG chart elements (bars, donut segments, data points):
```css
svg rect, svg circle, svg path.data-element {
  transition: opacity 0.2s, transform 0.2s;
}
svg rect:hover, svg circle:hover {
  opacity: 0.8;
  filter: brightness(1.1);
}
```
Always add `<title>` elements inside SVG shapes for native browser tooltips:
```html
<rect x="10" y="20" width="50" height="100">
  <title>Revenue: $142K</title>
</rect>
```

### Visual Polish (Stripe/Vercel-level)
- **Border radius:** `8px` consistently (not 12px, not 16px — Stripe uses 8px)
- **Shadows (dark mode):** Almost none — `box-shadow: 0 0 0 1px var(--border)` is sufficient. Let borders do the work.
- **Shadows (light mode):** Subtle layers — `box-shadow: 0 0 0 1px rgba(0,0,0,0.03), 0 2px 4px rgba(0,0,0,0.05)`
- **Card hover:** Shadow deepens slightly. NO translateY, NO scale transforms. Just: `box-shadow: 0 0 0 1px rgba(0,0,0,0.03), 0 8px 16px rgba(0,0,0,0.08)`
- **Clean card borders:** `border: 1px solid var(--border)` — no gradient borders, no colored left/top borders
- **Glass morphism:** Use sparingly, only for floating UI elements (menus, tooltips), not cards
- **Restrained accents:** Use accent color for ONE thing per section (a button, a link, an icon) — not everywhere
- **Transitions:** `transition: box-shadow 0.2s ease` — only animate what changes

### Background Atmosphere (Avoid Generic Dark)
Every visualization should have a SUBTLE background personality. Avoid flat `--bg` backgrounds that look like every dark template. Choose ONE technique per file:

1. **Subtle radial gradient** — a single, very faint radial gradient from the center:
   ```css
   body { background: var(--bg); }
   body::before {
     content: ''; position: fixed; inset: 0; z-index: -1;
     background: radial-gradient(ellipse 80% 50% at 50% 20%, 
       color-mix(in srgb, var(--accent), transparent 92%), transparent);
   }
   ```
2. **Noise/grain texture** (Vercel-style): use a tiny inline SVG noise filter:
   ```css
   body::after {
     content: ''; position: fixed; inset: 0; z-index: -1; opacity: 0.03;
     background: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
   }
   ```
3. **Dot grid** (use sparingly, only for tech/architecture files):
   ```css
   body { background-image: radial-gradient(circle, rgba(255,255,255,0.03) 1px, transparent 1px);
     background-size: 24px 24px; }
   ```

Choose the technique that matches the content personality. Timelines → radial gradient. Dashboards → grain. Architecture → dot grid. Slide decks → radial gradient with content-specific accent color.

### Dropdown Menu Styling (Mandatory)
The settings/export dropdown MUST look polished:
```css
.dropdown-menu {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.3), 0 0 0 1px rgba(255,255,255,0.05);
  padding: 4px;
  min-width: 160px;
  animation: dropdownIn 0.15s ease;
}
.dropdown-menu button {
  width: 100%; text-align: left; padding: 8px 12px;
  border-radius: 6px; border: none; background: transparent;
  color: var(--text-secondary); font-size: 0.875rem; cursor: pointer;
  transition: background 0.15s, color 0.15s;
}
.dropdown-menu button:hover {
  background: var(--surface-hover); color: var(--text);
}
@keyframes dropdownIn {
  from { opacity: 0; transform: translateY(-4px); }
  to { opacity: 1; transform: translateY(0); }
}
```

### Entrance Animations (Mandatory for All Files)
Every file MUST have subtle entrance animations. Static-feeling pages score low on interactivity. Use CSS-only `@keyframes` on page load:
```css
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(12px); }
  to { opacity: 1; transform: translateY(0); }
}
.card, .step, .quote-card, section > * {
  animation: fadeInUp 0.5s ease both;
}
/* Stagger children */
.card:nth-child(1) { animation-delay: 0s; }
.card:nth-child(2) { animation-delay: 0.08s; }
.card:nth-child(3) { animation-delay: 0.16s; }
.card:nth-child(4) { animation-delay: 0.24s; }
```
Also add hover states on ALL cards/items — even "static" content like cheatsheets and quote cards:
```css
.card:hover, .command-group:hover, blockquote:hover {
  background: var(--surface-hover);
  box-shadow: 0 0 0 1px var(--border), 0 8px 16px rgba(0,0,0,0.08);
}
```

### Theme-Adaptive Content (Carousels, Posters)
When cards use decorative gradients (e.g., Instagram-style pastel slides), the gradients MUST adapt to the theme. Don't use fixed pastel colors that look identical in dark/light mode:
```css
/* BAD — same gradient in both themes */
.card { background: linear-gradient(135deg, #ff9a9e, #fecfef); }

/* GOOD — theme-adaptive gradients */
.theme-dark .card-1 { background: linear-gradient(135deg, #1a1a2e, #16213e); }
.theme-light .card-1 { background: linear-gradient(135deg, #ff9a9e, #fecfef); }
```

### Slide Deck Light Mode
Slide decks are designed dark-first, but light mode must NOT feel like an afterthought. For presentations in light mode:
- Use a subtle warm gray background (`#f5f5f0`) not pure white
- Add a faint top-down gradient for depth
- Ensure headings use dark text with sufficient weight
- Grid/glow backgrounds should switch to subtle dot patterns or soft gradients in light mode

### Chart Accessibility (Mandatory)
All CSS-only charts (bars, radar, donut) and Chart.js charts MUST expose data to screen readers:
```html
<div role="img" aria-label="Bar chart showing React at 85%, Vue at 72%, Angular at 58%">
  <!-- visual chart here -->
  <div class="sr-only">React: 85%. Vue: 72%. Angular: 58%.</div>
</div>
```
Add `.sr-only { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0,0,0,0); }` to every file.

### Visual Restraint Anti-Patterns (NEVER DO)
- ❌ **Floating gradient orbs** — decorative blurred circles behind content look amateurish
- ❌ **Rainbow/gradient borders** — colored top-borders or left-borders on cards scream "template"
- ❌ **Gradient text** on headings — use solid colors. Gradient text is a 2020 trend that aged poorly
- ❌ **Scale transforms on hover** — `scale(1.02)` on cards feels janky, not premium
- ❌ **Glow effects** — `box-shadow: 0 0 20px rgba(blue)` never looks good
- ❌ **Decorative animations** — spinning rings, floating particles, pulsing dots are noise
- ❌ **Color-coded borders** — left/top colored borders on cards feel like Bootstrap components
- ❌ **Stat numbers with gradient text** — use a solid accent color or var(--text) instead

### Accessibility (Mandatory)

Every visualization MUST meet these baseline accessibility requirements:

**Minimum Accessibility Checklist:**
- [ ] Skip-to-content link present
- [ ] `role="region"` on all major sections with `aria-label`
- [ ] `role="group"` on comparison sections, architecture layers, slide groups
- [ ] `role="list"` / `role="listitem"` on timeline sections and items
- [ ] `aria-label` on all icon-only buttons
- [ ] `aria-describedby` on chart sections linking to data descriptions
- [ ] `:focus-visible` with `border-radius: 4px` on all interactive elements
- [ ] `aria-live="polite"` on slide counters / dynamic content

- **Skip navigation:** Add `<a href="#main-content" class="skip-link">Skip to content</a>` at the top of `<body>`. Style: visually hidden, visible on focus.
- **Landmark roles:** Use `<main>`, `<nav>`, `<header>`, `<footer>`, `<section>` with `aria-label` where there are multiple of the same landmark.
- **Interactive elements:** All buttons, links, and controls must have `aria-label` if their text content is not descriptive (e.g., icon-only buttons).
- **Focus indicators:** Add visible `:focus-visible` styles on all interactive elements: `outline: 2px solid var(--accent); outline-offset: 2px;`
- **Color-only indicators:** Status dots, colored badges, etc. MUST have a text alternative. E.g., a green status dot should also show "Healthy" text or `aria-label="Status: Healthy"`.
- **Charts and diagrams (MANDATORY):** 
  - Wrap chart canvas in container with `role="img" aria-label="Description of what the chart shows"`
  - **ALL charts MUST have hover tooltips enabled** — never disable Chart.js tooltips
  - Include data table alternative or visually-hidden summary for screen readers
  - Use high contrast colors with sufficient color difference between data series
- **Screen reader descriptions:** Add `aria-description` or visually-hidden text describing key takeaways for complex visualizations.
- **Slide decks:** Use `aria-live="polite"` on the slide counter, and `aria-label` on navigation buttons.

### Icons (Inline SVG Only)

Use inline SVG for all icons. **Never use emoji as icons** — they look unprofessional and render inconsistently.

Use simple Lucide-style paths: 24x24 viewBox, stroke-based, `stroke="currentColor" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"`.

Common icons to use:
- Moon/Sun for theme toggle
- Download arrow for PNG export  
- Printer for print
- Arrow left/right for navigation
- Check/X for pros/cons
- Globe, Smartphone, Monitor for device types

### Animations (CSS-First with Modern Features)

**CSS animations are the primary system.** They're reliable, performant, and never break from JS scoping issues.

See [references/animations.md](references/animations.md) for complete patterns.

**Modern CSS Animation Features (Progressive Enhancement):**

**Scroll-driven animations** (Chrome 115+) — Replace JS scroll listeners:
```css
.scroll-reveal {
  animation: fadeInUp 1ms linear;
  animation-timeline: view(); /* Animates based on viewport visibility */
}
.progress-bar {
  animation: grow 1ms linear;  
  animation-timeline: scroll(root inline); /* Animates based on page scroll */
}
```

**Three animation techniques (all baked into the skeleton):**

1. **Page-load entrance:** Add class `animate` (+ `delay-1` through `delay-6` for stagger)
   ```html
   <h1 class="animate">Title</h1>
   <div class="card animate delay-1">Card 1</div>
   <div class="card animate delay-2">Card 2</div>
   ```

2. **Scroll reveal:** Add `data-reveal` attribute. JS adds `.reveal` class (opacity:0), then `.visible` on scroll.
   ```html
   <section data-reveal>This fades in when scrolled into view</section>
   ```

3. **Number counters:** Add `data-count` attribute. JS animates from 0 to target.
   ```html
   <span data-count="77" data-suffix="%">77%</span>
   ```

**Hover effects** are pure CSS, baked into `.card` (translateY + scale on :hover).

**Rules:**
- Content is ALWAYS visible in CSS — JS animations are progressive enhancement
- Use `@keyframes` for page-load animations, CSS `transition` for hover/state changes
- `data-reveal` elements show their final content if JS fails (no blank sections)
- `prefers-reduced-motion` disables all animations automatically
- `data-reveal` elements MUST have `opacity: 1` as their default CSS state. JS adds `.reveal` class (which sets `opacity: 0`), then `.visible` restores it. If JS fails, content stays visible.
- On page load, trigger ALL reveal elements visible after a short delay (500ms) so full-page screenshots and PNG exports capture all content:
  ```javascript
  setTimeout(function() { document.querySelectorAll('.reveal').forEach(function(el) { el.classList.add('visible'); }); }, 500);
  ```

