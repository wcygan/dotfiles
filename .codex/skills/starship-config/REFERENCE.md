# Starship Configuration Reference

Detailed guide for advanced Starship customization and optimization.

## Configuration File Structure

```toml
# config/starship/starship.toml

# Global settings
format = "$all"           # Order of modules
scan_timeout = 30         # ms to scan for version info
command_timeout = 500     # ms for command execution
add_newline = true        # Blank line before prompt

# Individual module configuration
[module_name]
disabled = false          # Enable/disable module
symbol = "🚀 "           # Icon to display
style = "bold green"      # Color and formatting
format = "via [$symbol]($style) "  # Template string

# Custom commands
[[custom.module_name]]
command = "echo foo"      # Command to run
when = true              # Condition to show
```

## Format String Syntax

### Variables

```toml
format = "[$symbol$version]($style) "
```

- `$variable` - Insert variable value
- `${variable}` - Alternative syntax
- `$style` - Apply configured style
- `\$` - Literal dollar sign

### Style Strings

```toml
style = "bold green"
style = "fg:blue bg:yellow"
style = "underline italic #ff0000"
```

Colors: `black`, `red`, `green`, `yellow`, `blue`, `purple`, `cyan`, `white`
Modifiers: `bold`, `dimmed`, `italic`, `underline`, `blink`, `reverse`, `hidden`, `strikethrough`
True color: `#rrggbb`

### Conditional Display

```toml
format = "when($condition)[$symbol]($style) "
```

## Advanced Module Patterns

### Multi-Condition Display

```toml
[nodejs]
format = "via [⬢ $version](bold green) "
detect_extensions = ["js", "mjs", "cjs", "ts"]
detect_files = ["package.json", ".node-version"]
detect_folders = ["node_modules"]
```

Show module when ANY condition matches.

### Custom Commands

```toml
[[custom.nix_shell]]
command = "echo $IN_NIX_SHELL"
when = "test -n $IN_NIX_SHELL"
symbol = "❄️ "
style = "bold blue"
format = "via [$symbol nix-shell]($style) "
```

### Environment Variables

```toml
[env_var.USER]
variable = "USER"
default = "unknown"
format = "as [$env_value]($style) "
style = "yellow bold"
```

## Performance Tuning

### Lazy Evaluation

```toml
# Disable expensive detection
[package]
disabled = true

# Limit git operations
[git_status]
ahead_behind_limit = 1000  # Max commits to count
ignore_submodules = true   # Skip submodule checks
```

### Timeout Configuration

```toml
scan_timeout = 10          # Global: version detection
command_timeout = 500      # Global: command execution

[cmd_duration]
min_time = 500            # Only show if ≥500ms
show_milliseconds = false  # Round to seconds
```

### Selective Module Loading

```toml
# Only load relevant modules
format = """
$username\
$hostname\
$directory\
$git_branch\
$git_status\
$golang\
$rust\
$deno\
$cmd_duration\
$line_break\
$character"""

# Explicitly disable others
[package]
disabled = true
[nodejs]
disabled = true
[python]
disabled = true
```

## Preset Customization

### Starting from Preset

```bash
# Export preset as base
starship preset nerd-font-symbols -o config/starship/starship.toml

# Then customize sections
```

### Hybrid Approach

```toml
# Use preset format
format = """
[░▒▓](#a3aed2)\
[  ](bg:#a3aed2 fg:#090c0c)\
[](bg:#769ff0 fg:#a3aed2)\
$directory\
[](fg:#769ff0 bg:#394260)\
$git_branch\
$git_status\
[](fg:#394260 bg:#212736)\
$nodejs\
$rust\
$golang\
[](fg:#212736 bg:#1d2230)\
$time\
[ ](fg:#1d2230)\
"""

# But customize individual modules
[directory]
style = "fg:#e3e5e5 bg:#769ff0"
format = "[ $path ]($style)"
truncation_length = 3

[git_branch]
symbol = ""
style = "bg:#394260"
format = '[[ $symbol $branch ](fg:#769ff0 bg:#394260)]($style)'
```

## Module-Specific Tips

### Git Optimization

```toml
[git_status]
# Performance
ahead_behind_limit = 1000
ignore_submodules = true

# Minimal symbols
conflicted = "="
ahead = "⇡"
behind = "⇣"
diverged = "⇕"
untracked = "?"
stashed = "$"
modified = "!"
staged = "+"
renamed = "»"
deleted = "✘"

# Disable counts for speed
ahead = "⇡"  # Not "⇡${count}"
behind = "⇣"
```

### Directory Truncation

