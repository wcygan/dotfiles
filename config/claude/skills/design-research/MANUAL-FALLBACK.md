# Manual Design Research Fallback

When automated tools are blocked by bot protection, use this manual workflow.

## Prerequisites

- Modern browser (Chrome, Firefox, Edge, Safari)
- Access to the target website (complete any CAPTCHAs)
- Basic knowledge of browser DevTools

## Step 1: Manual Screenshots

### Desktop
1. Open browser, navigate to target URL
2. Set viewport: Right-click → Inspect → Toggle device toolbar
3. Select "Responsive" mode, set to 1920x1080
4. Take screenshot: Right-click → "Capture full-size screenshot"

### Mobile
1. In DevTools device toolbar, select "iPhone 12" or set 390x844
2. Capture full-size screenshot

### Tablet
1. Select "iPad Pro" or set 1024x1366
2. Capture full-size screenshot

### Dark Mode
1. In DevTools: Cmd+Shift+P (Mac) or Ctrl+Shift+P (Windows)
2. Type "Rendering" → "Emulate CSS prefers-color-scheme: dark"
3. Take screenshot

## Step 2: Extract CSS Design Tokens

Open DevTools Console and run:

```javascript
// Extract CSS custom properties
const props = new Map();
const root = document.documentElement;
const styles = getComputedStyle(root);
for (let i = 0; i < styles.length; i++) {
  const prop = styles[i];
  if (prop.startsWith('--')) {
    props.set(prop, styles.getPropertyValue(prop).trim());
  }
}
console.table(Array.from(props));
```

## Step 3: Extract Color Palette

```javascript
// Get colors from key elements
const colors = new Set();
['body', 'header', 'nav', 'button', 'a', '.btn'].forEach(selector => {
  const els = document.querySelectorAll(selector);
  els.forEach(el => {
    const s = getComputedStyle(el);
    ['color', 'background-color', 'border-color'].forEach(prop => {
      const val = s[prop];
      if (val && val !== 'rgba(0, 0, 0, 0)') colors.add(val);
    });
  });
});
console.log(Array.from(colors));
```

## Step 4: Typography Analysis

```javascript
// Extract font information
const fonts = [];
['h1', 'h2', 'h3', 'body', 'p'].forEach(sel => {
  const el = document.querySelector(sel);
  if (el) {
    const s = getComputedStyle(el);
    fonts.push({
      element: sel,
      family: s.fontFamily,
      size: s.fontSize,
      weight: s.fontWeight,
      lineHeight: s.lineHeight
    });
  }
});
console.table(fonts);
```

## Step 5: Framework Detection

```javascript
// Detect frontend technologies
const tech = {
  react: !!document.querySelector('[data-reactroot], #root, #__next'),
  vue: !!window.Vue || !!document.querySelector('[data-v-]'),
  angular: !!window.ng || !!document.querySelector('[ng-version]'),
  svelte: !!document.querySelector('[data-svelte]'),
  nextjs: !!window.__NEXT_DATA__,
  tailwind: !!document.querySelector('[class*="flex"], [class*="grid"]')
};
console.table(tech);
```

## Step 6: Document Findings

Create a markdown file with your findings:

```markdown
# Manual Design Research: [Site Name]

**URL:** [url]
**Date:** [date]
**Method:** Manual browser capture (automated tools blocked)

## Screenshots
- Desktop: [attach desktop.png]
- Mobile: [attach mobile.png]
- Tablet: [attach tablet.png]

## Color Palette
[paste color results]

## Typography
[paste font results]

## Technology Stack
[paste tech detection results]

## CSS Variables
[paste CSS custom properties]

## Notes
[any observations about components, layout, interactions]
```

## Tips

- Use browser extensions like "ColorZilla" for precise color picking
- Use "Fonts Ninja" extension to identify fonts
- Use "WhatFont" for typography inspection
- Take notes on hover states, animations, transitions
- Document breakpoint behavior by resizing viewport

## Return to Claude

Once you have manual data:
1. Share findings with Claude
2. Claude will generate the full research report
3. Continue with implementation recommendations
