# Accessibility And Interaction States

## Description

Use this reference when styling components with keyboard interaction, focus, labels, validation, dialogs, disclosure, tabs, navigation, or form states. Accessibility is part of the component contract, not a final audit pass.

Browse current official docs before making precise claims about WCAG requirements, ARIA patterns, keyboard behavior, accessible names, or form semantics.

## Docs To Browse

- W3C WCAG 2.2: https://www.w3.org/TR/WCAG22/
- WAI-ARIA Authoring Practices Guide: https://www.w3.org/WAI/ARIA/apg/
- MDN, HTML accessibility: https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Accessibility/HTML
- MDN, What is accessibility: https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Accessibility/What_is_accessibility
- web.dev, Learn Accessibility: https://web.dev/learn/accessibility

## Guidance

- Prefer native HTML controls. Add ARIA only when native semantics cannot express the component.
- Make every interactive element keyboard reachable and visible when focused.
- Use `:focus-visible` for clear focus rings without hiding keyboard state.
- Associate labels, help text, and errors with form controls.
- Preserve disabled, invalid, selected, expanded, pressed, current, loading, and empty states in markup and styling.
- Check contrast for text and meaningful non-text UI.
- Keep target sizes usable and leave enough spacing between adjacent actions.

## State Checklist

- `hover`: optional affordance only; never the sole way to reveal essential content.
- `focus-visible`: strong, high-contrast, not clipped by overflow.
- `active`: brief pressed feedback for commands.
- `disabled`: visibly inactive and programmatically disabled when appropriate.
- `invalid`: includes text, not color alone.
- `selected/current`: reflected in markup when possible, such as `aria-current`.
- `expanded`: paired with `aria-expanded` only when a custom disclosure is necessary.
