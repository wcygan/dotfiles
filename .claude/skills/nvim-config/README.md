# Neovim Configuration Skill

Agent skill for configuring Neovim with Lua-based init files, plugin management, LSP, keymaps, and options.

## Overview

This skill enables Claude to intelligently configure your Neovim editor. Your dotfiles repository has an empty `config/nvim/` directory ready for configuration, which will be symlinked to `~/.config/nvim/` (XDG standard location).

## Skill Activation

The skill activates automatically when you mention:

- **Configuration:** "Set up my Neovim configuration"
- **Plugins:** "Add Telescope plugin to Neovim"
- **LSP:** "Configure rust-analyzer in Neovim"
- **Keymaps:** "Add keybinding for save in Neovim"
- **Options:** "Change tab size to 2 in Neovim"

**Trigger keywords:** neovim, nvim, init.lua, vim, plugin, LSP, keymap, configure, vimscript

## File Structure

```
.claude/skills/nvim-config/
├── SKILL.md              # Main skill instructions
├── REFERENCE.md          # Advanced configuration patterns
├── README.md             # This file
└── scripts/
    └── setup-nvim.sh     # Bootstrap script for initial setup
```

## Configuration Files

The skill manages Neovim configuration in:

**Primary location:** `config/nvim/` (symlinked to `~/.config/nvim/`)

**Recommended structure:**
```
config/nvim/
├── init.lua              # Main entry point
├── lua/
│   ├── config/
│   │   ├── options.lua   # Editor options
│   │   ├── keymaps.lua   # Keybindings
│   │   ├── autocmds.lua  # Autocommands
│   │   └── lazy.lua      # Plugin manager setup
│   └── plugins/
│       ├── lsp.lua       # LSP configuration
│       ├── treesitter.lua # Syntax highlighting
│       └── ...           # Other plugin configs
└── after/
    └── plugin/           # Plugin-specific overrides
```

## Quick Start

### Option 1: Automated Setup

Run the bootstrap script to create a complete configuration:

```bash
.claude/skills/nvim-config/scripts/setup-nvim.sh
```

This creates:
- Modular Lua configuration structure
- lazy.nvim plugin manager
- Basic plugins (colorscheme, treesitter)
- Essential keymaps and options

### Option 2: Manual Setup with Claude

Simply ask Claude:

- "Set up a basic Neovim configuration"
- "Create a modular Neovim config with LSP"
- "Initialize my Neovim configuration"

Claude will create the appropriate structure and files.

## Example Usage

### Initial Setup

**You:** "Set up my Neovim configuration with lazy.nvim and LSP support"

**Claude:** Creates init.lua, config modules, plugin specs, and LSP configuration.

### Add Plugin

**You:** "Add Telescope fuzzy finder to Neovim"

**Claude:** Creates `lua/plugins/telescope.lua` with configuration and keybindings.

### Configure LSP

**You:** "Set up gopls for Go development"

**Claude:** Adds gopls to Mason ensure_installed, creates server configuration with Go-specific settings.

### Modify Keybindings

**You:** "Add ctrl-s to save file in Neovim"

**Claude:** Edits `lua/config/keymaps.lua` to add the keybinding.

### Change Options

**You:** "Set tab size to 2 spaces in Neovim"

**Claude:** Modifies `lua/config/options.lua` to update tabstop and shiftwidth.

## Features

### 1. Configuration Management

- **Editor options** (line numbers, tabs, search behavior)
- **UI settings** (colors, signs, statusline)
- **Performance tuning** (updatetime, timeoutlen)
- **File handling** (backup, swap, undo)

### 2. Plugin Management (lazy.nvim)

- Lazy loading by command, event, filetype, keys
- Plugin dependencies and build steps
- Automatic updates and version locking
- Performance optimization

### 3. Language Server Protocol

- Mason.nvim for LSP installation
- Server-specific configurations
- LSP keybindings and capabilities
- Diagnostic display and navigation

### 4. Keybinding System

- Mode-specific mappings (normal, insert, visual)
- Leader key patterns
- Descriptive keybindings for which-key
- Buffer and window navigation

### 5. Autocommands

- Highlight on yank
- Restore cursor position
- Format on save
- Filetype-specific behaviors

## Essential Plugins

The skill knows how to configure these common plugins:

**Core:**
- lazy.nvim (plugin manager)
- nvim-lspconfig (LSP)
- nvim-cmp (completion)
- nvim-treesitter (syntax)

