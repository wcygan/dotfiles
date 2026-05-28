---
name: dynamic-workflow
description: Author and run a dynamic workflow — orchestrate many parallel subagents via the Workflow tool to be comprehensive, confident, or to take on scale one context can't hold. Use for codebase audits, large migrations, multi-source research, high-stakes verification, or any task worth fanning out across dozens of agents. Keywords dynamic workflow, Workflow tool, fan out, orchestrate subagents, parallel agents, migration, audit, multi-agent.
disable-model-invocation: true
argument-hint: <task to orchestrate, e.g. "audit auth/ for security bugs">
---

# Dynamic Workflow

Invoking this skill is your **explicit opt-in** to call the `Workflow` tool. Author a script that orchestrates subagents deterministically and run it. Workflows can spawn dozens of agents and burn substantial tokens — that's expected here because the user asked for it.

A workflow moves the plan *into code*: the script holds the loop, the branching, and every intermediate result, so your context keeps only the final answer. That's the reason to reach for one over plain subagents — scale one conversation can't coordinate, plus a repeatable quality pattern (e.g. agents adversarially reviewing each other's findings before they're reported). If the task doesn't need that, it isn't a workflow.

The task is `$ARGUMENTS`. If empty, ask the user what to orchestrate before doing anything else.

## Do this in order

1. **Scope inline first (hybrid).** Discover the work-list before orchestrating — list the files, find the call sites, scope the diff, enumerate the sources. You need to know the *shape of the work* before fanning out, not the answer. Cheap reads/greps now save a malformed fan-out later.

2. **Pick the pattern from the shape, not habit.**
   - Multi-stage per-item work → `pipeline()` (the default — no barrier between stages).
   - Need *all* prior results together (dedup, merge, early-exit on zero) → `parallel()` barrier.
   - Unknown-size discovery (bugs, edge cases) → loop-until-dry: keep spawning finders until K rounds find nothing new.
   - Any finding that could be wrong → adversarial verify: N independent skeptics prompted to *refute*; keep only what survives a majority.
   - Wide solution space → judge panel: N independent attempts, scored, synthesized.

3. **Scale to the ask.** "Quick check" → a few agents, single-vote verify. "Thorough audit / be comprehensive" → larger finder pool, 3–5 vote adversarial pass, synthesis stage. If the user gave a token budget (`+500k`-style), drive a `budget.remaining()` loop; otherwise size it to the request.

4. **Write the script and call `Workflow`.** Start with the pure-literal `meta` block (name, description, phases). Use `schema:` on `agent()` calls whenever you need structured data back — validation beats parsing. Use `phase:` explicitly inside `pipeline`/`parallel` stages so progress groups don't race. Prefer one well-scoped fan-out per turn; for multi-phase work (understand → design → implement → review) run several workflows in sequence so you stay in the loop between them.

5. **Read the result and report.** The Workflow returns its script's return value. Surface the conclusion, what was verified, and — critically — anything the workflow *capped or skipped* (top-N, no-retry, sampling). Don't let silent truncation read as full coverage.

6. **Offer to save it if it's repeatable.** If the run did something the user will rerun (a per-branch review, a recurring audit), tell them they can save that run's script as a `/command` from `/workflows` → press `s` (project `.claude/workflows/` or personal `~/.claude/workflows/`). Don't save it yourself.

## Before a long run

- **Allowlist what the agents need.** Workflow subagents run in `acceptEdits` mode and **auto-approve file edits** regardless of your session's permission mode — but shell commands, web fetches, and MCP tools that aren't in your allowlist still prompt mid-run, stalling the run until someone answers. For a migration or audit that runs many commands, suggest the user allowlist those commands first.
- **Check the model.** Every agent uses the session model unless a stage routes elsewhere. If the user is on a small model for routine work, a heavy run may want a stronger one (or vice versa) — mention `/model` before launching.
- **No mid-run input.** A run can't pause for the user except on permission prompts. If the task needs human sign-off between stages, split it into separate workflows (one per turn) rather than one big script.

## Guardrails

- The full `Workflow` tool spec (API surface, concurrency caps, resume, the complete pattern catalog with code) is already in your context whenever the tool is available — read it there rather than guessing. This skill only tells you *when and how to apply* it.
- Don't `mkdir` or Write the script to a file first — pass it inline via `script`. To iterate, edit the auto-persisted script path the tool returns and re-invoke with `scriptPath`.
- Scripts are plain JavaScript: no TypeScript annotations, no `Date.now()`/`Math.random()`/argless `new Date()` (they break resume — pass timestamps via `args` instead).
- If the task is trivial or you already have the answer, say so and skip the workflow — fanning out a one-file change wastes tokens.
