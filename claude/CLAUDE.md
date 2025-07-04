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

#### Fresh 2.0 Essentials

Fresh 2.0 (alpha) is production-ready but has rough edges. Use fallback strategies for styling, proxy patterns for APIs, and pre-built Docker approaches for reliable deployments.

**Setup & Configuration:**

- Use JSR imports: `jsr:@fresh/core@^2.0.0-alpha.22` instead of deno.land URLs
- Initialize: `deno run -Ar jsr:@fresh/init@2.0.0-alpha.34 myapp`
- Essential tasks: `dev`, `build`, `start` with proper --watch flags
- Configure `nodeModulesDir: "auto"` for npm package compatibility

**Styling Strategy:**

- **ALWAYS leverage Tailwind's Preflight CSS reset** for cross-browser consistency and design system foundation
- Tailwind plugin is unreliable - implement CSS fallbacks in `static/styles.css`
- Define key utilities manually: `.min-h-screen`, `.flex`, `.items-center`, `.justify-center`
- Use AppShell pattern for consistent layout wrapper
- Embrace Preflight's opinionated defaults (no margins, unstyled headings/lists) for intentional design

**ConnectRPC Integration:**

- Use API proxy routes in `routes/api/[...path].ts` for backend communication
- Set up transport with `baseUrl: "/api"` for client-side RPC calls
- Use buf.build packages via npm imports for type safety

**Docker Best Practices:**

- Pre-build assets locally with `deno task build` before Docker build
- Copy built assets (including `_fresh/`) to container
- Use `deno cache --node-modules-dir=auto` for dependency caching
- Configure unique ports (e.g., 8007) to avoid conflicts

**Critical Notes:**

- Fresh 2.0 stable target: Q3 2025 - current alpha is production-ready but evolving
- Always have CSS fallbacks when Tailwind plugin fails to generate utilities
- npm registry issues in Docker - pre-building recommended
- Island architecture: `islands/` for interactive, `components/` for static

## Infrastructure Choices

IMPORTANT: I run a Talos Linux Kubernetes Cluster. Use these modern alternatives:

- **Database**: Postgres (NOT MySQL)
- **Cache**: DragonflyDB (NOT Redis)
- **Streaming**: RedPanda (NOT Kafka)
- **NoSQL**: ScyllaDB (NOT Cassandra)

## Modern Development Tools

### Preferred Command-Line Tools

**CRITICAL: When using Bash commands, ALWAYS prefer these modern, fast alternatives over legacy tools:**

- **ripgrep (rg)**: Use instead of grep for searching code - **NEVER use grep**
- **fd**: Use instead of find for finding files - **NEVER use find**
- **fzf**: Use for interactive fuzzy finding and selection
- **bat**: Use instead of cat for syntax-highlighted file viewing - **NEVER use cat for code**
- **exa/eza**: Use instead of ls for better file listings - **NEVER use plain ls**
- **delta**: Use for better git diffs - **NEVER use plain git diff**
- **zoxide**: Use instead of cd for smarter directory navigation
- **duf**: Use instead of df for disk usage - **NEVER use df**
- **htop/btop**: Use instead of top for process monitoring - **NEVER use top**
- **jq**: Use for JSON processing and manipulation - REQUIRED for all JSON tasks
- **yq**: Use for YAML processing and manipulation - REQUIRED for all YAML tasks
- **hexyl**: Use for hex viewing of binary files - **NEVER use xxd or hexdump**

**IMPORTANT**: These tools are NOT optional suggestions - they are MANDATORY preferences. When writing any Bash commands or scripts, you MUST use these modern alternatives instead of their legacy counterparts.

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

## Parallel Claude Code Sessions with Git Worktrees

Run multiple Claude Code sessions simultaneously on different features using Git worktrees, enabling true parallel development without branch switching conflicts.

### Git Worktree Workflow

**Create a new worktree for parallel development:**

```bash
# Create worktree for a feature branch
git worktree add ../project-feature feature-branch

# Create worktree with new branch
git worktree add -b new-feature ../project-new-feature

# Create worktree from specific commit or tag
git worktree add ../project-hotfix hotfix-branch origin/main

# List all worktrees
git worktree list

# Remove worktree when done
git worktree remove ../project-feature
```

