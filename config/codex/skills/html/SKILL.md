---
name: html
description: Use when Codex should create, edit, or review a standalone HTML artifact instead of Markdown, especially for rich specs, implementation plans, PR/code review explainers, research reports, status or incident reports, visual design explorations, design-system sheets, component matrices, interactive prototypes, SVG diagrams, slide decks, or custom one-off editors with copy/export controls.
---

# HTML Artifacts

Create readable, shareable, single-file HTML documents that communicate complex work better than a long Markdown file. Use HTML when the user needs visual comparison, dense synthesis, diagrams, interaction, rich code annotation, or an artifact other humans are likely to read.

## Reference Map

- `references/example-selector.md`: choose among the 20 local production starters; load when routing is unclear.
- `references/html-effectiveness-examples.md`: compact catalog of all local starters.
- `references/html-files/index.html`: browser-readable index of local starter files.
- `references/html-files/*.html`: production starter files to copy, adapt, and expand into the final standalone artifact.
- `references/selection-evals.md`: realistic prompts for checking selector quality after editing this skill.

## Core Workflow

1. Clarify the artifact's job in one sentence: compare options, explain code, review a PR, plan implementation, teach a concept, report status, prototype an interaction, or edit structured data.
2. Gather the real source context first: code, diffs, logs, metrics, screenshots, design tokens, tickets, issue comments, browser pages, or web sources. Do not invent specifics that should come from the repo or provided data.
3. Route the request to the closest local production starter before writing HTML. Use the quick decision tree below; for close calls load `references/example-selector.md`, then load only the 1-3 relevant starter files under `references/html-files/`.
4. Choose an output path. Honor an explicit user-provided path; otherwise write the artifact to `~/Downloads/<clear-slug>.html`, creating `~/Downloads/` first if needed.
5. Build one self-contained `.html` file by adapting the selected starter's structure, reading flow, and interaction model. Inline CSS and, only when useful, inline JavaScript in the final artifact. Avoid build steps and external dependencies unless the user explicitly wants them.
6. Make the first viewport immediately useful: title, concise context, key takeaway, and navigation or summary metrics when the artifact is large.
7. Verify in a browser when practical. For interactive artifacts, test controls, copy/export buttons, responsive layout, and console errors.
8. In the final response, link the local HTML file and summarize only the artifact's purpose and verification.

## Pattern Routing

Classify the task by the user's main uncertainty:

- **Which option should we choose?** Use exploration patterns: implementation approaches, visual directions, or implementation plan.
- **What changed or what should reviewers inspect?** Use PR/code review patterns: annotated PR review or PR writeup.
- **How does this work?** Use code understanding, feature explainer, concept explainer, flowchart, or SVG illustration patterns.
- **How should this look or feel?** Use design system, component variants, animation sandbox, or clickable prototype patterns.
- **What happened or what is the status?** Use weekly status or incident report patterns.
- **How can the user edit structured choices visually?** Use ticket triage, feature flag editor, or prompt tuner patterns.

Then refine by input and output:

- Diff or PR input: prefer `03-code-review-pr.html` for critique, `17-pr-writeup.html` for author guidance.
- Source files or architecture input: prefer `04-code-understanding.html`; use `14-research-feature-explainer.html` when the answer is a teachable feature summary with gotchas.
- Visual UI/design input: prefer `02-exploration-visual-designs.html`, `05-design-system.html`, or `06-component-variants.html`.
- Motion or workflow feel input: prefer `07-prototype-animation.html` for timing/easing, `08-prototype-interaction.html` for gesture/flow.
- Operational timeline or metrics input: prefer `11-status-report.html` for routine updates, `12-incident-report.html` for postmortems.
- Data to reorder, toggle, or tune: prefer `18-editor-triage-board.html`, `19-editor-feature-flags.html`, or `20-editor-prompt-tuner.html`.

## Pattern Map

Use these production starters as starting points, then adapt them to the user's actual task.

For detailed selection guidance, load `references/example-selector.md`. For concrete inspiration, load `references/html-effectiveness-examples.md` or open `references/html-files/index.html`. They catalog 20 local production starters derived from reviewing `https://thariqs.github.io/html-effectiveness/`, when each one is useful, and which structure or interaction model to adapt. The raw upstream HTML is not vendored because the upstream repository does not declare a license.

