# Responsive Design

## Description

Use this reference when making layouts adapt across phones, tablets, desktops, embedded panes, and resizable containers. Prefer intrinsic layout first; add breakpoints only when the composition actually needs a different arrangement.

Browse current official docs before making precise claims about media queries, container queries, viewport units, reduced motion, or browser support.

## Docs To Browse

- MDN, Responsive design: https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/CSS_layout/Responsive_Design
- MDN, CSS container queries: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_containment/Container_queries
- MDN, Using media queries: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_media_queries/Using_media_queries
- web.dev, Responsive design: https://web.dev/learn/design
- MDN, prefers-reduced-motion: https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion

## Guidance

- Use fluid defaults: normal flow, wrapping, `max-width`, `minmax()`, `clamp()`, and percentage or container-relative sizing.
- Use breakpoints for layout decisions, not device names.
- Use container queries when a component should react to its own available space rather than the viewport.
- Keep source order meaningful at every size.
- Avoid horizontal page overflow. Allow local overflow only for code blocks, dense tables, and intentionally scrollable regions.
- Test at narrow, medium, and wide widths. Include long labels and uneven content in the test data.
- Respect reduced motion for nonessential animation and transitions.

## Responsive Checklist

- Navigation wraps or collapses without covering content.
- Cards and panels keep stable spacing when content length changes.
- Form controls remain at usable sizes.
- Text line length stays readable.
- Images and media have stable aspect ratios.
- Focus outlines remain visible at every viewport.
