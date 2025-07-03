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

1. **$ARGUMENTS Pattern**: Use `[$ARGUMENTS]` for flexible, context-aware input parsing
2. **Contextual Intelligence**: Commands interpret project structure and existing state automatically
3. **Smart Inference**: Extract intent from natural language arguments rather than rigid syntax
4. **Context-First Design**: Analyze current environment before requiring user input
5. **Keyword Detection**: Parse `$ARGUMENTS` for intent keywords while using remainder as content
6. **No Wizards**: Avoid interactive prompts; infer from context and arguments instead

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

## Command Implementation Guidelines

### $ARGUMENTS Pattern Best Practices

**Context Analysis First:**

```bash
# Command should analyze existing state before parsing arguments
/docs-init [$ARGUMENTS]  # Checks for existing /docs, project type, git repo
/docs-add [$ARGUMENTS]   # Analyzes current doc structure, infers placement
/docs-update [$ARGUMENTS] # Detects what needs updating based on project changes
```

**Flexible Argument Parsing:**

- **No arguments**: Infer from context (current directory, project structure, existing files)
- **Single keyword**: Use as primary intent (`validate`, `force`, `diagrams`)
- **Multiple keywords**: Parse for type + content (`guide Quick Start`, `api User Management`)
- **Natural language**: Extract intent from full phrases (`Getting Started with Authentication`)

**Smart Defaults Over Configuration:**

- Detect project type from files (`deno.json`, `Cargo.toml`, `go.mod`, `package.json`)
- Use well-known file locations (`/docs`, `/src`, `/api`, `/tests`)
- Infer relationships between related files and directories
- Preserve existing patterns and conventions

**Context-Aware Behavior Examples:**

```bash
# Auto-detects project name, type, and configures appropriately
/docs-init

# Infers "guide" type from existing structure, places in guides/ folder
/docs-add Quick Start Guide

# Detects OpenAPI files, updates API docs, validates Mermaid diagrams
/docs-update

# Creates troubleshooting section, analyzes existing categories
/docs-add troubleshooting Common Issues
```

**Error Handling Philosophy:**

- Suggest corrective actions rather than failing
- Provide context about why something cannot be done
- Offer alternative approaches when primary action is blocked
- Use existing project patterns to guide suggestions

## Namespaced Slash Commands

Claude commands are organized using a namespace structure: `/<namespace>:<subnamespace>:<command>`

### Command Namespaces

- **agent:** - Multi-agent coordination (`/agent:core:init`, `/agent:persona:backend-specialist`)
- **context:** - Load technology context (`/context:deno:fresh`, `/context:rust:web`)
- **scaffold:** - Project scaffolding (`/scaffold:go:connect`, `/scaffold:rust:axum`)
- **git:** - Git operations (`/git:pr:create`, `/git:commit:push`)
- **docs:** - Documentation (`/docs:manage:init`, `/docs:generate:api`)
- **test:** - Testing (`/test:run:tdd`, `/test:analyze:coverage`)
- **code:** - Code operations (`/code:refactor:standard`, `/code:analyze:deps`)
- **task:** - Task management (`/task:manage:create`, `/task:view:current`)
- **ops:** - DevOps (`/ops:deploy:standard`, `/ops:monitor:setup`)
- **security:** - Security (`/security:audit:secrets`, `/security:model:threat`)
- **analyze:** - Analysis (`/analyze:think:standard`, `/analyze:research:web-deep`)
- **workflow:** - Workflow (`/workflow:manage:plan`, `/workflow:view:progress`)
- **meta:** - Meta utilities (`/meta:command:generate`, `/meta:search:smart`)
- **tool:** - Tool-specific (`/tool:diagram`, `/tool:zed-task`)

### Examples

```bash
# Old command → New namespaced command
/pr → /git:pr:create
/agent-persona-backend-specialist → /agent:persona:backend-specialist
/context-load-deno-fresh → /context:deno:fresh
/test-gen → /test:generate:unit
/docs-init → /docs:manage:init
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

### Multi-Agent Coordination

When using multiple Claude Code sessions:

- **Shared State Files**: Use `/tmp/{project-name}/` for coordination files
- **Status Communication**: Create JSON status files for structured updates
- **PR Comments**: Use GitHub PR comments for cross-session communication
- **Avoid Conflicts**: Each session works on separate files/features
- **Join Points**: Define clear synchronization points in PLAN.md

### Advantages

- **No Branch Switching**: Each session maintains its own branch context
- **True Parallelism**: Multiple developers or AI agents can work simultaneously
- **Isolated Environments**: Changes in one worktree don't affect others
- **Faster Development**: No need to stash/switch/pull between features
- **Better Organization**: Physical separation of different development streams
