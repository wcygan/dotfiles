---
title: Smart Composition
description: Algorithm for composing agent teams from task descriptions
tags: [composition, algorithm, tension, team-sizing]
---

# Smart Composition

When the user describes a task without specifying agents, use this process to recommend a team.

## 1. Classify the Task Type

| Signal in Request | Task Type | Likely Agents |
|-------------------|-----------|---------------|
| "review", "check", "audit" | Review | error-path-reviewer, contract-reviewer, simplifier |
| "design", "plan", "architect" | Design | contract-reviewer, devils-advocate, simplifier |
| "build", "implement", "create" | Development | contract-reviewer, test-strategist, error-path-reviewer |
| "debug", "fix", "investigate" | Investigation | error-path-reviewer, concurrency-reviewer, devils-advocate |
| "refactor", "clean up", "improve" | Refactoring | simplifier, test-strategist, contract-reviewer |
| "harden", "production-ready" | Hardening | error-path-reviewer, deploy-safety-reviewer, observability-advisor |
| "migrate", "upgrade" | Migration | contract-reviewer, deploy-safety-reviewer, devils-advocate |
| "add dependency", "new library" | Dependency | dependency-skeptic, simplifier, contract-reviewer |
| "deploy", "ship", "release" | Deployment | deploy-safety-reviewer, observability-advisor, error-path-reviewer |

## 2. Add Required Perspectives

Based on the task, consider adding:
- Touches **error handling or I/O**? → error-path-reviewer
- Changes **public interfaces**? → contract-reviewer
- Involves **database schemas**? → data-model-analyst
- Adds **new dependencies**? → dependency-skeptic
- Has **concurrent/async code**? → concurrency-reviewer
- **Major decision**? → devils-advocate
- Going to **production**? → deploy-safety-reviewer + observability-advisor
- Feels **over-engineered**? → simplifier

## 3. Select Productive Tension Pairs

Agents whose lenses naturally conflict create better outcomes through debate:

| Tension Pair | What They Debate |
|-------------|-----------------|
| simplifier vs error-path-reviewer | "Keep it simple" vs "Handle this failure mode" |
| simplifier vs observability-advisor | "That's noise, delete it" vs "You'll need this at 3 AM" |
| contract-reviewer vs simplifier | "You'll break consumers" vs "Just change the API" |
| dependency-skeptic vs anyone adding a lib | "Write it yourself" vs "Don't reinvent the wheel" |
| devils-advocate vs everyone | "Do we even need this?" |
| concurrency-reviewer vs simplifier | "Add synchronization" vs "Remove the shared state" |

## 4. Right-Size the Team

- **2 teammates**: simple, focused tasks
- **3 teammates**: most tasks (best coordination-to-value ratio)
- **4-5 teammates**: complex audits or multi-hypothesis debugging
- Aim for **5-6 tasks per teammate** to keep everyone productive
- Beyond 5, coordination overhead often outweighs benefit