**UI:**
- Telescope (fuzzy finder)
- neo-tree (file explorer)
- lualine (statusline)
- which-key (keybinding hints)

**Development:**
- gitsigns (git integration)
- Comment.nvim (commenting)
- nvim-autopairs (auto pairs)

**Language-Specific:**
- rust-tools (Rust)
- go.nvim (Go)
- typescript-tools (TypeScript)

## Current State

**Configuration:** Empty (ready for initial setup)

**Location:** `config/nvim/` (will be symlinked to `~/.config/nvim/`)

**Recommended approach:** Modern Lua-based configuration with modular structure

## Configuration Patterns

### Minimal (One File)

Single `init.lua` with all configuration inline:

```lua
vim.g.mapleader = " "
vim.opt.number = true
vim.opt.tabstop = 4
-- ... rest of config
```

### Modular (Recommended)

Separate files for different concerns:

- `init.lua` - Entry point, loads modules
- `lua/config/options.lua` - Editor options
- `lua/config/keymaps.lua` - Keybindings
- `lua/config/autocmds.lua` - Autocommands
- `lua/config/lazy.lua` - Plugin manager
- `lua/plugins/*.lua` - Individual plugin specs

### Per-Plugin Files

Each plugin gets its own file in `lua/plugins/`:

```lua
-- lua/plugins/telescope.lua
return {
  "nvim-telescope/telescope.nvim",
  dependencies = { "nvim-lua/plenary.nvim" },
  keys = {
    { "<leader>ff", "<cmd>Telescope find_files<cr>" },
  },
}
```

## Best Practices

1. **Lua over Vimscript** - Use Lua for new configurations
2. **Modular structure** - Separate concerns into different files
3. **Lazy loading** - Load plugins on demand for faster startup
4. **LSP-first** - Use built-in LSP instead of language-specific plugins
5. **Descriptive keymaps** - Always include descriptions for discoverability
6. **XDG compliance** - Use standard directory locations
7. **Persistent undo** - Enable undofile for history across sessions

## Troubleshooting

### Check Configuration Location

```vim
:echo stdpath('config')
```

Should show `~/.config/nvim`

### Reload Configuration

```vim
:source $MYVIMRC
:Lazy sync
```

### Check Plugin Status

```vim
:Lazy                    " Plugin manager UI
:checkhealth             " System diagnostics
:LspInfo                 " LSP server status
:Mason                   " LSP installer
```

### Verify Symlink

```bash
ls -la ~/.config/nvim
```

Should point to `dotfiles/config/nvim`

### Common Issues

**Plugins not loading:**
- Check lazy.nvim is bootstrapped in `lua/config/lazy.lua`
- Run `:Lazy sync` to install plugins
- Check for errors with `:messages`

**LSP not working:**
- Verify server installed: `:Mason`
- Check server status: `:LspInfo`
- Restart server: `:LspRestart`

**Keybindings not working:**
- Check leader key set before loading plugins
- Verify keymap file loaded in init.lua
- Use `:map <key>` to see current mappings

## Resources

- **Skill Instructions:** [SKILL.md](./SKILL.md)
- **Advanced Patterns:** [REFERENCE.md](./REFERENCE.md)
- **Setup Script:** [scripts/setup-nvim.sh](./scripts/setup-nvim.sh)
- [Neovim Documentation](https://neovim.io/doc/)
- [lazy.nvim](https://github.com/folke/lazy.nvim)
- [nvim-lspconfig](https://github.com/neovim/nvim-lspconfig)

## Next Steps

1. **Bootstrap configuration:**
   ```bash
   .claude/skills/nvim-config/scripts/setup-nvim.sh
   ```

2. **Open Neovim:**
   ```bash
   nvim
   ```
   lazy.nvim will auto-install plugins on first launch

3. **Add more plugins:**
   Create files in `lua/plugins/` or ask Claude to add them

4. **Configure LSP:**
   Ask Claude to set up language servers for your languages

5. **Customize keybindings:**
   Edit `lua/config/keymaps.lua` or ask Claude to add bindings

## Testing the Skill

Try these requests to test the skill:

1. "Set up my Neovim configuration"
2. "Add Telescope fuzzy finder"
3. "Configure rust-analyzer LSP"
4. "Change tab size to 2"
5. "Add keybinding for format document"
6. "Show my current Neovim keymaps"

---

**Note:** This skill respects your dotfiles workflow. All changes are git-tracked, atomic, and reversible. Configuration is portable across machines via symlinks.
