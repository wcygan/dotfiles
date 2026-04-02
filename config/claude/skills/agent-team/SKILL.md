---
name: agent-team
description: >
  Launch and coordinate Claude Code agent teams for complex tasks.
  Use when parallelizing work across multiple agents, running reviews, debugging,
  design, or feature development, or when asked to "create a team" or "spawn agents."
  Keywords: agent team, team, spawn, teammates, parallel agents, coordinate, collaborate, multi-agent
---

# Agent Team Launcher

> Before creating or configuring agent teams, WebFetch https://code.claude.com/docs/en/agent-teams for the latest docs.

Coordinate multiple Claude Code sessions working together. One session leads, teammates work independently in their own context windows, and they communicate via messaging.

## Workflow

### 1. Discover Available Agents

Check for custom agents (`~/.claude/agents/*.md` and `.claude/agents/*.md`) and merge with the built-in roster. Custom agents that overlap with built-in ones take precedence.

See [agent-roster](references/agent-roster.md) for the full roster and discovery details.

### 2. Compose the Team

Match the task to a proven composition or use smart composition to design a custom team.

See [composition](references/composition.md) for the composition algorithm and tension pairs.
See [recipes](references/recipes.md) for proven team compositions.

Present the recommendation before spawning:

```
Team: [Name] ([N] agents)
Task type: [Classification]

Agents:
1. [agent-name]: [what they'll focus on]
2. [agent-name]: [what they'll focus on]
3. [agent-name]: [what they'll focus on]

Key tension: [agent-a] vs [agent-b] will debate [topic]
Interaction model: [debate / independent review / coordinate-then-build]

Shall I proceed, or would you like to adjust?
```

Wait for user confirmation before spawning.

### 3. Craft the Team Prompt

Include in the prompt:
- **Task description**: What are we working on?
- **Role assignments**: What each teammate focuses on
- **Interaction model**: debate, independent review, or coordinate-then-build
- **Deliverable**: report, code, or plan
- **Plan approval**: Add "Require plan approval before changes" for risky work

### 4. Configure and Launch

**Display modes** (set `teammateMode` in `~/.claude.json`):
- `auto` (default): split panes if inside tmux, in-process otherwise
- `in-process`: all teammates in main terminal; Shift+Down to cycle
- `tmux`: split panes via tmux or iTerm2 (requires `tmux` or `it2` CLI)

Per-session override: `claude --teammate-mode in-process`

**Team sizing**:
- 2 teammates: simple, focused tasks
- 3 teammates: most tasks (sweet spot)
- 4-5 teammates: complex audits or multi-hypothesis debugging
- Aim for 5-6 tasks per teammate to keep everyone productive

### 5. Monitor and Steer

- Check teammate progress regularly
- Redirect approaches that aren't working
- Tell the lead to "wait for teammates to finish" if it starts implementing
- Teammates can message each other directly, not just the lead

### 6. Clean Up

Always use the lead to clean up — teammates should not run cleanup (can leave resources inconsistent). Shut down all teammates before cleaning up.

**Quality gate hooks** (enforce rules on task lifecycle):
- `TeammateIdle`: runs when a teammate is about to go idle (exit 2 to keep working)
- `TaskCreated`: runs when a task is created (exit 2 to prevent creation)
- `TaskCompleted`: runs when a task is marked complete (exit 2 to prevent completion)

### 7. Post-Team Wrap-Up

- Summarize findings across all agents
- Highlight disagreements (often the most valuable insights)
- If a specialist agent was needed but didn't exist, create one via `/agents` command or write to `~/.claude/agents/[name].md`

## Creating Custom Agents

When no existing agent fits, create one using the `/agents` command or by writing a markdown file to `~/.claude/agents/` (global) or `.claude/agents/` (project-local). See the [sub-agents docs](https://code.claude.com/docs/en/sub-agents) for the full agent file format and frontmatter fields.

## Known Limitations

- **No session resumption**: `/resume` and `/rewind` do not restore in-process teammates
- **Task status can lag**: teammates may not mark tasks complete; manually check or nudge
- **One team per session**: clean up current team before starting a new one
- **No nested teams**: teammates cannot spawn their own teams
- **Lead is fixed**: cannot promote a teammate to lead
- **Permissions set at spawn**: all teammates start with lead's mode; change individually after

## Anti-Patterns

- **Don't use teams for sequential tasks**: if step B depends on step A, use a single session or subagents
- **Don't have two agents edit the same file**: split work by file ownership
- **Don't create teams for trivial tasks**: a single agent handles simple reviews faster
- **Don't let teams run unattended too long**: check in to prevent wasted effort
- **Don't skip the devils-advocate**: one skeptic consistently produces better outcomes
- **Don't let teammates run cleanup**: only the lead should clean up team resources
- **Don't expect resume to restore teammates**: spawn new ones after resuming a session

## Quick Start Examples

**Minimal (2):**
```
Create a team with 2 agents to review auth: one on security, one on test coverage.
```

**Standard (3):**
```
Create a team to review PR #42 with agents covering vulnerabilities, efficiency, and test coverage.
Synthesize findings into a single review.
```

**Full debate (4):**
```
Create a team to design our notification system:
- one agent on interface design
- one on data modeling
- one on failure modes
- one as devils-advocate challenging whether we need this at all
Have them debate and converge on a recommended approach.
```

**Smart composition (let the skill choose):**
```
I need a team to review our payment processing module before
we go live. It handles Stripe webhooks, stores transaction
records, and sends email receipts.
```
