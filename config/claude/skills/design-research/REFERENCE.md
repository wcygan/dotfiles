# Design Research - Reference Guide

This reference provides detailed guidance for conducting thorough website design research.

## Research Methodology

### Phase 1: Initial Reconnaissance (5 minutes)

**Goal:** Get a high-level understanding of the site

1. **Visit the URL** and browse manually
2. **Take mental notes** of:
   - Overall aesthetic (modern, minimalist, bold, playful, corporate, etc.)
   - Primary colors used
   - Layout approach (centered, full-width, asymmetric, grid-based)
   - Navigation pattern (top nav, sidebar, hamburger, mega menu)
   - Notable interactions or animations

3. **Check multiple pages** if relevant:
   - Homepage (marketing/landing)
   - Product/service pages
   - Documentation or content pages
   - Sign-up/login flows (if accessible)

### Phase 2: Automated Capture (5 minutes)

**Goal:** Capture visual artifacts systematically

1. **Run screenshot script:**
   ```bash
   ./scripts/capture-screenshots.sh <URL>
   ```

2. **Review screenshots** to identify areas needing closer inspection

3. **Capture additional views** if needed:
   - Specific page states (modals open, forms with errors, etc.)
   - Scrolled positions to capture sticky headers
   - Interactive states (hover, focus) using Playwright's `page.hover()` and `page.focus()`

### Phase 3: CSS & Style Analysis (10 minutes)

**Goal:** Extract design system tokens

1. **Run style analyzer:**
   ```bash
   node scripts/analyze-styles.js <URL>
   ```

2. **Manually inspect with DevTools:**
   - Open browser DevTools
   - Inspect key elements (headers, buttons, forms)
   - Check computed styles tab for actual values
   - Look for CSS custom properties in `:root`
   - Examine hover/focus states

3. **Extract design tokens:**
   - Colors (convert rgb to hex for consistency)
   - Font families, sizes, weights
   - Spacing values (look for patterns: 4px, 8px, 16px, etc.)
   - Border radius values
   - Shadow values
   - Transition durations

### Phase 4: Component Analysis (10 minutes)

**Goal:** Document reusable UI patterns

1. **Identify component categories:**
   - Navigation components
   - Form elements
   - Buttons and CTAs
   - Cards and content containers
   - Modal/dialog patterns
   - Alerts/notifications
   - Loading states
   - Icons and iconography

2. **For each component type:**
   - Screenshot the component in isolation
   - Copy HTML structure from DevTools
   - Note key CSS properties
   - Document interactive states
   - Check accessibility (ARIA, semantic HTML)

3. **Look for composition patterns:**
   - How components nest
   - Common prop/variant patterns
   - Reusable utility classes

### Phase 5: Technology Detection (5 minutes)

**Goal:** Understand the underlying tech stack

1. **Framework detection:**
   - Check for React: `__REACT_DEVTOOLS_GLOBAL_HOOK__`, `data-reactroot`, `_reactRootContainer`
   - Check for Vue: `__VUE_DEVTOOLS_GLOBAL_HOOK__`, `data-v-` attributes
   - Check for Angular: `ng-version` attribute
   - Check for Svelte: `data-svelte` attributes
   - Check for Next.js: `__NEXT_DATA__` script tag
   - Check network tab for `.chunk.js` files (indicates code splitting)

2. **CSS framework/library detection:**
   - Tailwind: Look for utility classes like `flex`, `grid`, `px-4`, `text-lg`
   - Bootstrap: Look for classes like `container`, `row`, `col-*`
   - Material UI: Look for `Mui*` classes or `makeStyles-*`
   - Check `<link>` tags for external stylesheets

3. **Icon library detection:**
   - Font Awesome: `<i class="fa*">`
   - Heroicons: SVG paths with specific viewBox
   - Lucide: Check for `lucide-*` classes or imports
   - Material Icons: `<span class="material-icons">`

4. **Animation library detection:**
   - Framer Motion: Check for `motion.*` elements or `whileHover` props
   - GSAP: Check for `window.gsap` or TimelineMax
   - Anime.js: Check for `window.anime`
   - Check for CSS animations in stylesheets

### Phase 6: Layout & Responsive Analysis (10 minutes)

**Goal:** Understand how the site adapts to different screen sizes

1. **Inspect responsive breakpoints:**
   - Use DevTools responsive mode
   - Note at which widths layout changes occur
   - Common breakpoints: 640px (mobile), 768px (tablet), 1024px (desktop), 1280px (wide)

2. **Document responsive patterns:**
   - Mobile: Single column, hamburger menu, stacked cards
   - Tablet: 2-column grid, expanded navigation
   - Desktop: Full layout, sidebars, multi-column content
   - Wide: Max-width containers, increased spacing

