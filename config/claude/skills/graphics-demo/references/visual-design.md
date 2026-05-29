# Visual Design For Clean Interfaces

## Description

Use this reference when translating structure into a polished interface: spacing, typography, hierarchy, density, color, borders, shadows, and interaction feedback. Clean design comes from constraints, not decoration.

Browse current official or vendor design docs before making precise claims about accessibility thresholds, platform conventions, color systems, or typography recommendations.

## Docs To Browse

- MDN, CSS values and units: https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Values_and_units
- MDN, CSS colors: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_colors
- Material Design, Layout: https://m3.material.io/foundations/layout/overview
- Material Design, Typography: https://m3.material.io/styles/typography/overview
- WCAG, Contrast minimum: https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html

## Guidance

- Use a small spacing scale and repeat it consistently.
- Create hierarchy with size, weight, spacing, and grouping before adding decorative effects.
- Keep line length readable. Long prose needs a max width; dense tools need compact but legible labels.
- Use color semantically: status, severity, selection, category, or action.
- Use borders and shadows to clarify grouping, not to decorate every section.
- Keep cards for repeated items or true containers. Avoid nesting cards inside cards.
- Match visual density to the task. Operational tools should favor scanning and repeated use; editorial pages can use more expressive rhythm.

## Clean Design Checks

- Can the user identify the primary action and current state in a few seconds?
- Do related controls sit near the thing they affect?
- Does the layout still work when text wraps?
- Is the page using more type sizes, colors, shadows, or radii than the job requires?
- Are focus, hover, selected, disabled, invalid, and empty states visually distinct?
