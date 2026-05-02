---
name: agent-team
description: Launch and coordinate Claude Code agent teams for complex tasks. Use when parallelizing work across multiple agents, running reviews, debugging, design, or feature development, or when asked to "create a team" or "spawn agents." Keywords agent team, team, spawn, teammates, parallel agents, coordinate, multi-agent.
---

# Agent Team Launcher

> Before creating or configuring agent teams, WebFetch https://code.claude.com/docs/en/agent-teams for the latest docs.

Coordinate multiple Claude Code sessions working together. One session leads, teammates work independently in their own context windows, and they communicate via messaging.

The team is composed by **lens**, not by named agent. You decide which perspectives the task needs (error-path, contract, simplicity, skeptic, etc.) and craft a role prompt that establishes each lens. Most teammates run as `general-purpose`; use a project-local custom agent only if one matches a chosen lens precisely.

## Workflow

### 1. Compose by Lens

Pick the lenses the task needs and the productive tension between them.

See [composition.md](references/composition.md) for the lens library, the task-type → lens table, tension pairs, and the role-prompt template.
See [recipes.md](references/recipes.md) for proven lens combinations for common task types.

### 2. Discover Custom Agents (Optional)

Before defaulting every teammate to `general-purpose`, check `~/.claude/agents/*.md` and `.claude/agents/*.md`. If a custom agent's frontmatter matches a lens you want, use its `subagent_type` directly — its system prompt is already tuned for that lens. Otherwise spawn `general-purpose` with a role prompt.

### 3. Present the Plan

Before spawning, present:

```
Team: [Name] ([N] agents)
Task type: [Classification]

Teammates:
1. [Lens]: [what they'll focus on]  — agent: [general-purpose | custom-name]
2. [Lens]: [what they'll focus on]  — agent: [general-purpose | custom-name]
3. [Lens]: [what they'll focus on]  — agent: [general-purpose | custom-name]

Key tension: [Lens A] vs [Lens B] will debate [topic]
Interaction model: [debate / independent review / coordinate-then-build]

Shall I proceed, or would you like to adjust?
```

Wait for confirmation.

### 4. Craft the Team Prompt

Each teammate's prompt should include:

- **Task description**: what we're working on
- **Role / lens**: the specific perspective this teammate owns (see composition.md §5)
- **Out of scope**: lenses other teammates own — keeps focus tight
- **Interaction model**: debate, independent review, or coordinate-then-build
- **Deliverable**: report, code, or plan
- **Plan approval**: add "Require plan approval before changes" for risky work

### 5. Configure and Launch

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

### 6. Monitor and Steer

- Check progress regularly
- Redirect approaches that aren't working
- Tell the lead to "wait for teammates to finish" if it starts implementing prematurely
- Teammates can message each other directly, not just the lead

### 7. Clean Up

Always use the lead to clean up — teammates should not run cleanup (can leave resources inconsistent). Shut down all teammates before cleaning up.

**Quality gate hooks** (enforce rules on task lifecycle):
- `TeammateIdle`: runs when a teammate is about to go idle (exit 2 to keep working)
- `TaskCreated`: runs when a task is created (exit 2 to prevent creation)
- `TaskCompleted`: runs when a task is marked complete (exit 2 to prevent completion)

### 8. Wrap-Up

- Summarize findings across all teammates
- **Highlight disagreements** — they're often the most valuable output
- If a lens recurred and a custom agent would help next time, note it for follow-up

## Creating Custom Agents (Optional)

If a particular lens recurs across many sessions, encode it as a custom agent rather than re-writing the role prompt every time. Write a markdown file to `~/.claude/agents/<name>.md` (global) or `.claude/agents/<name>.md` (project-local). See the [sub-agents docs](https://code.claude.com/docs/en/sub-agents) for frontmatter fields.

The skill does not ship a fixed roster — there is no built-in `error-path-reviewer` or `simplifier`. Each lens lives only in the prompts you write (or in custom agents you choose to author).

## Known Limitations

- **No session resumption**: `/resume` and `/rewind` do not restore in-process teammates
- **Task status can lag**: teammates may not mark tasks complete; manually check or nudge
- **One team per session**: clean up current team before starting a new one
- **No nested teams**: teammates cannot spawn their own teams
- **Lead is fixed**: cannot promote a teammate to lead
- **Permissions set at spawn**: all teammates start with lead's mode; change individually after

## Anti-Patterns

- **Don't use teams for sequential tasks**: if step B depends on step A, use a single session or subagents
- **Don't have two teammates edit the same file**: split work by file ownership
- **Don't create teams for trivial tasks**: a single agent handles simple reviews faster
- **Don't let teams run unattended too long**: check in to prevent wasted effort
- **Don't skip the skeptic lens**: at least one teammate should challenge the premise
- **Don't let teammates run cleanup**: only the lead should clean up team resources
- **Don't expect resume to restore teammates**: spawn new ones after resuming a session

## Quick Start Examples

**Minimal (2):**
```
Create a team with 2 teammates to review auth: one with a security lens, one with a test-coverage lens.
```

**Standard (3):**
```
Create a team to review PR #42 with three lenses: vulnerabilities,
performance, and test coverage. Synthesize findings into a single review.
```

**Full debate (4):**
```
Create a team to design our notification system:
- one with an interface-design lens
- one with a data-modeling lens
- one with a failure-mode lens
- one playing skeptic, challenging whether we need this at all
Have them debate and converge on a recommended approach.
```

**Smart composition (let the skill choose):**
```
I need a team to review our payment processing module before
we go live. It handles Stripe webhooks, stores transaction
records, and sends email receipts.
```
