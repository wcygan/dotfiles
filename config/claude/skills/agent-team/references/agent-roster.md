---
title: Agent Roster
description: Agent definitions and discovery procedure for agent teams
tags: [agents, roster, discovery]
---

# Agent Roster

## Discovery

Before selecting agents, discover what's available:

1. Check `~/.claude/agents/*.md` (global) and `.claude/agents/*.md` (project-local)
2. Read each agent's frontmatter to understand capabilities
3. Custom agents that overlap with built-in ones take precedence
4. Present discovered agents when recommending teams

## Tier 1 — Core (use on most teams)

| Agent | Lens | Model | Best For |
|-------|------|-------|----------|
| **devils-advocate** | Challenges assumptions, argues for doing less | opus | Architectural decisions, RFCs, any "obvious" solution |
| **simplifier** | Rejects complexity, argues for deletion | sonnet | PR reviews, refactoring proposals, over-engineered code |
| **error-path-reviewer** | Focuses on what happens when things go wrong | sonnet | I/O, networking, parsing, anything that can fail |
| **contract-reviewer** | Guards backward compatibility and interface stability | sonnet | API changes, schema migrations, RPC modifications |

## Tier 2 — Common Tasks

| Agent | Lens | Model | Best For |
|-------|------|-------|----------|
| **test-strategist** | Right tests at right layer, rejects mocking theater | sonnet | Test strategy, reviewing test code, coverage debates |
| **data-model-analyst** | Schema integrity, migration safety, query correctness | sonnet | Table changes, migrations, query logic review |
| **dependency-skeptic** | Questions every new dependency | sonnet | Library additions, dependency updates, Cargo.toml/package.json changes |
| **concurrency-reviewer** | Finds races, deadlocks, cancellation bugs | opus | Async code, threads, channels, locks, shared state |
| **deploy-safety-reviewer** | Evaluates rollout risk and rollback safety | sonnet | Pre-deploy review, K8s manifests, migration ordering |
| **observability-advisor** | Argues for instrumentation and debuggability | sonnet | New services, error paths, performance-sensitive code |

## Key Tension Pairs

| Pair | What They Debate |
|------|-----------------|
| devils-advocate vs everyone | "Do we even need this?" |
| simplifier vs error-path-reviewer | "Keep it simple" vs "Handle this failure" |
| simplifier vs observability-advisor | "That's noise" vs "You'll need this at 3 AM" |
| contract-reviewer vs simplifier | "You'll break consumers" vs "Just change it" |
| dependency-skeptic vs anyone adding a library | "Write it yourself" vs "Don't reinvent the wheel" |
| test-strategist vs data-model-analyst | "Test the behavior" vs "Test the constraints" |
| concurrency-reviewer vs simplifier | "This needs synchronization" vs "Remove the concurrency" |
| deploy-safety-reviewer vs devils-advocate | "Here's how to ship it safely" vs "Don't ship it at all" |
