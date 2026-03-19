# Zed Key Bindings

## File Locations
- **macOS/Linux**: `~/.config/zed/keymap.json`
- **Windows**: `~\AppData\Roaming\Zed\keymap.json`
- **Open**: `zed: open keymap file` or `cmd-k cmd-s`

## Predefined Keymaps
VS Code (default), Atom, Emacs (Beta), JetBrains, Sublime Text, TextMate, Cursor, or None.
Modal modes: Vim, Helix.

## File Structure

JSON array of objects with optional `context` and required `bindings`:

```json
[
  {
    "bindings": {
      "ctrl-right": "editor::SelectLargerSyntaxNode"
    }
  },
  {
    "context": "ProjectPanel && not_editing",
    "bindings": {
      "o": "project_panel::Open"
    }
  }
]
```

## Modifier Keys

| Modifier | Key |
|----------|-----|
| `ctrl-` | Control |
| `cmd-` / `win-` / `super-` | Platform modifier (Cmd on macOS, Win on Windows, Super on Linux) |
| `alt-` | Alt/Option |
| `shift-` | Shift |
| `fn-` | Function |
| `secondary-` | `cmd` on macOS, `ctrl` on Windows/Linux |

## Key Sequences

Keypresses are space-separated:
- `"cmd-k cmd-s"` — Cmd+K then Cmd+S
- `"space e"` — Space then E
- `"shift shift"` — Press and release Shift twice

**Note**: `shift-` only combines with letters (e.g., `shift-g` = G). For punctuation like `(`, don't use shift modifier notation.

## Context System

Contexts form a hierarchical tree: `Workspace` > `Pane`/`Panel` > `Editor`

View context tree: `dev: open key context view`

Example:
```
Workspace os=macos keyboard_layout=com.apple.keylayout.QWERTY
  Pane
    Editor mode=full extension=md vim_mode=insert
```

### Context Expression Syntax
- `X && Y` — AND
- `X || Y` — OR
- `!X` — NOT
- `(X)` — Grouping
- `X > Y` — Ancestor-descendant relationship

### Context Examples
- `"Editor"` — Any editor
- `"Editor && mode == full"` — Main code editors only
- `"!Editor && !Terminal"` — Everywhere except editors/terminals
- `"os == macos > Editor"` — Editors on macOS

**Important**: Attributes apply only to their defined nodes. Combining debugger + vim mode: `debugger_stopped > vim_mode == normal`

## Action Formats

```json
// No arguments
"ctrl-a": "language_selector::Toggle"

// Single argument
"cmd-1": ["workspace::ActivatePane", 0]

// Multiple arguments
"ctrl-a": ["pane::DeploySearch", { "replace_enabled": true }]
```

## Precedence Rules

1. **Tree-based**: Bindings matching lower context tree nodes take priority
2. **Definition order**: Later definitions override earlier ones; user keymap overrides defaults
3. **Prefix sequences**: When one binding is a prefix of another (e.g., `"ctrl-w"` vs `"ctrl-w left"`), Zed waits 1 second

## Disabling Bindings

```json
{
  "context": "Workspace",
  "bindings": {
    "cmd-r": null
  }
}
```

## Key Remapping (SendKeystrokes)

```json
{
  "bindings": {
    "alt-down": ["workspace::SendKeystrokes", "down down down down"],
    "cmd-alt-c": ["workspace::SendKeystrokes", "ctrl-shift-right ctrl-shift-right cmd-c"]
  }
}
```

Max 100 simulated keys per binding. Asynchronous operations complete before sequence continues.

## Terminal Key Forwarding

```json
{
  "context": "Terminal",
  "bindings": {
    "ctrl-n": ["terminal::SendKeystroke", "ctrl-n"]
  }
}
```

## Non-QWERTY Keyboard Support

### macOS
- Cyrillic, Hebrew, Armenian: macOS auto-maps with `cmd`
- Extended Latin (AZERTY, QWERTZ): Auto-remap based on system defaults
- Enable key equivalent mapping:

```json
[
  {
    "use_key_equivalents": true,
    "bindings": {
      "ctrl->": "editor::Indent"
    }
  }
]
```

### Linux (v0.196.0+)
Non-ASCII characters automatically use QWERTY-layout equivalents for shortcuts.
