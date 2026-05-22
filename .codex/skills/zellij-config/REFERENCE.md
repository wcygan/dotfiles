# Zellij Configuration Reference

Quick reference for Zellij configuration using KDL format.

## KDL Format Basics

```kdl
// Comments use double slashes
key "value"
key value  // Quotes optional for simple values

// Nested blocks
block {
    nested_key "value"
}

// Multiple values
bind "key1" "key2" { Action1; Action2; }
```

## File Locations

```
~/.config/zellij/
├── config.kdl          # Main configuration
├── layouts/
│   ├── default.kdl     # Default layout
│   └── custom.kdl      # Custom layouts
└── themes/
    └── custom.kdl      # Custom themes
```

## General Settings

```kdl
// Mouse
mouse_mode true

// UI
pane_frames true
simplified_ui false
default_mode "normal"

// Copy/Paste
copy_on_select true
copy_command "pbcopy"              // macOS
// copy_command "xclip -selection clipboard"  // Linux X11
// copy_command "wl-copy"          // Linux Wayland

// Scrollback
scroll_buffer_size 10000

// Shell
default_shell "fish"

// Session
session_serialization true
pane_viewport_serialization false

// Layout and theme
default_layout "compact"
theme "catppuccin-mocha"

// Auto-attach
on_force_close "quit"
attach_to_session true

// Mirror sessions
mirror_session false
```

## Keybinding Modes

### Normal Mode (Default)

```kdl
keybinds {
    normal {
        // Mode switching
        bind "Ctrl g" { SwitchToMode "locked"; }
        bind "Ctrl p" { SwitchToMode "pane"; }
        bind "Ctrl t" { SwitchToMode "tab"; }
        bind "Ctrl n" { SwitchToMode "resize"; }
        bind "Ctrl s" { SwitchToMode "scroll"; }

        // Quick actions
        bind "Ctrl h" { MoveFocus "Left"; }
        bind "Ctrl l" { MoveFocus "Right"; }
        bind "Ctrl j" { MoveFocus "Down"; }
        bind "Ctrl k" { MoveFocus "Up"; }

        // Quit
        bind "Ctrl q" { Quit; }
    }
}
```

### Pane Mode

```kdl
pane {
    bind "Esc" { SwitchToMode "normal"; }
    bind "Ctrl c" { SwitchToMode "normal"; }

    // Navigation (vim-style)
    bind "h" { MoveFocus "Left"; }
    bind "l" { MoveFocus "Right"; }
    bind "j" { MoveFocus "Down"; }
    bind "k" { MoveFocus "Up"; }

    // Create panes
    bind "n" { NewPane; SwitchToMode "normal"; }
    bind "d" { NewPane "Down"; SwitchToMode "normal"; }
    bind "r" { NewPane "Right"; SwitchToMode "normal"; }

    // Close
    bind "x" { CloseFocus; SwitchToMode "normal"; }

    // Fullscreen
    bind "f" { ToggleFocusFullscreen; SwitchToMode "normal"; }

    // Rename
    bind "c" { SwitchToMode "renamepane"; }

    // Toggle frames
    bind "z" { TogglePaneFrames; SwitchToMode "normal"; }

    // Toggle floating
    bind "w" { ToggleFloatingPanes; SwitchToMode "normal"; }

    // Embed pane
    bind "e" { TogglePaneEmbedOrFloating; SwitchToMode "normal"; }
}
```

### Tab Mode

```kdl
tab {
    bind "Esc" { SwitchToMode "normal"; }
    bind "Ctrl c" { SwitchToMode "normal"; }

    // New/close
    bind "n" { NewTab; SwitchToMode "normal"; }
    bind "x" { CloseTab; SwitchToMode "normal"; }

    // Navigation
    bind "h" { GoToPreviousTab; }
    bind "l" { GoToNextTab; }
    bind "1" { GoToTab 1; SwitchToMode "normal"; }
    bind "2" { GoToTab 2; SwitchToMode "normal"; }
    bind "3" { GoToTab 3; SwitchToMode "normal"; }
    bind "4" { GoToTab 4; SwitchToMode "normal"; }
    bind "5" { GoToTab 5; SwitchToMode "normal"; }

    // Rename
    bind "r" { SwitchToMode "renametab"; }

    // Toggle tab bar
    bind "Tab" { ToggleTab; }
}
```

### Resize Mode

```kdl
resize {
    bind "Esc" { SwitchToMode "normal"; }
    bind "Ctrl c" { SwitchToMode "normal"; }

    // Vim-style
    bind "h" { Resize "Left"; }
    bind "j" { Resize "Down"; }
    bind "k" { Resize "Up"; }
    bind "l" { Resize "Right"; }

    // Fine control
    bind "=" { Resize "Increase"; }
    bind "-" { Resize "Decrease"; }
}
```

