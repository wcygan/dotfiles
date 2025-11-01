# Zed Configuration Skill

Agent skill for configuring Zed editor settings, keybindings, language servers, and AI agents.

## Overview

This skill enables Claude to intelligently modify your Zed editor configuration. Since your dotfiles repository has symlinked the global Zed configuration (`config/zed/` → `~/.config/zed/`), all changes made by this skill apply globally to your Zed installation.

## Skill Activation

The skill activates automatically when you mention:

- **Settings changes:** "Change my Zed theme to Tokyo Night"
- **Keybindings:** "Add a keybinding for cmd-r to rename"
- **Language servers:** "Configure rust-analyzer with inlay hints"
- **Formatters:** "Set up Prettier for JavaScript"
- **AI agents:** "Configure Claude Code as external agent"

**Trigger keywords:** zed, editor, settings, keybindings, keymap, LSP, language server, theme, agent, configure

## File Structure

```
.claude/skills/zed-config/
├── SKILL.md              # Main skill instructions
├── REFERENCE.md          # Advanced configuration reference
├── README.md             # This file
└── scripts/
    └── validate-config.sh # JSON validation utility
```

## Configuration Files

The skill manages two primary configuration files:

- **`config/zed/settings.json`** - Editor settings, themes, LSP, languages
- **`config/zed/keymap.json`** - Custom keybindings

## Example Usage

### Change Theme

**You:** "Switch Zed to dark mode with Tokyo Night theme"

**Claude:** Reads `settings.json`, edits the theme configuration, applies changes.

### Add Keybinding

**You:** "Add cmd-3 to open Claude Code agent"

**Claude:** Reads `keymap.json`, adds binding to the bindings array.

### Configure Language Server

**You:** "Set up gopls for Go with inlay hints enabled"

**Claude:** Adds gopls configuration under `lsp` section, configures Go language settings.

### Format on Save

**You:** "Enable format on save for Python using ruff"

**Claude:** Configures Python language settings with ruff formatter.

## Features

### 1. Settings Management

- Theme and appearance (light/dark, fonts, icons)
- Editor behavior (autosave, soft wrap, line length)
- Terminal configuration
- Tab settings
- Git integration

### 2. Language Server Configuration

- Multi-server setups per language
- Initialization options
- Custom binary paths
- Inlay hints and code actions
- Format on save

### 3. Language-Specific Settings

- Per-language tab size, formatters
- External formatters (Prettier, Black, etc.)
- Language server prioritization
- Format on save behavior

### 4. Keybinding Customization

- Context-aware bindings (Editor, Terminal, Workspace)
- Key sequences (e.g., `cmd-k cmd-s`)
- Action arguments
- Disable default bindings

### 5. AI Agent Configuration

- External agents (Claude Code, Gemini CLI)
- Agent profiles and tools
- Default models
- Environment variables

## Validation

After modifications, validate configuration:

```bash
./claude/skills/zed-config/scripts/validate-config.sh
```

This checks JSON syntax in both settings and keymap files.

## Current Configuration Summary

**Base Keymap:** JetBrains

**Configured Languages:**
- **Python:** ty + ruff LSP, format on save
- **TypeScript/TSX:** Deno LSP (disables default TS servers)

**Configured LSP Servers:**
- Deno (enabled)
- Rust Analyzer (inlay hints, analyzer target dir)
- Ruff (Python)

**Current Theme:**
- Mode: System
- Light: One Light
- Dark: Zedokai

**Agent Settings:**
- Default model: Google Gemini 2.5 Pro
- Always allow tool actions: true
- Sound on completion: true

## Best Practices

1. **Incremental changes** - Modify one setting at a time
2. **Read first** - Always read current config before editing
3. **Preserve structure** - Keep JSON formatting and comments
4. **Context-aware keybindings** - Use appropriate context for shortcuts
5. **Test after changes** - Zed applies most changes immediately

## Troubleshooting

### Changes Not Applying

- Verify symlink exists: `ls -la ~/.config/zed`
- Check Zed is reading correct config location
- Some LSP changes require server restart

### Invalid JSON

- Zed supports `//` comments
- Use validation script to check syntax
- Check for missing commas or braces

### LSP Issues

- Verify language server binary installed
- Check initialization_options structure
- View LSP logs in Zed: `lsp: show logs`

### Keybinding Conflicts

- Check base keymap conflicts
- Use `null` to disable conflicting bindings
- Test in correct context (Editor vs Terminal)

## Resources

- [SKILL.md](./SKILL.md) - Main skill instructions
- [REFERENCE.md](./REFERENCE.md) - Advanced configuration patterns
- [Zed Documentation](https://zed.dev/docs)
- [Configuring Zed](https://zed.dev/docs/configuring-zed)
- [Key Bindings Guide](https://zed.dev/docs/key-bindings)

## Notes

- Configuration is **global** (symlinked from dotfiles)
- Changes take effect immediately (no restart needed for most settings)
- Supports extended JSON with `//` comments
- Base keymap: JetBrains (affects default shortcuts)