### Best Practices for Parallel Sessions

1. **One Branch Per Claude Session**: Each Claude Code instance works on its own dedicated branch
2. **Descriptive Naming Convention**: Use clear worktree paths like `../project-auth-feature` or `../project-fix-bug-123`
3. **Independent Development**: Each worktree has its own working directory and dependencies
4. **Clean Separation**: Keep different features/fixes in separate branches to avoid conflicts
5. **PR-Based Integration**: Merge work back to main through pull requests

### Typical Parallel Workflow

```bash
# Terminal 1: Main development
cd ~/projects/myapp
claude code  # Working on main branch refactoring

# Terminal 2: New feature development
git worktree add -b feature-oauth ../myapp-oauth
cd ../myapp-oauth
deno task init  # Initialize dependencies for this worktree
claude code  # Working on OAuth feature independently

# Terminal 3: Critical bug fix
git worktree add -b fix-memory-leak ../myapp-fix-memory origin/main
cd ../myapp-fix-memory
claude code  # Working on memory leak fix independently

# Terminal 4: Experimental feature
git worktree add -b experiment-ai-chat ../myapp-ai-experiment
cd ../myapp-ai-experiment
claude code  # Working on experimental AI features
```

### Project Setup in Each Worktree

**IMPORTANT**: Each worktree needs its own environment setup:

```bash
# After creating a new worktree
cd ../project-new-feature

# For Deno projects
deno task init
deno cache --reload

# For Node projects
npm install

# For Rust projects
cargo build

# For Go projects
go mod download
```

### Managing Multiple Features

**Organizing Active Development:**

```bash
# See all active worktrees
git worktree list

# Example output:
# /Users/you/projects/myapp          abc123 [main]
# /Users/you/projects/myapp-oauth    def456 [feature-oauth]
# /Users/you/projects/myapp-fix      ghi789 [fix-memory-leak]

# Clean up completed features
cd ../myapp-oauth
gh pr create --title "Add OAuth authentication" --body "..."
cd ../myapp
git worktree remove ../myapp-oauth
```

### Advantages of Parallel Worktrees

- **No Context Switching**: Each session maintains its own branch context and file state
- **True Parallelism**: Work on multiple features without waiting or stashing changes
- **Isolated Environments**: Dependencies and build artifacts don't interfere between features
- **Faster Development**: No need to switch branches, stash changes, or rebuild between tasks
- **Better Organization**: Physical separation makes it clear what each session is working on
- **Risk Mitigation**: Experimental changes isolated from stable development

### Integration Strategy

**Merging Parallel Work:**

1. Complete feature development in worktree
2. Run tests and verify changes: `deno task test`
3. Create PR from worktree: `gh pr create`
4. Review and merge PR through GitHub
5. Remove worktree after merge: `git worktree remove ../feature-path`
6. Update main and pull changes to other worktrees as needed

### Common Patterns

**Feature Development:**

```bash
git worktree add -b feature-user-profiles ../app-user-profiles
cd ../app-user-profiles
# Develop feature in isolation
```

**Bug Fixes:**

```bash
git worktree add -b fix-issue-123 ../app-fix-123 origin/main
cd ../app-fix-123
# Fix bug without disrupting feature work
```

**Experimentation:**

```bash
git worktree add -b experiment-new-ui ../app-experiment
cd ../app-experiment
# Try new ideas without commitment
```

**Release Preparation:**

```bash
git worktree add -b release-v2.0 ../app-release origin/main
cd ../app-release
# Prepare release while development continues
```

### GitHub CLI (`gh`) Usage

**MANDATORY**: Use the GitHub CLI for all GitHub operations instead of web interface:

- **Load comprehensive guide**: Use `/context-load-gh-cli` command in Claude Code CLI
- **Pull Request creation**: Use HEREDOC for multi-line descriptions
- **API access**: Use `gh api` for operations not directly supported by CLI
- **JSON output**: Always use `--json` flags for parsing when available

**Key Commands:**

