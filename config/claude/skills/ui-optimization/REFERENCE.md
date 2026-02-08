# UI Optimization Reference

Design patterns, best practices, and checklists for UI optimization agents.

## Visual Design Principles

### Color & Contrast

**WCAG Contrast Ratios:**
- Normal text (< 18pt): 4.5:1 (AA), 7:1 (AAA)
- Large text (≥ 18pt or 14pt bold): 3:1 (AA), 4.5:1 (AAA)
- UI components: 3:1 minimum

**Common fixes:**
- `text-gray-400` → `text-gray-900` (light backgrounds)
- `text-gray-600` → `text-gray-100` (dark backgrounds)
- Avoid low-opacity text on colored backgrounds

**Tools to recommend:**
- WebAIM Contrast Checker
- Browser DevTools → Accessibility panel

### Typography

**Hierarchy:**
- Scale: 12px, 14px, 16px, 18px, 24px, 30px, 36px, 48px (1.2 ratio)
- Weight: 400 (normal), 500 (medium), 600 (semibold), 700 (bold)
- Line height: 1.5 for body, 1.2 for headings

**Readability:**
- Max line length: 60-80 characters (prose), 40-60 (UI)
- Paragraph spacing: 1.5× line height
- Letter spacing: -0.01em for large headings, 0 for body

**Common issues:**
- Too many font weights (use 2-3 max)
- Inconsistent sizing (missing scale)
- Poor line height (too tight < 1.3)

### Spacing & Layout

**Spacing scale (Tailwind-style):**
```
0.25rem (1) → 0.5rem (2) → 0.75rem (3) → 1rem (4) → 1.5rem (6) → 2rem (8) → 3rem (12) → 4rem (16)
```

**Common patterns:**
- Button padding: `px-4 py-2` or `px-6 py-3`
- Card padding: `p-6` or `p-8`
- Section spacing: `mb-12` or `mb-16`
- Grid gaps: `gap-4` or `gap-6`

**Layout smells:**
- Magic numbers (e.g., `margin: 13px` instead of using scale)
- Inconsistent spacing within component families
- Too much nesting (> 3 levels of flex/grid)

### Responsive Design

**Breakpoints (mobile-first):**
- `sm`: 640px (large phones, small tablets)
- `md`: 768px (tablets)
- `lg`: 1024px (laptops)
- `xl`: 1280px (desktops)
- `2xl`: 1536px (large desktops)

**Mobile-first strategy:**
```css
/* Base: mobile */
.card { padding: 1rem; }

/* Tablet and up */
@media (min-width: 768px) {
  .card { padding: 2rem; }
}
```

**Common issues:**
- Fixed widths without responsive alternatives
- Horizontal overflow on mobile
- Tiny touch targets (< 44×44px)
- Text too small on mobile (< 16px causes zoom on iOS)

---

## Accessibility (WCAG 2.1 AA)

### Keyboard Navigation

**Requirements:**
- All interactive elements reachable via Tab
- Logical tab order (matches visual order)
- Visible focus indicators (outline, ring, underline)
- Escape key closes modals/dropdowns
- Arrow keys navigate within components (select, tabs, menus)

**Focus indicators:**
```css
/* ✅ Good: Visible, high-contrast */
button:focus-visible {
  outline: 2px solid #3B82F6;
  outline-offset: 2px;
}

/* ❌ Bad: Invisible or removed */
button:focus {
  outline: none;
}
```

### ARIA & Semantics

