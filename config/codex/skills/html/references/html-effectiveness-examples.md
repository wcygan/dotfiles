# HTML Effectiveness Example Catalog

Use this catalog when a user asks for an HTML artifact and the requested shape resembles one of the examples from:

https://thariqs.github.io/html-effectiveness/

Reviewed on 2026-05-08. The likely upstream repository is `ThariqS/html-effectiveness`; GitHub reported `license: null` at review time. Raw upstream HTML is not vendored. Local first-party production starters live in `references/html-files/` and show when to use each pattern. Starter 21 is a first-party vendored pattern from local artifact comparison, not from the upstream review set.

## How To Use This Catalog

1. Pick the closest artifact job from the table.
2. Adapt the starter's structure, interaction model, and reading flow, not the sample content.
3. Replace Birchline/example data with real source context from the user's repo, PR, tickets, logs, metrics, or prompt.
4. Keep the artifact standalone unless the user explicitly asks for an app or build step.
5. Verify interactive artifacts in a browser.

## Examples

| Local Starter | Use When | Adapt This Shape |
| --- | --- | --- |
| [01 - Three code approaches](html-files/01-exploration-code-approaches.html) | The user wants to compare implementation strategies before choosing one. | Three-column approach cards with real code snippets, pros/cons, fit notes, and a final recommendation. Collapse to one column on narrow screens. |
| [02 - Visual design directions](html-files/02-exploration-visual-designs.html) | The user needs to react to multiple UI directions, tones, densities, or palettes. | Live mockups in a comparison grid, small rationale under each option, and a light/dark or surface toggle. |
| [03 - Annotated PR review](html-files/03-code-review-pr.html) | The user asks for a code review or PR explanation with risk triage. | PR header, summary, risk map, file-by-file diff panels, margin annotations, severity labels, collapsible lower-risk files, and reviewer checklist. |
| [04 - Code understanding module map](html-files/04-code-understanding.html) | The user wants to understand how a feature or subsystem flows through code. | One-paragraph mental model, SVG request/data path, callstack walkthrough, source snippets in details blocks, and sticky file list. |
| [05 - Design system reference](html-files/05-design-system.html) | The user wants a portable design-system sheet generated from tokens/components. | Swatches, type scale, spacing samples, buttons, form fields, checkboxes, and copyable token names grouped by semantic purpose. |
| [06 - Component variant matrix](html-files/06-component-variants.html) | The user wants to inspect one component across states, props, themes, or density settings. | Control bar with sliders/radios/toggles, repeated live component variants, hover prop notes, and best-for notes per variant. |
| [07 - Animation sandbox](html-files/07-prototype-animation.html) | The user is tuning a micro-interaction, transition, easing, or celebratory state. | Isolated interactive prototype, easing buttons, keyframe timeline, replay/reset behavior, and copyable CSS. |
| [08 - Clickable interaction prototype](html-files/08-prototype-interaction.html) | The user needs to feel a workflow or gesture before implementation. | Throwaway native interaction, direct manipulation, a side panel that explains design decisions, and explicit open questions. |
| [09 - Slide deck](html-files/09-slide-deck.html) | The user wants a short shareable presentation without a slide tool. | Full-screen slide sections, keyboard navigation, progress indicator, metric slides, and a concise decision or ask. |
| [10 - SVG illustration sheet](html-files/10-svg-illustrations.html) | The user needs several diagrams or blog/doc illustrations in one file. | Inline SVG figures with consistent palette/stroke rules, usage notes, and download/export buttons per SVG. |
| [11 - Weekly status report](html-files/11-status-report.html) | The user wants a skim-friendly team, project, or engineering status update. | Metric band, highlights, shipped table, work-in-progress section, small chart, risks/blockers, and time window/source labels. |
| [12 - Incident report](html-files/12-incident-report.html) | The user needs a postmortem or incident summary for stakeholders. | Sticky table of contents, TL;DR, severity/status facts, minute-by-minute timeline, root cause section, impact summary, and action items. |
| [13 - Annotated flowchart](html-files/13-flowchart-diagram.html) | The user wants a workflow/pipeline diagram with details on each step. | SVG flowchart with success/failure paths, legend, clickable nodes, and a details panel for commands, timing, and failure behavior. |
| [14 - Feature explainer](html-files/14-research-feature-explainer.html) | The user asks how a repo feature works from source files. | Files-read chips, TL;DR, step-by-step expandable path, tabbed config/code examples, gotchas, and FAQ. |
| [15 - Concept explainer](html-files/15-research-concept-explainer.html) | The user wants to learn a technical concept through interaction. | Live SVG/canvas-like visualization, sliders/buttons for parameters, comparison table, glossary, and hover-linked terms. |
| [16 - Implementation plan](html-files/16-implementation-plan.html) | The user wants a handoff-ready implementation plan. | Summary metrics, milestone timeline, package/surface map, mockups, data-flow SVG, key code snippets, risk table, rollout, rollback, and test plan. |
| [17 - PR writeup for reviewers](html-files/17-pr-writeup.html) | The user wants to attach reviewer guidance to a PR. | PR metadata, TL;DR, before/after behavior, file-by-file reading order, focus areas, rollout notes, and hidden details for secondary files. |
| [18 - Ticket triage board](html-files/18-editor-triage-board.html) | The user needs to sort, prioritize, or bucket work items. | Drag cards across Now/Next/Later/Cut columns, tag filtering, counts, reset, and copy-as-Markdown export. |
| [19 - Feature flag editor](html-files/19-editor-feature-flags.html) | The user needs a purpose-built editor for structured config with constraints. | Grouped toggles, dependency warnings, derived summary, changed-key diff, copy full JSON, copy diff, and reset. |
| [20 - Prompt tuner](html-files/20-editor-prompt-tuner.html) | The user wants to tune a prompt, template, or copy with live examples. | Contenteditable template, highlighted variable slots, sample inputs, live rendered previews, token/character counts, reset, and copy prompt. |
| [21 - Animated graph data flow](html-files/21-animated-graph-data-flow.html) | The user needs to understand data moving through a topology: gossip/flooding, routing, queues, replication, dependency traversal, retries, or graph state. | Inline SVG node-edge graph, active animated edges, muted inactive topology, edge labels, rule/state side panels, and reduced-motion fallback. |

