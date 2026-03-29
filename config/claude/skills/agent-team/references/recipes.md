---
title: Proven Team Compositions
description: Tested team recipes for common task types
tags: [recipes, compositions, examples]
---

# Proven Team Compositions

## Design Review (3 agents)

**When**: Evaluating a new feature design, API shape, or architecture proposal.

```
Create an agent team for a design review:
- api-designer: evaluate the interface from the consumer's perspective
- domain-modeler: evaluate whether the data model is correct
- devils-advocate: challenge assumptions and argue for simpler alternatives
Have them review [DESCRIBE WHAT] and debate their findings.
```

## Hardening (3 agents)

**When**: Preparing a service for production, auditing existing systems.

```
Create an agent team to harden [SERVICE/MODULE]:
- security-auditor: find vulnerabilities and attack vectors
- reliability-engineer: identify failure modes and missing resilience
- performance-analyst: find bottlenecks and scaling issues
Have each reviewer work independently, then synthesize findings.
```

## Full Architecture Review (4 agents)

**When**: Major architectural decisions, system design reviews.

```
Create an agent team to review [ARCHITECTURE/DESIGN]:
- tech-lead: evaluate overall approach and team impact
- security-auditor: assess security implications
- performance-analyst: analyze scaling and efficiency
- devils-advocate: challenge necessity and complexity
Require plan approval before any changes.
```

## Feature Development (3 agents)

**When**: Building a new feature with clear scope.

```
Create an agent team to implement [FEATURE]:
- api-designer: design the interface and contracts
- domain-modeler: design the data model and state management
- test-strategist: write tests in parallel based on the design
Have the api-designer and domain-modeler coordinate on the contract,
then the test-strategist writes tests against it.
```

## Pre-Production Audit (4 agents)

**When**: Final quality check before shipping.

```
Create an agent team to audit [SERVICE] before production:
- security-auditor: security vulnerabilities and dependency risks
- reliability-engineer: error handling and observability gaps
- test-strategist: test coverage and verification completeness
- performance-analyst: performance bottlenecks and scaling limits
Each reviewer should produce a findings report with severity ratings.
```

## Investigation (3 agents)

**When**: Understanding an unfamiliar codebase or debugging complex issues.

```
Create an agent team to investigate [TOPIC/BUG]:
- implementation-investigator: trace code paths and map architecture
- devils-advocate: challenge initial hypotheses
- reliability-engineer: analyze failure modes and error paths
Have them share findings and challenge each other's conclusions.
```

## Refactoring (3 agents)

**When**: Planning and executing a significant refactor.

```
Create an agent team to refactor [MODULE]:
- refactoring-strategist: identify smells and plan the refactoring
- test-strategist: ensure test safety net exists before changes
- performance-analyst: verify no performance regressions
Require plan approval from the refactoring-strategist before any changes.
```

## Debugging with Competing Hypotheses (4-5 agents)

**When**: Root cause is unclear, multiple theories exist.

```
Users report [SYMPTOM]. Create an agent team to investigate:
- Teammate 1: investigate [hypothesis A]
- Teammate 2: investigate [hypothesis B]
- Teammate 3: investigate [hypothesis C]
- devils-advocate: challenge each theory and look for what they're missing
Have them actively try to disprove each other's theories.
Update findings only when there's consensus.
```

## K8s Deployment Review (3 agents)

**When**: Reviewing Kubernetes deployments and infrastructure.

```
Create an agent team to review [K8S DEPLOYMENT]:
- kubernetes-architect: evaluate cluster architecture and configs
- security-auditor: assess RBAC, network policies, secrets management
- reliability-engineer: evaluate health checks, resource limits, disruption budgets
```
