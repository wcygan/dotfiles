# Zellij Exhaustive Reference

## All Keybind Actions (for config.kdl)

These are all actions usable in `bind` statements inside `keybinds { }` blocks.

### Pane Management

| Action | Parameters | Description |
|--------|-----------|-------------|
| `NewPane` | `"Down"`, `"Right"`, `"Stacked"` (optional) | Open new pane |
| `CloseFocus` | — | Close focused pane |
| `ToggleFocusFullscreen` | — | Toggle pane fullscreen |
| `TogglePaneFrames` | — | Toggle frame visibility |
| `TogglePaneEmbedOrFloating` | — | Convert between embedded/floating |
| `ToggleFloatingPanes` | — | Show/hide floating panes |
| `TogglePanePinned` | — | Pin/unpin floating pane (always-on-top) |
| `TogglePaneInGroup` | — | Toggle pane in pane group |
| `ToggleGroupMarking` | — | Toggle group marking |
| `PaneNameInput` | `0` | Start pane name input |
| `UndoRenamePane` | — | Undo pane rename |
| `Clear` | — | Clear scrollback buffer |
| `BreakPane` | — | Break pane to new tab |
| `BreakPaneRight` | — | Break pane right |
| `BreakPaneLeft` | — | Break pane left |

### Navigation

| Action | Parameters | Description |
|--------|-----------|-------------|
| `MoveFocus` | `"Left"`, `"Right"`, `"Up"`, `"Down"` | Move focus to direction |
| `MoveFocusOrTab` | `"Left"`, `"Right"` | Move focus or switch tab at edge |
| `FocusNextPane` | — | Focus next pane |
| `FocusPreviousPane` | — | Focus previous pane |
| `SwitchFocus` | — | Toggle focus between panes |
| `MovePane` | `"Left"`, `"Right"`, `"Up"`, `"Down"` | Move pane in direction |
| `MovePaneBackwards` | — | Rotate pane backward |

### Tab Management

| Action | Parameters | Description |
|--------|-----------|-------------|
| `NewTab` | `{ cwd; name; layout }` (optional) | New tab |
| `CloseTab` | — | Close current tab |
| `GoToTab` | `N` (1-indexed) | Go to tab by number |
| `GoToNextTab` | — | Next tab |
| `GoToPreviousTab` | — | Previous tab |
| `MoveTab` | `"Left"`, `"Right"` | Move tab position |
| `ToggleTab` | — | Toggle tab focus |
| `ToggleActiveSyncTab` | — | Sync input across all panes in tab |
| `TabNameInput` | `0` | Start tab name input |
| `UndoRenameTab` | — | Undo tab rename |

### Scrolling

| Action | Parameters | Description |
|--------|-----------|-------------|
| `ScrollUp` | — | Scroll up 1 line |
| `ScrollDown` | — | Scroll down 1 line |
| `ScrollToTop` | — | Jump to top |
| `ScrollToBottom` | — | Jump to bottom |
| `HalfPageScrollUp` | — | Half page up |
| `HalfPageScrollDown` | — | Half page down |
| `PageScrollUp` | — | Full page up |
| `PageScrollDown` | — | Full page down |

### Resize

| Action | Parameters | Description |
|--------|-----------|-------------|
| `Resize` | `"Left"`, `"Right"`, `"Up"`, `"Down"`, `"Increase"`, `"Decrease"`, `"Increase Left"`, `"Increase Right"`, `"Increase Up"`, `"Increase Down"` | Resize pane |

### Search

| Action | Parameters | Description |
|--------|-----------|-------------|
| `Search` | `"down"`, `"up"` | Search direction |
| `SearchInput` | `0` | Start search text input |
| `SearchToggleOption` | `"CaseSensitivity"`, `"Wrap"`, `"WholeWord"` | Toggle search option |

### Layout

| Action | Parameters | Description |
|--------|-----------|-------------|
| `NextSwapLayout` | — | Cycle to next swap layout |
| `PreviousSwapLayout` | — | Cycle to previous swap layout |

### Plugins

| Action | Parameters | Description |
|--------|-----------|-------------|
| `LaunchOrFocusPlugin` | `"url" { floating true; move_to_focused_tab true }` | Launch or focus plugin |
| `MessagePlugin` | `{ name; payload; ... }` | Send message to plugin |

