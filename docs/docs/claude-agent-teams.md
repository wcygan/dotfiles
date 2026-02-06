---
sidebar_position: 3
---

# Claude Code Agent Teams

Agent teams let you coordinate multiple Claude Code sessions working in parallel. One session acts as the **lead** (orchestrator), and others are **teammates** (workers). Teammates communicate through a shared task list and mailbox, each with their own full context window.

## When to Use Teams vs. Sub-Agents

| Use Case | Sub-Agents | Agent Teams |
|----------|-----------|-------------|
| Quick research or file search | Best choice | Overkill |
| Focused task, only result matters | Best choice | Unnecessary |
| Workers need to debate findings | Can't do this | Best choice |
| Cross-layer work (frontend + backend + tests) | Awkward | Best choice |
| Competing hypotheses that should challenge each other | Can't do this | Best choice |
| Multiple review perspectives simultaneously | Possible | Best choice |

**Rule of thumb**: If workers just report back, use sub-agents. If workers need to talk to each other, use teams.

## Setup

Agent teams are experimental. They're enabled in our dotfiles via `settings.json`:

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

This is already configured — no action needed if you've run `install.sh`.

## Available Agents

We maintain 13 custom agents. Each brings a distinct "lens" that creates productive tension with others.

### General-Purpose

| Agent | Lens | Memory |
|-------|------|--------|
| **tech-lead** | Senior leadership, architecture decisions, code review | — |
| **implementation-investigator** | Reverse-engineering codebases, tracing code paths | — |
| **refactoring-strategist** | Code smells, design patterns, refactoring plans | — |
| **security-auditor** | Threat modeling, vulnerabilities, supply chain | `user` |
| **test-strategist** | Test architecture, TDD coaching, coverage gaps | `user` |
| **performance-analyst** | Complexity analysis, profiling, optimization | `user` |
| **api-designer** | Interface ergonomics, consumer experience | — |
| **domain-modeler** | DDD, schemas, state machines, bounded contexts | `project` |
| **reliability-engineer** | Failure modes, observability, graceful degradation | `user` |
| **devils-advocate** | Assumption challenging, simplicity advocacy | — |

### Domain-Specific

| Agent | Lens |
|-------|------|
| **kubernetes-architect** | K8s cluster design, networking, storage, security |
| **skaffold-deployment-expert** | Skaffold configuration, K8s dev workflows |
| **fedora-sysadmin** | Fedora Linux administration, DNF, SELinux, systemd |

### What "Memory" Means

Agents with `memory: user` persist learnings across all projects in `~/.claude/agent-memory/<agent>/`. They remember your preferred tools, recurring patterns, and project-specific conventions. The `domain-modeler` uses `memory: project` because domain models are project-specific (stored in `.claude/agent-memory/domain-modeler/`).

Agents without memory approach each task fresh. The `devils-advocate` intentionally has no memory — unbiased skepticism is the point.

## Team Compositions

### Design Review

**Agents**: api-designer + domain-modeler + devils-advocate

**When**: Evaluating a new feature design, API shape, or architecture proposal.

```
Create an agent team for a design review:
- api-designer: evaluate the interface from the consumer's perspective
- domain-modeler: evaluate whether the data model is correct
- devils-advocate: challenge assumptions and argue for simpler alternatives
Have them review [WHAT YOU'RE REVIEWING] and debate their findings.
```

**Productive tension**: The api-designer wants a clean consumer experience. The domain-modeler wants correctness. The devils-advocate asks if we need this at all.

### Hardening

**Agents**: security-auditor + reliability-engineer + performance-analyst

**When**: Preparing a service for production, auditing existing systems.

```
Create an agent team to harden [SERVICE]:
- security-auditor: find vulnerabilities and attack vectors
- reliability-engineer: identify failure modes and missing resilience
- performance-analyst: find bottlenecks and scaling issues
Have each reviewer work independently, then synthesize findings.
```

**Productive tension**: Security wants more validation (slower). Performance wants less overhead (riskier). Reliability wants more fallbacks (more complex). The synthesis forces real trade-off decisions.

### Full Architecture Review

