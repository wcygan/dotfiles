---
name: agent-team
description: Launch and coordinate Claude Code agent teams for complex tasks. Use when the user wants to parallelize work across multiple agents, needs a team for review, debugging, design, or feature development, or asks to "create a team" or "spawn agents." Keywords: agent team, team, spawn, teammates, parallel agents, coordinate, collaborate, multi-agent
---

# Agent Team Launcher

Launch and coordinate Claude Code agent teams using the available agent roster. This skill knows which agents exist, how they complement each other, and which team compositions work best for different tasks.

## Prerequisites

Agent teams are experimental. Ensure this is set in settings.json:

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

## Available Agent Roster

### General-Purpose Agents

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

### Domain-Specific Agents

| Agent | Lens | Best For |
|-------|------|----------|
| **kubernetes-architect** | K8s infrastructure | Cluster design, networking, storage, security |
| **skaffold-deployment-expert** | K8s dev workflows | Skaffold config, local dev, CI/CD with Skaffold |
| **fedora-sysadmin** | Fedora Linux administration | DNF, SELinux, systemd, system troubleshooting |

## Proven Team Compositions

### Design Review (3 agents)
**When**: Evaluating a new feature design, API shape, or architecture proposal.
```
Create an agent team for a design review:
- api-designer: evaluate the interface from the consumer's perspective
- domain-modeler: evaluate whether the data model is correct
- devils-advocate: challenge assumptions and argue for simpler alternatives
Have them review [DESCRIBE WHAT] and debate their findings.
```

### Hardening (3 agents)
**When**: Preparing a service for production, auditing existing systems.
```
Create an agent team to harden [SERVICE/MODULE]:
- security-auditor: find vulnerabilities and attack vectors
- reliability-engineer: identify failure modes and missing resilience
- performance-analyst: find bottlenecks and scaling issues
Have each reviewer work independently, then synthesize findings.
```

### Full Architecture Review (4 agents)
**When**: Major architectural decisions, system design reviews.
```
Create an agent team to review [ARCHITECTURE/DESIGN]:
- tech-lead: evaluate overall approach and team impact
- security-auditor: assess security implications
- performance-analyst: analyze scaling and efficiency
- devils-advocate: challenge necessity and complexity
Require plan approval before any changes.
```

### Feature Development (3 agents)
**When**: Building a new feature with clear scope.
```
Create an agent team to implement [FEATURE]:
- api-designer: design the interface and contracts
- domain-modeler: design the data model and state management
- test-strategist: write tests in parallel based on the design
Have the api-designer and domain-modeler coordinate on the contract, 
then the test-strategist writes tests against it.
```

### Pre-Production Audit (4 agents)
**When**: Final quality check before shipping.
```
Create an agent team to audit [SERVICE] before production:
- security-auditor: security vulnerabilities and dependency risks
- reliability-engineer: error handling and observability gaps
- test-strategist: test coverage and verification completeness
- performance-analyst: performance bottlenecks and scaling limits
Each reviewer should produce a findings report with severity ratings.
```

### Investigation (3 agents)
**When**: Understanding an unfamiliar codebase or debugging complex issues.
```
Create an agent team to investigate [TOPIC/BUG]:
- implementation-investigator: trace code paths and map architecture
- devils-advocate: challenge initial hypotheses
- reliability-engineer: analyze failure modes and error paths
Have them share findings and challenge each other's conclusions.
```

### Refactoring (3 agents)
**When**: Planning and executing a significant refactor.
```
Create an agent team to refactor [MODULE]:
- refactoring-strategist: identify smells and plan the refactoring
- test-strategist: ensure test safety net exists before changes
- performance-analyst: verify no performance regressions
Require plan approval from the refactoring-strategist before any changes.
```

### Debugging with Competing Hypotheses (4-5 agents)
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

### K8s Deployment Review (3 agents)
**When**: Reviewing Kubernetes deployments and infrastructure.
```
Create an agent team to review [K8S DEPLOYMENT]:
- kubernetes-architect: evaluate cluster architecture and configs
- security-auditor: assess RBAC, network policies, secrets management
- reliability-engineer: evaluate health checks, resource limits, disruption budgets
```

## Instructions

When the user wants to create an agent team:

### 1. Identify the Task Type

Match the user's request to one of the proven compositions above, or design a custom team based on the task. Key questions:
- What kind of work? (review, build, investigate, debug, refactor)
- How many perspectives needed? (2-5 agents, prefer 3)
- Do agents need to debate or work independently?

### 2. Select Agents

Choose agents whose lenses create **productive tension**:

| Tension Pair | What They Debate |
|-------------|-----------------|
| security-auditor vs performance-analyst | "Is the security measure too expensive?" |
| api-designer vs domain-modeler | "Clean for consumers?" vs "Correct for the domain?" |
| reliability-engineer vs performance-analyst | "Add resilience overhead" vs "Reduce latency" |
| devils-advocate vs everyone | "Do we even need this?" |
| test-strategist vs performance-analyst | "More test coverage" vs "Faster test suite" |
| tech-lead vs devils-advocate | "Best practice says..." vs "In our context..." |

### 3. Craft the Team Prompt

A good team prompt includes:
- **Clear task description**: What are we working on?
- **Role assignments**: What each teammate focuses on
- **Interaction model**: Should they debate, work independently, or coordinate?
- **Deliverable**: What does the team produce? (report, code, plan)
- **Plan approval**: Add "Require plan approval before changes" for risky work

### 4. Configure the Team

**Use delegate mode** (Shift+Tab) to keep the lead orchestrating, not implementing.

**Display mode options**:
- In-process (default): Shift+Up/Down to switch between teammates
- Split panes: Set `"teammateMode": "tmux"` for tmux/iTerm2 users

**Size guidance**:
- 2 agents: Simple review or investigation
- 3 agents: Most tasks (sweet spot for coordination vs. value)
- 4-5 agents: Complex audits or multi-hypothesis debugging
- 6+: Rarely worth the coordination overhead and token cost

### 5. Monitor and Steer

- Check teammate progress regularly
- Redirect approaches that aren't working
- Tell the lead to "wait for teammates to finish" if it starts implementing
- Use "clean up the team" when done (shut down teammates first)

## Anti-Patterns

- **Don't use teams for sequential tasks**: If step B depends on step A's output, use a single session or subagents
- **Don't have two agents edit the same file**: Split work by file ownership
- **Don't create teams for trivial tasks**: A single agent handles simple reviews or fixes faster
- **Don't let teams run unattended too long**: Check in to prevent wasted effort
- **Don't skip the devils-advocate**: Including one skeptic consistently produces better outcomes

## Quick Start Examples

**Minimal team (2 agents):**
```
Create a team: security-auditor reviews the auth module while 
test-strategist checks test coverage for it.
```

**Standard team (3 agents):**
```
Create a team to review PR #42:
- security-auditor on vulnerabilities
- performance-analyst on efficiency
- test-strategist on test coverage
Synthesize findings into a single review.
```

**Full team with debate (4 agents):**
```
Create a team to design our new notification system:
- api-designer designs the interface
- domain-modeler designs the data model
- reliability-engineer plans for failure modes
- devils-advocate challenges whether we need this at all
Have them debate and converge on a recommended approach.
```
