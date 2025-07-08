---
sidebar_position: 2
---

# Editor Configuration

The dotfiles repository includes configuration for several popular editors.

## Visual Studio Code

### Keybindings

Custom keybindings optimized for productivity:

```json
{
  "key": "cmd+k cmd+t",
  "command": "workbench.action.terminal.toggleTerminal"
}
```

### Settings

Development-focused settings are included for:
- Auto-save configuration
- Format on save
- Extension recommendations
- Theme preferences

## Zed

### Keybindings

Custom Zed keybindings for common operations:

```json
{
  "context": "Editor",
  "bindings": {
    "cmd-d": "editor::DuplicateLine",
    "cmd-shift-k": "editor::DeleteLine"
  }
}
```

### Tasks

Zed task definitions for running common commands:
- Development server
- Test execution
- Build processes

## Cursor

### Configuration

Cursor-specific settings that enhance the AI-powered development experience:
- Custom keybindings
- AI interaction preferences
- Code completion settings

## Vim

### .vimrc Configuration

Essential Vim settings for modern development:

```vim
" Enable syntax highlighting
syntax on

" Show line numbers
set number

" Enable mouse support
set mouse=a

" Set tabs to 2 spaces
set tabstop=2
set shiftwidth=2
set expandtab
```

## Installation

Editor configurations are automatically installed when you run:

```bash
deno task install
```

## Customization

### Adding Personal Settings

Create editor-specific configuration files in your home directory that won't be overwritten:

- VS Code: `~/.vscode/settings.json`
- Zed: `~/.config/zed/settings.json`
- Vim: Use `~/.vimrc.local` and source it from `.vimrc`

### Extending Configurations

The provided configurations serve as a base. You can:

1. Override specific settings
2. Add custom keybindings
3. Install additional plugins/extensions
4. Create workspace-specific configurations

## Integration with Claude Code

Many editor configurations include integrations with Claude Code:

- Custom keybindings for Claude commands
- Task definitions for common workflows
- Settings optimized for AI-assisted development