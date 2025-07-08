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

## Performance-First Mindset

**ALWAYS optimize for parallel execution.** When facing any task that can be decomposed into independent subtasks, immediately delegate to sub-agents. This includes research, analysis, file discovery, and multi-aspect evaluations. Sequential execution should be the exception, not the rule.

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
2. **Deploy sub-agents** to analyze:
   - Agent 1: Existing code structure and patterns
   - Agent 2: Related test files and coverage
   - Agent 3: Dependencies and integration points
   - Agent 4: Similar implementations in codebase
3. Synthesize findings and write tests FIRST (TDD approach)
4. Implement feature following discovered patterns
5. Run tests and verify
6. Create PR using `gh pr create`
7. Remove worktree after merge

### Debugging Process

1. Read error message and identify file/line
2. **Launch parallel investigation**:
   - Agent 1: Analyze error context and surrounding code
   - Agent 2: Search for similar error patterns in codebase
   - Agent 3: Check related test files for expected behavior
   - Agent 4: Investigate recent changes in affected files
3. Synthesize findings from all agents
4. Propose minimal fix addressing root cause
5. Verify fix doesn't break existing tests

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

**CRITICAL: Prioritize sub-agent delegation for maximum performance and efficiency.**

Sub-agents enable parallel execution, dramatically reducing task completion time through concurrent processing. Claude Code automatically manages up to 10 parallel agents, queuing additional tasks as needed.

**ALWAYS use sub-agents for:**

- **Codebase exploration**: Parallel analysis of directories, file patterns, and code structure
- **Multi-aspect analysis**: Simultaneously analyze security, performance, tests, and documentation
- **Research tasks**: Gather information from multiple sources concurrently
- **File discovery**: Search for patterns, keywords, or structures across the codebase
- **Documentation tasks**: Generate or analyze docs for multiple components in parallel
- **Test analysis**: Coverage reports, test pattern identification, missing test detection
- **Dependency mapping**: Trace dependencies and usage patterns throughout the codebase
- **Code quality checks**: Run multiple linters, formatters, or analyzers simultaneously
- **Migration planning**: Analyze impact across different modules concurrently
- **Bug investigation**: Search for related issues across multiple files/directories

**Benefits of sub-agent delegation:**

- **5-10x faster execution** through parallelization
- **Comprehensive coverage** without sequential bottlenecks
- **Reduced token usage** per individual agent
- **Better organization** with clear task separation
- **Scalability** for large codebases

**Sub-agent best practices:**

1. **Launch early and often**: Start sub-agents as soon as you identify parallel opportunities
2. **Clear boundaries**: Each sub-agent should have a well-defined, independent scope
3. **Batch related tasks**: Group similar operations for efficiency
4. **Synthesize results**: Main agent should aggregate and analyze all findings

**Only avoid sub-agents for:**

- Sequential operations with dependencies
- Direct file modifications (unless independent)
- Git operations requiring coordination
- Single-file simple operations

### Git Worktrees

- One worktree per Claude session
- Naming: `../project-feature-name`
- Independent environment per worktree
- Remove after PR merge

## Examples & Patterns

### Sub-Agent Delegation Patterns

**Pattern 1: Comprehensive Codebase Analysis**

```
Deploy 5 agents to analyze the authentication system:
- Agent 1: Find all authentication endpoints
- Agent 2: Analyze security implementations
- Agent 3: Check test coverage for auth
- Agent 4: Document current auth flows
- Agent 5: Identify potential vulnerabilities
```

**Pattern 2: Refactoring Impact Analysis**

```
Before refactoring a core module, deploy agents:
- Agent 1: Find all direct imports/usage
- Agent 2: Identify indirect dependencies
- Agent 3: Analyze test dependencies
- Agent 4: Check for string references
- Agent 5: Review documentation mentions
```

**Pattern 3: Performance Investigation**

```
For performance issues, launch parallel analysis:
- Agent 1: Profile database queries
- Agent 2: Analyze algorithm complexity
- Agent 3: Check for N+1 problems
- Agent 4: Review caching opportunities
- Agent 5: Identify blocking operations
```

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
- **ALWAYS** use sub-agents for parallelizable tasks
- **PRIORITIZE** parallel execution over sequential processing
- **NEVER** use deprecated patterns or legacy tools
- **ALWAYS** prioritize performance and type safety
- **THINK** in terms of concurrent workflows
- **EXECUTE** tasks deterministically when possible
- **LEVERAGE** up to 10 concurrent sub-agents for maximum efficiency