**Agents**: tech-lead + security-auditor + performance-analyst + devils-advocate

**When**: Major architectural decisions or system design reviews.

```
Create an agent team to review [ARCHITECTURE]:
- tech-lead: evaluate overall approach and team impact
- security-auditor: assess security implications
- performance-analyst: analyze scaling and efficiency
- devils-advocate: challenge necessity and complexity
Require plan approval before any changes.
```

### Feature Development

**Agents**: api-designer + domain-modeler + test-strategist

**When**: Building a new feature with clear scope.

```
Create an agent team to implement [FEATURE]:
- api-designer: design the interface and contracts
- domain-modeler: design the data model and state management
- test-strategist: write tests in parallel based on the design
Have the api-designer and domain-modeler coordinate on the contract,
then the test-strategist writes tests against it.
```

### Pre-Production Audit

**Agents**: security-auditor + reliability-engineer + test-strategist + performance-analyst

**When**: Final quality check before shipping.

```
Create an agent team to audit [SERVICE] before production:
- security-auditor: security vulnerabilities and dependency risks
- reliability-engineer: error handling and observability gaps
- test-strategist: test coverage and verification completeness
- performance-analyst: performance bottlenecks and scaling limits
Each reviewer should produce a findings report with severity ratings.
```

### Investigation

**Agents**: implementation-investigator + devils-advocate + reliability-engineer

**When**: Understanding an unfamiliar codebase or debugging complex issues.

```
Create an agent team to investigate [TOPIC]:
- implementation-investigator: trace code paths and map architecture
- devils-advocate: challenge initial hypotheses
- reliability-engineer: analyze failure modes and error paths
Have them share findings and challenge each other's conclusions.
```

### Refactoring

**Agents**: refactoring-strategist + test-strategist + performance-analyst

**When**: Planning and executing a significant refactor.

```
Create an agent team to refactor [MODULE]:
- refactoring-strategist: identify smells and plan the refactoring
- test-strategist: ensure test safety net exists before changes
- performance-analyst: verify no performance regressions
Require plan approval from the refactoring-strategist before changes.
```

### Debugging with Competing Hypotheses

**Agents**: 3-5 investigators + devils-advocate

**When**: Root cause is unclear, multiple theories exist.

```
Users report [SYMPTOM]. Create an agent team to investigate:
- Teammate 1: investigate [hypothesis A]
- Teammate 2: investigate [hypothesis B]
- Teammate 3: investigate [hypothesis C]
- devils-advocate: challenge each theory and look for what they're missing
Have them actively try to disprove each other's theories.
```

This is the most powerful pattern for difficult bugs. Sequential investigation suffers from anchoring — once one theory is explored, subsequent investigation is biased toward it. Parallel adversarial investigation converges on the actual root cause faster.

### Kubernetes Deployment Review

**Agents**: kubernetes-architect + security-auditor + reliability-engineer

**When**: Reviewing K8s deployments and infrastructure.

```
Create an agent team to review [K8S DEPLOYMENT]:
- kubernetes-architect: evaluate cluster architecture and configs
- security-auditor: assess RBAC, network policies, secrets management
- reliability-engineer: evaluate health checks, resource limits, disruption budgets
```

## Operating Teams Effectively

### Display Modes

- **In-process** (default): All teammates in one terminal. Use `Shift+Up/Down` to select a teammate and type to message them directly. Press `Ctrl+T` to toggle the task list.
- **Split panes** (tmux/iTerm2): Each teammate gets its own pane. Set `"teammateMode": "tmux"` in settings.json. Click into a pane to interact directly.

### Delegate Mode

Press `Shift+Tab` to enable delegate mode. This restricts the lead to coordination-only — spawning, messaging, managing tasks. Without it, the lead sometimes starts implementing instead of waiting for teammates.

**Always use delegate mode** for teams of 3+ agents.

### Requiring Plan Approval

For risky changes, require teammates to plan before implementing:

```
Spawn a teammate to refactor the auth module.
Require plan approval before they make any changes.
Only approve plans that include test coverage.
```

The lead reviews and approves/rejects plans autonomously. You can influence its judgment with criteria in your prompt.

