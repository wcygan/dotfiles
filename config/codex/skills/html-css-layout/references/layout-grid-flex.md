# Layout With Normal Flow, Grid, And Flexbox

## Description

Use this reference when choosing layout primitives for pages, components, cards, toolbars, forms, and dashboards. The goal is to let the browser handle flow and alignment with the fewest layout rules.

Browse current official docs before making precise claims about Grid track sizing, Flexbox alignment, wrapping, gaps, or browser behavior.

## Docs To Browse

- MDN, Relationship of Grid layout with other layout methods: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_grid_layout/Relationship_of_grid_layout_with_other_layout_methods
- MDN, Basic concepts of Flexbox: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_flexible_box_layout/Basic_concepts_of_flexbox
- MDN, Basic concepts of Grid layout: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_grid_layout/Basic_concepts_of_grid_layout
- web.dev, Learn CSS Layout: https://web.dev/learn/css/layout
- CSSWG, CSS Grid Layout Module Level 2: https://www.w3.org/TR/css-grid-2/

## Guidance

- Start with normal flow when the document order already solves the layout.
- Use Flexbox when the main problem is distributing or aligning items along one axis.
- Use Grid when the main problem has rows and columns, named areas, or repeated tracks.
- Put page structure on parent containers. Put component internals inside the component.
- Use `gap` for spacing between grid or flex children. Avoid margins that depend on sibling position.
- Prefer `repeat(auto-fit, minmax(...))` for resilient galleries and dashboards.
- Avoid absolute positioning for primary layout. Reserve it for overlays, badges, and deliberate stacking.

## Decision Shortcut

- Navbar or toolbar: Flexbox.
- Icon plus text: Flexbox.
- Card gallery: Grid.
- Dashboard with sidebar, header, and panels: Grid.
- Form with labels and controls in aligned columns: Grid, with single-column fallback.
- Component internals with stacked content and one footer row: Grid or Flexbox, whichever reads simpler.
