# Debugging And Validation

## Description

Use this reference when diagnosing layout bugs, CSS conflicts, overflow, specificity problems, responsive regressions, browser support uncertainty, or visual QA gaps. Debug from the rendered box tree and cascade, not from guesses.

Browse current official docs before making precise claims about DevTools features, browser compatibility, CSS support queries, validation tools, or layout inspectors.

## Docs To Browse

- MDN, Debugging CSS: https://developer.mozilla.org/docs/Learn_web_development/Core/Styling_basics/Debugging_CSS
- Chrome DevTools, Inspect CSS grid layouts: https://developer.chrome.com/docs/devtools/css/grid
- Chrome DevTools, Inspect and debug CSS flexbox layouts: https://developer.chrome.com/docs/devtools/css/flexbox
- MDN, `@supports`: https://developer.mozilla.org/en-US/docs/Web/CSS/@supports
- MDN, Browser compatibility tables: https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Page_structures/Compatibility_tables

## Guidance

- Inspect the element first: box model, computed styles, matched rules, inherited values, and active pseudo-classes.
- Turn rules off one at a time to find the property that causes the behavior.
- Use Grid and Flexbox overlays when debugging layout tracks, gaps, alignment, and wrapping.
- Check `scrollWidth` against viewport width when tracking horizontal overflow.
- Use `@supports` for progressive enhancement when browser support is uncertain.
- Validate desktop, narrow, and intermediate widths before trusting a responsive change.

## Checks

- Is the failing rule visible in matched styles?
- Is the problem caused by box sizing, intrinsic size, overflow, min-width, or specificity?
- Does the bug reproduce with realistic content lengths?
- Is browser support verified for newer CSS features?
