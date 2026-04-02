---
title: Proven Team Compositions
description: Tested team recipes for common task types
tags: [recipes, compositions, examples]
---

# Proven Team Compositions

## Code Review (3 agents)

**When**: Reviewing a PR, evaluating code quality, or auditing a module.

```
Create a team to review [CODE/PR]:
- error-path-reviewer: find failure modes and unhandled errors
- simplifier: identify unnecessary complexity
- contract-reviewer: check for breaking changes
Synthesize findings into a single review.
```

## Hardening (3 agents)

**When**: Preparing a service for production.

```
Create a team to harden [SERVICE]:
- error-path-reviewer: find failure modes and missing resilience
- deploy-safety-reviewer: evaluate rollout safety and rollback plans
- observability-advisor: find observability gaps
Each reviewer works independently, then synthesize findings.
```

## Design Review (3 agents)

**When**: Evaluating a new feature design or architecture proposal.

```
Create a team to review [DESIGN]:
- contract-reviewer: evaluate interface stability and compatibility
- simplifier: challenge unnecessary complexity
- devils-advocate: question whether we need this at all
Have them debate and converge on a recommendation.
```

## Feature Development (3 agents)

**When**: Building a new feature with clear scope.

```
Create a team to review the plan for [FEATURE]:
- contract-reviewer: evaluate the interface design
- test-strategist: plan the testing approach
- error-path-reviewer: identify failure modes to handle
```

## Pre-Deploy Audit (3 agents)

**When**: Final check before shipping to production.

```
Create a team to audit [SERVICE] before deploy:
- deploy-safety-reviewer: rollout risk and rollback plan
- observability-advisor: monitoring and alerting gaps
- error-path-reviewer: unhandled failure modes
Each produces a go/no-go recommendation.
```

## Investigation (3 agents)

**When**: Debugging complex issues or understanding unfamiliar code.

```
Create a team to investigate [TOPIC/BUG]:
- error-path-reviewer: trace error paths and failure modes
- devils-advocate: challenge initial hypotheses
- concurrency-reviewer: analyze timing-dependent behavior
Have them share findings and challenge each other.
```

## Dependency Evaluation (2 agents)

**When**: Evaluating whether to add a new library or framework.

```
Create a team to evaluate adding [DEPENDENCY]:
- dependency-skeptic: assess necessity, risk, and alternatives
- devils-advocate: argue for the simplest path (maybe don't add it)
```

## Database Change Review (3 agents)

**When**: Reviewing schema changes, migrations, or query patterns.

```
Create a team to review [MIGRATION/SCHEMA]:
- data-model-analyst: schema correctness and migration safety
- contract-reviewer: backward compatibility with running code
- deploy-safety-reviewer: rollout ordering and rollback path
```

## Async/Concurrent Code Review (3 agents)

**When**: Reviewing code with threads, async/await, channels, or shared state.

```
Create a team to review [ASYNC CODE]:
- concurrency-reviewer: races, deadlocks, cancellation safety
- error-path-reviewer: error handling in concurrent context
- simplifier: can the concurrency be eliminated?
```
