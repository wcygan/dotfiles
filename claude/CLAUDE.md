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
2. **Deploy sub-agents with Task tool** to analyze:
   ```
   [Launch 4 parallel Task tools in single response]
   Task 1: "Analyze existing code patterns in [feature_area]. Find similar implementations, naming conventions, and architectural patterns."
   Task 2: "Find all test files related to [feature_area]. Analyze testing patterns, mocking strategies, and coverage."
   Task 3: "Map all dependencies and integration points for [feature_area]. Include imports, exports, and API contracts."
   Task 4: "Search for similar features in the codebase. Document their implementation approach and lessons learned."
   ```
3. Synthesize findings and write tests FIRST (TDD approach)
4. Implement feature following discovered patterns
5. Run tests and verify
6. Create PR using `gh pr create`
7. Remove worktree after merge

### Debugging Process

1. Read error message and identify file/line
2. **Launch parallel investigation with Task tool**:
   ```
   [Deploy 4 Task tools simultaneously]
   Task 1: "Analyze the error at [file:line]. Include 50 lines of context, check function signatures, and trace the call stack."
   Task 2: "Search for similar error patterns: '[error_message]' across the codebase. Find how they were resolved."
   Task 3: "Find tests for [affected_function/module]. Identify what behavior is expected and what edge cases exist."
   Task 4: "Check git history for [affected_file] in the last 30 commits. Find recent changes that might have introduced the bug."
   ```
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

#### Task Tool Usage

The Task tool is Claude Code's primary mechanism for launching sub-agents. It enables true parallel processing by delegating operations to specialized sub-agents that work simultaneously.

**Key Task Tool Concepts:**

1. **Parallel vs Sequential**: The Task tool transforms sequential workflows into parallel operations
2. **Token Efficiency**: Each sub-agent operates with focused context, reducing overall token usage
3. **Coordination**: The main agent synthesizes results from all sub-agents
4. **Performance**: Expect 5-10x speedup for parallelizable tasks

**Task Tool Invocation Pattern:**

```
When you need to analyze multiple aspects of a codebase:
1. Launch multiple Task tools in a single response
2. Each Task tool gets a specific, focused prompt
3. All tasks execute simultaneously
4. Main agent receives all results for synthesis
```

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

#### Task Grouping Strategies

**Effective Task Bundling:**

1. **Related Operations**: Group tasks that analyze the same domain
   - Example: All security-related checks in one batch
   - Example: All test-related operations together

2. **Resource-Based Grouping**: Tasks that operate on similar resources
   - Example: All database-related code analysis
   - Example: All API endpoint discovery

3. **Depth-Based Grouping**: Balance between breadth and depth
   - Shallow: Quick overview across many files
   - Deep: Detailed analysis of specific components

**Token Optimization Guidelines:**

- **Budget per Agent**: Allocate ~2000-4000 tokens per sub-agent task
- **Context Pruning**: Provide only essential context to each sub-agent
- **Result Format**: Request structured output for easier synthesis
- **Batching**: Launch 5-10 agents per batch for optimal throughput

#### Task Tool Anti-Patterns

**NEVER use Task tool for:**

1. **Simple File Reads**: Use Read tool directly for single files
2. **Sequential Dependencies**: Operations that must happen in order
3. **Stateful Operations**: Tasks requiring shared state
4. **Single-Line Commands**: Operations completable in one tool call

**Common Mistakes to Avoid:**

- Launching agents one-by-one (always batch in single response)
- Over-specifying agent tasks (keep prompts focused)
- Creating dependencies between parallel agents
- Using Task tool for trivial operations

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

**Implementation with Task Tool:**

```
I'll analyze your authentication system using 5 parallel agents:

[Launch all in single response]
Task 1: "Search for all REST endpoints, GraphQL resolvers, and RPC methods that handle authentication. Include login, logout, token refresh, and session management."
Task 2: "Analyze security implementations: password hashing, token generation, session storage, CSRF protection, and rate limiting."
Task 3: "Find all test files related to authentication and calculate coverage. Identify untested scenarios."
Task 4: "Document the complete authentication flow from user login to session expiry, including all middleware and guards."
Task 5: "Scan for OWASP Top 10 vulnerabilities in authentication: SQL injection, XSS, broken authentication, etc."
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

**Implementation with Task Tool:**

```
I'll analyze the refactoring impact of [module_name] using 5 parallel agents:

[Launch simultaneously]
Task 1: "Find all files that directly import or require [module_name]. List each import with its purpose."
Task 2: "Trace indirect dependencies: files that use components which depend on [module_name]."
Task 3: "Identify all test files that reference [module_name] and test scenarios that would break."
Task 4: "Search for string references to [module_name] in configs, scripts, and documentation."
Task 5: "Find all documentation, comments, and README sections mentioning [module_name]."
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