### I/O

| Action | Parameters | Description |
|--------|-----------|-------------|
| `Write` | `N` (byte value) | Write bytes to terminal |
| `WriteChars` | `"string"` | Write string to terminal |
| `EditScrollback` | — | Open scrollback in $EDITOR |
| `DumpScreen` | `"filepath"` | Dump pane contents to file |
| `Copy` | — | Copy selection to clipboard |

### Commands

| Action | Parameters | Description |
|--------|-----------|-------------|
| `Run` | `{ cmd; args; cwd; direction }` | Run command in pane |

### Mode Switching

| Action | Parameters | Description |
|--------|-----------|-------------|
| `SwitchToMode` | Mode name (see below) | Switch input mode |

Valid modes: `"Normal"`, `"Locked"`, `"Pane"`, `"Resize"`, `"Move"`, `"Tab"`, `"Scroll"`, `"Search"`, `"EnterSearch"`, `"RenameTab"`, `"RenamePane"`, `"Session"`, `"Tmux"`

### System

| Action | Parameters | Description |
|--------|-----------|-------------|
| `Detach` | — | Detach from session |
| `Quit` | — | Exit Zellij |
| `ToggleMouseMode` | — | Toggle mouse support |

---

## All Configuration Options

### Top-Level Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `on_force_close` | `"detach"` / `"quit"` | `"detach"` | Behavior on SIGTERM/SIGINT/SIGQUIT/SIGHUP |
| `simplified_ui` | bool | `false` | Simple UI without arrow fonts |
| `default_shell` | path | `$SHELL` | Default shell for new panes |
| `default_cwd` | path | — | Override cwd for new panes |
| `pane_frames` | bool | `true` | Show pane borders |
| `theme` | string | `"default"` | Active color theme |
| `default_layout` | string | `"default"` | Layout loaded at startup |
| `default_mode` | string | `"normal"` | Starting input mode |
| `mouse_mode` | bool | `true` | Enable mouse support |
| `scroll_buffer_size` | int | `10000` | Scrollback buffer lines |
| `copy_command` | string | — | Clipboard command (e.g., `"pbcopy"`) |
| `copy_clipboard` | `"system"` / `"primary"` | `"system"` | Clipboard target |
| `copy_on_select` | bool | `true` | Auto-copy on mouse release |
| `scrollback_editor` | path | `$EDITOR` / `$VISUAL` | Editor for scrollback |
| `mirror_session` | bool | `false` | Mirror mode for multiple users |
| `layout_dir` | path | config subdir | Custom layouts directory |
| `theme_dir` | path | config subdir | Custom themes directory |
| `auto_layout` | bool | `true` | Use swap layouts automatically |
| `styled_underlines` | bool | `true` | Extended ANSI underlines |
| `session_serialization` | bool | `true` | Enable session resurrection |
| `pane_viewport_serialization` | bool | `false` | Save visible pane content |
| `scrollback_lines_to_serialize` | int | `0` | Lines to serialize (0 = all) |
| `serialization_interval` | int | `1` | Seconds between serialization |
| `disable_session_metadata` | bool | `false` | Suppress metadata writing |
| `support_kitty_keyboard_protocol` | bool | `true` | Kitty keyboard support |
| `stacked_resize` | bool | `true` | Stack panes during resize |
| `show_startup_tips` | bool | `true` | Show tips on launch |
| `show_release_notes` | bool | `true` | Show release notes |
| `advanced_mouse_actions` | bool | `true` | Mouse hover/grouping effects |
| `max_panes` | int | — | Maximum pane limit |
| `post_command_discovery_hook` | string | — | Transform commands for resurrection |

### UI Sub-Options

```kdl
ui {
    pane_frames {
        rounded_corners true
        hide_session_name true
    }
}
```

### Environment Variables

```kdl
env {
    MY_VAR "value"
    EDITOR "nvim"
}
```

### Plugin Aliases

```kdl
plugins {
    tab-bar location="zellij:tab-bar"
    status-bar location="zellij:status-bar"
    compact-bar location="zellij:compact-bar"
    strider location="zellij:strider"
    session-manager location="zellij:session-manager"
    welcome-screen location="zellij:session-manager" { welcome_screen true }
    filepicker location="zellij:strider" { cwd "/" }
    configuration location="zellij:configuration"
    plugin-manager location="zellij:plugin-manager"
    about location="zellij:about"
}
```