## Selection Heuristics

- Start with an exploration artifact when the user has not chosen a direction.
- Start with a plan artifact when implementation is likely but tradeoffs, rollout, or risk are not yet aligned.
- Start with a PR review or PR writeup artifact when the input is a diff, branch, or pull request.
- Start with a code-understanding or feature-explainer artifact when the user asks "how does this work?"
- Start with a prototype when the key uncertainty is feel, motion, or workflow ergonomics.
- Start with an animated graph/data-flow artifact when topology, direction, fanout, duplicates, or state movement is the core teaching problem.
- Start with a report when the output is for stakeholders and the important work is synthesis.
- Start with a custom editor when text prompts are a poor way to express the desired changes and the user needs to export the edited state back to Codex.

## Interaction Patterns Observed

- Native form controls are enough for most useful interactivity: range inputs, radios, checkboxes, buttons, details, and contenteditable.
- Copy/export buttons matter most for editors and tuning sandboxes. Include a `file://` clipboard fallback.
- SVG is the dominant diagram mechanism: request paths, architecture maps, flowcharts, charts, visual concepts, and downloadable illustrations.
- Animated SVG edges can be the clearest way to explain data flow through a graph. Animate only meaningful paths, label the active edges, and keep a static legend and reduced-motion fallback.
- Sticky navigation helps long reports, code explainers, PR writeups, and editors.
- Collapsible details work well for optional code snippets and lower-priority files, but keep conclusions visible by default.
- For drag/drop, include clear counts, reset behavior, and an export format the user can paste back into the agent.