**Implementation with Task Tool:**

```
I'll investigate performance issues using 5 specialized agents:

[Batch execution]
Task 1: "Find all database queries. Identify queries without indexes, queries in loops, and queries fetching unnecessary data."
Task 2: "Analyze algorithm complexity in hot paths. Find O(n²) or worse algorithms, nested loops, and recursive functions."
Task 3: "Detect N+1 query problems in ORMs, GraphQL resolvers, and data fetching layers."
Task 4: "Identify caching opportunities: repeated calculations, frequent database reads, and API calls that could be memoized."
Task 5: "Find blocking I/O operations, synchronous file operations, and unoptimized async/await usage."
```

### Concrete Task Tool Examples

**Example 1: Full Stack Application Analysis (10 Agents)**

```
When asked to understand a full-stack application:

[Single response with 10 parallel tasks]
Task 1: "Map all API endpoints (REST/GraphQL/WebSocket) with their HTTP methods, paths, and handlers"
Task 2: "Analyze the database schema, models, migrations, and relationships"
Task 3: "Document the frontend routing structure and page components"
Task 4: "Identify all external service integrations (APIs, webhooks, third-party services)"
Task 5: "Find authentication/authorization implementation across the stack"
Task 6: "Map the state management approach (Redux, Context, Zustand, etc.)"
Task 7: "Analyze the build and deployment configuration"
Task 8: "Document all environment variables and configuration patterns"
Task 9: "Find all background jobs, cron tasks, and async workers"
Task 10: "Identify testing strategies and calculate coverage metrics"
```

**Example 2: Security Audit (8 Agents)**

```
For comprehensive security analysis:

[Batch all agents together]
Task 1: "Scan for SQL injection vulnerabilities in all database queries"
Task 2: "Find XSS vulnerabilities in user input handling and output rendering"
Task 3: "Check for insecure authentication: weak passwords, missing MFA, session issues"
Task 4: "Identify exposed secrets, API keys, or credentials in code"
Task 5: "Analyze CORS configuration and API security headers"
Task 6: "Find insecure dependencies with known CVEs"
Task 7: "Check for CSRF vulnerabilities and missing protections"
Task 8: "Identify information disclosure in error messages and logs"
```

**Example 3: Code Quality Assessment (7 Agents)**

```
For rapid code quality analysis:

[All agents in parallel]
Task 1: "Calculate cyclomatic complexity for all functions and identify hotspots"
Task 2: "Find code duplication across the codebase with similarity threshold >80%"
Task 3: "Identify functions longer than 50 lines that need refactoring"
Task 4: "Find all TODO, FIXME, HACK comments and technical debt markers"
Task 5: "Analyze test quality: assertion density, test naming, coverage gaps"
Task 6: "Find circular dependencies and architectural violations"
Task 7: "Identify dead code, unused exports, and unreachable code paths"
```

**Example 4: Migration Planning (6 Agents)**

```
When planning a technology migration:

[Simultaneous execution]
Task 1: "Find all usages of [old_technology] across the codebase"
Task 2: "Identify breaking changes and incompatibilities with [new_technology]"
Task 3: "Analyze data migration requirements and schema changes"
Task 4: "Find all tests that will need updates for the migration"
Task 5: "Identify configuration and deployment changes needed"
Task 6: "Create effort estimates based on file count and complexity"
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

## Task Tool Performance Metrics

**Expected Performance Gains:**

- **5-10x faster** for multi-file analysis tasks
- **8x faster** for comprehensive codebase exploration
- **10x faster** for security audits and migration planning
- **Instant** results for previously sequential operations

**Performance Comparison:**

| Task Type              | Sequential Time | Parallel Time (Task Tool) | Speedup |
| ---------------------- | --------------- | ------------------------- | ------- |
| Codebase Analysis      | 50-60 seconds   | 5-8 seconds               | ~10x    |
| Security Audit         | 40-50 seconds   | 5-7 seconds               | ~8x     |
| Test Coverage Analysis | 30-40 seconds   | 4-6 seconds               | ~7x     |
| Dependency Mapping     | 45-55 seconds   | 6-8 seconds               | ~7x     |
| Migration Planning     | 60-70 seconds   | 8-10 seconds              | ~7x     |

## Critical Reminders

- **YOU MUST** follow these guidelines exactly
- **ALWAYS** use sub-agents for parallelizable tasks
- **PRIORITIZE** parallel execution over sequential processing
- **NEVER** use deprecated patterns or legacy tools
- **ALWAYS** prioritize performance and type safety
- **THINK** in terms of concurrent workflows
- **EXECUTE** tasks deterministically when possible
- **LEVERAGE** up to 10 concurrent sub-agents for maximum efficiency
- **REMEMBER** the Task tool is your primary mechanism for achieving 5-10x performance gains
