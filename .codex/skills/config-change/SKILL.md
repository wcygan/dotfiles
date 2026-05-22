---
name: config-change
description: "Route dotfiles configuration changes to the right project-local skill. Use for fish, Ghostty, lazygit, Neovim, Starship, Zed, Zellij, or cross-platform config edits in this repository."
---

# Config Change Router

## Goal

Modify configuration files in this dotfiles repository through the specialized project skill that owns the relevant config area.

Success means the change follows the correct local conventions, preserves macOS, Ubuntu, and Fedora compatibility, and has a narrow verification command.

Stop when the requested config change is applied or the user has clarified which tool owns an ambiguous request.

## Route Map

- `fish-shell-config`: `config/fish/`, including `config.fish`, functions, abbreviations, prompts, and environment variables.
- `ghostty-config`: `config/ghostty/`, including themes, fonts, keybindings, and performance settings.
- `lazygit-config`: `config/git/lazygit/`, including `config.yml`, delta integration, themes, and keybindings.
- `nvim-config`: `config/nvim/`, including `init.lua`, plugins, LSP settings, and keymaps.
- `starship-config`: `config/starship.toml`, including prompt modules, presets, and performance.
- `zed-config`: `config/zed/`, including `settings.json`, `keymap.json`, themes, and agents.
- `zellij-config`: `config/zellij/`, including layouts, themes, keybindings, and KDL format.
- `cross-platform-guardian`: changes that affect more than one platform or risk OS-specific behavior.

## Workflow

1. Read the user's requested config change from the prompt.
2. Identify the affected config area from the route map.
3. Open the matching `.codex/skills/<skill-name>/SKILL.md` before editing.
4. Use multiple specialized skills when the change spans multiple config areas.
5. Include `cross-platform-guardian` when paths, shell startup, installed tools, file linking, or platform conditionals are involved.
6. Ask one concise clarifying question only when the owning tool cannot be inferred.

## Examples

- "add git alias for git log --oneline": use `fish-shell-config`.
- "change terminal font to JetBrains Mono": use `ghostty-config`.
- "add keybinding for split pane": clarify which tool if the prompt does not say Ghostty, Zellij, Neovim, or Zed.
- "update lazygit to use delta pager": use `lazygit-config`.
- "add TypeScript LSP to Neovim": use `nvim-config`.

## Constraints

- Keep config changes scoped to the requested tool.
- Preserve XDG Base Directory conventions when a tool supports them.
- Keep scripts and linking idempotent.
- Avoid hard-coded machine-specific paths.
- Update tests or docs when behavior changes.

## Completion

When finished, summarize:

- Files changed.
- Verification command and result.
- Rollback path, such as reverting a single config file or re-running the link script.
- Any follow-up config changes that are clearly implied by the request.
