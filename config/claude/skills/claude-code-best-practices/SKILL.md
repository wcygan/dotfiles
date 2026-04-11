---
name: claude-code-best-practices
description: >
  Reference guide for Claude Code features and best practices: writing a good CLAUDE.md,
  skills, hooks, sub-agents, agent teams, headless mode, scheduled tasks, channels, teleport,
  remote control, worktrees, batch, and frontend verification. Auto-loads when authoring or
  auditing a CLAUDE.md, working with Claude Code configuration, writing skills, setting up
  hooks, orchestrating agents, or optimizing workflows.
  Keywords: CLAUDE.md, claude md, project instructions, agent instructions, instruction budget,
  skill, hook, sub-agent, agent team, headless, scheduled task, channel, plugin, SKILL.md,
  teleport, remote control, worktree, batch, chrome extension, frontend, /loop, accumulator,
  stateful loop, silent accumulator, polling watcher, incremental explorer
allowed-tools: Read, Grep, Glob, WebFetch, WebSearch, Bash(cat *), Bash(gh *), Bash(git *), Bash(ls *)
---

# Claude Code Best Practices

Reference knowledge for Claude Code features. Each topic has a local summary and a canonical URL.

## Prime Directive: CLAUDE.md Is Load-Bearing

`CLAUDE.md` is the **only** file that goes into every Claude Code conversation by default. Every line competes for a finite instruction budget (~150–200 instructions, of which ~50 are already spent on the system prompt). Authoring or editing a `CLAUDE.md` — global, project, or skill-scoped — is **always** a high-leverage operation.

**Whenever the user asks you to write, refactor, audit, or add to a `CLAUDE.md`**, load [writing-claude-md](references/writing-claude-md.md) *first* and apply it. Proactively flag bloat, task-specific rules, linter-style guidance, and long inline examples. Prefer extracting deep content into `agent_docs/` (or equivalent) with a one-line pointer from the root file.

## Fetch Strategy

- **Quick answers**: use the local summary in the reference file
- **Before making changes or giving definitive guidance**: WebFetch the canonical URL to get the latest docs, then act on the live content

## Topic Routing

| Topic | Reference | Canonical URL |
|-------|-----------|---------------|
| **Writing a good CLAUDE.md** | [writing-claude-md](references/writing-claude-md.md) | https://www.humanlayer.dev/blog/writing-a-good-claude-md |
| Built-in tool catalog & behavior | [tools-reference](references/tools-reference.md) | https://code.claude.com/docs/en/tools-reference |
| Creating and configuring skills | [skills](references/skills.md) | https://code.claude.com/docs/en/skills |
| Skill authoring best practices | [skill-best-practices](references/skill-best-practices.md) | https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices |
| Spawning isolated subagents | [sub-agents](references/sub-agents.md) | https://code.claude.com/docs/en/sub-agents |
| Multi-session agent teams | [agent-teams](references/agent-teams.md) | https://code.claude.com/docs/en/agent-teams |
| Lifecycle hooks and automation | [hooks](references/hooks.md) | https://code.claude.com/docs/en/hooks-guide |
| Programmatic / CLI usage | [headless](references/headless.md) | https://code.claude.com/docs/en/headless |
| /loop, cron, reminders | [scheduled-tasks](references/scheduled-tasks.md) | https://code.claude.com/docs/en/scheduled-tasks |
| Push events into sessions | [channels](references/channels.md) | https://code.claude.com/docs/en/channels |
| Dynamic context injection (`!`command``) | [dynamic-context-injection](references/dynamic-context-injection.md) | https://code.claude.com/docs/en/skills#inject-dynamic-context |
| Complete skill-building guide | [skill-complete-guide](references/skill-complete-guide.md) | https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf |
| Teleport & Remote Control | [session-mobility](references/session-mobility.md) | https://code.claude.com/docs/en/remote-control |
| Git worktrees for parallel work | [worktrees](references/worktrees.md) | https://code.claude.com/docs/en/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees |
| /batch fan-out for large changesets | [batch](references/batch.md) | https://code.claude.com/docs/en/common-workflows |
| Chrome extension & Desktop preview | [frontend-verification](references/frontend-verification.md) | https://code.claude.com/docs/en/chrome |
| Loop patterns & stateful automation | [loop-patterns](references/loop-patterns.md) | https://code.claude.com/docs/en/scheduled-tasks |
