---
name: code-review
description: Strict maintainability and structural code review. Use when Codex is asked to review code, review a PR or current branch, perform a deep code quality audit, run a harsh or thermonuclear review, evaluate abstraction quality, detect spaghetti growth, or push for simpler implementation structure.
---

# Code Review

Use this skill for unusually strict code review focused on implementation quality, maintainability, abstraction quality, and codebase health.

Be ambitious about structure. Do not stop at local cleanup opportunities when there is a clear way to preserve behavior while making the implementation smaller, simpler, more direct, or easier to reason about.

Source adapted from Cursor's `thermo-nuclear-code-quality-review` skill:
https://raw.githubusercontent.com/cursor/plugins/3347cbab5b54136f6fba0994c3a01a56f7fb7fca/cursor-team-kit/skills/thermo-nuclear-code-quality-review/SKILL.md

## Workflow

1. Read the changed files, surrounding code, tests, and relevant project guidance before judging the design.
2. Identify the behavioral intent of the change and the existing ownership boundaries it touches.
3. Look for a simpler framing before suggesting local edits. Prefer changes that delete concepts, branches, flags, wrappers, or special cases.
4. Check whether new logic belongs in the current layer or should move behind an existing helper, canonical model, or dedicated abstraction.
5. Lead the review with findings ordered by severity. Include file and line references, explain why the current structure is risky, and give a concrete path to improve it.
6. Keep summaries brief and secondary. Do not bury structural findings behind praise or cosmetic notes.

## Review Bar

Start from this standard:

> Perform a deep code quality audit of the current branch's changes. Rethink how to structure or implement the changes to meaningfully improve code quality without changing behavior. Improve abstractions, modularity, succinctness, and legibility. Reduce spaghetti code. Be thorough and rigorous.

Do not approve merely because behavior appears correct. Approval requires:

- no clear structural regression
- no obvious missed opportunity to make the implementation dramatically simpler
- no unjustified file-size explosion
- no obvious spaghetti growth from ad-hoc special-case branching
- no hacky, magical, wrapper-heavy, cast-heavy, or optionality-heavy design that obscures the real invariant
- no clear architecture-boundary leak or avoidable duplication of canonical helpers
- no missed decomposition that would materially improve maintainability

Treat these as presumptive blockers unless the author can justify them clearly:

- the PR preserves incidental complexity when a plausible restructuring would delete it
- the PR pushes a file from below 1000 lines to above 1000 lines
- the PR adds branching that tangles an existing flow
- the PR solves a local problem by scattering feature checks across shared code
- the PR adds an unnecessary abstraction, wrapper, cast, or loosely typed contract
- the PR duplicates an existing helper or puts logic in the wrong layer

## Questions To Ask

For every meaningful change, ask:

- Is there a restructuring that would make this dramatically simpler?
- Can this change be reframed so fewer concepts, branches, helpers, modes, or layers are needed?
- Does this improve or worsen the local architecture?
- Did the diff add branching complexity where a better model or abstraction should exist?
- Did a cohesive module become more coupled, stateful, or harder to scan?
- Is this logic in the right file, package, service, and layer?
- Did this change enlarge a file or component past a healthy size boundary?
- Are repeated conditionals signaling a missing model, helper, dispatcher, or state machine?
- Is the implementation direct and legible, or does it rely on incidental control flow and special cases?
- Is the abstraction earning its keep, or is it only a wrapper?
- Did the diff introduce casts, optionality, `any`, `unknown`, or ad-hoc object shapes that hide the real invariant?
- Is independent work being serialized for no reason?
- Can related updates be made more atomic so state is not left half-applied?

## What To Flag

Escalate findings for:

- complicated implementations where a cleaner framing could delete whole categories of complexity
- refactors that move complexity around without reducing the number of concepts readers must hold
- files crossing 1000 lines due to the change, especially when new code has a natural module boundary
- conditionals bolted onto unrelated code paths
- one-off booleans, nullable modes, or flags that complicate control flow
- feature-specific logic leaking into general-purpose modules
- generic magic that hides a simple data shape
- thin wrappers or identity abstractions that add indirection without clarity
- unnecessary casts, `any`, `unknown`, optional params, or silent fallbacks that muddy the contract
- copy-pasted logic instead of a clear helper
- narrow edge-case handling inserted into an already busy function
- tests passing while the code becomes less modular or harder to read
- temporary branching that is likely to become permanent debt
- bespoke helpers when the codebase already has a canonical utility
- logic added in the wrong layer or package
- sequential async flow when independent work could stay clearer in parallel
- partial-update logic that makes state harder to reason about

## Preferred Remedies

When a code-quality problem is real, suggest the smallest high-leverage restructuring that preserves behavior:

- delete a layer of indirection instead of polishing it
- reframe the state model so conditionals disappear
- move ownership to the layer that already owns the concept
- turn special-case logic into a simpler default flow
- extract a focused helper, pure function, subcomponent, or module
- split a large file into smaller cohesive units
- move feature-specific logic behind a dedicated abstraction
- replace condition chains with a typed model or explicit dispatcher
- separate orchestration from business logic
- collapse duplicate branches into one clearer path
- remove wrappers that do not clarify the API
- reuse the canonical helper instead of adding a near-duplicate
- make type boundaries explicit so control flow gets simpler
- parallelize independent work when that also clarifies orchestration
- make related updates atomic when partial state would be brittle

Do not settle for rename-only feedback when the issue is structural. Do not settle for a cleaner version of the same messy idea if there is a plausible simpler idea.

## Tone

Be direct, serious, and demanding about quality. Be respectful, but do not soften major maintainability issues into mild suggestions.

Useful review language:

- `this pushes the file past 1k lines. can we decompose this first?`
- `this adds another special-case branch into an already busy flow. can we move this behind its own abstraction?`
- `this works, but it makes the surrounding code harder to reason about. let's keep the behavior and restructure the implementation.`
- `this feels like feature logic leaking into a shared path. can we isolate it?`
- `this abstraction seems unnecessary. can we keep the direct flow?`
- `why does this need a cast or optional here? can we make the boundary explicit instead?`
- `this looks like a bespoke helper for something we already have elsewhere. can we reuse the canonical one?`
- `there is a simplification available here. can we reframe this so these branches disappear?`
- `this refactor moves complexity around, but does not delete it. is there a way to make the model simpler?`

## Output

Prioritize findings in this order:

1. Structural code-quality regressions
2. Missed opportunities for dramatic simplification
3. Spaghetti or branching complexity increases
4. Boundary, abstraction, or type-contract problems that make the code harder to reason about
5. File-size and decomposition concerns
6. Modularity and abstraction issues
7. Legibility and maintainability concerns

Prefer a smaller number of high-conviction findings over a long list of cosmetic notes. If there are no issues, say so clearly and identify any residual test or review gaps.
