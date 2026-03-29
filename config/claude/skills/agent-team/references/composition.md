---
title: Smart Composition
description: Algorithm for composing agent teams from task descriptions, including tension pairs
tags: [composition, algorithm, tension, team-sizing]
---

# Smart Composition

When the user describes a task without specifying agents, use this process to recommend a team.

## 1. Classify the Task Type

| Signal in Request | Task Type | Likely Agents |
|-------------------|-----------|---------------|
| "review", "check", "audit" | Review | security-auditor, performance-analyst, test-strategist |
| "design", "plan", "architect" | Design | api-designer, domain-modeler, devils-advocate |
| "build", "implement", "create" | Development | api-designer, domain-modeler, test-strategist |
| "debug", "fix", "investigate" | Investigation | implementation-investigator, reliability-engineer, devils-advocate |
| "refactor", "clean up", "improve" | Refactoring | refactoring-strategist, test-strategist, performance-analyst |
| "harden", "production-ready" | Hardening | security-auditor, reliability-engineer, performance-analyst |
| "migrate", "upgrade" | Migration | tech-lead, reliability-engineer, devils-advocate |

## 2. Add Required Perspectives

Based on the task, consider adding:
- Touches **security boundaries**? → security-auditor
- Involves **data modeling**? → domain-modeler
- Needs **API/interface design**? → api-designer
- **Performance critical**? → performance-analyst
- Needs **test coverage**? → test-strategist
- **Major decision**? → devils-advocate
- Involves **failure handling**? → reliability-engineer

## 3. Select Productive Tension Pairs

Agents whose lenses naturally conflict create better outcomes through debate:

| Tension Pair | What They Debate |
|-------------|-----------------|
| security-auditor vs performance-analyst | "Is the security measure too expensive?" |
| api-designer vs domain-modeler | "Clean for consumers?" vs "Correct for the domain?" |
| reliability-engineer vs performance-analyst | "Add resilience overhead" vs "Reduce latency" |
| devils-advocate vs everyone | "Do we even need this?" |
| test-strategist vs performance-analyst | "More test coverage" vs "Faster test suite" |
| tech-lead vs devils-advocate | "Best practice says..." vs "In our context..." |

## 4. Right-Size the Team

- **2 teammates**: simple, focused tasks
- **3 teammates**: most tasks (best coordination-to-value ratio)
- **4-5 teammates**: complex audits or multi-hypothesis debugging
- Aim for **5-6 tasks per teammate** to keep everyone productive
- Beyond 5, coordination overhead often outweighs benefit
