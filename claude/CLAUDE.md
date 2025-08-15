# CLAUDE.md

Personal development preferences and guidelines for AI assistants working on my projects.

## Incremental Development Methodology

**CORE PHILOSOPHY: Deliver working, tested software in small, safe steps for perpetually releasable codebase.**

### The Incremental Loop

1. **Identify small next step** (single function, feature slice, or bug fix)
2. **Write test first** (TDD approach - define expected behavior)
3. **Implement minimal solution** (make test pass)
4. **Run all relevant tests** (ensure green build)
5. **Format & lint code** (automated quality checks)
6. **Commit atomically** (one logical change + tests)
7. **Repeat immediately**

### Benefits

- **Low defect risk** - Problems detected immediately
- **Fast feedback** - Know instantly if change breaks something
- **Easy rollback** - Each commit is a safe restore point
- **Better traceability** - Clear evolution of features
- **Reduced merge conflicts** - Smaller changes merge cleanly

### Never Commit Unless

- All tests pass (green build state)
- Code is formatted and linted
- Change is atomic (single logical unit)
- Includes corresponding test updates

## Technology Stack & Tools

### Backend Languages

- **Go**: ConnectRPC for RPC services, 95%+ test coverage, table-driven tests
- **Rust**: Axum + Tokio for web services, parallel units/sequential integration
- **Java**: Spring Boot + Quarkus, jOOQ over JPA

### Infrastructure & Scripting

- **Scripting**: Deno TypeScript only (JSR imports: `@std/*`)
- **Infrastructure**: Talos Linux Kubernetes, Postgres, DragonflyDB, RedPanda, ScyllaDB
- **Task Runner**: `deno.json` with standardized tasks (up/down/dev/test/build)

### Modern CLI Tools

- **PREFER**: `rg`, `fd`, `bat`, `eza`, `jq`, `yq`, `fzf`, `delta`, `gh`
- **AVOID (use only if needed)**: `grep`, `find`, `cat`, `ls`, `df`, `top`, `xxd`

## Development Workflow

### Feature Implementation

1. **Create git worktree** for isolated development
2. **Deploy sub-agents** to analyze existing patterns, tests, dependencies (don't use too many; usually 2-3 is enough)
3. **Write tests FIRST** (define expected behavior)
4. **Implement following discovered patterns**
5. **Run tests & verify** (must be green)
6. **Create PR using `gh pr create`**
7. **Remove worktree after merge**

### Debugging Process

1. **Read error & identify file:line**
2. **Launch 2 parallel agents**: analyze error, search similar patterns, find tests, check git history
3. **Synthesize findings** from all agents
4. **Apply minimal fix** addressing root cause
5. **Verify fix doesn't break existing tests**

### Standard Tasks

```bash
deno task up      # Start all services (e.g., with Docker)
deno task down    # Stop all services  (e.g., with Docker)
deno task dev     # Development mode
deno task test    # Run all tests
deno task build   # Production build
```

## Performance & Parallelization

**CRITICAL: Use sub-agents carefully**

### When to Use Sub-Agents (5x speedup)

- **Codebase exploration**: Multi-file analysis
- **Research tasks**: Information gathering
- **Code quality checks**: Multiple analyzers
- **Migration planning**: Impact analysis across modules
- **Bug investigation**: Pattern searches across files

### Task Tool Pattern

```
[Launch 2-3 agents simultaneously in single response]
Task 1: "Specific focused analysis task"
Task 2: "Independent parallel task" 
Task 3: "Another concurrent analysis"
Main agent synthesizes all results
```

### Never Use Task Tool For

- Single file reads (use Read directly)
- Sequential dependencies
- Direct file modifications
- Trivial single operations

## Code Standards

### Universal Rules

- Semantic commits: `feat:`, `fix:`, `docs:`
- Single test execution over full suites
- TestContainers for integration tests
- Format code before every commit
- Never commit without green builds

### Language-Specific

- **Deno/TypeScript**: JSR imports only, Dax for shell, organize tests in `/tests/unit/integration/e2e/`
- **Go**: ConnectRPC, table-driven tests, 95%+ coverage
- **Rust**: Axum + Tokio, hybrid testing approach
- **Java**: jOOQ over JPA, TestContainers

## Git & Testing Practices

### Git Worktrees

- One worktree per Claude session: `../project-feature-name`
- Independent environments for parallel development
- Remove after PR merge

### Testing Strategy

- **Write tests first** (TDD approach)
- **Run single tests** for fast feedback
- **All tests must pass** before commit
- **TestContainers** for integration testing
- **Parallel units, sequential integration**

### Commit Requirements

```bash
# Must pass before commit
deno fmt        # Format code
deno lint       # Lint check  
deno test       # All tests pass
git commit      # Atomic change + tests
```

## Task Tool Patterns

### Comprehensive Analysis (2-3 agents to work on these tasks)

```
Task 1: "Map all API endpoints and handlers"
Task 2: "Analyze database schema and models"  
Task 3: "Document authentication/authorization"
Task 4: "Find external service integrations"
Task 5: "Analyze test coverage and gaps"
```

### Code Quality Audit (2-3 agents to work on these tasks)

```
Task 1: "Calculate cyclomatic complexity hotspots"
Task 2: "Find code duplication >80% similarity"
Task 3: "Identify functions >50 lines needing refactor"
Task 4: "Find TODO/FIXME/HACK technical debt"
Task 5: "Analyze test quality and coverage gaps"
Task 6: "Detect dead code and unused exports"
```

### Performance Guidelines

- **Expected speedup**: 5-10x for parallelizable tasks
- **Token efficiency**: 2000-4000 tokens per sub-agent
- **Batch execution**: Launch 2-3 agents per response (don't go overboard; we don't need 8 agents at once)
- **Clear boundaries**: Independent, non-overlapping scopes

## Critical Rules & Reminders

### Immutable Constraints

- **NEVER** use legacy tools (grep, find, cat, ls)
- **ALWAYS** use Deno TypeScript for scripts
- **ALWAYS** write tests before implementation
- **ALWAYS** commit with green builds only
- **ALWAYS** use sub-agents for parallel tasks

### Communication Style

- **Concise responses** (max 4 lines unless asked)
- **No unnecessary preamble/postamble**
- **Include code snippets when relevant**
- **Direct answers without elaboration**

### Documentation Standards

- **README files**: Maximum 50 lines
- **Essential sections only**: Purpose, Quick Start, Key Commands
- **Single quick-start command** when possible
- **No excessive emojis or decorations**

### Performance Mindset

- **Default to parallel execution** (2-3 agents)
- **Don't abuse parallel agents** (don't go overboard; we don't need 8 agents at once — keep it simple)
- **Never analyze files sequentially** when parallelizable
- **Launch agents immediately** in first response
- **Synthesize results** after parallel completion

**Remember: Small steps, tests first, green builds, atomic commits. This is the path to maintainable, reliable software.**
