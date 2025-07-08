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

# Documentation
deno task docs:dev             # Start Docusaurus dev server
deno task docs:build           # Build documentation site
deno task docs:serve           # Serve built documentation

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
- `.claude/` - Hidden directory for project-specific Claude Code metadata
  - `.claude/commands/` - Project-specific slash commands (e.g., `/improve-slash-commands`)
  - `.claude/settings.local.json` - Local Claude Code settings overrides
  - This directory contains sensitive or project-specific configurations not meant for distribution
- `cursor/`, `vscode/`, `zed/` - Editor-specific configurations with keybindings
- `tools/` - User-installable scripts copied to ~/.tools during installation
- `docs/` - Docusaurus documentation site with guides and references (integrated with Deno tasks)
- Shell dotfiles are dynamically generated during installation

### Installation Process

The installation script (`install-safely.ts`) manages these dotfiles:

- `.zshrc`, `.bashrc`, `.bash_profile`
- `.path.sh`, `.exports.sh`, `.aliases.sh`, `.functions.sh`, `.extra.sh`
- `.vimrc`
- Claude configuration files (`CLAUDE.md`) to `~/.claude/`
- Claude custom commands from `claude/commands/` to `~/.claude/commands/`
- Claude settings from `claude/settings.json` to `~/.claude/settings.json`
- User scripts from `tools/` to `~/.tools/`

Each installation creates timestamped backups and provides rollback capability.

## Development Notes