```bash
# Pull Request operations
gh pr create --title "title" --body "$(cat <<'EOF'
## Summary
- Change description

## Test plan
- [ ] Tests pass
EOF
)"
gh pr list --json number,title,state
gh pr view 123 --json reviews
gh pr comment 123 --body "comment"
gh pr review --approve

# Issue operations  
gh issue create --title "Bug" --label "bug"
gh issue list --assignee @me
gh issue comment 123
gh issue view 123 --json title,body,state,assignees
gh issue edit 123 --add-label "priority:high"
gh issue close 123
gh issue reopen 123
gh issue status
gh issue pin 123
gh issue transfer 123 --repo owner/target-repo

# API usage for advanced operations
gh api repos/{owner}/{repo}/pulls/{number}/reviews
gh api search/issues --raw-field q="is:pr is:open review-requested:@me"
```

**Best Practices:**

- Check state before actions: `gh pr view --json state`
- Use explicit parameters over interactive mode
- Handle errors gracefully with existence checks
- Use API for review comments (CLI limitation)

## Claude Code Sub-Agent Architecture

**CRITICAL**: Sub-agents are the key to transforming Claude Code from a helpful assistant into a powerful parallel execution engine. Master these patterns to achieve 10x productivity gains.

### Core Principles

1. **Sub-Agents for Research, Not Decisions**
   - Sub-agents excel at information gathering, exploration, and analysis
   - Keep decision-making and code writing in the main agent
   - Each sub-agent has its own context window (leverage for large codebases)

2. **Parallel-First Design**
   - Launch multiple sub-agents immediately upon receiving complex tasks
   - Up to 10 concurrent sub-agents supported
   - Tasks queue automatically when exceeding limit
   - Let Claude Code manage parallelism automatically

3. **Token Cost Awareness**
   - Single agents use ~4x more tokens than chat
   - Multi-agent systems use ~15x more tokens than chat
   - Reserve for high-value tasks where performance gains justify costs
   - 90%+ performance improvements possible for suitable tasks

### Sub-Agent Task Patterns

**Safe for Parallel Execution:**

```markdown
✅ File discovery and analysis
✅ Code pattern searches across multiple files\
✅ Dependency analysis and mapping
✅ Documentation gathering
✅ Test file analysis
✅ Configuration exploration
✅ API endpoint discovery
✅ Database schema analysis
```

**Requires Sequential Coordination:**

```markdown
❌ Shared file modifications
❌ Integration point changes
❌ Configuration updates
❌ Database migrations
❌ Package dependency updates
❌ Git operations
```

### Multi-Phase Workflow Architecture

**Phase 1: Discovery (5-10 parallel sub-agents)**

```markdown
## Discovery Phase Tasks

- Analyze codebase structure
- Map file dependencies
- Identify coding patterns
- Locate test coverage
- Find configuration files
- Discover API endpoints
- Analyze database schemas
```

**Phase 2: Planning (Main agent only)**

```markdown
## Planning Phase

- Synthesize all findings
- Identify conflicts/dependencies
- Create implementation strategy
- Design task boundaries
```

**Phase 3: Implementation (3-7 parallel sub-agents)**

```markdown
## Implementation Phase Tasks

1. Component creation (owns: src/components/*)
2. Test implementation (owns: tests/*)
3. Style development (owns: styles/*)
4. Type definitions (owns: types/*)
5. Utility functions (owns: utils/*)
6. Documentation (owns: docs/*)
7. Mock data (owns: mocks/*)
```

**Phase 4: Integration (1-2 sub-agents)**

```markdown
## Integration Phase

- Validate cross-component consistency
- Run full test suite
- Update integration points
- Verify build success
```

### Implementation Guidelines

**In your project's CLAUDE.md file, add explicit sub-agent instructions:**

````markdown
## Sub-Agent Delegation Strategy

### Feature Implementation Workflow

When implementing new features, immediately delegate to parallel sub-agents:

