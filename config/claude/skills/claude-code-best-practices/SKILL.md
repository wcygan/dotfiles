---
name: claude-code-best-practices
description: >
  Reference guide for Claude Code features and best practices: skills, hooks, sub-agents,
  agent teams, headless mode, scheduled tasks, and channels. Auto-loads when working with
  Claude Code configuration, writing skills, setting up hooks, or orchestrating agents.
  Keywords: skill, hook, sub-agent, agent team, headless, scheduled task, channel, plugin, SKILL.md
allowed-tools: Read, Grep, Glob, WebFetch, WebSearch, Bash(cat *)
---

# Claude Code Best Practices

Reference knowledge for Claude Code features. Each topic has a local summary and a canonical URL.

## Fetch Strategy

- **Quick answers**: use the local summary in the reference file
- **Before making changes or giving definitive guidance**: WebFetch the canonical URL to get the latest docs, then act on the live content

## Topic Routing

| Topic | Reference | Canonical URL |
|-------|-----------|---------------|
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