| User Need | Strong HTML Shape |
| --- | --- |
| Explore implementation approaches | Side-by-side option grid with code snippets, tradeoffs, risks, and recommendation badges. |
| Explore visual directions | Live mockups in a comparison matrix with controls for theme, density, or state. |
| Explain or review a PR | File map, risk legend, rendered diff snippets, margin annotations, severity tags, and reviewer focus areas. |
| Explain a codebase topic | Architecture map, request/data flow SVG, hot-path walkthrough, collapsible code excerpts, gotchas. |
| Plan implementation | Milestone timeline, data-flow diagram, surface map, critical code snippets, risk table, rollout/rollback notes. |
| Design system reference | Token swatches, type scale, spacing samples, component examples, copyable variable names. |
| Component variants | Matrix of props, states, sizes, themes, and density controls with notes on when to use each variant. |
| Prototype interaction or motion | Working mini-prototype with sliders, toggles, timing controls, reset, and copyable parameters or CSS. |
| Technical diagram | Inline SVG or canvas with legend, clickable nodes, details panel, and failure paths when relevant. |
| Slide deck | Full-screen sections with keyboard navigation, progress indicator, and printable fallback. |
| Research/report | TL;DR, source list, metric cards, charts/tables, timeline, findings grouped by decision relevance. |
| Incident report | Sticky table of contents, impact summary, timeline, root cause diagram, action-item checklist. |
| Custom editor | Purpose-built UI for the data, validation/warnings, drag/drop or form controls, and "copy as JSON/Markdown/diff/prompt". |

## HTML Rules

- Keep artifacts standalone: inline CSS, inline SVG, inline JS. Use external images only when they are already available or when the task requires real images.
- Default generated artifact files to `~/Downloads/` unless the user names a different destination.
- Prefer semantic HTML: `header`, `nav`, `main`, `section`, `article`, `figure`, `table`, `details`, `button`, `label`, and form controls.
- Use real visual structure instead of ASCII diagrams. Prefer SVG for workflows, module maps, timelines, and architecture diagrams; use tables for comparable data.
- Render code as selectable text in `pre code`, not screenshots. Add line numbers, callouts, or side annotations when they help the reader.
- Make large artifacts navigable with a table of contents, sticky section nav, tabs, filters, or collapsible details. Do not hide critical findings behind interactions.
- Design for skimming first and deeper reading second: summary, visual map, details, then appendix.
- Keep JavaScript small and local. It should support reading, tuning, copying, filtering, navigating, or editing the artifact.
- Add export/copy controls to interactive editors and tuning sandboxes so user edits can return to Codex as JSON, Markdown, diff, CSS, or prompt text.
- Avoid secrets, private tokens, or sensitive raw logs. Redact before embedding.

## Visual Guidance

- Treat the HTML file as a crafted work document, not a landing page. The content is the product.
- Use color with meaning: severity, status, ownership, file type, data series, or interaction state. Include legends for non-obvious color mappings.
- Avoid one-note palettes, decorative gradient blobs, stock-like filler, and oversized hero sections.
- Use cards sparingly for repeated items such as metrics, options, variants, tickets, and findings. Keep main sections as full-width content areas or normal document flow.
- Keep typography compact and readable. Do not scale text with viewport width. Make long labels wrap cleanly in buttons, badges, tables, and cards.
- Make the page responsive by design: flexible grids, `minmax()`, horizontal overflow only for dense tables/code, and usable narrow-screen navigation.
- Preserve printable/read-only value. An artifact should still communicate if JavaScript is disabled, except for explicitly interactive prototypes/editors.

## Data And Evidence

- Show provenance for synthesized claims: source file paths, PR numbers, commit SHAs, issue IDs, timestamps, log windows, URLs, or "files read" chips.
- For research or reports, cite sources close to the relevant claim and include a compact source list.
- For code review, distinguish observed behavior, inferred risk, and recommended fix.
- For plans, include assumptions, open questions, rollout, rollback, and test strategy.
- For dashboards or status reports, define metrics and time windows; avoid unlabeled numbers.

## Interactivity

Use interaction only when it makes the artifact more useful than a static document.

- Prefer native controls: `button`, `input type="range"`, `select`, `details`, `dialog`, checkboxes, radios, and draggable elements where appropriate.
- Keep controls visible near the thing they affect.
- Make copy buttons deterministic. Export the exact edited state, ordering, diff, or parameter set.
- For drag/drop editors, also support click buttons or keyboard-accessible movement when feasible.
- Store throwaway state in memory or `localStorage` only when persistence is useful; label reset behavior clearly.

## Browser Verification

When the artifact is more than a static short page, verify with a browser:

1. Open the file locally.
2. Check desktop and a narrow/mobile viewport.
3. Test interactive controls and export/copy buttons.
4. Inspect for obvious layout overlap, unreadable contrast, horizontal page overflow, and console errors.
5. Capture a screenshot only when useful for the user's review or when visual correctness is the task.

Use the `browser-navigation` skill or Playwright/agent-browser tools when available.

## Production Starters

The starter set lives in `references/html-files/`. Treat those files as the concrete implementation base for new artifacts, not as decorative examples. Select the closest starter, copy its useful structure and interaction model, replace all sample content with real source context, and expand it into the final standalone artifact.

The final artifact should still be self-contained. If a starter uses shared local CSS for maintainability inside this skill directory, inline the relevant styling into the generated output file unless the user explicitly asks for a multi-file artifact.
