---
name: design-research
description: Research website design, styling, and frontend implementation using Playwright CLI to capture screenshots and analyze structure. Use when a software engineer wants to understand and implement a similar design. Keywords: design research, website design, frontend analysis, UI study, design system, screenshot, Playwright
disable-model-invocation: true
context: fork
agent: Explore
allowed-tools: Bash, Read, Write, Grep, Glob, WebFetch
---

# Design Research

Research and analyze website design, styling, and frontend implementation to help engineers understand and replicate design patterns.

## Overview

This skill uses Playwright CLI to systematically capture screenshots, inspect HTML structure, analyze CSS styling, and document design systems. It produces a comprehensive report covering layout, typography, colors, spacing, components, and implementation recommendations.

## Prerequisites

Playwright CLI must be available. If not installed:
```bash
# Check if available
npx playwright --version

# Install if needed (user should approve)
npm install -D playwright
npx playwright install chromium
```

## Instructions

When this skill is activated, follow this research workflow:

### 1. Validate Target URL

- Confirm the URL with the user if not provided
- Check if the site is publicly accessible
- Note: This skill works best with public websites; authentication flows require additional setup

### 2. Screenshot Capture Strategy

Use Playwright CLI to capture multiple views:

```bash
# Full page screenshot
npx playwright screenshot --full-page <URL> full-page.png

# Viewport screenshot (above the fold)
npx playwright screenshot <URL> viewport.png

# Mobile viewport
npx playwright screenshot --viewport-size=375,667 <URL> mobile.png

# Tablet viewport
npx playwright screenshot --viewport-size=768,1024 <URL> tablet.png

# Dark mode (if supported)
npx playwright screenshot --color-scheme=dark <URL> dark-mode.png
```

Save all screenshots to a `design-research-output/` directory.

### 2.5. Bot Protection Handling (Automatic)

The skill automatically detects and handles bot protection using a feedback loop:

**Detection:**
- Screenshot file size < 50KB
- HTML content contains "Cloudflare", "checking your browser", "captcha"
- Page redirects to `/cdn-cgi/challenge-platform/*`

**Automatic Retry Strategy:**

1. **Standard Playwright** (default, fast)
   - No stealth overhead
   - Works for most public sites
   - If blocked, automatically tries strategy 2

2. **Camoufox Stealth Mode** (if blocked)
   - Firefox-based anti-detect browser (0% detection score normally)
   - Automatically installed via UV: `uv run capture-stealth.py`
   - Adds human-like behavior and realistic fingerprints
   - Modifies browser at C++ level (not patchable JS)
   - Success rate: ~70% against moderate Cloudflare protection

3. **Manual Fallback** (if stealth fails)
   - Provides clear instructions for manual browser capture
   - Includes DevTools extraction scripts (CSS, colors, typography)
   - Documents manual screenshot workflow
   - See `MANUAL-FALLBACK.md` for complete instructions

**User Communication:**
- Clearly indicate which strategy is being used
- Show progress and retry attempts
- Provide actionable manual instructions if automated methods fail
- Never silently fail - always explain what happened and why

**Note:** The capture script uses UV-based Python scripts with inline dependencies (no package.json needed). UV must be available (already in dotfiles Nix flake).

### 3. HTML Structure Analysis

Use Playwright to extract and analyze structure:

```bash
# Get full HTML
npx playwright open <URL> --save-trace=trace.zip

# Or use WebFetch to get HTML content
```

Analyze:
- Semantic HTML usage (header, nav, main, article, section, footer)
- Component hierarchy and nesting patterns
- Class naming conventions (BEM, utility-first, CSS modules, etc.)
- Data attributes and JavaScript hooks
- Accessibility landmarks and ARIA attributes

### 4. CSS & Styling Analysis

Examine styling patterns:

```bash
# Extract stylesheets
npx playwright evaluate <URL> --expression "Array.from(document.styleSheets).map(s => s.href)"

# Get computed styles for key elements
npx playwright evaluate <URL> --expression "
  const nav = document.querySelector('nav');
  window.getComputedStyle(nav);
"
```

Document:
- **Color palette**: Primary, secondary, accent, neutral colors
- **Typography**: Font families, sizes, weights, line heights, letter spacing
- **Spacing system**: Margins, padding, gaps (check for consistent scale like 4px/8px grid)
- **Breakpoints**: Media query values for responsive design
- **Shadows & effects**: Box shadows, border radius, transitions, animations
- **Layout patterns**: Flexbox, Grid, positioning strategies

### 5. Component Inventory

Identify reusable components:
- Navigation (header, sidebar, mobile menu)
- Buttons (primary, secondary, ghost, icon buttons)
- Forms (inputs, selects, checkboxes, validation states)
- Cards (content cards, product cards, feature cards)
- Modals/Dialogs
- Alerts/Notifications
- Loading states
- Icons (icon system/library used)

For each component, note:
- Visual appearance (from screenshots)
- HTML structure
- CSS patterns
- Interactive states (hover, active, focus, disabled)

### 6. Design System Detection

Check for design system indicators:
- CSS custom properties (CSS variables): `--color-primary`, `--spacing-md`
- Utility class patterns: Tailwind, UnoCSS, custom utilities
- Component library: Material UI, Chakra UI, Ant Design, shadcn/ui, etc.
- CSS framework: Bootstrap, Bulma, Foundation
- CSS-in-JS: Styled Components, Emotion, vanilla-extract

