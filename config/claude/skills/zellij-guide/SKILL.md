---
name: zellij-guide
description: All-in-one Zellij terminal multiplexer guide. Use when the user asks about Zellij keybindings, configuration, layouts, plugins, sessions, CLI commands, or troubleshooting. Also use when helping with dotfiles config at ~/Development/dotfiles/config/zellij/.
---

# Zellij Guide — Personal Reference

> Binary: `/Users/wcygan/.nix-profile/bin/zellij` (installed via Nix flake)
> Config: `~/Development/dotfiles/config/zellij/config.kdl` → symlinked to `~/.config/zellij/config.kdl`
> Layouts: `~/Development/dotfiles/config/zellij/layouts/`

For exhaustive action/option/layout reference, see [reference.md](reference.md).

---

## Quick Start

```bash
zellij                           # New session (random name)
zellij -s work                   # New named session
zellij -l dev                    # New session with dev.kdl layout
zellij ls                        # List sessions (including exited)
zellij a work                    # Attach to "work" session
zellij d work                    # Delete exited session
```

---

## Your Keybinds (clear-defaults=true, vim-style)

Your config uses `clear-defaults=true` — only these bindings exist:

### Normal Mode (default)

| Key | Action |
|-----|--------|
| `Ctrl h` | Move focus / tab left |
| `Ctrl l` | Move focus / tab right |
| `Ctrl j` | Move focus down |
| `Ctrl k` | Move focus up |
| `Ctrl n` | New pane (auto direction) |
| `Ctrl s` | New pane down |
| `Ctrl v` | New pane right |
| `Ctrl -` | New pane down |
| `Ctrl /` | New pane right |
| `Ctrl x` | Close focused pane |
| `Ctrl z` | Toggle fullscreen |
| `Ctrl t` | New tab |
| `Ctrl w` | Close tab |
| `Ctrl 1-5` | Go to tab 1-5 |
| `Ctrl q` | Quit |
| `Ctrl d` | Detach |
| `Ctrl p` | → Pane mode |
| `Ctrl r` | → Resize mode |
| `Ctrl m` | → Move mode |
| `Ctrl g` | → Locked mode |
| `Ctrl b` | → Scroll mode |

### Pane Mode (`Ctrl p` to enter, `Esc` to exit)

| Key | Action |
|-----|--------|
| `h/j/k/l` | Move focus |
| `n` | New pane |
| `x` | Close pane |
| `f` | Toggle fullscreen |
| `w` | Toggle floating panes |
| `e` | Toggle embed/float |
| `r` | Rename pane |

### Resize Mode (`Ctrl r` to enter, `Esc` to exit)

| Key | Action |
|-----|--------|
| `h/j/k/l` | Resize in direction |
| `H/J/K/L` | Increase in direction |
| `=` | Increase size |
| `-` | Decrease size |

### Move Mode (`Ctrl m` to enter, `Esc` to exit)

| Key | Action |
|-----|--------|
| `h/j/k/l` | Move pane in direction |

### Scroll Mode (`Ctrl b` to enter, `Esc` to exit)

| Key | Action |
|-----|--------|
| `j/k` | Scroll down/up |
| `Ctrl d` / `Ctrl u` | Half page down/up |
| `g` | Scroll to top |
| `G` | Scroll to bottom |

### Locked Mode (`Ctrl g` to toggle)

All keys pass through to the terminal. Only `Ctrl g` exits.

### Modes NOT configured (from defaults)

Your config does not define: `tab`, `search`, `entersearch`, `renametab`, `renamepane`, `session`, `tmux`. Consider adding `search` and `session` modes for search-in-scrollback and session manager access.

---

## Your Config Summary

```kdl
// Key settings in config.kdl:
default_layout "compact"          // 1-line compact-bar (tab + status combined)
pane_frames false                 // No borders between panes
theme "default"                   // Base16 dark theme (defined inline)
default_shell "~/.nix-profile/bin/fish"
copy_on_select true
scrollback_editor "/usr/bin/nvim"
session_serialization true        // Enable resurrection
serialize_pane_viewport true      // Save visible content
max_panes 100
layout_dir "~/.config/zellij/layouts"
```

**Note**: `default_shell` and `layout_dir` use `/home/wcygan/` paths (Linux). On macOS these should be `/Users/wcygan/` paths. Consider using `$HOME` or updating for cross-platform use.