### Messaging Teammates Directly

You can bypass the lead and talk to any teammate:

- **In-process**: `Shift+Up/Down` to select, then type
- **Split panes**: Click into the pane

This is useful for giving additional context, redirecting an approach, or asking follow-up questions.

### Team Lifecycle

1. **Start**: Tell Claude to create a team, or use `/agent-team`
2. **Monitor**: Check progress, redirect approaches that aren't working
3. **Steer**: Message teammates directly if needed
4. **Shut down**: Ask the lead to "shut down [teammate name]"
5. **Clean up**: Ask the lead to "clean up the team" (all teammates must be shut down first)

## Best Practices

### Do

- **Give teammates enough context** in the spawn prompt — they don't inherit the lead's conversation history
- **Size tasks appropriately** — self-contained units with clear deliverables
- **Include a devils-advocate** for major decisions — it consistently produces better outcomes
- **Split work by file ownership** — each teammate owns distinct files
- **Check in regularly** — don't let teams run unattended for too long
- **Start with reviews and research** if you're new to teams — lower coordination overhead than parallel implementation

### Don't

- **Don't use teams for sequential tasks** — if B depends on A, use a single session
- **Don't have two teammates edit the same file** — leads to overwrites
- **Don't create teams for trivial tasks** — the coordination overhead isn't worth it
- **Don't skip delegate mode** — the lead will start implementing and ignore teammates
- **Don't create teams larger than 5** — coordination overhead and token cost rarely justify it

### Team Sizing Guide

| Task Complexity | Team Size | Notes |
|----------------|-----------|-------|
| Simple review | 2 | Two perspectives, low overhead |
| Standard review or feature | 3 | Sweet spot for most tasks |
| Complex audit or architecture | 4 | Multiple quality lenses |
| Multi-hypothesis debugging | 4-5 | One per hypothesis + skeptic |
| Anything | 6+ | Almost never worth it |

## Productive Tension Reference

The best teams have agents whose perspectives naturally conflict in useful ways:

| Agent A | Agent B | What They Debate |
|---------|---------|-----------------|
| security-auditor | performance-analyst | "Is the security measure too expensive?" |
| api-designer | domain-modeler | "Clean for consumers?" vs. "Correct for the domain?" |
| reliability-engineer | performance-analyst | "Add resilience overhead" vs. "Reduce latency" |
| devils-advocate | everyone | "Do we even need this?" |
| test-strategist | performance-analyst | "More test coverage" vs. "Faster test suite" |
| tech-lead | devils-advocate | "Best practice says..." vs. "In our context..." |

## Limitations

Agent teams are experimental. Key limitations:

- **No session resumption**: `/resume` doesn't restore in-process teammates. The lead may try to message teammates that no longer exist — tell it to spawn new ones.
- **One team per session**: Clean up the current team before starting a new one.
- **No nested teams**: Teammates can't spawn their own teams.
- **Lead is fixed**: The session that creates the team leads it for its lifetime.
- **Split panes need tmux/iTerm2**: In-process mode works in any terminal.
- **Permissions at spawn**: All teammates inherit the lead's permission mode. You can change individual modes after spawning.
- **Task status can lag**: Teammates sometimes forget to mark tasks done. Nudge them if something looks stuck.

## Token Cost

Each teammate is a separate Claude session with its own context window. Token usage scales linearly with team size. For research, review, and feature development, the extra tokens are usually worthwhile. For routine tasks, a single session is more cost-effective.

## Quick Reference

| Action | How |
|--------|-----|
| Create a team | Tell Claude, or use `/agent-team` |
| Switch between teammates | `Shift+Up/Down` |
| View task list | `Ctrl+T` |
| Enable delegate mode | `Shift+Tab` |
| Message a teammate directly | Select with `Shift+Up/Down`, then type |
| View teammate session | `Enter` on selected teammate |
| Interrupt teammate | `Escape` while viewing their session |
| Background a running task | `Ctrl+B` |
| Shut down a teammate | Tell the lead: "shut down [name]" |
| Clean up team | Tell the lead: "clean up the team" |
