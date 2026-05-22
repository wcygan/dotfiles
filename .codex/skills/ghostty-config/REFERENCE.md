# Ghostty Configuration Reference

Quick reference for common Ghostty configuration options and patterns.

## Configuration File Format

Ghostty uses INI-style format:
```ini
key = value
section.key = value
```

Comments start with `#`.

## Font Configuration

```ini
# Basic font setup
font-family = "JetBrains Mono"
font-size = 13

# Font variants
font-family-bold = "JetBrains Mono Bold"
font-family-italic = "JetBrains Mono Italic"
font-family-bold-italic = "JetBrains Mono Bold Italic"

# Disable synthetic styles
font-synthetic-style = false

# OpenType features
font-feature = -calt  # disable ligatures
font-feature = +ss01  # enable stylistic set 1

# Variable font axes
font-variation = wght=450
font-variation = slnt=-8
```

**Popular fonts for terminals:**
- JetBrains Mono (ligatures, excellent Unicode)
- Fira Code (ligatures)
- Iosevka (compact, customizable)
- Cascadia Code (Microsoft, ligatures)
- Monaco (macOS classic)

## Theme & Colors

### Built-in Themes

```ini
# Catppuccin variants
theme = catppuccin-mocha    # dark
theme = catppuccin-macchiato
theme = catppuccin-frappe
theme = catppuccin-latte    # light

# Other popular themes
theme = solarized-dark
theme = solarized-light
theme = gruvbox-dark
theme = gruvbox-light
theme = nord
theme = dracula
theme = one-dark
```

### Custom Colors

```ini
background = #1e1e2e
foreground = #cdd6f4
cursor-color = #f5e0dc
cursor-text = #1e1e2e
selection-background = #585b70
selection-foreground = #cdd6f4

# 16-color palette
palette = 0=#45475a
palette = 1=#f38ba8
palette = 2=#a6e3a1
palette = 3=#f9e2af
palette = 4=#89b4fa
palette = 5=#f5c2e7
palette = 6=#94e2d5
palette = 7=#bac2de
palette = 8=#585b70
palette = 9=#f38ba8
palette = 10=#a6e3a1
palette = 11=#f9e2af
palette = 12=#89b4fa
palette = 13=#f5c2e7
palette = 14=#94e2d5
palette = 15=#a6adc8
```

### Window Appearance

```ini
# Transparency
background-opacity = 0.95          # 1=opaque, 0=transparent
background-blur-radius = 20        # macOS/KDE only

# Window decorations
window-decoration = true           # titlebar and borders
window-padding-x = 4               # horizontal padding (pixels)
window-padding-y = 4               # vertical padding (pixels)

# Unfocused appearance
unfocused-split-opacity = 0.7
unfocused-split-fill = #313244
```

## Keybinding Actions Reference

### Window & Tab Management

```ini
keybind = super+n=new_window
keybind = super+t=new_tab
keybind = super+w=close_surface
keybind = super+shift+w=close_all_windows
keybind = super+q=quit

# Tab navigation
keybind = super+1=goto_tab:1
keybind = super+2=goto_tab:2
keybind = ctrl+tab=next_tab
keybind = ctrl+shift+tab=previous_tab

# Window navigation
keybind = super+shift+[=previous_window
keybind = super+shift+]=next_window
```

### Split Management

```ini
# Create splits
keybind = super+d=new_split:right
keybind = super+shift+d=new_split:down
keybind = super+shift+enter=new_split:auto

# Navigate splits (vim-style)
keybind = ctrl+h=goto_split:left
keybind = ctrl+j=goto_split:bottom
keybind = ctrl+k=goto_split:top
keybind = ctrl+l=goto_split:right

# Navigate splits (arrow keys)
keybind = ctrl+left=goto_split:left
keybind = ctrl+down=goto_split:bottom
keybind = ctrl+up=goto_split:top
keybind = ctrl+right=goto_split:right

# Resize splits
keybind = ctrl+shift+left=resize_split:left,10
keybind = ctrl+shift+down=resize_split:down,10
keybind = ctrl+shift+up=resize_split:up,10
keybind = ctrl+shift+right=resize_split:right,10

# Equalize splits
keybind = ctrl+shift+e=equalize_splits

# Toggle zoom
keybind = ctrl+shift+z=toggle_split_zoom
```

### Copy/Paste & Selection

```ini
keybind = super+c=copy_to_clipboard
keybind = super+v=paste_from_clipboard
keybind = super+shift+c=copy_to_selection
keybind = super+shift+v=paste_from_selection

# Copy without formatting
keybind = super+shift+alt+c=copy_to_clipboard:plain

# Select all
keybind = super+a=select_all
```

### Font Size

```ini
keybind = super+plus=increase_font_size:1
keybind = super+minus=decrease_font_size:1
keybind = super+0=reset_font_size
```

### Scrollback & Search

```ini
keybind = shift+page_up=scroll_page_up
keybind = shift+page_down=scroll_page_down
keybind = super+home=scroll_to_top
keybind = super+end=scroll_to_bottom

# Search
keybind = super+f=toggle_inspector
```

### Configuration & Debug

```ini
keybind = super+comma=reload_config
keybind = ctrl+shift+comma=open_config
keybind = super+shift+i=inspector:toggle
```

### Quick Terminal (Dropdown)