3. **Check layout techniques:**
   - Flexbox: `display: flex`, `justify-content`, `align-items`
   - CSS Grid: `display: grid`, `grid-template-columns`, `gap`
   - Float-based (legacy)
   - Position-based (sticky headers, fixed sidebars)

### Phase 7: Report Generation (15 minutes)

**Goal:** Synthesize findings into actionable recommendations

1. **Use the report template** (`templates/report-template.md`)
2. **Fill in all sections** with specific values and examples
3. **Include code snippets** for unique patterns
4. **Provide implementation recommendations** based on detected stack
5. **Link screenshots** for visual reference
6. **Add next steps** tailored to the engineer's goal

---

## Common Design System Patterns

### Naming Conventions

**CSS Custom Properties:**
```css
/* Color naming */
--color-primary-500      /* Main primary color */
--color-primary-400      /* Lighter */
--color-primary-600      /* Darker */

/* Spacing scale */
--spacing-1  /* 0.25rem = 4px */
--spacing-2  /* 0.5rem = 8px */
--spacing-4  /* 1rem = 16px */

/* Typography */
--font-size-sm   /* 14px */
--font-size-base /* 16px */
--font-size-lg   /* 18px */
```

**Tailwind-style Utilities:**
- Colors: `bg-blue-500`, `text-gray-700`
- Spacing: `p-4`, `m-8`, `gap-6`
- Typography: `text-lg`, `font-bold`, `leading-relaxed`

### Common Color Palettes

**Neutral Grays (typical scale):**
- 50: Very light (backgrounds)
- 100-200: Light (borders, hover states)
- 300-400: Medium-light (disabled states, placeholders)
- 500: Medium (secondary text)
- 600-700: Medium-dark (primary text)
- 800-900: Very dark (headings, emphasis)