1. **Component Agent** (owns: src/components/Feature/*)
   - Create React/Vue/Svelte components
   - Implement component logic
   - Add local state management

2. **Style Agent** (owns: styles/feature/*)
   - Create CSS/SCSS files
   - Implement responsive design
   - Add animations

3. **Test Agent** (owns: tests/feature/*)
   - Write unit tests
   - Create integration tests
   - Add e2e test scenarios

4. **Type Agent** (owns: types/feature.ts)
   - Define TypeScript interfaces
   - Create type guards
   - Export shared types

5. **API Agent** (owns: api/feature/*)
   - Implement API endpoints
   - Add request/response handling
   - Create API documentation

6. **Hook Agent** (owns: hooks/useFeature*)
   - Create custom React hooks
   - Implement state logic
   - Add effect management

7. **Documentation Agent** (owns: docs/feature.md)
   - Write feature documentation
   - Create usage examples
   - Update README if needed

### Research Workflow

For complex research tasks, use this pattern:

```bash
"Research these 3 approaches in parallel:
1. Research approach A for solving X
2. Research approach B for solving X  
3. Research approach C for solving X
Use 3 agents in parallel."
```
````

### Codebase Analysis Workflow

When analyzing large codebases:

```bash
"Analyze this codebase using 5 parallel agents:
1. Analyze authentication flow
2. Analyze data models
3. Analyze API structure
4. Analyze frontend components
5. Analyze test coverage"
```

````
### Communication Patterns

**Inter-Agent Communication via Scratchpad Files:**

```markdown
## Scratchpad Structure
/tmp/project-name/claude-scratch/
├── discovery-results.json     # Phase 1 findings
├── component-manifest.json    # Component registry
├── api-endpoints.json        # API documentation
├── type-definitions.json     # Shared types
└── integration-points.json   # Cross-component deps
````

**Status Tracking Format:**

```json
{
  "agent": "component-agent",
  "status": "completed",
  "created_files": [
    "src/components/UserProfile/index.tsx",
    "src/components/UserProfile/UserProfile.tsx"
  ],
  "exports": ["UserProfile", "UserProfileProps"],
  "dependencies": ["useAuth", "UserType"]
}
```

### Performance Optimization

1. **Batch Small Tasks**
   - Group related small operations into single sub-agent tasks
   - Reduces overhead and context setup costs
   - Example: One agent for all utility functions vs. one per function

2. **Strip Comments for Analysis**
   - Remove comments when passing code between agents
   - Reduces token usage by 20-30%
   - Preserve comments only when specifically needed

3. **Early Context Preservation**
   - Use sub-agents early in conversation
   - Preserves main agent context for decision-making
   - Delegates memory-intensive operations

4. **Optimize Parallelism Level**
   - Start with 5-7 agents for most tasks
   - Scale to 10 for truly independent operations
   - Monitor queue depth and adjust

### Example Workflows

**Full Feature Implementation:**

```markdown
Task: Implement user authentication feature

Phase 1 - Research (4 agents):

- Agent 1: Analyze existing auth patterns
- Agent 2: Research security best practices
- Agent 3: Evaluate auth libraries
- Agent 4: Review current user model

Phase 2 - Planning (Main agent):

- Synthesize research
- Design auth architecture
- Create task breakdown

Phase 3 - Implementation (7 agents):

- Agent 1: Auth components (login/register forms)
- Agent 2: Auth API endpoints
- Agent 3: Auth middleware
- Agent 4: Auth types/interfaces
- Agent 5: Auth tests
- Agent 6: Auth documentation
- Agent 7: Auth utilities

Phase 4 - Integration (2 agents):

- Agent 1: Integration testing
- Agent 2: Documentation updates
```

**Refactoring Workflow:**

```markdown
Task: Refactor payment system

Phase 1 - Analysis (5 agents):

- Agent 1: Map payment flow
- Agent 2: Identify code smells
- Agent 3: Analyze test coverage
- Agent 4: Find duplicate code
- Agent 5: Review error handling

Phase 2 - Planning (Main agent):

- Design refactoring strategy
- Identify breaking changes
- Plan migration path

Phase 3 - Execution (6 agents):

- Agent 1: Refactor payment models
- Agent 2: Update payment services
- Agent 3: Migrate payment tests
- Agent 4: Update payment APIs
- Agent 5: Refactor payment UI
- Agent 6: Update documentation
```

### Best Practices Summary

1. **Always delegate research tasks** to sub-agents
2. **Never delegate decision-making** to sub-agents
3. **Design clear file ownership** boundaries
4. **Use scratchpad files** for coordination
5. **Monitor token usage** and adjust strategy
6. **Start with templates** and iterate
7. **Batch related small tasks** together
8. **Strip comments** for analysis tasks
9. **Leverage parallel reads**, coordinate writes
10. **Document sub-agent patterns** in CLAUDE.md

### Pull Request Best Practices

**MANDATORY**: Follow these practices for well-crafted PRs:

**PR Structure & Size:**

- **Keep PRs small and focused** - fulfill a single purpose
- Break complex issues into smaller, logical pull requests for faster reviews
- Use time-boxed spikes to determine how to segment large features

**Clear Titles & Descriptions:**

- Write descriptive titles explaining WHAT is being solved
- Create descriptions that guide reviewers through the code
- Use clear sections: Summary, Changes, Test Plan, Related Issues
- Highlight related files and group them by concepts
- Include screenshots/visuals for frontend changes

**Self-Review Process:**

- **ALWAYS** review, build, and test your own PR before submitting
- Add inline comments to explain complex logic or guide reviewers
- Specify review order if multiple files are changed
- Indicate the type of feedback needed (quick look vs. deep critique)

**Security & Quality:**

- Check dependency changes and investigate security alerts
- Run all tests and linting before submission
- Include issue tracking keys for traceability
- Use semantic commit messages focusing on WHAT changed and WHY

**Reviewer-Centric Approach:**

- Think of PRs as a "product" where reviewers are "customers"
- Make the review process as easy and clear as possible
- Keep team informed with status labels (ready for review, blocked, in progress)
- Link related issues, project boards, and conversations

**PR Description Template:**

```markdown
## Summary

Brief description of changes and motivation

## Changes

- Specific change 1
- Specific change 2

## Test Plan

- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Related Issues

Fixes #123
Related to #456

## Review Notes

- Focus on [specific area]
- Review files in this order: [list]
```

### GitHub Issues for Work Tracking

**MANDATORY**: Use GitHub Issues for comprehensive work tracking and project management:

**Core Issue Management:**

- Use Issues to track ideas, feedback, tasks, and bugs
- Create issues through CLI for seamless workflow integration
- Support hierarchical work breakdown with sub-issues for complex tasks
- Link issues to pull requests using keywords (`fixes #123`, `closes #456`)

**Issue Creation Best Practices:**

- Write descriptive titles that clearly identify the problem/task
- Include detailed descriptions with:
  - Problem statement or feature requirement
  - Acceptance criteria using task lists `[ ]`
  - Context and background information
  - Screenshots or examples when applicable

**Workflow Integration:**

- **Create branches directly from issues** for feature development
- Use `@mentions` to notify collaborators and assign responsibilities
- Reference related issues with `#` prefix for cross-linking
- Convert issues to GitHub Discussions when conversations become exploratory

**Issue Organization:**

- Use **labels** for categorization (bug, enhancement, priority levels)
- Assign **milestones** for release planning and deadline tracking
- Pin important issues for visibility
- Filter and search issues for project insights

**Advanced Features:**

- Create **issue templates** to standardize bug reports and feature requests
- Use **saved replies** for common responses and efficiency
- Enable **automation** through GitHub Actions for issue management
- Integrate with **GitHub Projects** for comprehensive project tracking

**Issue Lifecycle Commands:**

```bash
# Create comprehensive issues
gh issue create --title "Feature: Add user authentication" --body "$(cat <<'EOF'
## Problem
Users need secure login functionality

## Acceptance Criteria
- [ ] Login form with email/password
- [ ] Password strength validation  
- [ ] Remember me functionality
- [ ] Password reset flow

## Related Issues
Related to #123 (API design)
EOF
)" --label "enhancement" --milestone "v2.0" --assignee @me

# Advanced issue management
gh issue list --state open --label "bug" --assignee @me --json number,title,labels
gh issue view 123 --json title,body,state,assignees,milestone
gh issue edit 123 --add-assignee @user --add-label "priority:high"
gh issue comment 123 --body "Updated implementation approach"

# Project planning
gh issue list --milestone "v2.0" --json number,title,state
gh issue status  # Show assigned issues across repositories
```

**Issue Automation Patterns:**

- Use keywords in PR descriptions to auto-close issues (`fixes #123`)
- Set up GitHub Actions for issue labeling and assignment
- Create issue templates for consistent reporting
- Use project boards for visual work tracking and sprint planning

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

**IMPORTANT**: For comprehensive sub-agent patterns and best practices, see the **Claude Code Sub-Agent Architecture** section above.

When working as part of a multi-agent team:

- **CHECK** `/tmp/{project-name}/project-status.md` or coordination files for shared state
- **WORK** only on assigned tasks to avoid conflicts
- **COMMUNICATE** progress through PR comments or status files
- **WAIT** at join points until all parallel work is complete
- **MERGE** work carefully following the plan's integration strategy
- **USE** git worktrees to work on separate branches without conflicts
- **CREATE** status files in `/tmp/{project-name}/claude-scratch/` for inter-agent communication
- **COORDINATE** using shared JSON status files for structured updates in project-specific directories
- **LEVERAGE** sub-agents for parallel research and exploration tasks (see Sub-Agent Architecture section)

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

## Project Lifecycle Management

### Deno as Lifecycle Operations Harness

**MANDATORY**: Use Deno as the primary lifecycle operations harness in the root of every project:

- **Central Command Hub**: All lifecycle operations MUST be defined in `deno.json` tasks
- **Standardized Commands**: Use consistent naming across all projects:
  - `deno task up` - Start/deploy all services (Docker Compose, local servers, etc.)
  - `deno task down` - Stop/undeploy all services
  - `deno task test` - Run all tests (unit, integration, e2e)
  - `deno task test:unit` - Run unit tests only
  - `deno task test:integration` - Run integration tests only
  - `deno task dev` - Start development environment with hot reload
  - `deno task build` - Build project for production
  - `deno task check` - Type checking
  - `deno task fmt` - Format code
  - `deno task lint` - Lint code
  - `deno task init` - Initialize project for new environment
  - `deno task ci` - Run full CI pipeline locally

### Integration with Project Tools

**Deno tasks MUST orchestrate project-specific tools:**

```json
{
  "tasks": {
    "up": "docker compose up -d && cd backend && cargo run",
    "down": "docker compose down",
    "test": "deno task test:backend && deno task test:frontend",
    "test:backend": "cd backend && cargo test",
    "test:frontend": "cd frontend && deno test",
    "dev": "docker compose up -d db && concurrently \"cd backend && cargo watch -x run\" \"cd frontend && deno task dev\""
  }
}
```

**Key Principles:**

- **Single Entry Point**: Developers should only need `deno task <command>` regardless of project complexity
- **Directory Awareness**: Tasks handle `cd` operations to run commands in correct directories
- **Tool Abstraction**: Abstract away whether using npm, cargo, gradle, make, etc.
- **Compose Integration**: Docker Compose services managed through Deno tasks
- **Environment Setup**: `deno task init` handles all first-time setup (deps, config, etc.)

## File Organization

- `/src/` - Source code
- `/tests/` - Test files organized by type
- `/scripts/` - Deno automation scripts
- `/tasks/` - Task management files (markdown + status.json)
- `deno.json` - Project configuration and tasks
- `import_map.json` - Import mappings (if needed)

## User Scripts Directory

**~/.tools Directory:**

- **Purpose**: Contains user-executable scripts installed from dotfiles
- **Installation**: Scripts from `dotfiles/tools/` are copied here during dotfiles installation
- **PATH Setup**: Add `export PATH="$HOME/.tools:$PATH"` to your shell config to run scripts from anywhere
- **Script Format**: Primarily Deno TypeScript scripts with proper shebang (e.g., `#!/usr/bin/env -S deno run --allow-env`)
- **Permissions**: Scripts are automatically made executable during installation

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
