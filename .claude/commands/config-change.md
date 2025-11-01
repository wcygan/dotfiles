---
description: Intelligently modify config files using specialized skills
---

You are helping the user modify configuration files in this dotfiles repository.

**User request:** $ARGUMENTS

# Available Configuration Skills

Based on the config change requested, activate the appropriate specialized skill:

- **fish-shell-config** → `config/fish/` changes (config.fish, functions, abbreviations, prompts, env vars)
- **ghostty-config** → `config/ghostty/` changes (themes, fonts, keybindings, performance)
- **lazygit-config** → `config/git/lazygit/` changes (config.yml, delta integration, themes, keybindings)
- **nvim-config** → `config/nvim/` changes (init.lua, plugins, LSP, keymaps)
- **starship-config** → `config/starship.toml` changes (prompt modules, presets, performance)
- **zed-config** → `config/zed/` changes (settings.json, keymap.json, themes, agents)
- **zellij-config** → `config/zellij/` changes (layouts, themes, keybindings, KDL format)
- **cross-platform-guardian** → Changes affecting multiple platforms (macOS/Ubuntu/Fedora compatibility)

# Execution Strategy

1. **Analyze the request**: Determine which config area(s) are affected by `$ARGUMENTS`
2. **Activate appropriate skill(s)**: Use the Skill tool to invoke the matching skill
3. **If multiple configs affected**: Use cross-platform-guardian to ensure compatibility
4. **If unclear which skill**: Ask the user to clarify which config they want to modify

# Examples

**Example 1**: User runs `/config-change add git alias for git log --oneline`
→ Activate `fish-shell-config` skill (git aliases go in fish config)

**Example 2**: User runs `/config-change change terminal font to JetBrains Mono`
→ Activate `ghostty-config` skill

**Example 3**: User runs `/config-change add keybinding for split pane`
→ Ask user: "Which tool? (ghostty, zellij, nvim, zed)"

**Example 4**: User runs `/config-change update lazygit to use delta pager`
→ Activate `lazygit-config` skill

**Example 5**: User runs `/config-change add typescript LSP to neovim`
→ Activate `nvim-config` skill

# Important Constraints

- **Never modify configs directly** without using the appropriate skill
- **Always check cross-platform implications** (macOS, Ubuntu, Fedora)
- **Follow XDG Base Directory conventions** (configs in `~/.config/` when possible)
- **Maintain idempotency** (changes should be safe to apply multiple times)
- **Test changes** after applying (suggest appropriate test command)

# Decision Tree

```
Is request about:
├─ Fish shell (aliases, functions, prompts)? → fish-shell-config
├─ Ghostty terminal settings? → ghostty-config
├─ Lazygit config? → lazygit-config
├─ Neovim editor? → nvim-config
├─ Starship prompt? → starship-config
├─ Zed editor? → zed-config
├─ Zellij multiplexer? → zellij-config
├─ Multi-platform compatibility? → cross-platform-guardian
└─ Unclear? → Ask user for clarification
```

# After Skill Execution

Once the skill completes:
1. **Summarize changes made** (which files modified)
2. **Provide test command** (how to verify the change works)
3. **Mention rollback** (how to undo if needed)
4. **Suggest related changes** (if applicable)

Now proceed based on the user's request: **$ARGUMENTS**