- All scripting uses Deno with JSR imports (@std/* packages)
- Cross-platform compatibility is maintained for macOS, Linux, and Windows

## Documentation (Docusaurus)

This project includes a comprehensive documentation site built with Docusaurus, fully integrated with the Deno task runner for a seamless development workflow.

### Overview

- Modern documentation site using Docusaurus v3.8.1
- Deployed to GitHub Pages at https://wcygan.github.io/dotfiles/
- Integrated with Deno tasks for consistent developer experience
- Dark mode enabled by default with user preference support

### Deno Integration

All documentation commands are available through `deno.json` tasks:

```bash
# Docusaurus commands via Deno tasks
deno task docs:install     # Install npm dependencies
deno task docs:dev         # Start development server (localhost:3000)
deno task docs:build       # Build static site
deno task docs:serve       # Serve built site locally
deno task docs:typecheck   # Type check TypeScript files

# Alternative: Direct npm commands
cd docs && npm start       # Same as deno task docs:dev
cd docs && npm run build   # Same as deno task docs:build
cd docs && npm run deploy  # Deploy to GitHub Pages
```

### Directory Structure

- `docs/` - Docusaurus root directory (excluded from Deno formatting)
  - `docs/` - Markdown documentation files
    - `getting-started/` - Installation and quick start guides
    - `configuration/` - Shell, editor, and tool configurations
    - `reference/` - Script reference documentation
  - `src/` - Custom components and pages
    - `components/` - HomepageFeatures component
    - `pages/` - Custom homepage with hero section
    - `css/` - Custom styling for light/dark themes
  - `static/` - Static assets directory
  - `build/` - Generated static site (git-ignored)
  - `docusaurus.config.ts` - Site configuration
  - `sidebars.ts` - Documentation structure

### Content Organization

- **Getting Started**: Installation guide with prerequisites, quick start, and backup/rollback procedures
- **Configuration**: Detailed guides for shell, editor, and tool configurations
- **Reference**: Comprehensive script documentation
- **Features**:
  - Sidebar navigation with collapsible sections
  - Syntax highlighting for bash, typescript, rust, go, and java
  - Edit on GitHub links for easy contributions
  - Broken link detection during builds

### Deployment

- **URL**: https://wcygan.github.io/dotfiles/
- **Base URL**: `/dotfiles/`
- **Deployment Branch**: `gh-pages`
- **Organization**: `wcygan`
- **Deploy Command**: `cd docs && npm run deploy`

### Development Workflow

1. **Initial Setup**: `deno task docs:install` to install dependencies
2. **Development**: `deno task docs:dev` starts the dev server with hot reload
3. **Type Checking**: `deno task docs:typecheck` ensures TypeScript correctness
4. **Building**: `deno task docs:build` creates production-ready static files
5. **Preview**: `deno task docs:serve` to preview the built site locally

### Integration Notes

- The `docs/` directory is excluded from Deno formatting (`fmt.exclude` in deno.json)
- Documentation complements this CLAUDE.md file:
  - **CLAUDE.md**: AI assistant context, development guidelines, and internal documentation
  - **Docs Site**: User-facing installation guides, configuration references, and public documentation
- Changes to shell configurations should be reflected in both places when appropriate

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

## Slash Command Template

The `/commit` command (@claude/commands/git/commit/commit.md) serves as the gold standard for implementing slash commands, demonstrating all key features and best practices.

### Gold Standard Example: /commit

```yaml
---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
description: Create a git commit
---

## Context

- Current git status: !`git status`
- Current git diff (staged and unstaged changes): !`git diff HEAD`
- Current branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -10`

## Your task

Generate a conventional commit message following https://www.conventionalcommits.org/en/v1.0.0/ specification and create the commit automatically.
```

### Key Features Demonstrated

1. **Front Matter Configuration**
   - `allowed-tools`: Explicitly scopes which Bash commands can be executed
   - `description`: Clear, concise purpose of the command

2. **Dynamic Context Injection**
   - Uses `!` prefix for bash command execution (this pulls in dynamic context into the prompt, very useful to get real world examples)
   - Provides real-time repository state
   - Multiple context commands for comprehensive understanding

3. **Clear Task Definition**
   - Specific, actionable instructions
   - References external standards (Conventional Commits)
   - Step-by-step process explanation

4. **Best Practices**
   - Security-first with minimal allowed commands
   - Read-only context commands (status, diff, log)
   - Clear examples of expected output
   - Automated action after analysis

### Template Structure

```yaml
---
allowed-tools: Tool1(command:scope), Tool2(command:scope)
description: Brief description of command purpose
---

## Context

- Dynamic context 1: !`bash command`
- Dynamic context 2: !`another command`
- File reference: @path/to/file

## Your task

Clear instructions on what to accomplish.

Steps:
1. First step
2. Second step
3. Final step

Example output:
- Example 1
- Example 2
```

### Implementation Guidelines

1. **Security Considerations**
   - Only allow necessary commands in `allowed-tools`
   - Prefer read-only commands for context gathering
   - Never allow commands that could modify system state unexpectedly

2. **Context Design**
   - Gather sufficient context for informed decision-making
   - Order context logically (current state → history → related info)
   - Use descriptive labels for each context item

3. **Task Clarity**
   - State the objective clearly
   - Provide step-by-step guidance when appropriate
   - Include examples of expected outcomes
   - Reference relevant standards or conventions

4. **User Experience**
   - Keep descriptions concise but complete
   - Use consistent formatting across commands
   - Provide feedback on command execution
   - Handle edge cases gracefully

### Advanced Features Integration

- **Arguments**: Use `$ARGUMENTS` for dynamic input from the user
- **File References**: Use `@file/path` to include file contents
- **Extended Thinking**: Commands can trigger deep analysis with thinking keywords (e.g., think, think deeply, think harder, ultrathink)
- **Namespacing**: Organize in subdirectories for logical grouping

## Sub-Agent Integration in Slash Commands

Based on insights from Claude Code sub-agent architecture, slash commands can leverage parallel execution for enhanced performance and capabilities.

### When to Use Sub-Agents in Slash Commands

**Ideal Use Cases:**

1. **Large-scale Code Analysis** - Exploring multiple files/directories in parallel
2. **Independent Research Tasks** - Gathering information from different sources simultaneously
3. **Multi-aspect Analysis** - Analyzing code quality, security, performance in parallel
4. **Documentation Generation** - Creating docs for multiple components concurrently

**Not Recommended For:**

1. **Sequential Operations** - Tasks with dependencies between steps
2. **Simple Single-file Operations** - Overhead outweighs benefits
3. **State-modifying Operations** - Risk of conflicts with parallel writes

### Sub-Agent Slash Command Template

```yaml
---
allowed-tools: Task, Bash(find:*), Bash(rg:*), Read
description: Analyze codebase architecture using parallel sub-agents
---

## Context

- Project structure: !`fd . -t d -d 3`
- File count by type: !`fd . -e js -e ts -e py | wc -l`

## Your task

Analyze this codebase using parallel sub-agents to understand:

1. **Architecture Agent**: Analyze overall project structure and design patterns
2. **Dependencies Agent**: Map out all dependencies and their relationships  
3. **Security Agent**: Identify potential security vulnerabilities
4. **Performance Agent**: Find performance bottlenecks and optimization opportunities
5. **Test Coverage Agent**: Analyze test coverage and testing patterns

Launch these 5 agents in parallel to explore the codebase. Each agent should:
- Focus only on their specific domain
- Create a summary report
- Identify key findings and recommendations

Synthesize all findings into a comprehensive architecture report.
```

### Implementation Patterns

**1. Discovery Pattern** - Multiple agents explore different aspects:

```yaml
## Your task

Use 4 parallel agents to discover:
  - Agent 1: All API endpoints in the codebase
  - Agent 2: Database schema and models
  - Agent 3: Authentication and authorization flows
  - Agent 4: External service integrations
```

**2. Analysis Pattern** - Deep dive into specific areas:

```yaml
## Your task

Analyze the authentication system using 3 parallel agents:
  - Agent 1: Review security implementation
  - Agent 2: Check test coverage
  - Agent 3: Document current flows
```

**3. Generation Pattern** - Create multiple artifacts:

```yaml
## Your task

Generate documentation using 5 parallel agents:
  - Agent 1: API documentation
  - Agent 2: Component documentation
  - Agent 3: Configuration guide
  - Agent 4: Deployment instructions
  - Agent 5: Troubleshooting guide
```

### Best Practices for Sub-Agent Commands

1. **Let Claude Code Manage Parallelism**
   - Don't specify exact parallelism levels
   - System automatically optimizes based on task complexity

2. **Clear Task Boundaries**
   - Each sub-agent should have a well-defined, independent scope
   - Avoid overlapping responsibilities

3. **Token Efficiency**
   - Be aware that each sub-agent consumes its own token budget
   - Use for high-value tasks where parallel execution provides significant benefits

4. **Context Preservation**
   - Main agent synthesizes findings from all sub-agents
   - Use structured output formats for easier aggregation

5. **Error Handling**
   - Design tasks to be resilient to partial failures
   - Main agent should handle missing or incomplete sub-agent results

### Example Sub-Agent Commands

**Code Quality Analysis** (`/analyze-code-quality`):

```yaml
---
allowed-tools: Task, Read, Grep, Bash(rg:*)
description: Comprehensive code quality analysis using parallel agents
---

## Your task

Perform comprehensive code quality analysis using multiple agents:

1. **Complexity Analysis**: Identify complex functions and modules
2. **Duplication Detection**: Find duplicate code patterns
3. **Style Consistency**: Check coding standards adherence
4. **Documentation Coverage**: Assess documentation completeness
5. **Dead Code Detection**: Find unused code
6. **Type Safety**: Analyze type coverage and safety

Each agent works independently. Compile findings into actionable recommendations.
```

**Migration Planning** (`/plan-migration`):

```yaml
---
allowed-tools: Task, Read, Grep
description: Plan technology migration using parallel analysis
---

## Your task

Plan migration from $ARGUMENTS using parallel agents to analyze:

1. **Current Implementation**: Map existing usage patterns
2. **Dependencies**: Identify all dependent code
3. **Risk Assessment**: Evaluate migration risks
4. **Migration Strategy**: Design phased approach
5. **Testing Requirements**: Define test scenarios

Synthesize into a comprehensive migration plan with timeline and risk mitigation.
```

### Performance Considerations

- **Token Usage**: Sub-agents multiply token consumption
- **Execution Time**: Parallel execution reduces wall-clock time significantly
- **Queue Management**: System handles up to 10 parallel tasks, queues additional
- **Context Windows**: Each sub-agent gets fresh context, enabling larger codebases

### Integration with Existing Features

Sub-agents work seamlessly with other slash command features:

- **Dynamic Context**: Use `!` commands to provide context to all agents
- **File References**: Share file contents across sub-agents with `@file`
- **Extended Thinking**: Combine with thinking modes for complex analysis
- **Arguments**: Pass user input to customize agent behavior

## Prompts as Code: Programming Slash Commands

Based on insights from treating prompts as executable programs, slash commands should be designed as deterministic, reproducible workflows rather than conversational interfaces.

### Core Philosophy

Think of LLMs as "extremely slow, unreliable computers programmed with natural language." This fundamental shift transforms slash commands from "requests" into "programs" with:

- Clear inputs and outputs
- Defined state management
- Explicit control flow
- Error handling capabilities

### Programming Constructs in Slash Commands

**1. Sequential Execution**

```yaml
## Your task
STEP 1: Analyze current implementation
STEP 2: Identify improvement opportunities
STEP 3: Generate refactoring plan
STEP 4: Apply changes systematically
```

**2. Conditional Logic**

```yaml
## Your task
IF the project uses TypeScript:
  - Validate type definitions
  - Check for any types
  - Suggest stricter typing
ELSE IF the project uses JavaScript:
  - Propose TypeScript migration
  - Add JSDoc annotations
  - Create type definition files
```

**3. Iteration and Loops**

```yaml
## Your task
FOR EACH component in the directory:
  - Analyze complexity
  - Check test coverage
  - Identify missing documentation
  - Generate improvement report
```

**4. State Management**

```yaml
## Context
- Session ID: !`gdate +%s%N`
- Previous state: @/tmp/analysis-state-$SESSION_ID.json
- Iteration count: !`jq .iteration < /tmp/state-$SESSION_ID.json`

## Your task
1. Load current state or initialize
2. Process next batch of files
3. Update state with progress
4. Save checkpoint for resumability
```

**5. Error Handling**

```yaml
## Your task
TRY:
  - Execute primary analysis
  - Generate recommendations
CATCH (missing dependencies):
  - Document missing requirements
  - Suggest installation steps
  - Save partial results
FINALLY:
  - Update state file
  - Report completion status
```

### Slash Command Programming Patterns

**State Machine Pattern**

```yaml
---
allowed-tools: Read, Write, Bash(jq:*), Bash(gdate:*)
description: Workflow with state transitions
---

## Context
- Session ID: !`gdate +%s%N`
- State file: /tmp/workflow-state-$SESSION_ID.json

## State Definition
- States: [initializing, analyzing, validating, implementing, complete]
- Current: !`jq .state < /tmp/workflow-state-$SESSION_ID.json`

## Your task
CASE current_state:
  WHEN "initializing":
    - Set up workspace
    - Transition to "analyzing"
  WHEN "analyzing":
    - Perform analysis
    - Transition to "validating"
  WHEN "validating":
    - AWAIT user confirmation
    - Transition to "implementing" or "analyzing"
```

**Pipeline Pattern**

```yaml
## Pipeline Definition
Input: $ARGUMENTS
  |
  v
Stage 1: Parse and validate input
  | Output: validated-input.json
  v
Stage 2: Process data
  | Output: processed-data.json
  v
Stage 3: Generate artifacts
  | Output: final-results/
```

**Checkpoint Pattern**

```yaml
## Context
- Session ID: !`gdate +%s%N`

## Your task
1. CHECKPOINT: Save current progress to /tmp/checkpoint-$SESSION_ID.json
2. Execute potentially long operation
3. IF interrupted:
   - User can resume from checkpoint
4. ELSE:
   - Continue to next phase
```

### Best Practices for Programmable Commands

**1. Deterministic Behavior**

- Same inputs should produce same outputs
- Avoid randomness or time-dependent logic
- Use explicit state files for variability

**2. Minimize Context Window Usage**

- Serialize state to disk between operations
- Use precise tools (jq, rg) for data extraction
- Reference files instead of embedding content

**3. Unique Temporary File Names**

- **CRITICAL**: Always use nanosecond precision timestamps to prevent file conflicts
- **GOOD**: `/tmp/state-$(gdate +%s%N).json` → `/tmp/state-1751703298807183000.json`
- **BAD**: `/tmp/state.json` (will cause conflicts with concurrent sessions)
- **Platform Note**: Use `gdate` on macOS (from coreutils), `date` on Linux

```yaml
## Context
- Session ID: !`gdate +%s%N`
- State file: @/tmp/workflow-state-$SESSION_ID.json
- Checkpoint: @/tmp/checkpoint-$SESSION_ID.json

## Your task
1. Initialize unique session files
2. Process data with session isolation
3. Clean up session-specific files on completion
```

**4. Human-in-the-Loop Checkpoints**

```yaml
## Your task
1. Analyze system
2. Generate plan
3. CHECKPOINT: Present plan for approval
4. IF approved:
   - Execute plan
5. ELSE:
   - Revise based on feedback
   - GOTO step 3
```

**5. Modular Design**

```yaml
## Your task
CALL analyze_module($ARGUMENTS)
CALL validate_results()
CALL generate_report()
CALL cleanup_temp_files()
```

### Example: Complex Workflow as Program

```yaml
---
allowed-tools: Task, Read, Write, Bash(jq:*), Bash(rg:*), Bash(gdate:*)
description: Automated refactoring workflow with checkpoints
---

## Context
- Session ID: !`gdate +%s%N`

## Program Definition
INPUT: target_directory = $ARGUMENTS
STATE_FILE: /tmp/refactor-state-$SESSION_ID.json
CHECKPOINT_DIR: /tmp/refactor-checkpoints-$SESSION_ID/

## Main Program
PROCEDURE main():
  state = load_or_initialize_state()
  
  WHILE state.phase != "complete":
    CASE state.phase:
      WHEN "scanning":
        candidates = scan_for_refactoring_targets()
        state.candidates = candidates
        state.phase = "planning"
        save_state(state)
        
      WHEN "planning":
        plan = generate_refactoring_plan(state.candidates)
        write_file(CHECKPOINT_DIR + "plan.md", plan)
        PRINT "Review plan at: " + CHECKPOINT_DIR + "plan.md"
        state.phase = "awaiting_approval"
        save_state(state)
        
      WHEN "awaiting_approval":
        PRINT "Awaiting user approval. Run with --approve to continue"
        BREAK
        
      WHEN "executing":
        FOR EACH change IN state.approved_changes:
          apply_refactoring(change)
          state.completed.push(change)
          save_state(state)
        state.phase = "complete"
        
  generate_summary_report()
  cleanup_temp_files()
```

### Benefits of Programming Approach

1. **Reproducibility**: Identical execution paths for same inputs
2. **Resumability**: Interrupted workflows continue from checkpoints
3. **Debuggability**: Clear execution flow and state transitions
4. **Composability**: Commands can call other commands as subroutines
5. **Testability**: Predictable behavior enables testing

### Integration Guidelines

When creating slash commands:

1. Think "program" not "conversation"
2. Define clear inputs, outputs, and state
3. Use control flow constructs explicitly
4. Implement checkpoint/resume capabilities
5. Handle errors gracefully
6. Minimize token usage through state serialization

This programming paradigm transforms slash commands from simple automations into robust, production-ready workflows.

## Claude Code Hooks

Claude Code supports hooks that execute commands at specific points in its lifecycle, enabling powerful automation workflows.

### Hook Types

1. **PreToolUse** - Runs before tool execution
2. **PostToolUse** - Runs after tool completion (most commonly used)
3. **Notification** - Triggers on notifications
4. **Stop** - Runs when agents finish responding
5. **SubagentStop** - Runs when subagents finish responding

### Hook Configuration

Hooks are configured in Claude settings files (`~/.claude/settings.json` or `.claude/settings.json`):

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write|MultiEdit",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/script.sh"
          }
        ]
      }
    ]
  }
}
```

### Common Hook Use Cases

**1. Code Formatting**

- Auto-format files after editing (most popular use case)
- Language-specific formatting (Go, TypeScript, Python, etc.)
- Markdown and documentation formatting

**2. Git Integration**

- Auto-stage formatted files
- Prepare commit messages
- Update git status

**3. Command Logging**

- Log all executed commands for audit trails
- Track Claude's actions for debugging
- Analytics and usage patterns

**4. Notifications**

- Desktop notifications when tasks complete
- Sound alerts for long-running operations
- Status updates via external services

**5. Validation & Testing**

- Run tests after code changes
- Type-check TypeScript files
- Lint modified files
- Version consistency checks

### Hook Implementation Example

**Auto-formatting hook** (`.claude/hooks/format.sh`):

```bash
#!/bin/bash
# Read JSON input from stdin
input=$(cat)

# Extract file path from JSON
file_path=$(echo "$input" | jq -r '.tool_input.file_path // .tool_response.filePath // empty')

# Format based on file extension
case "${file_path##*.}" in
  go) go fmt "$file_path" ;;
  js|ts) npx prettier --write "$file_path" ;;
  py) black "$file_path" ;;
esac
```

### Finding Hooks on GitHub

To discover how others are using Claude Code hooks:

**Search for hook configurations:**

```
https://github.com/search?q=path:*claude*/settings*.json+"PostToolUse"&type=code
https://github.com/search?q=path:*claude*/settings*.json+"hooks"&type=code
```

**Search for hook scripts:**

```
https://github.com/search?q=path:.claude/hooks+extension:sh&type=code
```

**Using GitHub CLI:**

```bash
# Search for PostToolUse hooks
gh api search/code --raw-field q='path:*claude*/settings*.json "PostToolUse"'

# Search for hook scripts
gh api search/code --raw-field q='path:.claude/hooks extension:sh'
```

### Best Practices

1. **Security**: Only execute trusted scripts, validate inputs
2. **Performance**: Keep hooks fast to avoid slowing down Claude
3. **Error Handling**: Hooks should fail gracefully
4. **Logging**: Log hook actions for debugging
5. **Idempotency**: Hooks should be safe to run multiple times

### Hook Input Format

Hooks receive JSON input via stdin containing:

- `tool_name`: The tool that triggered the hook
- `tool_input`: Input parameters to the tool
- `tool_response`: Response from the tool (PostToolUse only)

Example input:

```json
{
  "tool_name": "Edit",
  "tool_input": {
    "file_path": "/path/to/file.go",
    "old_string": "...",
    "new_string": "..."
  }
}
```

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