**Semantic HTML first:**
- Use `<button>`, `<a>`, `<input>` instead of `<div role="button">`
- Use `<nav>`, `<main>`, `<article>` for landmarks
- Use `<h1>`-`<h6>` for headings (don't skip levels)

**ARIA patterns:**
- `aria-label`: Label when visible text is insufficient
- `aria-labelledby`: Reference another element's text
- `aria-describedby`: Additional context (errors, hints)
- `aria-expanded`: Disclosure state (dropdowns, accordions)
- `aria-hidden="true"`: Hide decorative elements from screen readers

**Common mistakes:**
- Missing alt text on images (`alt=""` for decorative)
- Links with "click here" or "read more" (not descriptive)
- Forms without `<label>` or `aria-label`
- Modals without focus trap or `aria-modal="true"`

### Screen Reader Testing

**Quick checks:**
- Does the component announce its purpose?
- Can you complete tasks without seeing the screen?
- Are state changes announced (loading, errors, success)?

**VoiceOver (macOS):**
```
Cmd + F5          - Toggle VoiceOver
VO + Right Arrow  - Next item
VO + Space        - Activate
VO + A            - Read all
```

### Color Blindness

**Rules:**
- Never rely on color alone (use icons, text, patterns)
- Test with grayscale filter
- Use colorblind-safe palettes (avoid red-green only)

**Common issues:**
- Error states in red only (add icon + text)
- Success in green only (add checkmark)
- Chart lines differentiated by color only

---

## Performance Optimization

### CSS Performance

**Efficient selectors:**
```css
/* ✅ Fast: Class selector */
.button { }

/* ⚠️ Slower: Descendant combinator */
.nav ul li a { }

/* ❌ Slow: Universal selector */
* { box-sizing: border-box; }
```

**Layout thrashing (avoid):**
```js
// ❌ Bad: Read-write-read-write cycle
element.style.width = element.offsetWidth + 10 + 'px'; // Read + write
element.style.height = element.offsetHeight + 10 + 'px'; // Read + write

// ✅ Good: Batch reads, then batch writes
const width = element.offsetWidth;
const height = element.offsetHeight;
element.style.width = width + 10 + 'px';
element.style.height = height + 10 + 'px';
```

### Animation Performance

**Use `transform` and `opacity` (GPU-accelerated):**
```css
/* ✅ Good: Smooth 60fps */
.slide-in {
  transform: translateX(100%);
  transition: transform 0.3s ease;
}

/* ❌ Bad: Triggers layout, janky */
.slide-in {
  left: 100%;
  transition: left 0.3s ease;
}
```

**Will-change hint (use sparingly):**
```css
.carousel-item {
  will-change: transform; /* Hint to browser: optimize this */
}

/* Remove after animation */
.carousel-item:not(.animating) {
  will-change: auto;
}
```

**Common issues:**
- Animating `width`, `height`, `top`, `left` (use `transform`)
- No `will-change` for complex animations
- Too many simultaneous animations (> 5-6)

### Bundle Size

**CSS bloat sources:**
- Unused utility classes (use PurgeCSS/Tailwind JIT)
- Duplicate styles (consolidate into classes)
- Large icon fonts (use SVG sprites)
- Unoptimized images (use WebP, responsive images)

**Quick wins:**
- Remove unused CSS (check coverage in DevTools)
- Extract critical CSS for above-fold content
- Lazy load non-critical CSS

---

## Component Patterns

### Buttons

**Accessible button:**
```tsx
<button
  type="button"
  className="px-4 py-2 bg-blue-600 text-white rounded-md
             hover:bg-blue-700 focus-visible:ring-2 focus-visible:ring-blue-500
             disabled:opacity-50 disabled:cursor-not-allowed"
  disabled={loading}
  aria-busy={loading}
>
  {loading ? 'Loading...' : 'Submit'}
</button>
```

**Checklist:**
- [ ] Min 44×44px touch target
- [ ] Visible focus indicator
- [ ] Disabled state with `aria-busy` or `aria-disabled`
- [ ] Loading state with text change or spinner
- [ ] High contrast (3:1 minimum)

### Forms

**Accessible form field:**
```tsx
<div className="space-y-2">
  <label htmlFor="email" className="block text-sm font-medium">
    Email address
  </label>
  <input
    id="email"
    type="email"
    aria-describedby={error ? 'email-error' : undefined}
    aria-invalid={!!error}
    className="w-full px-3 py-2 border rounded-md focus:ring-2 focus:ring-blue-500"
  />
  {error && (
    <p id="email-error" className="text-sm text-red-600" role="alert">
      {error}
    </p>
  )}
</div>
```

**Checklist:**
- [ ] `<label>` with `htmlFor` matches input `id`
- [ ] Error messages with `aria-describedby` and `role="alert"`
- [ ] Required fields marked with `aria-required` or `required`
- [ ] Autocomplete attributes for common fields (`autocomplete="email"`)
- [ ] Validation on blur, not on every keystroke

### Modals/Dialogs

**Accessible modal:**
```tsx
<dialog
  open={isOpen}
  aria-labelledby="modal-title"
  aria-describedby="modal-description"
  className="backdrop:bg-black/50"
>
  <div className="p-6">
    <h2 id="modal-title">Confirm deletion</h2>
    <p id="modal-description">This action cannot be undone.</p>
    <div className="flex gap-2 mt-4">
      <button onClick={onCancel}>Cancel</button>
      <button onClick={onConfirm}>Delete</button>
    </div>
  </div>
</dialog>
```

**Checklist:**
- [ ] Focus trapped inside modal (can't tab out)
- [ ] Escape key closes modal
- [ ] Focus returns to trigger element on close
- [ ] `aria-labelledby` and `aria-describedby`
- [ ] Backdrop prevents interaction with page behind

---

## Tools & Testing

### Browser DevTools

**Lighthouse (Performance + A11y):**
- Chrome DevTools → Lighthouse tab
- Run audit (Performance, Accessibility, Best Practices)
- Focus on red/orange items first

**Accessibility Inspector:**
- Chrome DevTools → Accessibility panel
- Shows ARIA tree, contrast ratios
- Simulate vision deficiencies (color blindness, blurred vision)

**Coverage Tool:**
- Chrome DevTools → Coverage tab
- Shows unused CSS/JS (% utilized)
- Candidates for removal or lazy loading

### Command-line Tools

**Axe-core (accessibility testing):**
```bash
npm install -D @axe-core/cli
npx axe http://localhost:3000 --tags wcag2aa
```

**Lighthouse CI:**
```bash
npm install -D @lhci/cli
lhci autorun --collect.url=http://localhost:3000
```

---

## Common Anti-patterns

### Visual

- ❌ Inconsistent spacing (mixing px values, no scale)
- ❌ Too many colors (> 5-6 primary colors)
- ❌ Low contrast text (gray-400 on white)
- ❌ Overly complex shadows (multiple box-shadows)

### Accessibility

- ❌ Missing alt text (`<img src="..." />` without `alt`)
- ❌ Click handlers on `<div>` (use `<button>`)
- ❌ No focus indicators (`:focus { outline: none; }`)
- ❌ Poor heading hierarchy (h1 → h3, skipping h2)

### Performance

- ❌ Animating layout properties (`width`, `height`, `top`)
- ❌ Unused CSS (large Tailwind bundle without purging)
- ❌ Synchronous layout reads in loops (layout thrashing)
- ❌ Inline styles instead of classes (no caching)

---

## Decision Framework

When multiple improvements conflict, prioritize:

1. **Accessibility** - Always fix critical a11y issues first (keyboard nav, screen readers, contrast)
2. **Functionality** - Ensure the component works correctly
3. **Performance** - Fix performance blockers (janky animations, slow renders)
4. **Visual Polish** - Improve aesthetics, consistency, spacing

If the user has a design system, **follow it religiously**. Don't introduce new spacing values, colors, or patterns unless explicitly requested.
