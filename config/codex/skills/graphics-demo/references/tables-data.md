# Tables And Dense Data

## Description

Use this reference when displaying tabular records, comparison matrices, pricing details, status lists, logs, or dense operational data. Tables are for data relationships, not general layout.

Browse current official docs before making precise claims about table semantics, captions, header scope, row groups, sortable controls, responsive overflow, or accessibility.

## Docs To Browse

- MDN, `<table>` element: https://developer.mozilla.org/docs/Web/HTML/Reference/Elements/table
- MDN, HTML table accessibility: https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content/Table_accessibility
- W3C WAI, Tables tutorial: https://www.w3.org/WAI/tutorials/tables/
- MDN, Styling tables: https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Tables
- MDN, `overflow`: https://developer.mozilla.org/en-US/docs/Web/CSS/overflow

## Guidance

- Use tables only for data that benefits from row and column relationships.
- Add a concise `caption` so users know whether the table is relevant before reading cells.
- Use `th` with `scope="col"` or `scope="row"` for straightforward tables.
- Use `thead`, `tbody`, and `tfoot` when grouping improves scanning.
- Wrap dense tables in a local overflow container instead of allowing page-wide horizontal overflow.
- Keep interactive controls inside cells simple and reachable.

## Checks

- Does each cell's meaning follow from visible or programmatic headers?
- Can the table be scanned without losing column context?
- Does the table stay usable on small screens?
- Are status colors paired with text?