### Scroll Mode

```kdl
scroll {
    bind "Esc" { SwitchToMode "normal"; }
    bind "Ctrl c" { SwitchToMode "normal"; }

    // Navigation
    bind "j" { ScrollDown; }
    bind "k" { ScrollUp; }
    bind "d" { HalfPageScrollDown; }
    bind "u" { HalfPageScrollUp; }
    bind "f" { PageScrollDown; }
    bind "b" { PageScrollUp; }

    // Search
    bind "/" { Search "Down"; }
    bind "?" { Search "Up"; }
    bind "n" { SearchToggleOption "CaseSensitivity"; }
    bind "w" { SearchToggleOption "Wrap"; }
    bind "o" { SearchToggleOption "WholeWord"; }

    // Edges
    bind "g" { ScrollToTop; }
    bind "G" { ScrollToBottom; }
}
```

### Locked Mode

```kdl
locked {
    bind "Ctrl g" { SwitchToMode "normal"; }
}
```

## Available Actions

### Pane Actions

```kdl
NewPane                          // Create horizontal split
NewPane "Down"                   // Create below
NewPane "Right"                  // Create right
CloseFocus                       // Close focused pane
MoveFocus "Left"                 // Focus left pane
MoveFocus "Right"                // Focus right
MoveFocus "Up"                   // Focus up
MoveFocus "Down"                 // Focus down
ToggleFocusFullscreen            // Maximize/restore pane
TogglePaneFrames                 // Show/hide borders
ToggleFloatingPanes              // Toggle floating mode
TogglePaneEmbedOrFloating        // Embed/float pane
SwitchToMode "renamepane"        // Rename pane
```

### Tab Actions

```kdl
NewTab                           // Create new tab
CloseTab                         // Close current tab
GoToTab 1                        // Jump to tab number
GoToPreviousTab                  // Previous tab
GoToNextTab                      // Next tab
ToggleTab                        // Toggle tab bar
SwitchToMode "renametab"         // Rename tab
```

### Resize Actions

```kdl
Resize "Left"                    // Resize left
Resize "Right"                   // Resize right
Resize "Up"                      // Resize up
Resize "Down"                    // Resize down
Resize "Increase"                // Increase size
Resize "Decrease"                // Decrease size
```

### Scroll Actions

```kdl
ScrollDown                       // Scroll down one line
ScrollUp                         // Scroll up one line
PageScrollDown                   // Scroll down one page
PageScrollUp                     // Scroll up one page
HalfPageScrollDown               // Half page down
HalfPageScrollUp                 // Half page up
ScrollToTop                      // Jump to top
ScrollToBottom                   // Jump to bottom
Search "Down"                    // Search forward
Search "Up"                      // Search backward
SearchToggleOption "CaseSensitivity"
SearchToggleOption "Wrap"
SearchToggleOption "WholeWord"
```

### Session Actions

```kdl
SwitchToMode "session"           // Enter session mode
Detach                           // Detach from session
Quit                             // Quit Zellij
```

## Layout Examples

### Simple Two-Pane

```kdl
layout {
    pane split_direction="vertical" {
        pane size="60%"
        pane size="40%"
    }
}
```

### Development Layout

```kdl
layout {
    default_tab_template {
        pane size=1 borderless=true {
            plugin location="zellij:tab-bar"
        }
        children
        pane size=2 borderless=true {
            plugin location="zellij:status-bar"
        }
    }

    tab name="code" focus=true {
        pane split_direction="vertical" {
            pane size="70%"
            pane split_direction="horizontal" {
                pane
                pane
            }
        }
    }

    tab name="servers" {
        pane split_direction="horizontal" {
            pane command="npm" {
                args "run" "dev"
            }
            pane command="docker" {
                args "compose" "logs" "-f"
            }
        }
    }
}
```

### Multi-Tab Workspace

```kdl
layout {
    tab name="editor" focus=true {
        pane
    }

    tab name="terminal" {
        pane split_direction="horizontal" {
            pane size="50%"
            pane size="50%"
        }
    }

    tab name="monitoring" {
        pane split_direction="vertical" {
            pane command="htop"
            pane command="docker" {
                args "stats"
            }
        }
    }
}
```

### Complex Grid Layout

```kdl
layout {
    pane split_direction="vertical" {
        pane size="30%"
        pane split_direction="horizontal" {
            pane size="50%"
            pane split_direction="vertical" {
                pane size="50%"
                pane size="50%"
            }
        }
    }
}
```

## Pane Properties

