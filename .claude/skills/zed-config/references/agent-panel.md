# Zed Agent Panel

## Overview
The Agent Panel enables interaction with AI agents that can read, write, and run code. Access via `agent: new thread` or the sparkle icon in the status bar.

## Setup
Requires at least one configured LLM provider or external agent:
- Zed Pro subscription for hosted models
- Custom API keys (Anthropic, OpenRouter, etc.)
- External agents (Gemini CLI, Claude Agent)

## Thread Management
- **New thread**: `agent: new thread` command
- **Recent threads**: `cmd-shift-j` / `ctrl-shift-j`
- **All threads**: `cmd-shift-h` / `ctrl-shift-h`
- **Message editing**: Click sent message cards to edit prompts and context
- **Message queueing**: Messages sent during generation are queued automatically

## Adding Context
Type `@` to mention:
- Files and directories
- Symbols
- Previous threads
- Rules files
- Diagnostics

**Selection as context**: `cmd->` / `ctrl->` or `agent: add selection to thread`
**Image support**: Vision-capable models accept images via @-mention or drag-and-drop

## Checkpoints & Restoration
"Restore Checkpoint" buttons appear after model edits, allowing rollback to code states before that message.

## Change Review
After agent modifications:
- File counts and line changes shown
- Expand accordion or `ctrl-shift-r` to open multi-buffer review
- Accept/reject individual hunks or entire change sets
- Single-file diffs controlled by `agent.single_file_review` setting

## Follow Agent
Crosshair icon at bottom-left auto-jumps editor to files the agent touches. Hold `cmd`/`ctrl` when submitting to auto-follow.

## Notifications
When Zed is backgrounded:
- `agent.notify_when_agent_waiting` - visual notifications
- `agent.play_sound_when_agent_done` - sound notifications

## Tool Profiles
Three built-in profiles:
- **Write**: All tools enabled; permits file writes and terminal commands
- **Ask**: Read-only tools for code questions
- **Minimal**: No tools; general LLM conversation

**Management**: `agent: manage profiles` or `cmd-alt-p` / `ctrl-alt-p`
**Cycle profiles**: `shift-tab`

### Custom Profiles
Create via Agent Profile modal or `agent.profiles` settings key.

## Tool Permissions
`agent.tool_permissions.default` setting (v0.224.0+):
- `"confirm"` (default): Prompts before actions
- `"allow"`: Auto-approves
- `"deny"`: Blocks all

Per-tool and pattern-based rules supported. Even with auto-approval, `always_deny` and `always_confirm` patterns are respected.

## Model Selection
- **Switch model**: Click selector or `cmd-alt-/` / `ctrl-alt-/`
- **Favorites**: Star models or use `agent.favorite_models` setting
- **Cycle favorites**: `alt-tab` / `alt-l`

## Token Usage
Token consumption displays near profile selector. When approaching limits, banner suggests "New from Summary" thread.

## Text Threads
Alternative format presenting conversations as raw text with full user control. No autonomous code editing available.

## Keybinding Summary
| Action | Keybinding |
|--------|-----------|
| New thread | `agent: new thread` |
| Recent threads | `cmd-shift-j` |
| All threads | `cmd-shift-h` |
| Change review | `ctrl-shift-r` |
| Add selection | `cmd->` |
| Model selector | `cmd-alt-/` |
| Manage profiles | `cmd-alt-p` |
| Cycle profiles | `shift-tab` |
| Cycle favorites | `alt-tab` |
| Paste raw text | `cmd-shift-v` |