**Semantic Colors:**
- Success: Green (#10B981, #22C55E)
- Error: Red (#EF4444, #DC2626)
- Warning: Yellow/Orange (#F59E0B, #F97316)
- Info: Blue (#3B82F6, #0EA5E9)

### Typography Scales

**Common scales:**

**Type Scale (1.250 - Major Third):**
- 12px → 15px → 19px → 24px → 30px → 37px → 46px

**Type Scale (1.333 - Perfect Fourth):**
- 12px → 16px → 21px → 28px → 37px → 50px → 67px

**Type Scale (1.5 - Perfect Fifth):**
- 12px → 18px → 27px → 41px → 61px → 91px

**Tailwind default scale:**
- xs: 12px
- sm: 14px
- base: 16px
- lg: 18px
- xl: 20px
- 2xl: 24px
- 3xl: 30px
- 4xl: 36px

### Spacing Systems

**8px Grid (most common):**
- 0: 0px
- 1: 8px
- 2: 16px
- 3: 24px
- 4: 32px
- 5: 40px
- 6: 48px
- 8: 64px
- 10: 80px

**4px Base (Tailwind-style):**
- 0: 0px
- 1: 4px
- 2: 8px
- 4: 16px
- 6: 24px
- 8: 32px
- 12: 48px
- 16: 64px

---

## Playwright CLI Advanced Usage

### Interactive Mode

For sites requiring authentication or complex interactions:

```bash
# Launch browser in headed mode
npx playwright open <URL>

# Record actions
npx playwright codegen <URL>

# Save trace for debugging
npx playwright open <URL> --save-trace=trace.zip

# View trace
npx playwright show-trace trace.zip
```

### Element Inspection

```bash
# Get element text content
npx playwright evaluate <URL> --expression "document.querySelector('h1').textContent"

# Get computed styles
npx playwright evaluate <URL> --expression "
  const el = document.querySelector('.button');
  window.getComputedStyle(el);
"

# Get all links
npx playwright evaluate <URL> --expression "
  Array.from(document.querySelectorAll('a')).map(a => ({
    text: a.textContent,
    href: a.href
  }))
"

# Check for accessibility
npx playwright evaluate <URL> --expression "
  Array.from(document.querySelectorAll('img')).filter(img => !img.alt)
"
```

### Custom Viewport Sizes

```bash
# Common device viewports
npx playwright screenshot --viewport-size=390,844 <URL> iphone-13.png    # iPhone 13
npx playwright screenshot --viewport-size=393,851 <URL> pixel-7.png     # Pixel 7
npx playwright screenshot --viewport-size=1024,1366 <URL> ipad-pro.png  # iPad Pro
npx playwright screenshot --viewport-size=1440,900 <URL> macbook.png    # MacBook Pro 13"
npx playwright screenshot --viewport-size=1920,1080 <URL> desktop.png   # Full HD
npx playwright screenshot --viewport-size=2560,1440 <URL> 2k.png        # 2K Display
```

### Emulate User Preferences

```bash
# Dark mode
npx playwright screenshot --color-scheme=dark <URL> dark.png

# Reduced motion
npx playwright screenshot --reduced-motion=reduce <URL> reduced-motion.png

# High contrast
npx playwright screenshot --forced-colors=active <URL> high-contrast.png
```

---

## Best Practices

### Research Quality

1. **Be thorough but focused**
   - If the engineer wants to replicate a specific page, focus deeply on that page
   - Don't try to document the entire site if only one section is relevant

2. **Prioritize actionable insights**
   - Exact color values > "blue-ish"
   - Specific font sizes > "large"
   - Implementation code snippets > vague descriptions

3. **Cross-reference similar systems**
   - "Similar to Material UI's Button component with custom styling"
   - "Uses a Tailwind-like spacing scale"
   - "Color palette resembles Radix Colors"

4. **Note what's NOT there**
   - "No animations or transitions"
   - "No dark mode support"
   - "Accessibility issues: missing alt text, no focus indicators"

### Report Writing

1. **Use concrete values**
   - ✅ `font-size: 16px; line-height: 1.5; font-weight: 400`
   - ❌ "Normal sized text"

2. **Include visual examples**
   - Reference screenshots: "See `viewport.png` for desktop layout"
   - Embed code snippets showing actual implementation

3. **Provide starting points**
   - Exact npm packages to install
   - Starter templates that match the stack
   - Links to similar open-source examples

4. **Make it scannable**
   - Use headings and sections
   - Bullet points over paragraphs
   - Code blocks for technical details
   - Tables for comparing variants

### Common Pitfalls

1. **Don't assume frameworks**
   - Just because it looks like React doesn't mean it is
   - Verify with actual detection, not guesses

2. **Don't miss mobile patterns**
   - Always capture mobile screenshots
   - Document how navigation changes on small screens
   - Note touch-friendly hit targets

3. **Don't overlook accessibility**
   - Check semantic HTML
   - Verify ARIA attributes
   - Test keyboard navigation
   - Check color contrast

4. **Don't ignore edge cases**
   - Error states in forms
   - Loading states
   - Empty states
   - Disabled/inactive states

---

## Quick Reference: CSS Property Cheat Sheet

### Layout
```css
display: flex | grid | block | inline-block
justify-content: flex-start | center | space-between | space-around
align-items: flex-start | center | flex-end | stretch
gap: <value>
grid-template-columns: repeat(3, 1fr) | <custom>
```

### Spacing
```css
margin: <value>
padding: <value>
gap: <value>  /* for flex/grid */
```

### Typography
```css
font-family: <value>
font-size: <value>
font-weight: 100-900 | normal | bold
line-height: <unitless-value> | <value>
letter-spacing: <value>
text-align: left | center | right
```

### Colors
```css
color: <value>
background-color: <value>
border-color: <value>
```

### Effects
```css
border-radius: <value>
box-shadow: <x> <y> <blur> <spread> <color>
opacity: 0-1
transition: <property> <duration> <easing>
```

### Positioning
```css
position: static | relative | absolute | fixed | sticky
top | right | bottom | left: <value>
z-index: <integer>
```

---

## Troubleshooting

### Playwright Issues

**Error: "Executable doesn't exist"**
```bash
npx playwright install chromium
```

**Error: "Navigation timeout"**
```bash
# Increase timeout
npx playwright screenshot --timeout=60000 <URL> output.png
```

**Error: "Page crashed"**
```bash
# Disable GPU acceleration
npx playwright screenshot --browser-args="--disable-gpu" <URL> output.png
```

### CORS Issues with Stylesheets

If external stylesheets can't be read due to CORS:
- Use WebFetch to get the stylesheet URL separately
- Note in report that some styles may be in external sheets
- Use computed styles from elements instead

### Authentication Required

If site requires login:
- Use Playwright's `npx playwright codegen` to record login flow
- Save auth state and reuse it
- Or document public pages only and note limitation

### Large/Slow Sites

If site is very large or slow to load:
- Focus on specific pages/sections
- Use `--wait-until=domcontentloaded` instead of `networkidle`
- Capture screenshots first, analyze later
- Set reasonable timeouts

---

## Additional Tools

### Browser Extensions (for manual research)

- **WhatFont** - Identify fonts on hover
- **ColorZilla** - Pick colors from webpage
- **Pesticide** - Visualize CSS box model
- **React DevTools** - Inspect React component tree
- **Vue DevTools** - Inspect Vue component tree
- **Accessibility Insights** - Check accessibility issues

### Online Tools

- **Who Use What** (whatruns.com) - Detect technologies
- **BuiltWith** (builtwith.com) - Technology profiler
- **CSS Stats** (cssstats.com) - Analyze stylesheets
- **Color Contrast Checker** (webaim.org/resources/contrastchecker/)

### Complementary Skills

Consider using these other skills in combination:

- **`web-research`** - For researching the company/product context
- **`ux-review`** - For UX analysis beyond visual design
- **`frontend-design`** - For actually implementing the design