```kdl
pane {
    // Direction
    split_direction="vertical"      // or "horizontal"

    // Size
    size="70%"                       // percentage
    size=20                          // fixed

    // Command
    command="htop"                   // executable
    args "arg1" "arg2"              // arguments

    // Behavior
    focus=true                       // initial focus
    borderless=true                  // no borders
    name="My Pane"                   // pane title

    // Working directory
    cwd "/path/to/dir"

    // Start suspended
    start_suspended=true
}
```

## Theme Structure

### Simple Theme

```kdl
themes {
    simple {
        fg "#cdd6f4"
        bg "#1e1e2e"
        black "#45475a"
        red "#f38ba8"
        green "#a6e3a1"
        yellow "#f9e2af"
        blue "#89b4fa"
        magenta "#f5c2e7"
        cyan "#94e2d5"
        white "#bac2de"
        orange "#fab387"
    }
}
```

### Detailed Theme with UI Components

```kdl
themes {
    detailed {
        // Base colors
        fg "#cdd6f4"
        bg "#1e1e2e"
        black "#45475a"
        red "#f38ba8"
        green "#a6e3a1"
        yellow "#f9e2af"
        blue "#89b4fa"
        magenta "#f5c2e7"
        cyan "#94e2d5"
        white "#bac2de"
        orange "#fab387"

        // Frame colors (RGB values)
        text_unselected {
            base 205 214 244
            background 30 30 46
        }

        text_selected {
            base 49 50 68
            background 205 214 244
        }

        ribbon_unselected {
            base 205 214 244
            background 88 91 112
        }

        ribbon_selected {
            base 49 50 68
            background 137 180 250
        }

        frame_unselected {
            base 88 91 112
            background 30 30 46
        }

        frame_selected {
            base 137 180 250
            background 30 30 46
        }

        exit_code_success {
            base 166 227 161
            background 30 30 46
        }

        exit_code_error {
            base 243 139 168
            background 30 30 46
        }
    }
}
```

## Popular Theme Color Schemes

### Catppuccin Mocha

```kdl
themes {
    catppuccin_mocha {
        fg "#cdd6f4"
        bg "#1e1e2e"
        black "#45475a"
        red "#f38ba8"
        green "#a6e3a1"
        yellow "#f9e2af"
        blue "#89b4fa"
        magenta "#f5c2e7"
        cyan "#94e2d5"
        white "#bac2de"
        orange "#fab387"
    }
}
```

### Nord

```kdl
themes {
    nord {
        fg "#d8dee9"
        bg "#2e3440"
        black "#3b4252"
        red "#bf616a"
        green "#a3be8c"
        yellow "#ebcb8b"
        blue "#81a1c1"
        magenta "#b48ead"
        cyan "#88c0d0"
        white "#e5e9f0"
        orange "#d08770"
    }
}
```

### Gruvbox Dark

```kdl
themes {
    gruvbox_dark {
        fg "#ebdbb2"
        bg "#282828"
        black "#282828"
        red "#cc241d"
        green "#98971a"
        yellow "#d79921"
        blue "#458588"
        magenta "#b16286"
        cyan "#689d6a"
        white "#a89984"
        orange "#d65d0e"
    }
}
```

## Useful Commands

```bash
# Setup
zellij setup --dump-config > ~/.config/zellij/config.kdl
zellij setup --check

# Launch with options
zellij --layout custom
zellij --layout https://example.com/layout.kdl
zellij options --theme nord
zellij options --default-mode locked

# Session management
zellij attach session-name
zellij list-sessions
zellij delete-session session-name
zellij delete-all-sessions

# Actions (from within Zellij)
zellij action new-pane
zellij action move-focus left
zellij action write 27  # Send Escape
```

## Environment Variables

```bash
# Config directory
export ZELLIJ_CONFIG_DIR="$HOME/.config/zellij"

# Config file
export ZELLIJ_CONFIG_FILE="$HOME/.config/zellij/custom.kdl"

# Auto-attach
export ZELLIJ_AUTO_ATTACH=true
export ZELLIJ_AUTO_EXIT=true
```

## Tips & Best Practices

1. **Start with defaults**: Generate config with `zellij setup --dump-config`
2. **Use modes**: Organize keybinds by context (pane, tab, resize, etc.)
3. **Layout reuse**: Create layouts for common workflows
4. **Theme consistency**: Match terminal theme with Zellij theme
5. **Minimal bindings**: Override only what you need
6. **Test layouts**: Use `zellij --layout` to test before setting as default
7. **Session names**: Use descriptive names for easy attachment
8. **Floating panes**: Great for temporary commands/notes
9. **Copy mode**: Use `copy_on_select` for efficiency
10. **Shell integration**: Enable for better directory inheritance
