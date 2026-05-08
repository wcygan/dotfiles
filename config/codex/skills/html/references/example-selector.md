# HTML Artifact Example Selector

Use this selector after loading `SKILL.md` when the best artifact starter is not obvious. It is a routing reference for the production starter files in `references/html-files/`. Load only the rows or local starters relevant to the user's request.

## Routing Workflow

1. Identify the user's primary intent: explore, review, explain, design, prototype, diagram, report, present, or edit.
2. Identify the input type: code/diff, visual UI, design tokens, operational data, conceptual topic, structured data, tickets, prompt text, or incident timeline.
3. Identify the audience: self, implementer, reviewer, team, leadership, learners, or operators.
4. Identify the needed interaction level: static document, collapsible reading aid, parameter tuning, direct manipulation, live preview, or exportable editor.
5. Pick the closest primary starter and optionally one secondary starter to borrow a substructure from.
6. Load the chosen starter under `references/html-files/` before creating the artifact.

## Selection Matrix

| Local Starter | Best Trigger Signals | Negative Triggers | Pair With | Structure To Adapt | Interaction | Verification |
| --- | --- | --- | --- | --- | --- | --- |
| `01-exploration-code-approaches.html` | "compare approaches", "options", "which implementation", "tradeoffs", early technical design | User already chose the approach; needs step-by-step execution | `16` for final handoff, `04` for existing flow context | Option columns, real snippets, pros/cons, recommendation | Static | Check snippets are grounded in repo files and recommendation names the decisive tradeoff. |
| `02-exploration-visual-designs.html` | "directions", "mockups", "visual options", "tone", "density", "palette" | User needs a production component matrix or token reference | `05` for tokens, `06` for component states, `08` for flow | Live visual variants, common frame, theme toggle, tradeoff labels | Light controls | Browser-check light/dark or state controls and mobile grid. |
| `03-code-review-pr.html` | "review this PR", "find risks", "annotate diff", "what should I worry about" | Author wants a friendly PR explainer rather than critique | `17` for reviewer writeup, `04` for subsystem explanation | PR header, risk map, annotated diffs, severity labels, checklist | Collapsible details | Confirm findings tie to real diff lines and severity labels are meaningful. |
| `04-code-understanding.html` | "how does this code work", "module map", "request path", "architecture note" | User needs a general concept lesson or step-by-step feature summary | `14` for feature gotchas, `13` for clickable workflow | Mental model, flow SVG, callstack, snippets, file list | Collapsible snippets | Verify file paths exist and flow matches source order. |
| `05-design-system.html` | "design system", "tokens", "brand reference", "style guide", "component inventory" | User wants to compare just one component's variants | `06` for one component, `02` for directions | Swatches, type scale, spacing, controls, copyable token names | Mostly static | Verify token values against source files and contrast is readable. |
| `06-component-variants.html` | "component variants", "states", "props", "size matrix", "density" | User is still exploring broad visual directions | `05` for tokens, `07` for component motion | Control bar, repeated variants, prop/state notes, best-for labels | Controls and hover | Browser-check controls update all variants and layout holds on mobile. |
| `07-prototype-animation.html` | "animation", "easing", "timing", "micro-interaction", "celebration" | User needs multi-screen flow or drag/drop behavior | `06` for component states, `08` for workflow feel | Isolated animation, replay, easing controls, timeline, copyable CSS | Replay/tuning | Test replay/reset, reduced-motion fallback where relevant, and exported CSS. |
| `08-prototype-interaction.html` | "prototype this flow", "drag", "reorder", "clickable flow", "feel it" | User needs visual directions without interaction | `07` for motion timing, `18` for sortable real data | Native prototype, direct manipulation, design-decision panel, open questions | Direct manipulation | Test core interaction and document intentionally omitted edge cases. |
| `09-slide-deck.html` | "deck", "presentation", "slides", "demo", "talk track" | User needs a written report or detailed implementation handoff | `11` for metrics, `16` for plan content | Full-screen slides, keyboard nav, progress, metrics, ask | Keyboard navigation | Test arrow keys, slide count, and print/read-only fallback. |
| `10-svg-illustrations.html` | "SVG illustrations", "diagram sheet", "blog figures", "download SVG" | User needs an explanatory flow with per-step details | `13` for workflow detail, `15` for learning visual | Consistent SVG figures, usage notes, export buttons | Download/copy | Test standalone SVG export if included and check labels fit. |
| `11-status-report.html` | "weekly status", "what shipped", "project update", "leadership summary" | Incident/postmortem with root cause and timeline | `09` for presenting, `12` for incident section | Metric band, highlights, shipped table, chart, risks | Static | Verify date range, metric definitions, and source provenance. |
| `12-incident-report.html` | "incident", "postmortem", "SEV", "outage", "timeline", "root cause" | Routine status update without a failure narrative | `11` for metrics, `13` for system flow | Facts, TL;DR, timeline, root cause, impact, action items | Sticky nav/static | Verify timestamps, impact numbers, owners, and action items. |
| `13-flowchart-diagram.html` | "flowchart", "pipeline", "workflow", "failure paths", "click each step" | Need several standalone illustrations instead of one operational flow | `10` for figure style, `04` for code path | SVG flowchart, legend, clickable nodes, detail panel | Clickable nodes | Test every node detail and success/failure path. |
| `14-research-feature-explainer.html` | "explain feature", "how rate limiter works", "gotchas", "FAQ", source-backed learning | User needs low-level architecture map only | `04` for callstack, `15` for concept teaching | Files-read chips, TL;DR, expandable steps, tabbed snippets, FAQ | Details/tabs | Verify all claims cite source files and tabs switch correctly. |
| `15-research-concept-explainer.html` | "teach me concept", "interactive explainer", "show how parameters affect it" | The topic is a repo-specific feature with concrete source files | `14` for source-backed feature summary, `10` for figure styling | Interactive visualization, sliders, comparison table, glossary | Live controls | Test parameter changes and ensure concept remains understandable without JS. |
| `16-implementation-plan.html` | "implementation plan", "handoff", "milestones", "rollout", "risk table" | User only wants options or a PR explanation | `01` for approach comparison, `17` for PR writeup after implementation | Summary metrics, milestones, mockups, data-flow, code snippets, risks/tests | Mostly static | Confirm plan is actionable, scoped, rollbackable, and source-grounded. |
| `17-pr-writeup.html` | "write up PR", "reviewer guide", "attach to PR", "what changed and why" | User asked for critical review or bug finding | `03` for review findings, `11` for status framing | PR metadata, TL;DR, before/after, file reading order, focus areas | Collapsible details | Verify changed files and focus areas match the actual PR. |
| `18-editor-triage-board.html` | "triage", "prioritize", "sort tickets", "Now/Next/Later/Cut", "drag cards" | User needs config validation or prompt tuning | `11` for status after triage, `16` for plan from priorities | Drag columns, counts, tag filters, reset, Markdown export | Drag/export | Test drag/drop, filtering, reset, and export format. |
| `19-editor-feature-flags.html` | "feature flags", "config editor", "dependencies", "copy diff", JSON/YAML toggles | User just needs a read-only config explainer | `14` for config explanation, `18` for bucketing items | Grouped toggles, dependency warnings, changed-key diff, full JSON export | Form/export | Test dependency warnings, dirty state, reset, and copy diff. |
| `20-editor-prompt-tuner.html` | "prompt tuner", "template variables", "live preview", "copy prompt", "sample inputs" | User needs a final static prompt spec only | `15` for concept visualization, `19` for structured config constraints | Editable template, slot highlighting, previews, counters, copy/reset | Live preview/export | Test paste handling, slot rendering, counters, reset, and copy. |

## Tie Breakers

- Choose `03` over `17` when the artifact should critique a PR; choose `17` when it should help reviewers understand the author's intent.
- Choose `04` over `14` when source traversal and module boundaries matter most; choose `14` when the user wants a teachable feature summary with gotchas.
- Choose `01` over `16` when the decision is still open; choose `16` when execution is the point.
- Choose `02` over `06` when broad design direction is open; choose `06` when a specific component's state/prop space is under review.
- Choose `07` over `08` when timing/easing is the main uncertainty; choose `08` when workflow ergonomics are the main uncertainty.
- Choose `10` over `13` for multiple reusable figures; choose `13` for one operational flow with step details.
- Choose `11` over `12` for routine updates; choose `12` for incidents with root cause and follow-up owners.
- Choose `18`, `19`, or `20` when the user should manipulate the content and export the result. The exported format is the product.

## Loading Discipline

- Load this file only when routing is unclear or multiple patterns fit.
- Load at most 1-3 local starter files before writing the artifact.
- Start from the closest file in `references/html-files/`; do not use a separate blank template fallback.
- Do not copy raw upstream example files; the local starter files are first-party production bases.
