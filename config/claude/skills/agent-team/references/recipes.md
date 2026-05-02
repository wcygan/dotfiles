---
title: Proven Team Recipes
description: Lens-based team templates for common task types
tags: [recipes, lenses, examples]
---

# Proven Team Recipes

Each recipe lists the **lenses** to use, not specific agent names. When spawning, write a role prompt that establishes each lens (see [composition.md](composition.md) §5). Use `general-purpose` agents unless a project-local custom agent fits a lens precisely.

## Code Review (3 lenses)

**When**: Reviewing a PR or auditing a module.

```
Create a team to review [CODE/PR]:
- Error-path lens: find failure modes and unhandled errors
- Simplicity lens: identify unnecessary complexity
- Contract lens: check for breaking changes to public interfaces
Synthesize findings into a single review.
```

## Hardening (3 lenses)

**When**: Preparing a service for production.

```
Create a team to harden [SERVICE]:
- Error-path lens: failure modes and missing resilience
- Deploy-safety lens: rollout safety and rollback plan
- Observability lens: instrumentation and alerting gaps
Each works independently, then we synthesize.
```

## Design Review (3 lenses)

**When**: Evaluating a new design or architecture proposal.

```
Create a team to review [DESIGN]:
- Contract lens: interface stability and compatibility
- Simplicity lens: challenge unnecessary complexity
- Skeptic lens: question whether we need this at all
Have them debate and converge on a recommendation.
```

## Feature Development (3 lenses)

**When**: Building a new feature with clear scope.

```
Create a team to review the plan for [FEATURE]:
- Contract lens: interface design
- Test-strategy lens: testing approach and coverage layers
- Error-path lens: failure modes to handle
```

## Pre-Deploy Audit (3 lenses)

**When**: Final check before production.

```
Create a team to audit [SERVICE] before deploy:
- Deploy-safety lens: rollout risk and rollback plan
- Observability lens: monitoring and alerting gaps
- Error-path lens: unhandled failure modes
Each produces a go/no-go recommendation.
```

## Investigation (3 lenses)

**When**: Debugging a complex issue or understanding unfamiliar code.

```
Create a team to investigate [TOPIC/BUG]:
- Error-path lens: trace error paths and failure modes
- Skeptic lens: challenge initial hypotheses
- Concurrency lens: timing-dependent behavior
Have them share findings and challenge each other.
```

## Dependency Evaluation (2 lenses)

**When**: Considering adding a new library or framework.

```
Create a team to evaluate adding [DEPENDENCY]:
- Dependency-skeptic lens: necessity, maintenance risk, alternatives
- Skeptic lens: argue for the simplest path (maybe don't add it)
```

## Database Change Review (3 lenses)

**When**: Reviewing schema changes, migrations, or query patterns.

```
Create a team to review [MIGRATION/SCHEMA]:
- Data-model lens: schema correctness and migration safety
- Contract lens: backward compatibility with running code
- Deploy-safety lens: rollout ordering and rollback path
```

## Async / Concurrent Code Review (3 lenses)

**When**: Reviewing code with threads, async/await, channels, or shared state.

```
Create a team to review [ASYNC CODE]:
- Concurrency lens: races, deadlocks, cancellation safety
- Error-path lens: error handling under concurrent failure
- Simplicity lens: can the concurrency be eliminated?
```

## Refactor Review (3 lenses)

**When**: Evaluating a refactor before merging.

```
Create a team to review the refactor of [MODULE]:
- Simplicity lens: did we actually delete complexity, or just move it?
- Test-strategy lens: are existing behaviors covered?
- Contract lens: any subtle public-interface changes?
```
