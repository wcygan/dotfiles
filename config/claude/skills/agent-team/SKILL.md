---
name: agent-team
description: Launch and coordinate Claude Code agent teams for complex tasks. Use when the user wants to parallelize work across multiple agents, needs a team for review, debugging, design, or feature development, or asks to "create a team" or "spawn agents." Keywords: agent team, team, spawn, teammates, parallel agents, coordinate, collaborate, multi-agent
---

# Agent Team Launcher

Launch and coordinate Claude Code agent teams using the available agent roster. This skill knows which agents exist, how they complement each other, and which team compositions work best for different tasks.

It can also **recommend compositions** from a task description, **discover custom agents**, and **generate new agents** on the fly when no existing one fits.

## Prerequisites

Agent teams are experimental. Ensure this is set in settings.json:

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

## Agent Discovery

Before selecting agents, always check for custom agents that may already exist.

### Discovery Procedure

1. **Check global agents** (available in all projects):
   ```bash
   ls ~/.claude/agents/*.md 2>/dev/null
   ```

2. **Check project-local agents** (specific to this repo):
   ```bash
   ls .claude/agents/*.md 2>/dev/null
   ```

3. **Read agent frontmatter** to understand each agent's capabilities:
   ```bash
   # Quick summary of all available agents
   for f in ~/.claude/agents/*.md .claude/agents/*.md; do
     head -5 "$f" 2>/dev/null
   done
   ```

