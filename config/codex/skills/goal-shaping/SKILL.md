---
name: goal-shaping
description: Use when Codex should help a user choose, clarify, rank, write, or set a durable goal objective for long-running work. Trigger for requests about finding a good goal, deciding what to work toward, turning an open-ended domain direction into impactful opportunities, defining measurable success criteria, drafting a verifiable stopping condition, setting an active goal with the available goal tool, or preparing a goal prompt that includes concrete anchors such as URLs, files, issues, logs, metrics, environments, progress artifacts, or task lists.
---

# Goal Shaping

## Overview

Use this skill to help the user identify and set a goal worth giving Codex as a long-running objective. Shape the work until it is bigger than one prompt, smaller than an open-ended backlog, and has a verifiable stopping condition. Treat the goal text as the exit criteria Codex will judge against after later turns, not as a large implementation plan.

## Core Rule

Optimize for a useful goal contract, not a large plan. A strong goal says:

- what Codex should achieve
- the measurable exit criteria, ideally a number, threshold, or explicit checklist
- what Codex should avoid changing
- which concrete references anchor the work in reality
- which short list of tasks Codex should improve first
- which context Codex must inspect first
- which commands, artifacts, or checks prove progress
- which realistic environment, data, browser, device, or deployment should be used for validation
- which durable progress artifact should track multi-hour work
- which final cleanup or review step prevents leftover failed attempts
- which checkpoint or condition means Codex should stop, pause, or ask

Do not turn unrelated ideas into one goal. Split them into separate candidate goals and help the user choose the one with the highest expected payoff.

## Goal Tool Default

When the user invokes this skill to turn direction into a Codex goal, treat that as permission to set the active goal once the contract is strong enough. Do not ask the user to copy a `/goal` prompt or confirm that Codex should set it.

Prefer the active goal-setting tool over a text-only prompt. If `set_goal` is available, use it. If this session exposes an equivalent tool such as `create_goal`, use that instead. Before creating a new goal, inspect the active goal when a goal-inspection tool is available. If there is already an active, conflicting goal, pause and ask how to proceed.

The goal text passed to the tool should be the strongest durable prompt Codex can construct for the user's intent. Put the verifiable stopping condition near the front because it is the practical exit criteria. Include the objective, measured success, reality anchors, constraints and non-goals, checkpoint plan, validation commands, progress artifact when needed, final cleanup step, and pause conditions. Keep it compact enough to be usable as a goal, but complete enough that Codex can resume from it later without reconstructing the user's intent.

Only fall back to producing a `/goal` prompt when a goal-setting tool is unavailable, when the user explicitly asks only for a prompt, or when the missing context materially changes the goal.

## Workflow

1. Establish the user's direction.
   - Ask what domain, product, repo, workflow, or personal/business outcome they want to move toward.
   - Ask what constraint matters most: revenue, reliability, learning speed, polish, customer pain, migration risk, time box, or maintenance burden.
   - Ask what measurable target, baseline, threshold, or acceptance checklist would prove success.
   - Ask for concrete references if they are missing and likely to change the goal: URLs, repo paths, issue/PR numbers, screenshots, logs, failing commands, metrics, customer examples, specs, notes, or rough task ideas.
   - Ask what realistic validation environment matters if local checks may be misleading: production-like flags, deploy previews, staging data, browser sessions, physical devices, logged-in tools, or representative datasets.
   - If the user already gave enough context, infer the direction and state assumptions instead of blocking on questions.

2. Build an opportunity inventory.
   - Identify concrete opportunities from the user's direction: fixes, migrations, prototypes, experiments, evals, automations, tests, docs, launches, or research loops.
   - Preserve the user's strongest anchors as explicit evidence: exact links, file paths, issue IDs, commands, observed failures, current metrics, named users, sample inputs, or screenshots.
   - Prefer opportunities where Codex can read the relevant artifacts, make scoped progress, measure progress, and validate each checkpoint.
   - If no measurement exists yet, prefer candidates where the first checkpoint can create or choose one: a benchmark, eval suite, screenshot diff, coverage report, status file, trace, or acceptance checklist.
   - Reject vague backlog buckets such as "improve the app" unless they can be narrowed to a measurable behavior or artifact.

