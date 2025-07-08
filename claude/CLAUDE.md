# CLAUDE.md

Personal development preferences and guidelines for AI assistants working on my projects.

## Project Overview & Context

### About

This document defines immutable system rules for AI collaboration across my development projects. These instructions supersede conversational prompts and ensure consistent, high-quality assistance.

### Technology Stack

- **Backend Languages**: Go (ConnectRPC), Rust (Axum), Java (Spring Boot/Quarkus)
- **Scripting**: Deno TypeScript (mandatory - no Bash/Python)
- **Web Framework**: Deno Fresh 2.0
- **Infrastructure**: Talos Linux Kubernetes, Postgres, DragonflyDB, RedPanda, ScyllaDB
- **Version Control**: Git with worktree-based parallel development

### Project Structure Pattern

```
/project-root
├── ...            # Other project-specific files and directories
├── /scripts       # Deno automation scripts
├── /docs          # Documentation (Either pure markdown or Docusaurus)
├── deno.json      # Task runner & configuration
└── CLAUDE.md      # Project-specific AI instructions
```

## Operational Rules & Constraints

### File Access Permissions

**ALLOWED TO USE:**

- Modern CLI tools: `rg`, `fd`, `bat`, `eza`, `jq`, `yq`, `fzf`, `delta`
- Deno for all scripting with JSR imports (`@std/*`)
- Git worktrees for parallel development
- GitHub CLI (`gh`) for all GitHub operations

**FORBIDDEN TO USE:**

- Legacy tools: `grep`, `find`, `cat`, `ls`, `df`, `top`, `xxd`
- Bash/Python for scripting (use Deno TypeScript)
- Web interface for GitHub operations (use `gh` CLI)

### Code Standards

#### Universal Rules

- Write clear, descriptive test names
- Run single tests over full suites for performance
- Use semantic commit messages (feat:, fix:, docs:, etc.)
- Format code before committing
- Never commit without running pre-commit checks
- TestContainers for integration tests

#### Language-Specific Standards

**Deno/TypeScript:**

- JSR imports only: `import { walk } from "@std/fs"`
- Use Dax for shell operations
- Organize tests: `/tests/unit/`, `/tests/integration/`, `/tests/e2e/`

**Go:**

- Use ConnectRPC for RPC services
- Target 95%+ test coverage
- Table-driven tests standard

**Rust:**

- Use Axum + Tokio for web services
- Hybrid testing: parallel units, sequential integration

**Java:**

- Spring Boot with Quarkus
- jOOQ over JPA

## Development Workflows

### Feature Implementation Process

1. Create git worktree for isolated development
2. Read existing code structure
3. Write tests FIRST (TDD approach)
4. Implement feature
5. Run tests and verify
6. Create PR using `gh pr create`
7. Remove worktree after merge

### Debugging Process

1. Read error message and identify file/line
2. Check immediate context (±5 lines)
3. Read entire function if unclear
4. Trace call stack if necessary
5. Propose minimal fix addressing root cause

### Project Lifecycle Commands

All projects MUST use Deno as task runner with standardized commands:

- `deno task up` - Start all services
- `deno task down` - Stop all services
- `deno task dev` - Development mode
- `deno task test` - Run all tests
- `deno task build` - Production build
- `deno task init` - Initialize environment

## Communication Standards

### Response Format

- Be direct and concise (max 4 lines unless asked)
- Use bullet points for multiple items
- Include code snippets when relevant
- Explain reasoning only for significant decisions

### Code Output Format

- Include necessary imports
- Follow project's existing patterns
- Use descriptive variable names
- Add comments only for complex logic

### Error Handling

- Never hide or suppress errors
- Provide clear, actionable error messages
- Include relevant context
- Suggest specific solutions

### Documentation Style

- README files: Maximum 50 lines
- No excessive emojis or decorations
- Essential sections only: Purpose, Quick Start, Key Commands
- Single quick-start command when possible

## Module-Specific Instructions

### Sub-Agent Architecture

**Use sub-agents for:**

- Parallel research and analysis (up to 10 concurrent)
- File discovery and pattern searches
- Documentation gathering
- Test coverage analysis

**Never use sub-agents for:**

- Decision-making or code writing
- Shared file modifications
- Git operations
- Configuration updates

### Git Worktrees

- One worktree per Claude session
- Naming: `../project-feature-name`
- Independent environment per worktree
- Remove after PR merge

## Examples & Patterns

### Deno Task Configuration

```json
{
  "tasks": {
    "up": "docker compose up -d && cd backend && cargo run",
    "down": "docker compose down",
    "test": "deno task test:backend && deno task test:frontend",
    "dev": "docker compose up -d db && concurrently \"cd backend && cargo watch\" \"cd frontend && deno task dev\""
  }
}
```

### Modern CLI Usage

```bash
# Search code (NEVER use grep)
rg "pattern" --type rust

# Find files (NEVER use find)
fd ".rs$" src/

# View files (NEVER use cat)
bat src/main.rs

# List files (NEVER use ls)
eza -la --git

# Process JSON (ALWAYS use jq)
kubectl get pods -o json | jq '.items[].metadata.name'
```

### Pull Request Pattern

```bash
gh pr create --title "feat: add user auth" --body "$(cat <<'EOF'
## Summary
- Implement OAuth2 authentication
- Add user session management

## Test Plan
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Related Issues
Fixes #123
EOF
)"
```

## Context Window Management

### Priority Information (Always Include)

1. Current task definition
2. Relevant file contents
3. Error messages and stack traces
4. Direct dependencies

### Secondary Information (Include if Space)

1. Related test files
2. Configuration details
3. Similar code examples
4. Historical context

### Exclude Unless Necessary

1. Boilerplate code
2. Unrelated modules
3. Generated files
4. Build artifacts

## Thinking Modes

Use extended thinking for complex tasks:

- `think` - Standard analysis (4,000 tokens)
- `think hard` - Enhanced analysis
- `think harder` - Deep computation
- `ultrathink` - Maximum analysis (31,999 tokens)

## Critical Reminders

- **YOU MUST** follow these guidelines exactly
- **ALWAYS** ask for clarification if requirements conflict
- **NEVER** use deprecated patterns or legacy tools
- **ALWAYS** prioritize performance and type safety
- **THINK** programmatically, not conversationally
- **EXECUTE** tasks deterministically when possible
