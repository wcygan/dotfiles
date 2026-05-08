---
name: goal-shaping
description: Use when Codex should help a user choose, clarify, rank, or write a durable `/goal` objective for long-running work. Trigger for requests about finding a good goal, deciding what to work toward, turning an open-ended domain direction into impactful opportunities, defining success criteria, drafting a verifiable stopping condition, or preparing a goal prompt that includes concrete anchors such as URLs, files, issues, logs, metrics, or task lists.
---

# Goal Shaping

## Overview

Use this skill to help the user identify a goal worth giving Codex as a long-running objective. Shape the work until it is bigger than one prompt, smaller than an open-ended backlog, and has a verifiable stopping condition.

## Core Rule

Optimize for a useful goal contract, not a large plan. A strong goal says:

- what Codex should achieve
- what Codex should avoid changing
- which concrete references anchor the work in reality
- which short list of tasks Codex should improve first
- which context Codex must inspect first
- which commands, artifacts, or checks prove progress
- which checkpoint or condition means Codex should stop, pause, or ask

Do not turn unrelated ideas into one goal. Split them into separate candidate goals and help the user choose the one with the highest expected payoff.

## Workflow

1. Establish the user's direction.
   - Ask what domain, product, repo, workflow, or personal/business outcome they want to move toward.
   - Ask what constraint matters most: revenue, reliability, learning speed, polish, customer pain, migration risk, time box, or maintenance burden.
   - Ask for concrete references if they are missing and likely to change the goal: URLs, repo paths, issue/PR numbers, screenshots, logs, failing commands, metrics, customer examples, specs, notes, or rough task ideas.
   - If the user already gave enough context, infer the direction and state assumptions instead of blocking on questions.

2. Build an opportunity inventory.
   - Identify concrete opportunities from the user's direction: fixes, migrations, prototypes, experiments, evals, automations, tests, docs, launches, or research loops.
   - Preserve the user's strongest anchors as explicit evidence: exact links, file paths, issue IDs, commands, observed failures, current metrics, named users, sample inputs, or screenshots.
   - Prefer opportunities where Codex can read the relevant artifacts, make scoped progress, and validate each checkpoint.
   - Reject vague backlog buckets such as "improve the app" unless they can be narrowed to a measurable behavior or artifact.

3. Rank the candidates.
   Score each candidate qualitatively with:
   - Impact: meaningful user, business, learning, quality, or maintenance gain.
   - Evidence: available files, logs, issues, metrics, user examples, specs, or failing tests.
   - Codex leverage: enough implementation, analysis, or iteration work for Codex to do independently.
   - Verifiability: clear commands, screenshots, evals, tests, artifacts, or acceptance checks.
   - Risk: blast radius, reversibility, external dependencies, secrets, production access, or unclear ownership.

4. Choose or propose the goal.
   - Recommend one goal when the tradeoff is clear.
   - Offer two or three ranked options when the user needs a strategic choice.
   - Ask at most three short questions when the missing information changes which goal is best.

5. Draft the goal contract.
   Include:
   - Objective: one sentence.
   - Stopping condition: the exact verifiable end state.
   - Reality anchors: exact URLs, file paths, issue IDs, docs, logs, metrics, screenshots, examples, or user notes that Codex should treat as grounding evidence.
   - Highlighted tasks: 3-7 concrete improvements, investigations, or decisions that turn the direction into visible work.
   - Read first: files, docs, issues, logs, metrics, or plans to inspect.
   - Constraints and non-goals: boundaries that prevent scope creep.
   - Validation loop: commands or artifacts to check after each checkpoint.
   - Checkpoints: small ordered milestones with proof for each.
   - Pause conditions: when Codex should stop and ask for input.

6. Produce a `/goal` prompt when ready.
   Keep it compact, but include anchors and tasks when they exist. Do not invent references. If useful anchors are missing, make the first checkpoint gather them or ask the user for them.

   Use this shape:

   ```text
   /goal Complete [objective] without stopping until [verifiable end state].

   Reality anchors:
   - [URL/file/issue/log/metric/example that grounds the work]

   Highlighted tasks:
   - [specific improvement, investigation, or decision]

   First read [context]. Keep changes within [scope/non-goals]. Work in checkpoints; after each checkpoint run [validation] and record a short progress log. Pause if [pause conditions].
   ```

## Conversation Style

- Work with the user to clarify where they want to head in their domain before prescribing work.
- Use the user's language for their domain, customers, repo, product, or craft.
- Keep questions few and high leverage. Prefer "which outcome matters most?" over broad interviews.
- Surface tradeoffs directly: high-impact but risky, quick win but low leverage, valuable but not yet verifiable.
- Prefer concrete references over abstract summaries when drafting the final prompt; file paths, URLs, issue IDs, command names, and metric names make better anchors than prose labels.
- If the user asks to start immediately, still check that the goal has a stopping condition and validation loop before starting.

## Fitness Checks

A candidate is a good `/goal` if:

- it can survive multiple turns without constant steering
- it has one durable objective, not a mixed list
- it names the real artifacts, links, or observations that should guide the work
- it highlights the first few tasks or decisions that should get attention
- it can be validated with commands, artifacts, screenshots, evals, logs, or an explicit acceptance checklist
- it has clear boundaries and rollback or pause points
- it is feasible for Codex to advance with the available tools and permissions

A candidate needs more shaping if:

- success is subjective and no acceptance evidence is named
- the prompt only paraphrases the user's direction and lacks concrete anchors or task focus
- the work depends on unavailable credentials, private decisions, or production changes
- the scope mixes unrelated codebases, products, or strategic bets
- the first checkpoint cannot be identified

## Output Template

When presenting the result, use the smallest useful form:

````markdown
**Recommendation**
[One-sentence recommended goal and why it outranks the alternatives.]

**Goal Contract**
- Objective: ...
- Stopping condition: ...
- Reality anchors: ...
- Highlighted tasks: ...
- Read first: ...
- Constraints/non-goals: ...
- Validation loop: ...
- Checkpoints: ...
- Pause conditions: ...

**Goal Prompt**
```text
/goal ...
```
````

If the user is still choosing direction, replace the goal contract with a ranked list of candidates and the one or two questions needed to pick.

## Source Guidance

Base the goal shape on the OpenAI Codex "Follow a goal" use case: use `/goal` for long-running work with a clear target, validation loop, scoped progress, and a verifiable stopping condition.