3. Rank the candidates.
   Score each candidate qualitatively with:
   - Impact: meaningful user, business, learning, quality, or maintenance gain.
   - Evidence: available files, logs, issues, metrics, user examples, specs, or failing tests.
   - Codex leverage: enough implementation, analysis, or iteration work for Codex to do independently.
   - Measurability: a baseline, target, threshold, eval, diff, report, or checklist can show progress without gaming the result.
   - Verifiability: clear commands, screenshots, evals, tests, artifacts, or acceptance checks.
   - Environment fidelity: Codex can validate in a local, staging, preview, browser, device, or data environment close enough to the real problem.
   - Risk: blast radius, reversibility, external dependencies, secrets, production access, or unclear ownership.

4. Choose or propose the goal.
   - Recommend one goal when the tradeoff is clear.
   - Offer two or three ranked options when the user needs a strategic choice.
   - Ask at most three short questions when the missing information changes which goal is best.

5. Draft the goal contract.
   Include:
   - Objective: one sentence.
   - Stopping condition: the exact verifiable end state, preferably with a number, threshold, or explicit acceptance checklist.
   - Reality anchors: exact URLs, file paths, issue IDs, docs, logs, metrics, screenshots, examples, or user notes that Codex should treat as grounding evidence.
   - Measurement strategy: the baseline, target, benchmark, eval, visual diff, checklist, metric, or artifact that proves progress.
   - Highlighted tasks: 3-7 concrete improvements, investigations, or decisions that turn the direction into visible work.
   - Read first: files, docs, issues, logs, metrics, or plans to inspect.
   - Environment: where validation should run and what data, flags, browser, device, deployment, or credentials are in scope.
   - Constraints and non-goals: boundaries that prevent scope creep and prevent bad shortcuts such as deleting tests, lowering coverage, inlining screenshots, hard-coding fixtures, or weakening requirements to satisfy the metric.
   - Validation loop: commands or artifacts to check after each checkpoint.
   - Checkpoints: small ordered milestones with proof for each, ending with a cleanup/review checkpoint for long-running work.
   - Progress artifact: commits, draft PR, status markdown, report, dashboard, image, or message target for multi-hour or multi-day goals.
   - Pause conditions: when Codex should stop and ask for input.

6. Set the goal when ready.
   Keep the goal compact, but include anchors and tasks when they exist. Do not invent references. If useful anchors are missing and they would materially change the goal, ask for them. If missing anchors can be discovered during the work, make the first checkpoint gather them.

   If a goal-setting tool is available, pass it a goal shaped like this:

   ```text
   Complete [objective] without stopping until [measurable or checklist-based end state].

   Reality anchors:
   - [URL/file/issue/log/metric/example that grounds the work]

   Measurement and environment:
   - [baseline, target, benchmark, eval, diff, checklist, or artifact]
   - [local/staging/preview/browser/device/data environment to validate in]

   Highlighted tasks:
   - [specific improvement, investigation, or decision]

   First read [context]. Keep changes within [scope/non-goals and anti-shortcut constraints]. Work in checkpoints; after each checkpoint run [validation] and record progress in [artifact or brief log]. Final checkpoint: review the diff, remove dead attempts, and rerun [final validation]. Pause if [pause conditions].
   ```

   If no goal-setting tool is available, produce a `/goal` prompt instead:

   Use this shape:

   ```text
   /goal Complete [objective] without stopping until [measurable or checklist-based end state].

   Reality anchors:
   - [URL/file/issue/log/metric/example that grounds the work]

   Measurement and environment:
   - [baseline, target, benchmark, eval, diff, checklist, or artifact]
   - [local/staging/preview/browser/device/data environment to validate in]

   Highlighted tasks:
   - [specific improvement, investigation, or decision]

   First read [context]. Keep changes within [scope/non-goals and anti-shortcut constraints]. Work in checkpoints; after each checkpoint run [validation] and record progress in [artifact or brief log]. Final checkpoint: review the diff, remove dead attempts, and rerun [final validation]. Pause if [pause conditions].
   ```

