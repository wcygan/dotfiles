---
title: Tools Reference
canonical_url: https://code.claude.com/docs/en/tools-reference
fetch_before_acting: true
---

# Tools Reference

> Before writing permission rules, subagent tool lists, or hook matchers, WebFetch https://code.claude.com/docs/en/tools-reference for the latest tool set.

## Summary

Claude Code ships with a fixed set of built-in tools. The **tool name** is the exact string used in:

- [Permission rules](https://code.claude.com/docs/en/permissions#tool-specific-permission-rules) (`allow` / `deny` / `ask`)
- [Subagent](https://code.claude.com/docs/en/sub-agents) `tools:` lists
- [Hook](https://code.claude.com/docs/en/hooks) `matcher` fields
- Skill frontmatter `allowed-tools`

To disable a tool entirely, add its name to `deny` in permission settings. To add *custom* tools, connect an [MCP server](https://code.claude.com/docs/en/mcp). Skills are not tools — they run through the `Skill` tool.

## Full Tool Table

Legend: **Perm?** = whether the tool triggers a permission prompt by default.

| Tool | Perm? | Purpose |
|------|:-----:|---------|
| `Agent` | No | Spawn a subagent with its own context window |
| `AskUserQuestion` | No | Multiple-choice questions to gather/clarify requirements |
| `Bash` | Yes | Execute shell commands — see [Bash behavior](#bash-tool-behavior) |
| `CronCreate` | No | Schedule recurring/one-shot prompt in current session |
| `CronDelete` | No | Cancel a scheduled task by ID |
| `CronList` | No | List scheduled tasks in the session |
| `Edit` | Yes | Targeted edits to specific files |
| `EnterPlanMode` | No | Enter plan mode to design an approach |
| `EnterWorktree` | No | Create an isolated git worktree and switch into it |
| `ExitPlanMode` | Yes | Present a plan for approval and exit plan mode |
| `ExitWorktree` | No | Exit worktree session, return to original directory |
| `Glob` | No | Find files by pattern |
| `Grep` | No | Search file contents (built on ripgrep) |
| `ListMcpResourcesTool` | No | List resources exposed by connected MCP servers |
| `LSP` | No | Code intelligence via language servers — see [LSP behavior](#lsp-tool-behavior) |
| `Monitor` | Yes | Run a command in the background and stream output lines back — see [Monitor](#monitor-tool) |
| `NotebookEdit` | Yes | Modify Jupyter notebook cells |
| `PowerShell` | Yes | PowerShell on Windows (opt-in preview) — see [PowerShell](#powershell-tool) |
| `Read` | No | Read file contents |
| `ReadMcpResourceTool` | No | Read a specific MCP resource by URI |
| `SendMessage` | No | Message an agent-team teammate or resume a subagent by ID *(requires `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`)* |
| `Skill` | Yes | Execute a skill within the main conversation |
| `TaskCreate` | No | Create a task in the task list |
| `TaskGet` | No | Retrieve full details for a task |
| `TaskList` | No | List all tasks with status |
| `TaskOutput` | No | **Deprecated** — prefer `Read` on the task output file path |
| `TaskStop` | No | Kill a running background task by ID |
| `TaskUpdate` | No | Update task status, dependencies, details, or delete tasks |
| `TeamCreate` | No | Create an agent team *(requires `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`)* |
| `TeamDelete` | No | Disband an agent team *(requires `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`)* |
| `TodoWrite` | No | Session task checklist — **non-interactive / Agent SDK only**. Interactive sessions use `TaskCreate` / `TaskGet` / `TaskList` / `TaskUpdate` |
| `ToolSearch` | No | Search for and load deferred tools when MCP tool search is enabled |
| `WebFetch` | Yes | Fetch content from a URL |
| `WebSearch` | Yes | Perform web searches |
| `Write` | Yes | Create or overwrite files |

Configure permissions via `/permissions` or [permission settings](https://code.claude.com/docs/en/settings#available-settings).

## Tool Categories

Rough groupings to help pick the right tool:

| Category | Tools |
|----------|-------|
| **File I/O** | `Read`, `Write`, `Edit`, `NotebookEdit`, `Glob`, `Grep` |
| **Shell execution** | `Bash`, `PowerShell`, `Monitor` |
| **Code intelligence** | `LSP` |
| **Web** | `WebFetch`, `WebSearch` |
| **Orchestration** | `Agent`, `SendMessage`, `TeamCreate`, `TeamDelete`, `Skill` |
| **Planning / tasks** | `EnterPlanMode`, `ExitPlanMode`, `TaskCreate`, `TaskGet`, `TaskList`, `TaskUpdate`, `TaskStop`, `TaskOutput`, `TodoWrite`, `AskUserQuestion` |
| **Scheduling** | `CronCreate`, `CronList`, `CronDelete` |
| **Worktrees** | `EnterWorktree`, `ExitWorktree` |
| **MCP** | `ListMcpResourcesTool`, `ReadMcpResourceTool`, `ToolSearch` |

## Bash tool behavior

Each `Bash` command runs in a separate process. Important persistence rules:

- **Working directory carries over** across Bash calls *in the main session*, as long as `cd` lands inside the project dir or an [additional working directory](https://code.claude.com/docs/en/permissions#working-directories) added via `--add-dir`, `/add-dir`, or `additionalDirectories`.
  - If `cd` lands outside those, Claude Code **resets to the project directory** and appends `Shell cwd was reset to <dir>` to the tool result.
  - Subagent sessions **never** carry working directory between Bash calls.
  - To disable carry-over entirely (every command starts in project dir): set `CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR=1`.
- **Environment variables do NOT persist.** `export FOO=bar` in one command is gone in the next.

Workarounds for env vars:

- Activate virtualenv / conda *before* launching Claude Code.
- Set [`CLAUDE_ENV_FILE`](https://code.claude.com/docs/en/env-vars) to a shell script to persist env across Bash calls.
- Use a [`SessionStart` hook](https://code.claude.com/docs/en/hooks#persist-environment-variables) to populate env dynamically.

## LSP tool behavior

`LSP` gives Claude language-server intelligence. After each file edit, it automatically reports type errors and warnings, so Claude can fix issues without a separate build step.

Direct operations Claude can invoke:

- Jump to a symbol's definition
- Find all references to a symbol
- Get type info at a position
- List symbols in a file or workspace
- Find implementations of an interface
- Trace call hierarchies

**Inactive until you install a [code intelligence plugin](https://code.claude.com/docs/en/discover-plugins#code-intelligence)** for your language. The plugin bundles the LSP configuration; the language server binary is installed separately.

## Monitor tool

> Requires Claude Code **v2.1.98 or later**.

`Monitor` watches something in the background and streams output lines back to Claude mid-conversation. Use cases:

- Tail a log file and flag errors
- Poll a PR or CI job, report when status changes
- Watch a directory for file changes
- Track any long-running script's output

Claude writes a small watch script, runs it in the background, and receives each output line as it arrives. You keep working in the same session; Claude interjects when an event lands. Stop by asking Claude to cancel, or ending the session.

**Permissions**: shares `Bash`'s allow/deny patterns.

**Not available on**: Amazon Bedrock, Google Vertex AI, Microsoft Foundry.

## PowerShell tool

Windows-only, **opt-in preview**. Runs PowerShell commands natively instead of routing through Git Bash.

### Enable

Set `CLAUDE_CODE_USE_POWERSHELL_TOOL=1` in environment or `settings.json`:

```json
{
  "env": {
    "CLAUDE_CODE_USE_POWERSHELL_TOOL": "1"
  }
}
```

Auto-detects `pwsh.exe` (PowerShell 7+) with fallback to `powershell.exe` (5.1). **`Bash` remains registered alongside** — may need to explicitly ask Claude to use PowerShell.

### Shell selection points

| Setting | Where | Effect |
|---------|-------|--------|
| `"defaultShell": "powershell"` | `settings.json` | Routes interactive `!` commands through PowerShell (requires tool enabled) |
| `"shell": "powershell"` | Per command hook | That hook runs in PowerShell (works regardless of the env var — hooks spawn directly) |
| `shell: powershell` | Skill frontmatter | `` !`command` `` blocks use PowerShell (requires tool enabled) |

The same main-session cwd reset behavior and `CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR` flag apply.

### Preview limitations

- Auto mode not supported yet
- PowerShell profiles not loaded
- No sandboxing
- Native Windows only — not WSL
- Git Bash still required to *start* Claude Code

## Checking which tools are available

Your exact tool set depends on provider, platform, settings, and feature flags. To see what a running session has:

```text
What tools do you have access to?
```

For exact MCP tool names, run `/mcp`.

## Common Gotchas

- **`TodoWrite` vs `TaskCreate`**: `TodoWrite` only exists in non-interactive / Agent SDK contexts. Inside an interactive Claude Code session, use the `Task*` family. Don't reference `TodoWrite` in skill instructions that target interactive use.
- **`TaskOutput` is deprecated**: read the task's output file path directly with `Read`.
- **Agent team tools hidden by default**: `SendMessage`, `TeamCreate`, `TeamDelete` only appear when `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`.
- **Permission rules are case-sensitive** and must use the exact strings above. `bash` won't match — use `Bash`.
- **Bash env vars don't persist** — a surprisingly common source of "it worked when I ran it myself" bugs.
- **Cwd may silently reset** if you `cd` outside the project dir — watch for `Shell cwd was reset to <dir>` in tool results.
- **`Monitor` uses `Bash`'s permission patterns**, so a `deny` on `Bash(rm *)` also applies to a Monitor script that runs `rm`.

## See also

- [Permissions](https://code.claude.com/docs/en/permissions) — rule syntax and tool-specific patterns
- [MCP servers](https://code.claude.com/docs/en/mcp) — add custom tools
- [Sub-agents](https://code.claude.com/docs/en/sub-agents) — scope tool access per agent
- [Hooks](https://code.claude.com/docs/en/hooks-guide) — run commands before/after tool execution