```bash
# Check for CSS custom properties
npx playwright evaluate <URL> --expression "
  Array.from(document.styleSheets)
    .flatMap(sheet => Array.from(sheet.cssRules))
    .filter(rule => rule.cssText.includes('--'))
    .map(rule => rule.cssText)
    .slice(0, 20)
"
```

### 7. Technology Stack Detection

Identify frontend technologies:

```bash
# Check for framework signatures
npx playwright evaluate <URL> --expression "
  ({
    react: !!document.querySelector('[data-reactroot], #root'),
    vue: !!window.Vue,
    angular: !!window.ng,
    svelte: !!document.querySelector('[data-svelte]'),
    nextjs: !!window.__NEXT_DATA__,
    gatsby: !!window.___gatsby,
    astro: !!document.querySelector('[data-astro-cid]')
  })
"
```

### 8. Performance & Optimization Notes

Observe:
- Image formats (WebP, AVIF, responsive images)
- Font loading strategies (FOUT, FOIT, preload)
- Code splitting / lazy loading patterns
- CSS delivery (critical CSS, async loading)

### 9. Generate Research Report

Create a markdown report (`design-research-report.md`) with:

```markdown
# Design Research Report: [Site Name]

**URL:** <target-url>
**Date:** <current-date>
**Purpose:** [Briefly state what the engineer wants to implement]

## Visual Overview

[Reference screenshots with brief descriptions]
- Full page: `full-page.png`
- Viewport: `viewport.png`
- Mobile: `mobile.png`
- Dark mode: `dark-mode.png` (if applicable)

## Design System

### Color Palette
- Primary: #XXXXXX
- Secondary: #XXXXXX
- Accent: #XXXXXX
- Neutral: #XXXXXX (shades: 50, 100, 200, ..., 900)
- Success/Error/Warning/Info states

### Typography
- Headings: [Font family, sizes, weights]
  - H1: ...
  - H2: ...
- Body: [Font family, size, line-height, weight]
- Code: [Monospace font]
- Font loading: [Strategy used]

### Spacing System
- Base unit: Xpx
- Scale: [e.g., 4, 8, 16, 24, 32, 48, 64]
- Grid: [If using grid system]

### Components
[For each major component:]
- **Component Name**
  - Visual: [Screenshot reference or description]
  - HTML structure: [Simplified markup]
  - Key styles: [Important CSS patterns]
  - States: [hover, active, disabled, etc.]
  - Accessibility: [ARIA attributes, keyboard navigation]

## Layout Patterns

- Page layout: [Flexbox/Grid/Float/etc.]
- Container widths: [max-width values, breakpoints]
- Responsive strategy: [Mobile-first, desktop-first, fluid]
- Breakpoints:
  - Mobile: Xpx
  - Tablet: Xpx
  - Desktop: Xpx
  - Wide: Xpx

## Technology Stack

- Framework: [React/Vue/Svelte/etc.]
- Meta-framework: [Next.js/Nuxt/SvelteKit/etc.]
- Component library: [Material UI/shadcn/etc.]
- CSS approach: [Tailwind/CSS Modules/Styled Components/etc.]
- Animation library: [Framer Motion/GSAP/etc.]
- Icons: [Heroicons/Lucide/Font Awesome/etc.]

## Implementation Recommendations

### Quick Start
[Recommended tools and libraries to replicate the design]

### Key Patterns to Replicate
1. [Pattern 1]: [Implementation approach]
2. [Pattern 2]: [Implementation approach]
3. [Pattern 3]: [Implementation approach]

### Suggested Component Structure
```
/components
  /ui
    Button.tsx
    Card.tsx
    Input.tsx
    ...
  /layout
    Header.tsx
    Footer.tsx
    Navigation.tsx
  /features
    ...
```

### Design Tokens (if applicable)
```css
/* colors.css */
:root {
  --color-primary: #XXXXXX;
  ...
}

/* spacing.css */
:root {
  --spacing-xs: 4px;
  ...
}
```

## Additional Notes

[Any unique patterns, gotchas, or interesting implementation details]

## Next Steps

1. Set up project with recommended stack
2. Implement design tokens/theme configuration
3. Build core UI components
4. Implement layout structure
5. Apply responsive patterns
6. Add interactions and animations
7. Optimize for performance

---

**Screenshots and detailed analysis available in:** `design-research-output/`
```

## Output

The skill produces:

1. **`design-research-output/`** directory containing:
   - `full-page.png` - Full page screenshot
   - `viewport.png` - Above-the-fold screenshot
   - `mobile.png` - Mobile viewport screenshot
   - `tablet.png` - Tablet viewport screenshot
   - `dark-mode.png` - Dark mode screenshot (if applicable)
   - Any additional screenshots captured

2. **`design-research-report.md`** - Comprehensive markdown report covering:
   - Visual overview with screenshot references
   - Design system documentation (colors, typography, spacing)
   - Component inventory with implementation details
   - Layout patterns and responsive strategies
   - Technology stack detection
   - Implementation recommendations

3. **Summary to user** - Brief overview of findings with actionable next steps

## Tips

- For complex sites, focus on the specific page/section the user wants to replicate
- If a design system is detected, prioritize documenting the system over individual components
- Include code snippets for unique patterns worth replicating
- Cross-reference similar open-source component libraries that match the style
- Note any accessibility patterns worth adopting
- If authentication is required, guide the user to use Playwright's interactive mode

## Error Handling

- If Playwright is not installed, prompt user to install it
- If site requires authentication, note it in the report and suggest manual exploration
- If screenshots fail, continue with HTML/CSS analysis and note the limitation
- For rate-limited or blocked sites, use WebFetch as fallback for HTML analysis
