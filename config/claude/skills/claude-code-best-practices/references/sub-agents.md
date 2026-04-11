---
title: Sub-agents
canonical_url: https://code.claude.com/docs/en/sub-agents
fetch_before_acting: true
---

# Sub-agents

> Before configuring sub-agents, WebFetch https://code.claude.com/docs/en/sub-agents for the latest.

## Contents

- [Summary](#summary)
- [When to Use](#when-to-use)
- [Two Ways to Spawn](#two-ways-to-spawn)
- [File Locations & Priority](#file-locations--priority)
- [Frontmatter Fields](#frontmatter-fields)
- [Preload Skills into Subagents](#preload-skills-into-subagents)
- [Persistent Memory](#persistent-memory)
- [Define Hooks for Subagents](#define-hooks-for-subagents)
- [MCP Servers Scoped to a Subagent](#mcp-servers-scoped-to-a-subagent)
- [Worktree Isolation](#worktree-isolation)
- [Resuming Subagents](#resuming-subagents)
- [Sub-agents vs Agent Teams](#sub-agents-vs-agent-teams)

## Summary

Sub-agents run tasks in isolated context windows within a single Claude Code session. They protect the main conversation from expensive exploration, enable parallel work, and can be defined as reusable markdown files with their own tools, model, skills, hooks, and memory. Built-ins include `Explore` (read-only, Haiku), `Plan`, and `general-purpose`.

## When to Use

- Heavy codebase exploration that would bloat main context
- Parallel independent research tasks
- Read-only analysis (use `agent: Explore`)
- Tasks that don't need conversation history
- Enforcing tool restrictions (e.g., read-only DB access)
- Routing work to cheaper models (Haiku)

**Not for**: tasks needing iterative back-and-forth with you, multi-phase work that shares context, quick targeted edits. Subagents cannot spawn other subagents.

## Two Ways to Spawn

**Runtime (ad-hoc) via the `Agent` tool** — spawn a one-off subagent from the current conversation with a self-contained prompt:

- `prompt` — task description (must be self-contained; no conversation history)
- `subagent_type` — `Explore`, `general-purpose`, `Plan`, or a custom name
- `isolation: "worktree"` — optional git worktree isolation
- `run_in_background: true` — optional async execution
- `model` — per-invocation override

**File-based (reusable) via markdown definitions** — check-in a `.md` file with frontmatter, invoke by name:

- Natural language: "Use the code-reviewer subagent to…"
- `@-mention`: `@"code-reviewer (agent)"` guarantees that subagent runs
- Session-wide: `claude --agent code-reviewer` makes the main thread *itself* take on that subagent's system prompt, tools, and model
- Per-session JSON: `claude --agents '{...}'` defines ephemeral subagents for one run

## File Locations & Priority

Higher-priority locations win when names collide.

| Location | Scope | Priority |
|----------|-------|----------|
| Managed settings | Organization-wide | 1 (highest) |
| `--agents` CLI JSON | Current session | 2 |
| `.claude/agents/` | Current project | 3 |
| `~/.claude/agents/` | All your projects | 4 |
| Plugin `agents/` dir | Where plugin is enabled | 5 (lowest) |

Subagents are loaded at session start. After manually adding a file, restart or run `/agents` to pick it up. Run `claude agents` (non-interactive) or `/agents` (interactive) to list and manage.

> Plugin subagents do **not** support `hooks`, `mcpServers`, or `permissionMode` — those fields are silently ignored. Copy into `.claude/agents/` if you need them.

## Frontmatter Fields

Only `name` and `description` are required.

| Field | Purpose |
|-------|---------|
| `name` | Unique lowercase-hyphen identifier |
| `description` | When Claude should delegate to it (drives auto-invocation) |
| `tools` | Allowlist; inherits all tools if omitted |
| `disallowedTools` | Denylist; applied before `tools` |
| `model` | `sonnet`, `opus`, `haiku`, full model ID, or `inherit` (default) |
| `permissionMode` | `default`, `acceptEdits`, `auto`, `dontAsk`, `bypassPermissions`, `plan` |
| `maxTurns` | Cap on agentic turns |
| `skills` | List of skills to **preload** into context at startup |
| `mcpServers` | Inline MCP server defs or references to existing servers |
| `hooks` | Lifecycle hooks scoped to this subagent |
| `memory` | Persistent memory scope: `user`, `project`, or `local` |
| `background` | `true` → always run as background task |
| `effort` | `low`, `medium`, `high`, `max` (Opus 4.6 only) |
| `isolation` | `worktree` → run in a temporary git worktree |
| `color` | Display color in task list and transcript |
| `initialPrompt` | Auto-submitted first user turn when run as main session via `--agent` |

Subagents only see their system prompt plus basic env details — **not** the main Claude Code system prompt, and **not** skills inherited from the parent. Pass everything explicitly.

### Restrict which agents can be spawned

When a custom agent runs as the main thread via `claude --agent`, you can constrain what it delegates to using `Agent(type)` syntax in `tools`:

```yaml
tools: Agent(worker, researcher), Read, Bash
```

Allowlist only; bare `Agent` allows any; omitting `Agent` entirely blocks all delegation. Does nothing in nested subagent definitions (subagents can't spawn subagents).

## Preload Skills into Subagents

Subagents do **not** inherit skills from the parent conversation. Use the `skills` field to inject the full content of specific skills into the subagent's context at startup — not just make them available for later invocation.

```yaml
---
name: api-developer
description: Implement API endpoints following team conventions
skills:
  - api-conventions
  - error-handling-patterns
---

Implement API endpoints. Follow the conventions and patterns from the preloaded skills.
```

This is the **inverse** of `context: fork` in a skill: with `context: fork`, the skill injects its content into a spawned agent; with `skills:` in a subagent, the subagent loads skill content on startup. Both use the same underlying mechanism.

Use when a subagent needs specific domain knowledge without having to discover and load it mid-run.

## Persistent Memory

The `memory` field gives a subagent a directory that survives across conversations, so it can accumulate patterns, debugging insights, and architectural decisions over time.

```yaml
---
name: code-reviewer
description: Reviews code for quality and best practices
memory: project
---

You are a code reviewer. As you review code, update your agent memory with
patterns, conventions, and recurring issues you discover.
```

### Scopes

| Scope | Location | Use when |
|-------|----------|----------|
| `user` | `~/.claude/agent-memory/<name>/` | knowledge applies across all projects |
| `project` | `.claude/agent-memory/<name>/` | **(recommended default)** project-specific, shared via VCS |
| `local` | `.claude/agent-memory-local/<name>/` | project-specific, **not** checked in |

### How it works

When memory is enabled, the subagent automatically gets:
- System-prompt instructions for reading and writing its memory directory
- The first **200 lines or 25KB** of `MEMORY.md` injected at startup (whichever comes first), with instructions to curate if it exceeds that
- `Read`, `Write`, and `Edit` tools enabled so it can manage its own memory files

### Tips

- Default to `project` scope so memory is reviewable in VCS
- Tell the subagent to consult memory before starting: *"check your memory for patterns you've seen before"*
- Tell it to update memory when done: *"save what you learned to your memory"*
- Bake proactive memory curation into the markdown body so the subagent maintains its own knowledge base without being prompted

## Define Hooks for Subagents

Two separate configuration paths depending on **where** the hook should fire:

### 1. Hooks in subagent frontmatter

Run only while that specific subagent is active; cleaned up when it finishes. All [hook events](https://code.claude.com/docs/en/hooks) are supported; most common:

| Event | Matcher | Fires |
|-------|---------|-------|
| `PreToolUse` | Tool name | Before the subagent uses a tool |
| `PostToolUse` | Tool name | After the subagent uses a tool |
| `Stop` | (none) | When subagent finishes (converted to `SubagentStop`) |

```yaml
---
name: code-reviewer
description: Review code changes with automatic linting
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-command.sh"
  PostToolUse:
    - matcher: "Edit|Write"
      hooks:
        - type: command
          command: "./scripts/run-linter.sh"
---
```

Hook input is passed as JSON via stdin. Exit code `2` blocks the tool call and surfaces stderr back to Claude. This is the go-to for conditional rules — e.g., allowing `SELECT` but blocking `INSERT/UPDATE/DELETE` on a `db-reader` subagent's Bash.

### 2. Project-level hooks in `settings.json`

Fire in the **main** session when subagents start or stop. Use `SubagentStart` / `SubagentStop`:

```json
{
  "hooks": {
    "SubagentStart": [
      {
        "matcher": "db-agent",
        "hooks": [{ "type": "command", "command": "./scripts/setup-db-connection.sh" }]
      }
    ],
    "SubagentStop": [
      {
        "hooks": [{ "type": "command", "command": "./scripts/cleanup-db-connection.sh" }]
      }
    ]
  }
}
```

Matchers target specific agent type names; omit for all subagents. Useful for setup/teardown that must happen in the main session's context (e.g., ephemeral resources, notifications).

## MCP Servers Scoped to a Subagent

Give a subagent MCP tools that aren't available to the main conversation — keeps tool descriptions out of the parent's context budget.

```yaml
---
name: browser-tester
description: Tests features in a real browser using Playwright
mcpServers:
  - playwright:
      type: stdio
      command: npx
      args: ["-y", "@playwright/mcp@latest"]
  - github  # reference to already-configured server
---
```

Inline definitions use the same schema as `.mcp.json` entries (`stdio`, `http`, `sse`, `ws`). Inline servers connect when the subagent starts and disconnect when it finishes. String references share the parent session's connection.

## Worktree Isolation

Set `isolation: worktree` (frontmatter) or pass `isolation: "worktree"` (runtime `Agent` tool) to run the subagent in a temporary git worktree with its own copy of the repo. `cd` within a subagent never persists between tool calls and never affects the parent — worktree isolation gives it a real independent checkout. Auto-cleaned up if the subagent makes no changes.

## Resuming Subagents

Each `Agent` invocation creates a fresh instance. To continue a prior subagent with full history (tool calls, reasoning, results), ask Claude to resume it — it uses the `SendMessage` tool with the stored agent ID. `SendMessage` requires `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`. Transcripts live at `~/.claude/projects/{project}/{sessionId}/subagents/agent-{agentId}.jsonl` and persist independently of main-conversation compaction.

## Sub-agents vs Agent Teams

| Sub-agents | Agent Teams |
|------------|-------------|
| Same session, isolated context | Separate sessions |
| Report to parent only | Can message each other via `SendMessage` |
| Lightweight, fast to spawn | Heavier, persistent |
| Cannot spawn other subagents | Can coordinate nested work |
| Good for 1-5 parallel tasks | Good for complex multi-agent coordination |
