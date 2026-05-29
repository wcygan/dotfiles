# Forms And Validation

## Description

Use this reference when building or reviewing forms, settings panels, filters, checkout steps, onboarding flows, and editable component states. Good forms combine semantic controls, readable layout, validation timing, and explicit states.

Browse current official docs before making precise claims about form submission, labels, fieldsets, constraint validation, required fields, input types, or accessible error behavior.

## Docs To Browse

- MDN, `<form>` element: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/form
- MDN, Client-side form validation: https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Forms/Form_validation
- MDN, `<label>` element: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/label
- web.dev, Forms: https://web.dev/learn/html/forms
- web.dev, Form fields: https://web.dev/learn/forms/form-fields

## Guidance

- Use the correct native input type before custom JavaScript validation.
- Give every control a label. Use `fieldset` and `legend` for grouped choices.
- Put help text and errors near the control they explain.
- Connect errors and help text programmatically with `aria-describedby` when needed.
- Validate at useful moments. Avoid loud validation before the user has had a chance to complete a field.
- Preserve form states: default, focus, invalid, disabled, read-only, loading, success, and empty.

## Checks

- Can a keyboard user reach and operate every control?
- Does each control have an accessible name?
- Are invalid states communicated with text, not color alone?
- Does the form still fit on narrow screens when labels and errors wrap?
