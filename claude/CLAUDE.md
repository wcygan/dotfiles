# CLAUDE.md

IMPORTANT: These are my development preferences and guidelines. YOU MUST follow them when working on my projects.

## Code Style & Workflow

### Testing

- **ALWAYS** write clear, descriptive test names for better readability
- **ALWAYS** prefer running single tests over the whole test suite for performance
- Use `deno test --filter="test name"` or framework-specific single test runners

### Language & Framework Preferences

#### Backend Programming

IMPORTANT: I am primarily a backend developer and prefer these languages and frameworks:

- **Go**: Use [ConnectRPC](https://github.com/connectrpc/connect-go) for RPC services
- **Rust**: Use [axum](https://github.com/tokio-rs/axum) for web services
- **Java**: Use [Spring Boot](https://spring.io/projects/spring-boot) with [Quarkus](https://quarkus.io/)

#### Scripting & Automation

**YOU MUST** use Deno for all scripting tasks instead of Bash or Python:

- Create `deno.json` in project root with tasks for common operations
- Use JSR imports: `import { walk } from "@std/fs";` NOT `https://deno.land/...`
- Use [Dax](https://github.com/dsherret/dax) for cross-platform shell operations
- Example deno.json imports: `"@std/fs": "jsr:@std/fs@^1.0.17"`

#### Web Development

Use [Deno Fresh](https://fresh.deno.dev/) with these practices:

- Built-in test runner: `Deno.test()`
- Organize tests: `/tests/unit/`, `/tests/component/`, `/tests/e2e/`
- Mock external dependencies for fast, reliable tests
- Use fresh-testing-library for component/handler testing

## Infrastructure Choices

IMPORTANT: I run a Talos Linux Kubernetes Cluster. Use these modern alternatives:

- **Database**: Postgres (NOT MySQL)
- **Cache**: DragonflyDB (NOT Redis)
- **Streaming**: RedPanda (NOT Kafka)
- **NoSQL**: ScyllaDB (NOT Cassandra)

## Modern Development Tools

### Preferred Command-Line Tools

**ALWAYS** prefer these modern, fast alternatives:

- **ripgrep (rg)**: Use instead of grep for searching code
- **fd**: Use instead of find for finding files
- **fzf**: Use for interactive fuzzy finding
- **bat**: Use instead of cat for syntax-highlighted file viewing
- **exa/eza**: Use instead of ls for better file listings
- **delta**: Use for better git diffs
- **zoxide**: Use instead of cd for smarter directory navigation
- **duf**: Use instead of df for disk usage
- **htop/btop**: Use instead of top for process monitoring
- **jq**: Use for JSON processing and manipulation
- **yq**: Use for YAML processing and manipulation
- **hexyl**: Use for hex viewing of binary files

### Output Format Preferences

**ALWAYS** prefer JSON output for parsing when available:

- Use `-o json` or `--json` flags when available (e.g., `kubectl get nodes -o json`)
- Parse structured JSON output instead of text formats for reliability
- Use `jq` for JSON processing in scripts
- Examples:
  - `kubectl get pods -o json | jq '.items[].metadata.name'`
  - `docker inspect container-name | jq '.[0].State.Status'`
  - `aws ec2 describe-instances --output json | jq '.Reservations[].Instances[]'`

### Common Commands

```bash
# Modern tool usage
rg "pattern" --type rust        # Search Rust files
fd ".rs$" src/                   # Find all Rust files
bat src/main.rs                  # View file with syntax highlighting
eza -la --git                    # List files with git status
delta                            # Better git diff viewer

# Deno development
deno task dev          # Start development server
deno task test         # Run all tests
deno test --filter="specific test"  # Run single test
deno task build        # Build project
deno check            # Type check
deno fmt              # Format code
deno lint             # Lint code

# Project setup
deno task init        # Initialize / configure the project for a new environment
deno task deps        # Update dependencies

# Git worktree (for multi-agent workflows)
git worktree add ../project-feature feature-branch
git worktree list
git worktree remove ../project-feature
```

## Development Workflow

1. **ALWAYS** run type checking/linting after code changes (e.g., `deno check`, `go vet`, `cargo check`)
2. **ALWAYS** format code before committing using project's formatter
3. **ALWAYS** run relevant tests before pushing changes
4. **NEVER** commit without running pre-commit checks
5. **ALWAYS** use semantic commit messages (feat:, fix:, docs:, refactor:, test:, chore:)

### AI-Assisted Development Pattern

1. **WRITE** failing tests first (test-driven development)
2. **GENERATE** implementation with AI assistance
3. **VERIFY** code meets requirements and security standards
4. **REFACTOR** at appropriate checkpoints, not continuously
5. **LOG** extensively for debugging AI-generated code

### Context Management

- **PROVIDE** clear, specific requirements to minimize context gaps
- **INCLUDE** relevant project context in prompts
- **DOCUMENT** assumptions and decisions in code comments

## Security & Code Verification

### AI-Generated Code Review

- **ALWAYS** review and understand AI-generated code before accepting
- **NEVER** commit code you don't fully understand
- **RUN** security scanning on all generated code
- **VERIFY** all third-party dependencies suggested by AI
- **TEST** edge cases and error handling thoroughly

### Sensitive Data Protection

- **NEVER** share API keys, credentials, or proprietary code with AI
- **USE** environment variables or secret management tools
- **SANITIZE** logs and debug output before sharing

## Project Planning & Coordination

### PLAN.md Adherence

When a `PLAN.md` file exists in the project root, **YOU MUST**:

1. **READ** the PLAN.md file at the start of each session to understand current tasks and priorities
2. **FOLLOW** the task breakdown and execution strategy defined in the plan
3. **RESPECT** task dependencies and join points for multi-agent coordination
4. **UPDATE** task status in the plan as work progresses
5. **COORDINATE** with other agents at defined synchronization points
6. **USE** the TodoWrite tool to track individual tasks from the plan

### Multi-Agent Workflow

When working as part of a multi-agent team:

- **CHECK** `/tmp/{project-name}/project-status.md` or coordination files for shared state
- **WORK** only on assigned tasks to avoid conflicts
- **COMMUNICATE** progress through PR comments or status files
- **WAIT** at join points until all parallel work is complete
- **MERGE** work carefully following the plan's integration strategy
- **USE** git worktrees to work on separate branches without conflicts
- **CREATE** status files in `/tmp/{project-name}/claude-scratch/` for inter-agent communication
- **COORDINATE** using shared JSON status files for structured updates in project-specific directories

## Performance & Optimization

### Token Efficiency

- **OPTIMIZE** prompts for clarity and brevity
- **BATCH** related operations in single requests
- **USE** structured outputs (JSON) for parsing efficiency
- **CACHE** common patterns and solutions locally

### Parallel Development

- **USE** Docker containers for isolated AI agent environments
- **IMPLEMENT** clear synchronization points for multi-agent work
- **MAINTAIN** shared state files in `/tmp/{project-name}/`

## Task Management

Use the task management system for tracking work items:

- **Location**: Tasks are stored in `/tasks/` directory with `status.json` index
- **Commands**: Use `/task-create`, `/task-update`, `/task-list`, `/task-show`, `/task-log`, `/task-search`, `/task-archive`
- **Format**: Tasks are markdown files with structured metadata
- **Integration**: Active tasks sync with TodoWrite for session tracking

## File Organization

- `/src/` - Source code
- `/tests/` - Test files organized by type
- `/scripts/` - Deno automation scripts
- `/tasks/` - Task management files (markdown + status.json)
- `deno.json` - Project configuration and tasks
- `import_map.json` - Import mappings (if needed)

## Documentation Style

### README Files

**KEEP README FILES CONCISE AND SCANNABLE:**

- **Maximum 50 lines** for most projects
- **No excessive emojis** or decorative elements
- **Essential sections only**: Purpose, Quick Start, Key Commands
- **No verbose explanations** - let code and comments speak
- **Single quick start command** when possible
- **Brief feature lists** without detailed descriptions
- **Minimal project structure** - only if complex
- **Essential links only** - avoid resource dumps

**Example concise README:**

````markdown
# Project Name

Brief one-line description of what it does.

## Quick Start

```bash
deno task init && deno task dev
```
````

## Key Commands

- `deno task test` - Run tests
- `deno task build` - Build project

## Features

- Core feature 1
- Core feature 2
- Core feature 3

```
**Avoid:**
- Long feature descriptions
- Extensive project structure diagrams  
- Multiple installation methods
- Verbose technical explanations
- Marketing-style language
- Detailed configuration options in main README

## Claude Code Features

### Thinking Modes
- `think` - Standard mode (4,000 tokens)
- `think hard` - Enhanced analysis
- `think harder` - Deep computation
- `ultrathink` - Maximum analysis (31,999 tokens)

### Effective Usage
- **USE** thinking modes for complex architectural decisions
- **AVOID** over-thinking simple tasks
- **BALANCE** computation time with task complexity

## IMPORTANT Notes

- **YOU MUST** follow these guidelines exactly as written
- **ALWAYS** ask for clarification if requirements conflict
- **NEVER** use deprecated patterns or old import styles
- **ALWAYS** prioritize performance and type safety
```