## Conversation Style

- Work with the user to clarify where they want to head in their domain before prescribing work.
- Use the user's language for their domain, customers, repo, product, or craft.
- Keep questions few and high leverage. Prefer "which outcome matters most?" over broad interviews.
- Do not ask permission to set the goal after the user has invoked this skill. Ask only for facts that materially change the goal or for direction when an existing active goal conflicts.
- Surface tradeoffs directly: high-impact but risky, quick win but low leverage, valuable but not yet verifiable.
- Prefer concrete references over abstract summaries when drafting the goal text; file paths, URLs, issue IDs, command names, and metric names make better anchors than prose labels.
- Prefer measured or checklist-based outcomes over broad qualitative targets. If a number is artificial or misleading, use an explicit acceptance checklist instead.
- For visual goals, treat images as context and define success with feature checklists, design-system rules, screenshot diffs, or reviewable acceptance criteria. Avoid "pixel perfect" as the only stopping condition unless Codex has a reliable comparison tool and the non-visual requirements are also covered.
- For long-running goals, include a durable progress trail such as meaningful commits, a draft PR, a markdown status artifact, screenshots, reports, or another agreed update channel.
- If the user asks to start immediately, still check that the goal has a stopping condition and validation loop before starting.

## Fitness Checks

A candidate is a good active goal if:

- it can survive multiple turns without constant steering
- it has one durable objective, not a mixed list
- it names the real artifacts, links, or observations that should guide the work
- it highlights the first few tasks or decisions that should get attention
- it has a measurement strategy or a first checkpoint to create one
- it can be validated with commands, artifacts, screenshots, evals, logs, or an explicit acceptance checklist
- it names a validation environment realistic enough for the problem
- it includes anti-shortcut constraints when the metric could be gamed
- it has clear boundaries and rollback or pause points
- it includes final cleanup or review when the goal may run through multiple attempts
- it is feasible for Codex to advance with the available tools and permissions

A candidate needs more shaping if:

- success is subjective and no acceptance evidence is named
- the prompt only paraphrases the user's direction and lacks concrete anchors or task focus
- the target can be satisfied by weakening the workload, deleting tests, lowering quality, hard-coding results, or hiding missing behavior
- the validation environment is unrealistic for the outcome the user cares about
- the goal is mostly visual but lacks a comparison tool, design-system checklist, or reviewable acceptance criteria
- the work depends on unavailable credentials, private decisions, or production changes
- the scope mixes unrelated codebases, products, or strategic bets
- the first checkpoint cannot be identified

## Output Template

When presenting the result before setting a goal, use the smallest useful form:

````markdown
**Recommendation**
[One-sentence recommended goal and why it outranks the alternatives.]

**Goal Contract**
- Objective: ...
- Stopping condition: ...
- Reality anchors: ...
- Measurement strategy: ...
- Highlighted tasks: ...
- Read first: ...
- Environment: ...
- Constraints/non-goals: ...
- Validation loop: ...
- Checkpoints: ...
- Progress artifact: ...
- Pause conditions: ...

**Goal Prompt**
```text
/goal ...
```
````

If the user is still choosing direction, replace the goal contract with a ranked list of candidates and the one or two questions needed to pick.

When the goal has been set with a goal tool, do not also present a long `/goal` prompt. Briefly state that the goal was set, summarize the objective and stopping condition, then start or continue the first checkpoint.

## Source Guidance

Base the goal shape on the OpenAI Codex "Follow a goal" use case: use `/goal` for long-running work with a clear target, validation loop, scoped progress, and a verifiable stopping condition.