```toml
[directory]
truncation_length = 3              # Show last 3 dirs
truncate_to_repo = true            # Or to git root
repo_root_style = "bold blue"      # Highlight repo root
home_symbol = "~"                  # Use ~ for home
read_only = " 🔒"                  # Indicate read-only

# Substitutions for common paths
[directory.substitutions]
"Documents" = "󰈙 "
"Downloads" = " "
"Music" = " "
"Pictures" = " "
```

### Language Version Display

```toml
[golang]
format = "via [🐹 $version](cyan bold) "
version_format = "v${major}.${minor}"  # Don't show patch

[rust]
format = "via [🦀 $version](red bold) "
detect_extensions = ["rs"]
detect_files = ["Cargo.toml"]

[deno]
format = "via [🦕 $version](green bold) "
detect_extensions = ["ts", "js"]
detect_files = ["deno.json", "deno.jsonc"]
```

## Testing Configurations

### Isolated Testing

```bash
# Test config without installing
env STARSHIP_CONFIG=./test-config.toml fish

# Or create test script
#!/usr/bin/env fish
set -x STARSHIP_CONFIG (pwd)/test-config.toml
starship init fish | source
```

### Performance Profiling

```bash
# Show module timings
starship timings

# Explain current prompt
starship explain

# Validate config
starship config
```

### Module Testing

```bash
# Test specific module
cd /tmp/test-project
npm init -y  # Create package.json
starship module nodejs

# Test git modules
git init
git status  # Should show git_branch module
```

## Common Patterns

### Minimal Performance Config

```toml
format = """
$directory\
$git_branch\
$git_status\
$character"""

[directory]
truncation_length = 3
scan_timeout = 10

[git_status]
ahead_behind_limit = 100
disabled = false

[character]
success_symbol = "[➜](bold green)"
error_symbol = "[➜](bold red)"

scan_timeout = 10
command_timeout = 500
```

### Comprehensive Development Config

```toml
format = """
$username\
$hostname\
$directory\
$git_branch\
$git_status\
$golang\
$rust\
$deno\
$nodejs\
$docker_context\
$kubernetes\
$cmd_duration\
$line_break\
$character"""

[directory]
truncation_length = 5
truncate_to_repo = true

[git_branch]
symbol = "🌱 "

[git_status]
ahead = "⇡${count}"
behind = "⇣${count}"
diverged = "⇕⇡${ahead_count}⇣${behind_count}"

[golang]
symbol = "🐹 "

[rust]
symbol = "🦀 "

[deno]
symbol = "🦕 "

[cmd_duration]
min_time = 500
format = "took [$duration](bold yellow)"
```

### Cloud/DevOps Config

```toml
format = """
$username\
$hostname\
$directory\
$git_branch\
$kubernetes\
$docker_context\
$aws\
$gcloud\
$azure\
$terraform\
$line_break\
$character"""

[kubernetes]
disabled = false
format = 'on [⛵ $context\($namespace\)](dimmed green) '

[docker_context]
format = "via [🐋 $context](blue bold)"

[aws]
symbol = "☁️  "
format = 'on [$symbol($profile )(\($region\) )]($style)'

[terraform]
format = "via [💠 $version$workspace]($style) "
```

## Troubleshooting

### Symbols Not Showing

**Problem**: Boxes or missing icons

**Solution**:
1. Install Nerd Font: https://www.nerdfonts.com/
2. Configure terminal to use Nerd Font
3. Test: `echo -e "\ue0b0 \u00b1 \ue0a0 \u27a6 \u2718 \u26a1 \u2699"`

### Slow Prompt

**Problem**: Delay before prompt appears

**Debug**:
```bash
starship timings  # See which modules are slow
```

**Solutions**:
- Disable slow modules: `[module] disabled = true`
- Reduce git depth: `ahead_behind_limit = 100`
- Increase timeouts: `scan_timeout = 10`
- Skip package detection in large node_modules

### Config Not Loading

**Problem**: Changes not applying

**Check**:
```bash
# Verify config location
echo $STARSHIP_CONFIG  # Should be empty (uses default)
ls -la ~/.config/starship.toml  # Should exist

# Validate syntax
starship config

# Force reload
exec fish -l
```

### Module Not Appearing

**Problem**: Expected module doesn't show

**Debug**:
```bash
# Check if module would show
starship module <module_name>

# Explain current prompt
starship explain
```

**Common causes**:
- Module disabled: `disabled = true`
- Detection failed: missing files/extensions
- Wrong directory: no matching files
- Timeout: `scan_timeout` too low

## Resources

- **Official Docs**: https://starship.rs/config/
- **Advanced Guide**: https://starship.rs/advanced-config/
- **Presets**: https://starship.rs/presets/
- **GitHub**: https://github.com/starship/starship
- **Nerd Fonts**: https://www.nerdfonts.com/
