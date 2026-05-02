---
title: Smart Composition
description: Design agent teams by selecting perspectives (lenses), not named agents
tags: [composition, perspectives, tension, team-sizing]
---

# Smart Composition

Compose teams by **perspective**, not by named agent. Each teammate is a `general-purpose` agent (or a project-local custom agent if one fits) with a role prompt that establishes a specific lens. Different lenses produce productive disagreement; that disagreement is the point.

## 1. Classify the Task

| Signal in Request | Task Type | Useful Lenses |
|-------------------|-----------|---------------|
| "review", "check", "audit" | Review | error paths, breaking changes, simplicity |
| "design", "plan", "architect" | Design | interface stability, simplicity, skeptic |
| "build", "implement", "create" | Development | interface design, test strategy, error paths |
| "debug", "fix", "investigate" | Investigation | error paths, concurrency/timing, skeptic |
| "refactor", "clean up", "improve" | Refactoring | simplicity, test coverage, contract stability |
| "harden", "production-ready" | Hardening | error paths, deploy safety, observability |
| "migrate", "upgrade" | Migration | contract stability, deploy safety, skeptic |
| "add dependency", "new library" | Dependency | dependency skepticism, simplicity, contract impact |
| "deploy", "ship", "release" | Deployment | deploy safety, observability, error paths |

## 2. Add Lenses Based on Code Touched

| Code touches… | Add lens |
|---------------|----------|
| Error handling, I/O, parsing | **Error-path** — what breaks under failure? |
| Public interfaces, APIs, schemas | **Contract** — who depends on this and how? |
| Database schemas, migrations | **Data-model** — schema integrity, migration safety, query correctness |
| New dependencies / libraries | **Dependency-skeptic** — is this necessary? what's the maintenance cost? |
| Async, threads, channels, locks | **Concurrency** — races, deadlocks, cancellation, ordering |
| Production deploy / rollout | **Deploy-safety** + **Observability** — rollback path, instrumentation gaps |
| Tests, coverage, mocking | **Test-strategy** — right tests at right layer, no mocking theater |
| "Obvious" or "necessary" claim | **Skeptic** — do we even need this? |
| Feels over-engineered | **Simplicity** — what can be deleted? |

## 3. Pick Tension Pairs

Productive teams have lenses that disagree. Some proven tensions:

| Tension | What They Debate |
|---------|------------------|
| simplicity ↔ error-path | "delete it" vs "handle this failure" |
| simplicity ↔ observability | "that's noise" vs "you'll need this at 3 AM" |
| contract ↔ simplicity | "you'll break consumers" vs "just change the API" |
| dependency-skeptic ↔ feature-builder | "write it yourself" vs "don't reinvent the wheel" |
| skeptic ↔ everyone | "do we even need this?" |
| concurrency ↔ simplicity | "add synchronization" vs "remove the shared state" |
| deploy-safety ↔ skeptic | "here's how to ship safely" vs "don't ship at all" |
| test-strategy ↔ data-model | "test the behavior" vs "test the constraints" |

A team without tension converges too fast and produces shallow output. Always include at least one lens that will push back on the default direction.

## 4. Right-Size

- **2 teammates**: simple, focused tasks
- **3 teammates**: most tasks (best coordination-to-value ratio)
- **4-5 teammates**: complex audits or multi-hypothesis debugging
- Aim for **5-6 tasks per teammate** to stay productive
- Beyond 5 teammates, coordination overhead usually outweighs value

## 5. Write the Role Prompt

When spawning each teammate, the prompt establishes the lens. Generic patterns:

```
You are reviewing <thing> through a <lens> lens.

Your job is to <one-sentence mission tied to the lens>. Argue for
<what the lens defends>. Push back on <what the lens rejects>.
Cite specific files and lines.

Out of scope for you: <other lenses>. Other teammates own those.

Deliverable: <report / pass-fail / list-of-issues>.
```

Concrete example for the error-path lens on a payment module:

```
You are reviewing the payments module through an error-path lens.

Your job is to find every failure mode that the current code does not
handle correctly. Argue for explicit error handling, retries with
clear semantics, and surfaced failures over silent ones. Push back on
"this never fails" claims unless the type system enforces it.

Out of scope: code style, simplicity, naming. Other teammates own those.

Deliverable: a list of (file:line, failure mode, current behavior,
recommended behavior).
```

## 6. Use Project-Local Custom Agents If They Fit

Before defaulting to `general-purpose`, check `~/.claude/agents/` and `.claude/agents/` for custom agents whose frontmatter matches the lens you want. If one fits, use its `subagent_type` directly — its system prompt is already tuned. If nothing fits, use `general-purpose` with a role prompt and consider creating a custom agent afterward if the lens recurs.