---

## Your Layouts

### dev.kdl (3-tab development layout)

```
Tab "main" (focused):
┌─────────────────────┬──────────┐
│                     │ terminal │
│  editor (70%)       ├──────────┤
│                     │  logs    │
└─────────────────────┴──────────┘

Tab "git":     lazygit (full pane)
Tab "monitor": btop (50%) + services (50%)
```

Load with: `zellij -l dev` or `zellij --layout ~/.config/zellij/layouts/dev.kdl`

---

## Modes Reference (13 total)

| Mode | Purpose | Your binding |
|------|---------|-------------|
| `normal` | Default operations | (default) |
| `locked` | Pass-through (safety) | `Ctrl g` |
| `pane` | Pane management | `Ctrl p` |
| `resize` | Resize panes | `Ctrl r` |
| `move` | Move panes | `Ctrl m` |
| `scroll` | Scroll buffer | `Ctrl b` |
| `tab` | Tab management | *(not bound)* |
| `search` | Search in scrollback | *(not bound)* |
| `entersearch` | Type search query | *(not bound)* |
| `renametab` | Rename a tab | *(not bound)* |
| `renamepane` | Rename a pane | *(not bound)* |
| `session` | Session management | *(not bound)* |
| `tmux` | tmux compatibility | *(not bound)* |

---

## CLI Quick Reference

### Session Management

```bash
zellij                                    # New session
zellij -s <name>                          # Named session
zellij ls                                 # List all (running + exited)
zellij attach <name>                      # Attach / resurrect
zellij attach -c <name>                   # Create-or-attach
zellij kill-session <name>                # Kill running session
zellij delete-session <name>              # Delete exited session
zellij kill-all-sessions                  # Kill all
zellij delete-all-sessions                # Delete all exited
```

### Run Commands in Panes

```bash
zellij run -- htop                        # New pane running htop
zellij run -f -- htop                     # Floating pane
zellij run -f --width 80% --height 80% -- htop  # Sized floating
zellij run -i -- make build               # In-place (replaces current pane)
zellij run -c -- make test                # Close pane on exit
zellij run -s -- dangerous-cmd            # Start suspended (ENTER to run)
zellij run -n "build" -- make             # Named pane
```

### Edit Files

```bash
zellij edit src/main.rs                   # Open in $EDITOR pane
zellij edit -f src/main.rs                # Floating editor pane
zellij edit -l 42 src/main.rs             # Open at line 42
```

### Actions (from outside or within)

```bash
zellij action new-pane                    # New pane
zellij action new-pane --floating         # New floating pane
zellij action new-tab --name "build"      # Named new tab
zellij action go-to-tab 2                 # Switch to tab 2
zellij action dump-layout                 # Export current layout to stdout
zellij action dump-screen /tmp/out.txt    # Dump pane content
zellij action switch-mode locked          # Enter locked mode
zellij action toggle-floating-panes       # Toggle floats
zellij action rename-session "work"       # Rename session
```

### Setup Utilities

```bash
zellij setup --dump-config                # Print default config
zellij setup --dump-layout default        # Print default layout
zellij setup --dump-layout compact        # Print compact layout
zellij setup --dump-swap-layout default   # Print swap layout
zellij setup --generate-completion fish   # Fish completions
zellij setup --generate-auto-start fish   # Auto-start script
zellij setup --check                      # Validate config
```

### Convenience Aliases (from shell completions)

| Alias | Expands to |
|-------|-----------|
| `zr` | `zellij run --` |
| `zrf` | `zellij run --floating --` |
| `ze` | `zellij edit` |

---

## Session Resurrection

Your config has resurrection enabled (`session_serialization true`, `serialize_pane_viewport true`).

**What's saved**: Layout, pane structure, commands, visible viewport, scrollback.
**What's NOT saved**: Running processes. Commands show "Press ENTER to run..." on resurrection.

```bash
zellij ls                                 # Shows EXITED sessions
zellij attach <exited-session>            # Resurrect it
zellij attach <name> --force-run-commands # Skip ENTER confirmation
zellij delete-session <name>              # Permanently remove
```

Serialized sessions are human-readable KDL layout files in the cache directory. They can be shared, modified, or loaded directly with `zellij --layout`.

---

## Floating & Stacked Panes