---

## Theme System

### Legacy Syntax (your current config)

```kdl
themes {
    default {
        fg "#D8D8D8"
        bg "#181818"
        black "#181818"
        red "#AB4642"
        green "#A1B56C"
        yellow "#F7CA88"
        blue "#7CAFC2"
        magenta "#BA8BAF"
        cyan "#86C1B9"
        white "#D8D8D8"
        orange "#DC9656"
    }
}
```

### Modern Component-Based Syntax

```kdl
themes {
    my-theme {
        text_unselected {
            base 200 200 200
            background 24 24 24
            emphasis_0 171 70 66    // red accent
            emphasis_1 161 181 108  // green accent
            emphasis_2 124 175 194  // blue accent
            emphasis_3 186 139 175  // magenta accent
        }
        text_selected { ... }
        ribbon_unselected { ... }
        ribbon_selected { ... }
        table_title { ... }
        table_cell_unselected { ... }
        table_cell_selected { ... }
        list_unselected { ... }
        list_selected { ... }
        frame_unselected { ... }
        frame_selected { ... }
        frame_highlight { ... }
        exit_code_success { ... }
        exit_code_error { ... }
        multiplayer_user_colors {
            player_1 ... player_10
        }
    }
}
```

Each component block accepts: `base`, `background`, `emphasis_0` through `emphasis_3` (RGB triplets).

Themes can also live in separate files in `theme_dir` or `CONFIG_DIR/themes/`.

---

## Swap Layouts

Swap layouts rearrange panes automatically as you add/remove them. Defined inline in layouts or in separate `.swap.kdl` files.

### Tiled Swap Layout

```kdl
swap_tiled_layout name="vertical-stack" {
    tab max_panes=3 {
        pane split_direction="vertical" {
            pane
            pane
        }
    }
    tab max_panes=5 {
        pane split_direction="vertical" {
            pane
            pane { children; }
        }
    }
}
```

### Floating Swap Layout

```kdl
swap_floating_layout {
    floating_panes max_panes=3 {
        pane x=0 y=0 width="25%"
        pane x="25%" width="50%"
    }
}
```

### Constraints

| Constraint | Description |
|-----------|-------------|
| `max_panes` | Apply when pane count <= N |
| `min_panes` | Apply when pane count >= N |
| `exact_panes` | Apply at exactly N panes |

Switch manually: `Alt + [` / `Alt + ]` (default binds) or `NextSwapLayout` / `PreviousSwapLayout` actions.

Dump defaults: `zellij setup --dump-swap-layout default`

---

## Plugin System

### Plugin Locations

| Prefix | Source |
|--------|--------|
| `zellij:name` | Built-in plugin |
| `file:/path/plugin.wasm` | Local WASM file |
| `http(s)://url/plugin.wasm` | Remote WASM |
| bare alias name | From `plugins { }` config block |

### Built-in Plugins

| Plugin | Description | Typical size |
|--------|-------------|-------------|
| `zellij:tab-bar` | Tab bar | 1 line |
| `zellij:status-bar` | Status bar with keybind hints | 2 lines |
| `zellij:compact-bar` | Combined tab+status | 1 line |
| `zellij:strider` | File browser sidebar | pane |
| `zellij:session-manager` | Session management UI | pane |
| `zellij:configuration` | Runtime config editor | pane |
| `zellij:plugin-manager` | Plugin management | pane |

### Loading Plugins at Startup

```kdl
load_plugins {
    https://example.com/my-plugin.wasm
    file:/path/to/plugin.wasm
}
```

### Plugin in Layouts

```kdl
pane size=1 borderless=true {
    plugin location="zellij:tab-bar"
}
```

### Plugin CLI

```bash
zellij plugin -- zellij:session-manager     # Load plugin
zellij plugin -f -- zellij:session-manager  # Floating
zellij pipe -p zellij:session-manager       # Pipe data to plugin
```

---

## Complete CLI Reference

### Top-Level Commands

