# Zed Tasks

## Overview
Tasks execute commands through Zed's integrated terminal with access to limited editor state.

## Task Sources
1. **Global**: `~/.config/zed/tasks.json` — available across all projects (`zed: open tasks`)
2. **Project**: `.zed/tasks.json` — project-specific (`zed: open project tasks`)
3. **Oneshot**: Created on-the-fly via task modal (session-only persistence)
4. **Language extensions**: Provided by language support

## Task Format

```json
{
  "label": "Task name",
  "command": "command to execute",
  "args": ["arg1", "arg2"],
  "env": { "FOO": "bar" },
  "cwd": "/path/to/working/directory",
  "use_new_terminal": false,
  "allow_concurrent_runs": false,
  "reveal": "always",
  "hide": "never",
  "shell": "system",
  "show_summary": true,
  "show_command": true,
  "save": "all",
  "tags": [],
  "reevaluate_context": false
}
```

## Properties

| Property | Values | Purpose |
|----------|--------|---------|
| `label` | string | Display name in task modal |
| `command` | string | Command to execute |
| `args` | string[] | Command arguments |
| `env` | object | Environment variables |
| `cwd` | string | Working directory |
| `reveal` | `"always"`, `"no_focus"`, `"never"` | Terminal pane behavior on start |
| `hide` | `"never"`, `"always"`, `"on_success"` | Terminal pane behavior on completion |
| `save` | `"all"`, `"current"`, `"none"` | Which buffers to save before running |
| `shell` | `"system"`, `{"program": "sh"}`, `{"with_arguments": {...}}` | Shell configuration |
| `use_new_terminal` | boolean | Reuse tab or create new one |
| `allow_concurrent_runs` | boolean | Allow multiple simultaneous instances |
| `reevaluate_context` | boolean | Recalculate variables on each rerun |
| `show_summary` | boolean | Show task summary in terminal |
| `show_command` | boolean | Show command in terminal |
| `tags` | string[] | Bind to inline runnable indicators |

## Variables

Zed injects editor context as environment variables:

| Variable | Description |
|----------|-------------|
| `ZED_COLUMN` | Cursor column |
| `ZED_ROW` | Cursor row |
| `ZED_FILE` | Absolute file path |
| `ZED_FILENAME` | Just the filename |
| `ZED_DIRNAME` | Directory of current file |
| `ZED_RELATIVE_FILE` | Path relative to worktree root |
| `ZED_RELATIVE_DIR` | Directory relative to worktree root |
| `ZED_STEM` | Filename without extension |
| `ZED_SYMBOL` | Currently selected symbol |
| `ZED_SELECTED_TEXT` | Selected text content |
| `ZED_LANGUAGE` | Language identifier (e.g., "Rust") |
| `ZED_WORKTREE_ROOT` | Project root path |
| `ZED_CUSTOM_RUST_PACKAGE` | Parent Rust package name |

**Syntax**: `$VAR_NAME` or `${VAR_NAME:default_value}` for defaults.

Tasks with unavailable variables (except those with defaults) are hidden from the task modal.

## Core Actions
- **`task: spawn`**: Opens modal with available tasks
- **`task: rerun`**: Reruns most recently spawned task

## Oneshot Tasks
Type a command in the modal text field, use `opt-enter` to spawn. These persist during the session.
Use `cmd` modifier when spawning for **ephemeral** tasks (don't affect rerun history).

## Custom Keybindings

```json
{
  "context": "Workspace",
  "bindings": {
    "alt-g": ["task::Spawn", { "task_name": "echo current file's path" }]
  }
}
```

Optional `reveal_target` parameter: `"center"` to show output in center pane.

## Runnable Tags

Bind tasks to inline code action indicators:

```json
{
  "label": "Run test",
  "command": "cargo test $ZED_SYMBOL",
  "tags": ["rust-test"]
}
```

Access via `editor: Toggle Code Actions` or `cmd-.` / `ctrl-.`.

## Bash Script Execution
Zed auto-detects `.sh` and `.bash` files as runnable with `bash-script` tag.

## Shell Initialization
Tasks launch in login shells, sourcing init files (`.bash_profile`, `.zshrc`). Override via `terminal.shell` setting.