```ini
keybind = global:super+grave=toggle_quick_terminal
keybind = global:super+shift+grave=new_window
```

### Text Actions

```ini
# Send literal text (Zig string syntax)
keybind = ctrl+a=text:hello world
keybind = ctrl+u=text:\x15          # Ctrl-U

# Send CSI sequences
keybind = ctrl+shift+up=csi:A       # cursor up

# Send escape sequences
keybind = alt+d=esc:d               # delete word forward
```

### Special Actions

```ini
# Ignore key completely
keybind = ctrl+s=ignore

# Unbind previous binding
keybind = ctrl+shift+n=unbind

# Toggle fullscreen
keybind = super+ctrl+f=toggle_fullscreen

# Toggle tab bar
keybind = super+shift+t=toggle_tab_overview
```

## Keybind Prefixes

```ini
# Global (system-wide, macOS only)
keybind = global:super+shift+t=new_window

# All surfaces (every terminal)
keybind = all:ctrl+shift+r=reload_config

# Unconsumed (pass through to program)
keybind = unconsumed:ctrl+a=reload_config

# Performable (only consume if action can execute)
keybind = performable:super+c=copy_to_clipboard

# Combine prefixes
keybind = global:unconsumed:ctrl+space=text:\x00
```

## Shell Integration

```ini
# Auto-detect shell capabilities
shell-integration = detect

# Available features
shell-integration-features = cursor,sudo,title,no-cursor,no-sudo,no-title

# Custom shell
command = /usr/bin/fish
command = /bin/bash --login

# Environment variables
env = EDITOR=nvim
env = TERM=xterm-256color
env = PATH=/custom/path:$PATH
```

## Window Behavior

```ini
# Size and position
window-width = 100              # columns
window-height = 30              # rows
# OR
window-width = 1024px           # pixels
window-height = 768px

# Initial position
initial-window-position-x = center
initial-window-position-y = center

# State persistence
window-save-state = default     # save size/position
window-inherit-working-directory = true
window-inherit-font-size = true

# New tab behavior
window-new-tab-position = current  # or "end"
```

## Quick Terminal Configuration

```ini
# Toggle behavior
keybind = global:super+grave=toggle_quick_terminal

# Position and size
quick-terminal-position = top       # top, bottom, left, right
quick-terminal-screen = main        # main or current
quick-terminal-animation-duration = 0.2

# Size (percentage or pixels)
quick-terminal-size = 50%           # half screen
quick-terminal-size = 400px         # fixed pixels
```

## Performance Settings

```ini
# Scrollback buffer
scrollback-limit = 10000            # lines (memory-based)

# Mouse
mouse-scroll-multiplier = 3
mouse-hide-while-typing = false
mouse-shift-capture = true          # shift for mouse selection

# Selection
copy-on-select = clipboard          # or "selection" or "false"
click-repeat-interval = 0.5         # seconds
```

## macOS-Specific

```ini
# macOS native tabs
macos-non-native-fullscreen = false
macos-option-as-alt = true
macos-window-shadow = true
macos-titlebar-style = native       # or "transparent", "hidden"

# macOS keybinds
keybind = super+h=hide_window
keybind = super+m=minimize_window
```

## Linux-Specific

```ini
# X11/Wayland
linux-cgroup = true                 # enable cgroups for cleanup
gtk-single-instance = true
gtk-titlebar = true
gtk-wide-tabs = true
```

## Useful Debugging Commands

```bash
# List all default keybindings
ghostty +list-keybinds --default

# List current keybindings
ghostty +list-keybinds

# Validate config
ghostty +validate-config

# Show version and features
ghostty --version
ghostty +list-features
```

## Example Complete Configs

### Minimal Config

```ini
font-family = "JetBrains Mono"
font-size = 13
theme = catppuccin-mocha
shell-integration = detect
copy-on-select = clipboard
```

### Power User Config

```ini
# Font
font-family = "JetBrains Mono"
font-size = 13
font-feature = -calt

# Theme
theme = catppuccin-mocha
background-opacity = 0.95
background-blur-radius = 20

# Window
window-padding-x = 4
window-padding-y = 4
window-save-state = default
window-inherit-working-directory = true

# Shell
shell-integration = detect
shell-integration-features = cursor,sudo,title
command = /usr/bin/fish

# Behavior
copy-on-select = clipboard
scrollback-limit = 10000
mouse-scroll-multiplier = 3

# Vim-style split navigation
keybind = ctrl+h=goto_split:left
keybind = ctrl+j=goto_split:bottom
keybind = ctrl+k=goto_split:top
keybind = ctrl+l=goto_split:right

# Quick terminal
keybind = global:super+grave=toggle_quick_terminal
quick-terminal-position = top
quick-terminal-size = 50%

# Font sizing
keybind = super+plus=increase_font_size:1
keybind = super+minus=decrease_font_size:1
keybind = super+0=reset_font_size
```

## Important Notes

1. **Runtime changes**: Most settings only affect new terminals/windows
2. **Config reload**: `reload_config` action or restart Ghostty
3. **Physical keys**: Case-sensitive W3C codes (e.g., `KeyA` not `keya`)
4. **Priority**: Physical keys match before Unicode codepoints
5. **Global keybinds**: macOS only, requires accessibility permissions
6. **Opacity**: Fully opaque = 1.0, fully transparent = 0.0
7. **Theme files**: Can be absolute paths or relative to config dir
