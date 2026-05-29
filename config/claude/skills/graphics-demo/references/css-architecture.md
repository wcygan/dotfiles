# CSS Architecture

## Description

Use this reference when organizing CSS across multiple components, shared tokens, utilities, resets, cascade layers, and override boundaries. The goal is predictable CSS that a maintainer can reason about quickly.

Browse current official docs before making precise claims about cascade order, specificity, layers, custom properties, nesting, or scoped styles.

## Docs To Browse

- MDN, Cascade, specificity, and inheritance: https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Handling_conflicts
- MDN, Specificity: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_cascade/Specificity
- MDN, Cascade layers: https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Cascade_layers
- MDN, Using CSS custom properties: https://developer.mozilla.org/en-US/docs/Web/CSS/Using_CSS_custom_properties
- BEM, Naming methodology: https://getbem.com/naming/

## Guidance

- Keep specificity low. Prefer class selectors over IDs and long descendant chains.
- Use cascade layers for large projects: reset, base, layout, components, utilities.
- Use custom properties for tokens and component-level knobs.
- Keep selectors local to the component unless styling a deliberate layout parent or global element default.
- Make overrides explicit by layer, variant class, or custom property. Avoid surprise overrides through ancestry.
- Avoid `!important` except for documented utility escape hatches or third-party overrides.
- Keep naming consistent with the project: BEM, CSS Modules, utility classes, framework conventions, or existing local patterns.

## Component Boundary Pattern

```css
@layer reset, base, layout, components, utilities;

@layer components {
  .product-card {
    --card-padding: var(--space-4);
    display: grid;
    gap: var(--space-3);
    padding: var(--card-padding);
  }

  .product-card[data-density="compact"] {
    --card-padding: var(--space-2);
  }
}
```

This keeps the variant easy to read and avoids a specificity race.
