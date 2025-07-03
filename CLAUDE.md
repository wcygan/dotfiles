# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository (https://github.com/wcygan/dotfiles).

## Project Overview

This is a modern dotfiles repository built with Deno TypeScript scripts. It provides safe installation of shell configurations across platforms (Bash, Zsh) with automatic backup functionality. The project uses Deno for all scripting and automation.

## Key Commands

```bash
deno task install              # Install dotfiles safely (with backup)

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
  - `claude/commands/` - Namespaced slash commands for Claude Code CLI organized by domain:
    - `agent/` - Multi-agent coordination and personas
    - `context/` - Context loading for various technologies
    - `scaffold/` - Project scaffolding templates
    - `git/` - Git and GitHub operations
    - `docs/` - Documentation management
    - `test/` - Testing and quality assurance
    - `code/` - Code operations and analysis
    - `task/` - Task management
    - `ops/` - DevOps and operations
    - `security/` - Security auditing and hardening
    - `analyze/` - Analysis and research tools
    - `workflow/` - Workflow management
    - `meta/` - Meta commands and utilities
    - `tool/` - Tool-specific commands
- `cursor/`, `vscode/`, `zed/` - Editor-specific configurations with keybindings
- `tools/` - User-installable scripts copied to ~/.scripts during installation
- Shell dotfiles are dynamically generated during installation

### Installation Process

The installation script (`install-safely.ts`) manages these dotfiles:

- `.zshrc`, `.bashrc`, `.bash_profile`
- `.path.sh`, `.exports.sh`, `.aliases.sh`, `.functions.sh`, `.extra.sh`
- `.vimrc`
- Claude configuration files (`CLAUDE.md`) to `~/.claude/`
- Claude custom commands from `claude/commands/` to `~/.claude/commands/`
- Claude settings from `claude/settings.json` to `~/.claude/settings.json`
- User scripts from `tools/` to `~/.scripts/`

Each installation creates timestamped backups and provides rollback capability.

## Development Notes

- All scripting uses Deno with JSR imports (@std/* packages)
- Cross-platform compatibility is maintained for macOS, Linux, and Windows

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

## Command Implementation Guidelines

### Command Organization Structure

Commands are organized in a namespaced directory structure under `claude/commands/`:

- Each namespace has its own directory (e.g., `git/`, `test/`, `docs/`)
- Sub-namespaces create nested directories (e.g., `git/pr/`, `test/analyze/`)
- Command files use descriptive names with prefixes (e.g., `pr-create.md` instead of `create.md`)

### Creating New Commands

When creating new commands, follow the namespace structure:

1. **Identify the appropriate namespace** - Choose from existing namespaces or propose a new one
2. **Create the file in the correct directory** - e.g., `claude/commands/test/analyze/analyze-test-complexity.md`
3. **Name the file descriptively** - Use the final command name with namespace prefixes
4. **The command will be accessible as** - `/analyze-test-complexity`

Example directory structure:

```
claude/commands/
├── git/
│   ├── pr/
│   │   ├── pr-create.md     → /pr-create
│   │   └── pr-review.md     → /pr-review
│   └── commit/
│       └── commit.md   → /commit
└── test/
    ├── generate/
    │   └── generate-unit-tests.md     → /generate-unit-tests
    └── analyze/
        └── analyze-test-coverage.md   → /analyze-test-coverage
```

## Slash Commands with Bash Command Execution

Claude Code CLI supports Bash command execution within slash commands, enabling dynamic context injection and powerful automation workflows.

### Bash Command Syntax

**allowed-tools Declaration:**

```yaml
---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
description: Create a git commit
---
```

**Context Injection with !`command`:**

```yaml
## Context

- Current git status: !`git status`
- Current git diff (staged and unstaged changes): !`git diff HEAD`
- Current branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -10`

## Your task

Based on the above changes, create a single git commit.
```

### Key Features

- **Scoped Permissions**: Use `allowed-tools` to restrict which Bash commands can be executed
- **Dynamic Context**: Commands prefixed with !` are executed and their output injected into the prompt
- **Security**: Commands are sandboxed and restricted to allowed operations only
- **Real-time Data**: Context commands run at command invocation time, providing current state

### Best Practices

1. **Minimize Allowed Commands**: Only allow necessary commands for the specific workflow
2. **Use Read-Only Commands for Context**: Prefer informational commands (status, log, diff) for context
3. **Combine with Extended Thinking**: For complex decisions based on command output
4. **Error Handling**: Commands that fail will show error output in context

## Extended Thinking

Use extended thinking for complex architectural decisions, challenging bugs, or planning multi-step implementations that require deep reasoning.

### Usage Examples

**Basic thinking:**

```
> I need to implement a new authentication system using OAuth2 for our API. Think deeply about the best approach for implementing this in our codebase.
```

**Intensified thinking with follow-ups:**

```
> think about potential security vulnerabilities in this approach

> think harder about edge cases we should handle
```

### Thinking Depth Levels

- `think` - Basic extended thinking
- `think more`, `think a lot`, `think harder`, `think longer` - Triggers deeper thinking
- Context-specific intensifiers can be added to focus on particular aspects

### Best Use Cases for Extended Thinking

1. **Planning complex architectural changes** - System design decisions
2. **Debugging intricate issues** - Multi-layer problems requiring deep analysis
3. **Creating implementation plans** - Breaking down complex features
4. **Understanding complex codebases** - Analyzing interdependencies
5. **Evaluating tradeoffs** - Comparing different technical approaches

Extended thinking is visible in the interface and allows for iterative refinement through follow-up prompts.

## Parallel Claude Code Sessions with Git Worktrees

Run multiple Claude Code sessions simultaneously on different features using Git worktrees, enabling true parallel development without branch switching conflicts.

### Git Worktree Workflow

**Create a new worktree for parallel development:**

```bash
# Create worktree for a feature branch
git worktree add ../project-feature feature-branch

# Create worktree with new branch
git worktree add -b new-feature ../project-new-feature

# List all worktrees
git worktree list

# Remove worktree when done
git worktree remove ../project-feature
```

### Best Practices for Parallel Sessions

1. **One Worktree Per Claude Session**: Each Claude Code instance should work in its own worktree
2. **Clear Naming Convention**: Use descriptive worktree paths like `../project-feature-auth` or `../project-fix-bug-123`
3. **Independent Development**: Each worktree has its own working directory, allowing truly parallel work
4. **Coordinate Through PRs**: Use pull requests to merge parallel work back to main branch

### Typical Parallel Workflow

```bash
# Terminal 1: Main development
cd ~/projects/myapp
claude code  # Working on main branch

# Terminal 2: Feature development
git worktree add -b feature-oauth ../myapp-oauth
cd ../myapp-oauth
claude code  # Working on OAuth feature independently

# Terminal 3: Bug fix
git worktree add -b fix-123 ../myapp-fix-123 origin/main
cd ../myapp-fix-123
claude code  # Working on bug fix independently
```

### Advantages

- **No Branch Switching**: Each session maintains its own branch context
- **True Parallelism**: Multiple developers or AI agents can work simultaneously
- **Isolated Environments**: Changes in one worktree don't affect others
- **Faster Development**: No need to stash/switch/pull between features
- **Better Organization**: Physical separation of different development streams
