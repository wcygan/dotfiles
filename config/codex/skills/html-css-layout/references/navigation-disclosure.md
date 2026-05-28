# Navigation And Disclosure

## Description

Use this reference when building nav bars, sidebars, tabs, breadcrumbs, accordions, disclosure groups, dialogs, popovers, skip links, or other show/hide surfaces. Prefer native navigation and disclosure primitives when they match the interaction.

Browse current official docs before making precise claims about `nav`, `details`, `summary`, `dialog`, popover, tabs, ARIA-expanded, keyboard behavior, or focus management.

## Docs To Browse

- MDN, `<nav>` element: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/nav
- MDN, `<details>` element: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/details
- MDN, `<dialog>` element: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/dialog
- MDN, Popover API: https://developer.mozilla.org/en-US/docs/Web/API/Popover_API
- WAI-ARIA APG, Patterns: https://www.w3.org/WAI/ARIA/apg/patterns/

## Guidance

- Label navigation regions when there are multiple nav landmarks.
- Use `aria-current` for the current page or step when the native element does not already expose it.
- Use `details` and `summary` for simple disclosure content.
- Use `dialog` only when the experience is genuinely modal or dialog-like and focus management is handled.
- Do not hide essential navigation behind hover.
- Keep disclosure state visually obvious and reflected in markup when using custom controls.

## Checks

- Can the user skip repeated navigation?
- Is the current location clear?
- Does focus move predictably when content opens and closes?
- Does hidden content avoid accidental tab stops?
