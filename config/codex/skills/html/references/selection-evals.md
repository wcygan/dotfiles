# HTML Pattern Selection Evals

Use these prompts as a lightweight manual check after changing `SKILL.md`, `example-selector.md`, or the local starter files. The selector passes when the primary choice is correct and the secondary choice, if any, is reasonable.

## How To Run

1. Read only `SKILL.md` and `references/example-selector.md`.
2. For each prompt, choose the best primary local starter and up to two secondary starters.
3. Compare against the expected routing below.
4. If a prompt routes ambiguously, improve the selector or the relevant starter files.

## Eval Cases

| Prompt | Expected Primary | Expected Secondary | Why |
| --- | --- | --- | --- |
| "Compare three ways to add debounced search to this React task filter. Show code and tradeoffs." | `01-exploration-code-approaches.html` | `16-implementation-plan.html` | The decision is still open and needs implementation options. |
| "Create six different empty-state directions for our onboarding page so design can pick a tone." | `02-exploration-visual-designs.html` | `05-design-system.html`, `06-component-variants.html` | The task is broad visual exploration, with tokens/components as supporting context. |
| "Review this PR for optimistic updates. I want risk callouts and annotated diff snippets." | `03-code-review-pr.html` | `04-code-understanding.html` | The task is critical review of a diff, not author guidance. |
| "I do not understand how auth flows through this app. Read the code and make a diagram." | `04-code-understanding.html` | `14-research-feature-explainer.html`, `13-flowchart-diagram.html` | The task is source-backed architecture and call path understanding. |
| "Generate a portable design system reference from our CSS variables and core Button/Input components." | `05-design-system.html` | `06-component-variants.html` | The output should document tokens and common components. |
| "Show every Card variant across padding, border, shadow, hover, and selected states." | `06-component-variants.html` | `05-design-system.html` | The unit of comparison is a single component's state/prop surface. |
| "Prototype the task-complete checkmark animation with sliders for duration and easing and copyable CSS." | `07-prototype-animation.html` | `06-component-variants.html` | The key uncertainty is timing/easing of one micro-interaction. |
| "Make a throwaway HTML prototype for dragging sidebar items to reorder them. I need to feel the interaction." | `08-prototype-interaction.html` | `07-prototype-animation.html` | The key uncertainty is workflow ergonomics, not just timing. |
| "Turn this platform engineering weekly update into a 5-slide browser deck for Friday demo." | `09-slide-deck.html` | `11-status-report.html` | The requested output is a presentation, with status content as input. |
| "Create three consistent SVG diagrams for our background jobs docs and let me download each SVG." | `10-svg-illustrations.html` | `13-flowchart-diagram.html` | The task asks for multiple reusable figures and export. |
| "Summarize this week's merged PRs, deploys, incidents, flaky tests, risks, and next week focus." | `11-status-report.html` | `09-slide-deck.html` | Routine status with metrics and shipped work. |
| "Write a postmortem for this SEV-2: include timeline, root cause, impact, and follow-up owners." | `12-incident-report.html` | `13-flowchart-diagram.html`, `11-status-report.html` | Incident-specific communication with accountable actions. |
| "Draw the deploy pipeline from git push to production. Let me click each step to see commands and failure paths." | `13-flowchart-diagram.html` | `10-svg-illustrations.html` | One workflow needs clickable step details and failure paths. |
| "Read our rate limiter files and produce a readable explainer with files read, gotchas, config snippets, and FAQ." | `14-research-feature-explainer.html` | `04-code-understanding.html` | Source-backed feature summary with gotchas and snippets. |
| "Teach consistent hashing with an interactive ring, sliders for nodes and keys, and a comparison to mod N." | `15-research-concept-explainer.html` | `10-svg-illustrations.html` | Abstract concept that benefits from a manipulable visualization. |
| "Create a handoff-ready implementation plan for threaded comments with milestones, mockups, data flow, risks, tests, rollout, and rollback." | `16-implementation-plan.html` | `01-exploration-code-approaches.html` | The user needs execution structure after scope is known. |
| "Write a PR artifact for reviewers explaining why notification delivery moved to a queue and which files to read first." | `17-pr-writeup.html` | `03-code-review-pr.html` | The task is author guidance, not a critique-first review. |
| "Make a draggable board to sort 30 Linear tickets into Now, Next, Later, and Cut, then export Markdown." | `18-editor-triage-board.html` | `16-implementation-plan.html` | The output is a custom editor for bucketing work. |
| "Build a form editor for feature flags that warns about dependency violations and copies only changed keys." | `19-editor-feature-flags.html` | `14-research-feature-explainer.html` | Structured config editing with validation and diff export. |
| "Build a prompt tuning page with an editable template, highlighted variables, three live sample previews, counters, reset, and copy." | `20-editor-prompt-tuner.html` | `15-research-concept-explainer.html` | Prompt/template editing with live previews and export. |
| "Explain gossip flooding by showing a packet move through a mesh graph, with animated A-B, B-D, B-E, C-E, and C-F edges plus Bloom-filter duplicate suppression." | `21-animated-graph-data-flow.html` | `15-research-concept-explainer.html`, `13-flowchart-diagram.html` | The topology and moving data are the teaching surface; the Bloom/visited state explains duplicate suppression. |

## Pass Criteria

- At least 19 of 21 primary choices should route exactly as expected.
- For the two hardest tie-breakers, the agent should explain the ambiguity and choose a reasonable secondary card.
- Every eval should route to one of the production starters under `references/html-files/`; there is no separate blank template fallback.
- PR critique should route to `03`; PR author guidance should route to `17`.
- General concept teaching should route to `15`; source-backed feature explanation should route to `14`.