| Command | Alias | Description |
|---------|-------|-------------|
| `zellij` | — | Start new session |
| `zellij attach` | `a` | Attach to session |
| `zellij list-sessions` | `ls` | List sessions |
| `zellij kill-session` | `k` | Kill running session |
| `zellij kill-all-sessions` | `ka` | Kill all running |
| `zellij delete-session` | `d` | Delete exited session |
| `zellij delete-all-sessions` | `da` | Delete all exited |
| `zellij run` | `r` | Run command in new pane |
| `zellij edit` | `e` | Edit file in new pane |
| `zellij action` | `ac` | Send action to session |
| `zellij plugin` | `p` | Load a plugin |
| `zellij pipe` | — | Pipe data to plugins |
| `zellij options` | — | Change runtime options |
| `zellij setup` | — | Setup utilities |
| `zellij list-aliases` | `la` | List plugin aliases |
| `zellij convert-config` | — | Convert old config format |
| `zellij convert-layout` | — | Convert old layout format |
| `zellij convert-theme` | — | Convert old theme format |

### Global Flags

| Flag | Env Var | Description |
|------|---------|-------------|
| `-s, --session <NAME>` | — | Session name |
| `-l, --layout <LAYOUT>` | — | Layout file |
| `-n, --new-session-with-layout <LAYOUT>` | — | Always new session |
| `-c, --config <FILE>` | `ZELLIJ_CONFIG_FILE` | Config file path |
| `--config-dir <DIR>` | `ZELLIJ_CONFIG_DIR` | Config directory |
| `--max-panes <N>` | — | Max panes |
| `-d, --debug` | — | Debug mode |
| `--data-dir <DIR>` | — | Plugin directory |

### `zellij run` Flags

| Flag | Description |
|------|-------------|
| `-c, --close-on-exit` | Close pane when command exits |
| `--cwd <DIR>` | Working directory |
| `-d, --direction <DIR>` | Pane direction (up/down/left/right) |
| `-f, --floating` | Floating pane |
| `--height <N>` | Height (int or percent) |
| `--width <N>` | Width (int or percent) |
| `-x <N>` | X position (int or percent) |
| `-y <N>` | Y position (int or percent) |
| `-i, --in-place` | Replace current pane |
| `-n, --name <NAME>` | Pane name |
| `--pinned` | Pin floating pane |
| `-s, --start-suspended` | Wait for ENTER |
| `--stacked` | Stacked pane |

### `zellij edit` Flags

| Flag | Description |
|------|-------------|
| `--cwd <DIR>` | Working directory |
| `-d, --direction <DIR>` | Pane direction |
| `-f, --floating` | Floating pane |
| `--height/--width` | Size |
| `-i, --in-place` | Replace current pane |
| `-l, --line-number <N>` | Open at line |
| `--pinned` | Pin floating pane |
| `-x, -y` | Position |

### `zellij attach` Flags

| Flag | Description |
|------|-------------|
| `-c, --create` | Create session if it doesn't exist |
| `-b, --create-background` | Create in background |
| `-f, --force-run-commands` | Skip ENTER confirmation on resurrection |
| `-i, --index <N>` | Attach by session index |

---

## Stacked Panes

Panes stacked vertically where only the focused pane is expanded; others show just their title line.

### In Layouts

```kdl
pane stacked=true {
    pane name="editor" expanded=true
    pane name="tests"
    pane name="logs" command="tail" { args "-f" "app.log"; }
}
```

### Resize-Based Stacking

With `stacked_resize true` (default):
- `Alt +` increases pane size; if insufficient space, creates a stack
- `Alt -` decreases size; breaks stacks apart
- If already stacked fullscreen, `Alt +` again → true fullscreen

### CLI

```bash
zellij action stack-panes terminal_1 terminal_2  # Stack specific panes
zellij run --stacked -- htop                      # New stacked pane
```

---

## Session Resurrection Details

### Configuration

```kdl
session_serialization true         // Enable (default: true)
pane_viewport_serialization true   // Save visible content (default: false)
scrollback_lines_to_serialize 0    // 0 = all, N = limit
serialization_interval 1           // Seconds between saves
```

### post_command_discovery_hook

Custom command to transform serialized commands:

```kdl
post_command_discovery_hook "echo $RESURRECT_COMMAND | sed 's/sudo //g'"
```

The hook receives each command via `$RESURRECT_COMMAND` env var and should output the modified command.

