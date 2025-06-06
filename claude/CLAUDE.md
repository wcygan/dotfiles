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
- **CHECK** `/tmp/project-status.md` or coordination files for shared state
- **WORK** only on assigned tasks to avoid conflicts
- **COMMUNICATE** progress through PR comments or status files
- **WAIT** at join points until all parallel work is complete
- **MERGE** work carefully following the plan's integration strategy
- **USE** git worktrees to work on separate branches without conflicts
- **CREATE** status files in `/tmp/claude-scratch/` for inter-agent communication
- **COORDINATE** using shared JSON status files for structured updates

## File Organization

- `/src/` - Source code
- `/tests/` - Test files organized by type
- `/scripts/` - Deno automation scripts
- `deno.json` - Project configuration and tasks
- `import_map.json` - Import mappings (if needed)

## IMPORTANT Notes

- **YOU MUST** follow these guidelines exactly as written
- **ALWAYS** ask for clarification if requirements conflict
- **NEVER** use deprecated patterns or old import styles
- **ALWAYS** prioritize performance and type safety