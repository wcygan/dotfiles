# Pi Skill Design

Design the target Pi skill as a capability package rather than an answer sheet.

## Router structure

Keep `SKILL.md` short enough for a weaker model to navigate reliably. It should:

- state the capability and trigger scenarios precisely;
- name the required first references for common task classes;
- define the core decision procedure;
- declare safety and state boundaries;
- explain when to stop or ask for missing information; and
- specify the requested answer or report discipline.

Use exact paths relative to the skill directory. Weak models may otherwise
resolve `references/...` against the project root.

## Pure-router profile

Use a pure router when required-reference reads are part of acceptance. In that
profile, `SKILL.md` contains:

- trigger scenarios and task classes;
- an explicit first-read gate;
- a cue-to-reference or cross-domain routing table;
- source precedence and safety boundaries;
- stop conditions; and
- answer or report discipline.

Keep operational conclusions, exceptions, command behavior, and detailed
decision rules in focused references. If the router contains enough facts to
answer the evaluation directly, a weaker model may skip the intended references
while still appearing correct.

For a mixed task, require the union of applicable references before reasoning.
Do not require unrelated reads merely to inflate an activation metric.

## Focused resources

Place durable details under:

- `references/` for rules, terminology, precedence, schemas, and examples;
- `scripts/` for deterministic parsing, conversion, lookup, validation, or
  other mechanical operations; and
- `assets/` for templates, fixtures, and static data.

Require only the references relevant to the current task. For mixed evaluation
batches, explicitly require every applicable focused reference.

## What belongs in the skill

Good teaching content includes:

- stable domain rules;
- exact boundaries and exceptions;
- decision tables;
- short contrasting examples;
- mechanical checks for known reasoning failures; and
- helper scripts that remove error-prone clerical work.

Bad teaching content includes:

- answer letters or case IDs;
- verbatim certification questions;
- a growing list of one-off corrections with no general rule;
- hidden controller reasoning;
- credentials or machine-local state;
- arbitrary instructions that only improve the current score; and
- vague reminders such as "be careful" without an observable procedure.

## Multiple-choice reliability

When Pi commonly retrieves the right rule but emits the wrong letter, teach a
mechanical private mapping:

```text
question ID -> retrieved rule -> exact matching option text -> printed letter
```

Require a two-way audit from the selected letter back to the exact option text.
Keep this separate from domain retrieval so the controller can distinguish a
knowledge failure from an answer-mapping failure.

## Natural discovery

Descriptions are routing infrastructure. Front-load the capability and concrete
trigger language so Pi can recognize when to load the skill naturally.

Natural discovery is still probabilistic. A production controller should use
the explicit skill path and slash expansion even when natural-discovery tests
pass.

After project trust and catalog exposure are confirmed, cap natural-discovery
diagnostics to a small development set. A correct answer without an observed
read is prior knowledge, not discovery success. If loading remains unreliable,
record the limitation and use forced activation rather than consuming domain
teaching cycles.
