# Semantic HTML

## Description

Use this reference when deciding which HTML elements should express the document, region, component, or control before styling begins. Semantic HTML is the first accessibility layer and the best way to keep CSS selectors honest.

Browse current official docs before making precise claims about element behavior, landmark roles, form controls, heading structure, or ARIA fallback.

## Docs To Browse

- MDN, Document and website structure: https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content/Structuring_documents
- MDN, HTML elements reference: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements
- web.dev, Semantic HTML: https://web.dev/learn/html/semantic-html
- WHATWG HTML, Sections: https://html.spec.whatwg.org/multipage/sections.html
- WAI, First rule of ARIA use: https://www.w3.org/TR/using-aria/#rule1

## Guidance

- Use `header`, `nav`, `main`, `section`, `article`, `aside`, and `footer` when they describe page structure.
- Use native controls such as `button`, `a`, `label`, `input`, `select`, `textarea`, `fieldset`, `legend`, `summary`, and `details` before custom roles.
- Use headings to communicate document outline and scan path. Do not choose heading levels only for font size.
- Use lists for repeated related items, tables for true tabular data, and figures for media plus captions.
- Use `div` and `span` only as neutral grouping or styling hooks when no semantic element fits.

## Common Mistakes

- Styling every region as a `div` and adding ARIA later.
- Using links for actions or buttons for navigation.
- Reordering content visually with CSS in a way that breaks reading and tab order.
- Adding landmarks without unique labels when multiple landmarks of the same kind exist.