**Floating**: `Ctrl p` then `w` (toggle), `e` (embed/float), or `Alt f` (if default binds)
**Pinned floating**: Always-on-top panes (pin via CLI: `zellij run -f --pinned -- cmd`)
**Stacked**: Panes in a stack where only the focused one is expanded. Define in layouts with `stacked=true`.

---

## Plugins (Built-in)

| Plugin | Location | Description |
|--------|----------|-------------|
| `tab-bar` | `zellij:tab-bar` | Tab bar (1 line) |
| `status-bar` | `zellij:status-bar` | Status bar with keybind hints (2 lines) |
| `compact-bar` | `zellij:compact-bar` | Combined tab+status (1 line) |
| `strider` | `zellij:strider` | File browser sidebar |
| `session-manager` | `zellij:session-manager` | Session switcher + resurrection UI |
| `filepicker` | `zellij:strider` | File picker (cwd based) |
| `configuration` | `zellij:configuration` | Runtime config editor |
| `plugin-manager` | `zellij:plugin-manager` | Plugin management UI |

Load in layouts:
```kdl
pane size=1 borderless=true {
    plugin location="zellij:compact-bar"
}
```

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| macOS Alt key not working | Configure in terminal app (iTerm2: Profiles → Keys → Left Option = Esc+) |
| Copy not working | Add `copy_command "pbcopy"` to config |
| Font/character issues | Use Nerd Font or `simplified_ui true` |
| Ctrl+H triggers Move mode | Terminal sends Ctrl+H as backspace — remap in terminal or Zellij |
| Nesting prevention | Check `$ZELLIJ` env var before starting |
| Mouse selection | Hold SHIFT to bypass Zellij mouse capture |
| Styled underline colors wrong | Add `styled_underlines false` |
| Config not loading | Check `zellij setup --check` and verify path |

### Fish Shell Integration

```fish
# Nesting prevention (add to config.fish or conf.d/)
if status is-interactive; and not set -q ZELLIJ
    zellij attach -c default
end

# Generate completions
zellij setup --generate-completion fish > ~/.config/fish/completions/zellij.fish
```

### Environment Variables

| Variable | Description |
|----------|-------------|
| `ZELLIJ` | Set to `0` inside a session (use for nesting prevention) |
| `ZELLIJ_SESSION_NAME` | Current session name |
| `ZELLIJ_CONFIG_DIR` | Override config directory |
| `ZELLIJ_CONFIG_FILE` | Override config file |
| `ZELLIJ_AUTO_ATTACH` | Auto-attach to existing session |
| `ZELLIJ_AUTO_EXIT` | Exit shell when Zellij exits |

---

## Layout Authoring Quick Reference

```kdl
layout {
    // Tab template applied to all tabs
    default_tab_template {
        pane size=1 borderless=true { plugin location="zellij:tab-bar" }
        children    // ← where tab content goes
        pane size=2 borderless=true { plugin location="zellij:status-bar" }
    }

    tab name="code" focus=true {
        pane split_direction="vertical" {
            pane size="60%" name="editor" edit="src/main.rs"
            pane size="40%" split_direction="horizontal" {
                pane name="term"
                pane name="test" command="make" { args "test"; }
            }
        }
    }

    tab name="git" {
        pane command="lazygit"
    }

    // Floating panes section
    floating_panes {
        pane x="10%" y="10%" width="80%" height="80%" name="scratch"
    }
}
```

### Key layout attributes

| Attribute | Applies to | Values |
|-----------|-----------|--------|
| `split_direction` | pane | `"vertical"`, `"horizontal"` |
| `size` | pane | `"50%"` or fixed int (lines/cols) |
| `command` | pane | Command to execute |
| `args` | child of command pane | `"arg1" "arg2"` |
| `edit` | pane | File path (opens in $EDITOR) |
| `cwd` | pane, tab, layout | Working directory |
| `name` | pane, tab | Display name |
| `focus` | pane, tab | `true` for initial focus |
| `borderless` | pane | `true` to hide frame |
| `close_on_exit` | pane | Close when command exits |
| `start_suspended` | pane | Wait for ENTER |
| `stacked` | pane | Stack children |
| `plugin location` | child block | Plugin URL |

CWD composes: pane cwd → tab cwd → layout cwd → execution directory. Relative paths chain; absolute paths override.

For the full actions reference, theme system, swap layouts, and plugin configuration, see [reference.md](reference.md).
