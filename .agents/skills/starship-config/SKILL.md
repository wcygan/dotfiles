---
name: starship-config
description: "Configure and optimize Starship cross-shell prompt with presets, custom modules, and performance tuning. Use when setting up Starship, creating prompt configs, customizing prompt appearance, or troubleshooting prompt issues. Keywords: starship, prompt, shell prompt, PS1, starship.toml, preset, prompt config, shell theme"
---

# Starship Configuration Manager

Manages complete Starship prompt configuration lifecycle including setup, customization, and optimization.

## Instructions

### 1. Understand Context

Check project structure:
- **Config location**: `config/starship.toml` (symlinked to `~/.config/starship.toml`)
- **Existing config**: Read current `starship.toml` if present
- **Shell integration**: Check `config/fish/conf.d/30-starship.fish` for hook
- **Nix package**: Verify starship in `flake.nix`

### 2. Configuration Operations

#### Setup New Config

```toml
# Minimal starting point
format = """
$username\
$hostname\
$directory\
$git_branch\
$git_status\
$cmd_duration\
$line_break\
$character"""

[character]
success_symbol = "[➜](bold green)"
error_symbol = "[➜](bold red)"

[directory]
truncation_length = 3
truncate_to_repo = true
```

#### Apply Preset

Available presets: `nerd-font-symbols`, `pure-preset`, `pastel-powerline`, `tokyo-night`, `gruvbox-rainbow`

```bash
# Preview a preset before selecting sections for config/starship.toml
starship preset nerd-font-symbols
```

#### Custom Module Configuration

Common modules to configure:

**Language/Runtime:**
```toml
[golang]
symbol = "🐹 "
format = "via [$symbol($version )]($style)"

[rust]
symbol = "🦀 "
format = "via [$symbol($version )]($style)"

[nodejs]
symbol = "⬢ "
format = "via [$symbol($version )]($style)"

[deno]
symbol = "🦕 "
format = "via [$symbol($version )]($style)"
```

**Git:**
```toml
[git_branch]
symbol = "🌱 "
format = "on [$symbol$branch]($style) "

[git_status]
conflicted = "🏳"
ahead = "⇡${count}"
behind = "⇣${count}"
diverged = "⇕⇡${ahead_count}⇣${behind_count}"
untracked = "🤷"
stashed = "📦"
modified = "📝"
staged = '[++\($count\)](green)'
renamed = "👅"
deleted = "🗑"
```

**Performance:**
```toml
[cmd_duration]
min_time = 500
format = "took [$duration](bold yellow)"

[directory]
read_only = " 🔒"
```

#### Context-Aware Variables

```toml
# Show Kubernetes context when kubectl available
[kubernetes]
disabled = false
format = 'on [⛵ ($context \($namespace\))](dimmed green) '

# Show AWS profile
[aws]
format = 'on [$symbol($profile )]($style)'
symbol = "☁️  "

# Show Docker context
[docker_context]
format = "via [🐋 $context](blue bold)"
```

### 3. Performance Optimization

#### Disable Expensive Modules

```toml
# Disable modules in large repos
[package]
disabled = true

[nodejs]
disabled = true  # Only if not a Node project

# Timeout protection
[cmd_duration]
min_time = 500
show_milliseconds = false

[git_status]
disabled = false
# Limit git operations in large repos
ahead_behind_limit = 1000
```

#### Scan Timeout Configuration

```toml
scan_timeout = 30  # ms, default is 30

[directory]
scan_timeout = 10
```

### 4. Verify the tracked configuration

From the repository root, parse the TOML and render the prompt with the file
you edited. Choose a directory and command status that exercise the changed
module.

```sh
python3 -c 'import tomllib; tomllib.load(open("config/starship.toml", "rb"))'
STARSHIP_CONFIG="$PWD/config/starship.toml" starship prompt
```

### 5. Troubleshooting

**Prompt not appearing:**
- Check shell integration: `config/fish/conf.d/30-starship.fish`
- Verify: `starship init fish | source`
- Confirm starship installed: `type -q starship`

**Slow prompt:**
- Enable timings: `starship timings`
- Disable expensive modules
- Increase scan timeout
- Check git status on large repos

**Modules missing:**
- Verify symbols/fonts: Nerd Font required
- Check module requirements (e.g., `kubectl` for kubernetes module)
- Review `disabled = false` settings

**Config not loading:**
- Check config path: `echo $STARSHIP_CONFIG` (should be unset or correct path)
- Verify symlink: `ls -la ~/.config/starship.toml`
- Parse and render the tracked file using the checks above.

### 6. Finish the change

Report which module changed and which prompt output you checked. If the prompt
rendered from the tracked file differs from the running shell, inspect the
Fish initialization and the resolved host link. For a link repair, follow
[dotfiles-operations](../dotfiles-operations/SKILL.md). Commit only when the
user has authorized a commit.

## Module Priority Guide

**Essential modules** (always include):
- `character` - prompt symbol
- `directory` - current path
- `git_branch`, `git_status` - git info
- `cmd_duration` - command timing

**Language modules** (include based on project):
- Deno/Node projects: `deno`, `nodejs`
- Go projects: `golang`
- Rust projects: `rust`
- Java projects: `java`

**Context modules** (optional):
- `kubernetes` - if using kubectl
- `docker_context` - if using Docker
- `aws` - if using AWS CLI

**Avoid in performance-critical environments:**
- `package` - slow in large node_modules
- Heavy git status in monorepos

## Reference Documentation

- Official config: https://starship.rs/config/
- Advanced config: https://starship.rs/advanced-config/
- Presets gallery: https://starship.rs/presets/

## Project Context

This is a Nix-based dotfiles repository:
- Starship installed via `flake.nix`
- Config lives in `config/starship.toml`
- Symlinked to `~/.config/starship.toml` by `src/dotfiles_setup/links.py`
- Fish shell integration in `config/fish/conf.d/30-starship.fish`
- Cross-platform support: macOS, Ubuntu, Fedora
