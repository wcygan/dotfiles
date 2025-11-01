# Neovim Configuration

Modern Neovim configuration with Lua, lazy.nvim plugin manager, and sensible defaults.

## Structure

```
config/nvim/
├── init.lua              # Entry point
├── lua/
│   ├── config/
│   │   ├── options.lua   # Editor options (tabs, UI, etc.)
│   │   ├── keymaps.lua   # Keybindings
│   │   ├── autocmds.lua  # Autocommands
│   │   └── lazy.lua      # Plugin manager setup
│   └── plugins/
│       ├── colorscheme.lua # Tokyo Night theme
│       └── treesitter.lua  # Syntax highlighting
└── README.md
```

## Features

- **Leader key:** Space
- **Line numbers:** Relative and absolute
- **Tabs:** 4 spaces
- **Smart search:** Case-insensitive unless uppercase used
- **Persistent undo:** Enabled
- **Clipboard:** System clipboard integration

## Keybindings

### Window Navigation
- `Ctrl+h/j/k/l` - Move between windows
- `Ctrl+Up/Down/Left/Right` - Resize windows

### Buffer Navigation
- `Shift+h` - Previous buffer
- `Shift+l` - Next buffer

### Leader Commands
- `<leader>w` - Save file
- `<leader>q` - Quit
- `<leader>e` - Show diagnostics

### Editing
- `Alt+j/k` - Move lines up/down
- `<` / `>` in visual mode - Indent (stays in visual mode)
- `[d` / `]d` - Previous/next diagnostic

## Plugins

Managed by [lazy.nvim](https://github.com/folke/lazy.nvim):

- **tokyonight.nvim** - Color scheme
- **nvim-treesitter** - Advanced syntax highlighting

Plugins auto-install on first launch.

## Setup

The configuration is symlinked from dotfiles:
```bash
~/.config/nvim -> ~/Development/dotfiles/config/nvim
```

## Adding Plugins

Create a new file in `lua/plugins/`:

```lua
-- lua/plugins/myplugin.lua
return {
  "author/plugin-name",
  config = function()
    -- Setup here
  end,
}
```

## Commands

- `:Lazy` - Plugin manager UI
- `:checkhealth` - Check Neovim health
- `:TSUpdate` - Update Treesitter parsers

## Fish Shell Integration

The following aliases automatically use Neovim:
- `vim` → `nvim`
- `vi` → `nvim`
- `nv` → `nvim`
