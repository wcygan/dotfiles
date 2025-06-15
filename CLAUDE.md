# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a modern dotfiles repository built with Deno TypeScript scripts. It provides safe installation/rollback of shell configurations across platforms (Bash, Zsh, PowerShell) with automatic backup functionality. The project uses Deno for all scripting and automation.

## Key Commands

```bash
# Installation & Management
deno task install              # Install dotfiles safely (with backup)
deno task install:force        # Force install without prompts
deno task rollback             # Rollback to previous configuration
deno task rollback:force       # Force rollback without prompts

# Development & Testing
deno task test                 # Run integration tests
deno task check                # Type check all TypeScript files
deno task pre-commit           # Run pre-commit checks
deno task pre-commit:fix       # Run pre-commit checks with auto-fix
deno task ci:check             # CI environment validation
deno task ci:fix               # CI environment validation with fixes

# Scripts
deno run --allow-all install-safely.ts           # Main installation script
deno run --allow-all integration-test.ts         # Integration test runner
deno run --allow-all scripts/pre-commit-check.ts # Pre-commit validation
```

## Architecture

### Core Scripts

- `install-safely.ts` - Main installation script with backup/restore logic
- `integration-test.ts` - Comprehensive test suite for installation/rollback
- `profile.ps1` - PowerShell profile configuration

### Script Utilities (`scripts/`)

- `ci-environment-check.ts` - CI environment validation and setup
- `pre-commit-check.ts` - Pre-commit hook validation
- `test-actions-locally.ts` - Local GitHub Actions testing

### Configuration Directories

- `claude/` - Claude AI assistant configuration and scripts
  - `claude/commands/` - Custom slash commands for Claude Code CLI
- `cursor/`, `vscode/`, `zed/` - Editor-specific configurations with keybindings
- Shell dotfiles are dynamically generated during installation

### Installation Process

The installation script (`install-safely.ts`) manages these dotfiles:

- `.zshrc`, `.bashrc`, `.bash_profile`
- `.path.sh`, `.exports.sh`, `.aliases.sh`, `.functions.sh`, `.extra.sh`
- `.vimrc`
- Claude configuration files (`CLAUDE.md`) to `~/.claude/`
- Claude custom commands from `claude/commands/` to `~/.claude/commands/`

Each installation creates timestamped backups and provides rollback capability.

## Development Notes

- All scripting uses Deno with JSR imports (@std/* packages)
- Cross-platform compatibility is maintained for macOS, Linux, and Windows
- The project follows safe installation patterns with automatic backup/restore
- Integration tests run in isolated temporary environments
- Pre-commit hooks validate code quality before commits
- **ALWAYS** run `deno fmt` immediately after writing or editing any file in this repository
- This ensures consistent formatting and prevents `deno fmt --check` failures in CI
- **ALWAYS** run `deno fmt --check` after making changes to verify formatting
- Apply formatting fixes with `deno fmt` if needed

## Zed Editor Tasks

Zed tasks are commands that run in the integrated terminal. Tasks can be defined in:

- Global: `~/.config/zed/tasks.json`
- Project: `.zed/tasks.json`
- Temporary: Oneshot tasks via command palette

### Task Configuration

```json
{
  "label": "Task name",
  "command": "deno task test",
  "env": {
    "KEY": "value"
  },
  "cwd": "$ZED_WORKTREE_ROOT",
  "use_new_terminal": false,
  "allow_concurrent_runs": false,
  "reveal": "always",
  "shell": "zsh"
}
```

### Available Variables

- `$ZED_FILE` - Current file path
- `$ZED_WORKTREE_ROOT` - Project root directory
- `$ZED_COLUMN` - Cursor column
- `$ZED_ROW` - Cursor row

### Running Tasks

- `cmd-shift-p` → `task: spawn` - Run a task
- `task: rerun` - Rerun last task
- Custom keybindings can trigger specific tasks

## Command Ideation Process

### Systematic Process for Discovering New Claude Commands

#### Phase 1: Ecosystem Analysis

1. **Command Inventory**: Count and categorize all existing commands by workflow stage
2. **Gap Identification**: Map workflow stages with low command coverage
3. **Pattern Recognition**: Identify naming conventions and usage patterns

#### Phase 2: Pain Point Research

1. **Developer Workflow Gaps**: Survey latest trends and manual pain points
2. **Technology Evolution**: Research emerging tools and frameworks
3. **Enterprise Needs**: Identify complex workflows needing automation

#### Phase 3: Command Design Principles

1. **Simple Usage**: `/command [optional-context]` or `/command` (auto-detects)
2. **Contextual Intelligence**: Commands interpret project structure automatically
3. **Interactive Fallback**: Guided selection when no argument provided
4. **Smart Defaults**: Work with sensible defaults for common cases

#### Phase 4: Validation Framework

**Tier 1**: High-impact pain points affecting 50%+ of developers
**Tier 2**: Strategic workflow automation for growing technologies\
**Tier 3**: Emerging technology foundation and niche value

### Research Triggers

- Major technology shifts (framework migrations, new tools)
- Repeated manual tasks in development workflow
- Team pain points from retrospectives
- Industry best practice evolution

### Command Categories to Monitor

- **AI/ML Workflows**: Fastest-growing development segment
- **Frontend Build Tools**: Rapid ecosystem changes
- **Cloud-Native Complexity**: K8s and container orchestration
- **Mobile Development**: CI/CD and testing gaps
- **Database Operations**: Migration and performance management
- **Security Automation**: Compliance and vulnerability management
