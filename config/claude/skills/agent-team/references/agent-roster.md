---
title: Agent Roster
description: Built-in agent definitions and discovery procedure for agent teams
tags: [agents, roster, discovery]
---

# Agent Roster

## Discovery

Before selecting agents, discover what's available:

1. Check `~/.claude/agents/*.md` (global) and `.claude/agents/*.md` (project-local)
2. Read each agent's frontmatter to understand capabilities
3. Custom agents that overlap with built-in ones take precedence (tailored to user's workflow)
4. Present both custom and built-in agents when recommending teams

## General-Purpose Agents

| Agent | Lens | Memory | Best For |
|-------|------|--------|----------|
| **tech-lead** | Senior leadership, architecture decisions | none | Code reviews, architectural guidance, technical strategy |
| **implementation-investigator** | Reverse-engineering codebases | none | Understanding how things work, tracing code paths |
| **refactoring-strategist** | Code quality, design patterns | none | Identifying tech debt, planning refactors |
| **security-auditor** | Threat modeling, vulnerabilities | user | Security reviews, dependency audits, threat modeling |
| **test-strategist** | Test architecture, TDD, coverage | user | Test design, coverage gaps, flaky test diagnosis |
| **performance-analyst** | Complexity, profiling, optimization | user | Bottleneck analysis, caching strategy, query optimization |
| **api-designer** | Interface ergonomics, consumer UX | none | API design, CLI design, library interface review |
| **domain-modeler** | DDD, schemas, state machines | project | Data modeling, bounded contexts, state management |
| **reliability-engineer** | Failure modes, observability | user | Error handling, resilience patterns, monitoring design |
| **devils-advocate** | Assumption challenging, simplicity | none | Preventing groupthink, simplicity advocacy, stress-testing proposals |

## Domain-Specific Agents

| Agent | Lens | Best For |
|-------|------|----------|
| **kubernetes-architect** | K8s infrastructure | Cluster design, networking, storage, security |
| **skaffold-deployment-expert** | K8s dev workflows | Skaffold config, local dev, CI/CD with Skaffold |
| **fedora-sysadmin** | Fedora Linux administration | DNF, SELinux, systemd, system troubleshooting |
