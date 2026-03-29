---
title: Sub-agents
canonical_url: https://code.claude.com/docs/en/sub-agents
fetch_before_acting: true
---

# Sub-agents

> Before configuring sub-agents, WebFetch https://code.claude.com/docs/en/sub-agents for the latest.

## Summary

Sub-agents run tasks in isolated context windows within a single Claude Code session. They protect the main conversation from expensive exploration and enable parallel work.

### When to Use

- Heavy codebase exploration that would bloat main context
- Parallel independent research tasks
- Read-only analysis (use `agent: Explore`)
- Tasks that don't need conversation history

### How to Spawn

Use the `Agent` tool with parameters:
- `prompt` — task description (must be self-contained)
- `subagent_type` — `Explore` (read-only), `general-purpose`, `Plan`, etc.
- `isolation: "worktree"` — optional git worktree isolation
- `run_in_background: true` — optional async execution

### Key Behaviors

- Subagents have NO conversation history — include all context in the prompt
- Results returned as a single message to the parent
- Can restrict tools via `allowed-tools` in skill frontmatter
- `context: fork` in skill frontmatter automatically runs as subagent

### Sub-agents vs Agent Teams

| Sub-agents | Agent Teams |
|------------|-------------|
| Same session, isolated context | Separate sessions |
| Report to parent only | Can message each other |
| Lightweight, fast to spawn | Heavier, persistent |
| Good for 1-5 parallel tasks | Good for complex coordination |