4. **Merge with built-in roster**: Custom agents supplement the roster below. If a custom agent overlaps with a built-in one, prefer the custom agent (it may be tailored to the user's workflow).

### When presenting team options, list both:
- Built-in agents from the roster below
- Any discovered custom agents with their descriptions

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

## Smart Composition

When the user describes a task without specifying agents, analyze the task and recommend a team.

### Composition Algorithm

**Step 1: Classify the task type**

| Signal in Request | Task Type | Likely Agents |
|-------------------|-----------|---------------|
| "review", "check", "audit" | Review | security-auditor, performance-analyst, test-strategist |
| "design", "plan", "architect" | Design | api-designer, domain-modeler, devils-advocate |
| "build", "implement", "create" | Development | api-designer, domain-modeler, test-strategist |
| "debug", "fix", "investigate" | Investigation | implementation-investigator, reliability-engineer, devils-advocate |
| "refactor", "clean up", "improve" | Refactoring | refactoring-strategist, test-strategist, performance-analyst |
| "harden", "production-ready" | Hardening | security-auditor, reliability-engineer, performance-analyst |
| "migrate", "upgrade" | Migration | tech-lead, reliability-engineer, devils-advocate |

**Step 2: Identify required perspectives**

For each task, ask:
- Does this touch **security boundaries**? Add security-auditor.
- Does this involve **data modeling**? Add domain-modeler.
- Does this need **API/interface design**? Add api-designer.
- Is **performance critical**? Add performance-analyst.
- Does this need **test coverage**? Add test-strategist.
- Is this a **major decision**? Add devils-advocate.
- Does this involve **failure handling**? Add reliability-engineer.

**Step 3: Identify productive tension pairs**

Select agents whose lenses naturally conflict -- this creates better outcomes:

| Tension Pair | What They Debate |
|-------------|-----------------|
| security-auditor vs performance-analyst | "Is the security measure too expensive?" |
| api-designer vs domain-modeler | "Clean for consumers?" vs "Correct for the domain?" |
| reliability-engineer vs performance-analyst | "Add resilience overhead" vs "Reduce latency" |
| devils-advocate vs everyone | "Do we even need this?" |
| test-strategist vs performance-analyst | "More test coverage" vs "Faster test suite" |
| tech-lead vs devils-advocate | "Best practice says..." vs "In our context..." |

**Step 4: Right-size the team**

- Default to 3 agents (best coordination-to-value ratio)
- Use 2 for simple, focused tasks
- Use 4-5 only for complex audits or multi-hypothesis debugging
- Never use 6+

**Step 5: Present the recommendation**

Before spawning, present the team to the user:

```
Based on your task, I recommend this team:

Team: [Name] ([N] agents)
Task type: [Classification]

Agents:
1. [agent-name]: [what they'll focus on]
2. [agent-name]: [what they'll focus on]
3. [agent-name]: [what they'll focus on]

Key tension: [agent-a] vs [agent-b] will debate [topic]

Interaction model: [debate / independent review / coordinate-then-build]

Shall I proceed, or would you like to adjust the composition?
```

Wait for user confirmation before spawning.

## Dynamic Agent Generation

When no existing agent (built-in or custom) fits the task, generate one on the fly.

### When to Generate

- The task requires domain expertise not covered by the roster (e.g., "ML pipeline reviewer", "accessibility auditor", "database migration specialist")
- The user explicitly asks for a specialist not in the roster
- A team composition has a gap that no existing agent fills

### Agent Definition Template

```markdown
---
name: [kebab-case-name]
description: [When to use this agent. Include 2-3 examples in the description.]
color: [choose: cyan, magenta, yellow, green, blue, bright_red, bright_green]
memory: [none | user | project]
---

[Opening paragraph: Who this agent is, their core expertise, their communication style]

## Core Mindset

- [3-5 principles that guide this agent's thinking]

## Evaluation Framework

[The systematic approach this agent uses to analyze problems in their domain]

### [Category 1]
- [Specific things to check]

### [Category 2]
- [Specific things to check]

## Output Format

[How this agent structures its findings/recommendations]

## Communication Style

- [3-5 style guidelines]
```

### Where to Save

- **Global agents** (useful across projects): `~/.claude/agents/[name].md`
- **Project-specific agents** (tailored to one repo): `.claude/agents/[name].md`

Decision rule: If the agent's expertise is tied to a specific technology used in this project, save it project-locally. Otherwise, save globally.

### Post-Team Persistence

After a team run completes, if an ad-hoc agent was generated and proved useful:

1. Ask the user: "The [agent-name] agent worked well. Want to save it for future use?"
2. If yes, write the agent definition to the appropriate location
3. If the agent should be available everywhere: `~/.claude/agents/[name].md`
4. If project-specific: `.claude/agents/[name].md`

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

### 1. Discover Available Agents

Run agent discovery (see Agent Discovery section above) to find custom agents alongside the built-in roster.

### 2. Identify the Task Type

Match the user's request to one of the proven compositions above, or use Smart Composition to design a custom team. Key questions:
- What kind of work? (review, build, investigate, debug, refactor)
- How many perspectives needed? (2-5 agents, prefer 3)
- Do agents need to debate or work independently?
- Does any custom agent fit better than a built-in one?

### 3. Select and Recommend Agents

If the user specified agents, use their selection. Otherwise, use Smart Composition to recommend a team and present it for confirmation.

If no existing agent fits a needed role, use Dynamic Agent Generation to create one.

### 4. Craft the Team Prompt

A good team prompt includes:
- **Clear task description**: What are we working on?
- **Role assignments**: What each teammate focuses on
- **Interaction model**: Should they debate, work independently, or coordinate?
- **Deliverable**: What does the team produce? (report, code, plan)
- **Plan approval**: Add "Require plan approval before changes" for risky work

### 5. Configure the Team

**Use delegate mode** (Shift+Tab) to keep the lead orchestrating, not implementing.

**Display mode options**:
- In-process (default): Shift+Up/Down to switch between teammates
- Split panes: Set `"teammateMode": "tmux"` for tmux/iTerm2 users

**Size guidance**:
- 2 agents: Simple review or investigation
- 3 agents: Most tasks (sweet spot for coordination vs. value)
- 4-5 agents: Complex audits or multi-hypothesis debugging
- 6+: Rarely worth the coordination overhead and token cost

### 6. Monitor and Steer

- Check teammate progress regularly
- Redirect approaches that aren't working
- Tell the lead to "wait for teammates to finish" if it starts implementing
- Use "clean up the team" when done (shut down teammates first)

### 7. Post-Team Wrap-Up

After the team completes:
- If any ad-hoc agents were generated, offer to persist them
- Summarize findings across all agents
- Highlight disagreements between agents (these are often the most valuable insights)

## Anti-Patterns

- **Don't use teams for sequential tasks**: If step B depends on step A's output, use a single session or subagents
- **Don't have two agents edit the same file**: Split work by file ownership
- **Don't create teams for trivial tasks**: A single agent handles simple reviews or fixes faster
- **Don't let teams run unattended too long**: Check in to prevent wasted effort
- **Don't skip the devils-advocate**: Including one skeptic consistently produces better outcomes
- **Don't generate agents when an existing one fits**: Check discovery first

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

**Smart composition (let the skill choose):**
```
I need a team to review our payment processing module before
we go live. It handles Stripe webhooks, stores transaction
records, and sends email receipts.
```
