---
name: html-css-layout
description: "Use when structuring, styling, reviewing, or teaching HTML and CSS for components, layouts, responsive pages, design systems, semantic markup, Grid, Flexbox, cascade architecture, accessibility, visual hierarchy, or clean frontend design. Browse current official HTML, CSS, MDN, web.dev, W3C, WCAG, and ARIA docs before giving precise guidance or making layout decisions."
---

# HTML CSS Layout

Use this skill to produce HTML and CSS that is understandable, maintainable, responsive, and accessible. Treat markup, layout, styling, and interaction states as separate design decisions.

Success means:
- HTML expresses document and component meaning before visual structure.
- CSS uses the simplest layout primitive that fits the job.
- Components own their internal styling; parents own placement.
- The answer or implementation cites current official docs for precise claims.
- Demos or examples are inspectable without a build step when useful.

## Workflow

1. Identify the surface: document shell, navigation, form, card list, dashboard, data table, component library, article artifact, or standalone demo.
2. Inspect local project conventions first: framework, CSS strategy, design tokens, existing components, naming, resets, accessibility helpers, and test/browser workflow.
3. Load the smallest relevant reference file from the map below.
4. Browse current official docs before precise claims about HTML semantics, CSS syntax, layout behavior, accessibility requirements, or browser support.
5. Choose semantics before layout. Prefer native elements and labels over ARIA or custom div controls.
6. Choose layout by dimensionality:
   - Use Flexbox for one-dimensional alignment, toolbars, nav rows, inline media, button contents, and wrapping chips.
   - Use Grid for two-dimensional page shells, dashboards, galleries, dense forms, and rows plus columns.
   - Use normal flow when it already produces the right reading order.
7. Define component boundaries. Parent layouts place children; components control their own spacing, typography, states, and variants.
8. Keep CSS low-specificity and tokenized. Prefer classes, custom properties, cascade layers, and small utilities over ID selectors, long descendant chains, and `!important`.
9. Verify the result in the narrowest meaningful loop: static file open, local dev server, browser screenshot, keyboard check, or existing tests.

## Reference Map

- `references/semantic-html.md`: document structure, sectioning, landmarks, native controls, and when `div` is acceptable.
- `references/layout-grid-flex.md`: choosing normal flow, Grid, Flexbox, alignment, gaps, nesting, and page/component layout split.
- `references/responsive-design.md`: intrinsic responsive layout, media queries, container queries, fluid sizing, and reduced motion.
- `references/css-architecture.md`: cascade, specificity, layers, custom properties, naming, resets, and keeping component CSS maintainable.
- `references/visual-design.md`: spacing, typography, hierarchy, color, density, shadows, borders, and clean design constraints.
- `references/accessibility-states.md`: keyboard paths, focus, labels, forms, landmarks, contrast, target size, and ARIA fallback.
- `references/media-images.md`: images, figures, aspect ratios, object fit, responsive media, and layout stability.
- `references/forms-validation.md`: form structure, labels, field groups, client validation, errors, and submission states.
- `references/tables-data.md`: tabular semantics, captions, header scope, responsive table containers, and data density.
- `references/navigation-disclosure.md`: nav patterns, skip links, details/summary, dialogs, popovers, tabs, and disclosure behavior.
- `references/motion-interaction.md`: transitions, animations, interaction feedback, view transitions, and reduced-motion safeguards.
- `references/debugging-validation.md`: DevTools workflows, layout overlays, computed styles, browser support checks, and validation passes.

## Demo Map

Use `examples/*.html` as vendored teaching artifacts. Each demo is static, shares the same navigation bar, and uses only HTML and CSS.

- `examples/semantic-document.html`: semantic page shell with landmarks, article cards, aside, and footer.
- `examples/grid-dashboard.html`: responsive dashboard shell using CSS Grid, named sections, and stable cards.
- `examples/flex-toolbar.html`: Flexbox toolbar, grouped controls, wrapping filters, and aligned media rows.
- `examples/responsive-cards.html`: intrinsic card gallery with `auto-fit`, `minmax()`, `aspect-ratio`, and readable metadata.
- `examples/form-accessibility.html`: accessible form layout with labels, help text, fieldsets, focus states, and error copy.
- `examples/cascade-tokens.html`: cascade layers, tokens, component variants, and theme-like overrides without specificity fights.
- `examples/media-objects.html`: stable media cards with figures, captions, aspect ratios, and `object-fit`.
- `examples/data-table.html`: accessible table with caption, scoped headers, status chips, and a responsive overflow wrapper.
- `examples/disclosure-navigation.html`: native details/summary disclosure groups, skip link, and section navigation.
- `examples/page-shell.html`: responsive app shell with header, sidebar navigation, main content, and aside regions.
- `examples/motion-states.html`: visible component states, transition tokens, and reduced-motion fallback.
- `examples/debugging-checklist.html`: inspectable layout debugging checklist for overflow, box model, cascade, and responsive checks.

## Implementation Rules

- Start from semantic markup, then add class names for styling hooks.
- Keep reading order and visual order aligned unless there is a strong accessibility reason and a tested keyboard path.
- Prefer `gap` over margin choreography inside Grid and Flexbox.
- Prefer `max-width`, `minmax()`, `clamp()` for dimensions, and container/media queries only when intrinsic layout is insufficient.
- Use logical properties such as `margin-inline`, `padding-block`, and `inset-inline` when the component does not depend on physical left/right direction.
- Use CSS custom properties for design tokens and component-local knobs.
- Prefer class selectors with one or two class names. Avoid IDs in CSS, deep ancestry, and `!important` unless overriding third-party CSS with a documented reason.
- Keep component states explicit: hover, active, focus-visible, disabled, selected, expanded, invalid, loading, and empty states where they apply.
- Never hide important text or controls behind hover-only interactions.

## Verification

Use the smallest check that proves the work:

- For standalone demos: open the HTML file or run a static server and verify desktop plus narrow widths.
- For component work: run the project typecheck/test and inspect the changed UI in a browser.
- For accessibility-sensitive work: tab through controls, inspect labels and names, and check contrast against WCAG.
- For responsive work: test at a narrow mobile width, a mid-width tablet range, and a desktop range.
- For CSS architecture changes: search for overly broad selectors, duplicated tokens, unnecessary `!important`, and layout rules leaking across components.

## Quality Bar

- The first viewport should show the actual product, tool, document, or demo, not a marketing wrapper.
- The layout should be stable when labels wrap, cards have uneven content, or controls enter focus.
- Text should fit inside its parent on mobile and desktop.
- Color should carry meaning and maintain contrast.
- Styling should be boring where the product is operational and more expressive only when the domain warrants it.
- Official docs are the source of truth for syntax, semantics, and accessibility. Bundled references are routing guides, not frozen copies of the platform.