### Resurrection Flow

1. Session serializes layout + commands every N seconds to cache
2. On `Quit` or crash, serialized state persists
3. `zellij ls` shows session as EXITED
4. `zellij attach <name>` recreates the layout
5. Each command pane shows "Press ENTER to run..." (safety)
6. `--force-run-commands` skips the confirmation

### Session Manager Plugin

Inside Zellij:
1. Enter session mode (default: `Ctrl o`)
2. Press `w` to open session manager
3. Press `TAB` to toggle between RUNNING and EXITED sessions
4. `ENTER` to attach/resurrect

---

## Config File Locations (Priority Order)

1. `--config-dir` CLI flag
2. `ZELLIJ_CONFIG_DIR` environment variable
3. `$HOME/.config/zellij/`
4. Platform default (macOS: `~/Library/Application Support/org.Zellij-Contributors.Zellij/`)
5. `/etc/zellij/` (system-wide)

Config can be bypassed with `zellij options --clean`.

Zellij watches config for changes and applies most settings live.

---

## Keybind Syntax Reference

### Basic Binding

```kdl
keybinds {
    normal {
        bind "Ctrl a" { NewPane; }
    }
}
```

### Multiple Keys → One Action

```kdl
bind "h" "Left" { MoveFocus "Left"; }
```

### One Key → Multiple Actions

```kdl
bind "f" { ToggleFocusFullscreen; SwitchToMode "Normal"; }
```

### Clear Defaults

```kdl
keybinds clear-defaults=true { ... }     // Clear all
keybinds {
    normal clear-defaults=true { ... }    // Clear per-mode
}
```

### Unbinding

```kdl
keybinds {
    unbind "Ctrl g"                       // Unbind from all modes
    normal { unbind "Alt h" "Alt n"; }    // Unbind from specific mode
}
```

### Shared Bindings

```kdl
keybinds {
    shared_except "locked" {
        bind "Ctrl g" { SwitchToMode "Locked"; }
    }
    shared_except "normal" "locked" {
        bind "Enter" "Esc" { SwitchToMode "Normal"; }
    }
}
```

### Key Names

Modifiers: `Ctrl`, `Alt`, `Shift`
Special keys: `Enter`, `Esc`, `Tab`, `Backspace`, `Delete`, `Insert`, `Home`, `End`, `PageUp`, `PageDown`, `Left`, `Right`, `Up`, `Down`, `F1`-`F12`, `Space`

---

## Layout Templates

### Pane Template

```kdl
layout {
    pane_template name="with-monitoring" split_direction="horizontal" {
        children
        pane size="20%" command="htop"
    }
    with-monitoring {
        pane command="vim"
    }
}
```

### Tab Template

```kdl
layout {
    tab_template name="with-bars" {
        pane size=1 borderless=true { plugin location="zellij:tab-bar" }
        children
        pane size=2 borderless=true { plugin location="zellij:status-bar" }
    }
    with-bars name="code" { pane }
}
```

### default_tab_template vs new_tab_template

- `default_tab_template`: Applied to ALL tabs defined in the layout AND new tabs opened at runtime
- `new_tab_template`: Only for dynamically opened new tabs (overrides default_tab_template for new tabs)

---

## Useful Patterns

### IDE-Like Layout

```kdl
layout {
    default_tab_template {
        pane size=1 borderless=true { plugin location="zellij:tab-bar" }
        children
    }
    tab name="code" focus=true {
        pane split_direction="vertical" {
            pane size="20%" { plugin location="zellij:strider" }
            pane size="60%" name="editor"
            pane size="20%" split_direction="horizontal" {
                pane name="terminal"
                pane name="output"
            }
        }
    }
}
```

### Task Runner Layout

```kdl
tab name="tasks" {
    pane stacked=true {
        pane name="build" command="make" { args "build"; } expanded=true
        pane name="test" command="make" { args "test"; }
        pane name="lint" command="make" { args "lint"; }
    }
}
```

### Multi-Service Dev

```kdl
tab name="services" {
    pane split_direction="vertical" {
        pane name="api" command="make" { args "run-api"; }
        pane name="web" command="make" { args "run-web"; }
        pane name="worker" command="make" { args "run-worker"; }
    }
}
```
