---
allowed-tools: Read, Grep, Glob, Bash(git:*), Bash(rg:*), Bash(fd:*), Bash(jq:*), Bash(bat:*), Bash(eza:*), Bash(gdate:*), TodoWrite, Task
description: Automatically detect and load comprehensive project context with intelligent environment analysis
---

## Context

- Session ID: !`gdate +%s%N`
- Current directory: !`pwd`
- Git branch: !`git branch --show-current 2>/dev/null || echo "Not a git repository"`
- Project name: !`basename "$(git rev-parse --show-toplevel 2>/dev/null || pwd)"`
- Recent commits: !`git log --oneline -5 2>/dev/null || echo "No git history"`
- Uncommitted changes: !`git status --porcelain 2>/dev/null | wc -l | tr -d ' ' || echo "0"`
- Active worktrees: !`git worktree list 2>/dev/null | wc -l | tr -d ' ' || echo "0"`
- Language detected: !`if [ -f "deno.json" ] || [ -f "deno.jsonc" ]; then echo "Deno/TypeScript"; elif [ -f "package.json" ]; then echo "Node.js"; elif [ -f "Cargo.toml" ]; then echo "Rust"; elif [ -f "go.mod" ]; then echo "Go"; elif [ -f "pom.xml" ]; then echo "Java/Maven"; elif [ -f "requirements.txt" ] || [ -f "pyproject.toml" ]; then echo "Python"; else echo "Unknown"; fi`
- Framework detected: !`if [ -f "deno.json" ] && rg -q "@fresh/core" deno.json 2>/dev/null; then echo "Fresh"; elif [ -f "package.json" ] && rg -q "next" package.json 2>/dev/null; then echo "Next.js"; elif [ -f "Cargo.toml" ] && rg -q "axum" Cargo.toml 2>/dev/null; then echo "Axum"; elif [ -f "go.mod" ] && rg -q "connect-go" go.mod 2>/dev/null; then echo "ConnectRPC"; else echo "See dependencies"; fi`
- Issue context available: !`BRANCH=$(git branch --show-current 2>/dev/null); PROJECT=$(basename $(git rev-parse --show-toplevel 2>/dev/null || pwd)); if [ -f "/tmp/$PROJECT/$BRANCH-issue-context.md" ]; then echo "✓ Available"; else echo "✗ None"; fi`
- PLAN.md exists: !`if [ -f "PLAN.md" ]; then echo "✓ Available"; else echo "✗ None"; fi`
- CLAUDE.md exists: !`if [ -f "CLAUDE.md" ]; then echo "✓ Project-specific"; elif [ -f "$HOME/.claude/CLAUDE.md" ]; then echo "✓ Global only"; else echo "✗ None"; fi`

## Your Task

Automatically detect and load comprehensive project context for: **$ARGUMENTS** (optional focus area)

STEP 1: Initialize context loading session

- CREATE session state file: `/tmp/auto-context-$SESSION_ID.json`
- INITIALIZE project analysis workspace: `/tmp/auto-context-workspace-$SESSION_ID/`
- SET UP context discovery tracking

```json
// /tmp/auto-context-$SESSION_ID.json
{
  "sessionId": "$SESSION_ID",
  "timestamp": "ISO_8601_TIMESTAMP",
  "project": {
    "name": "detected_project_name",
    "path": "absolute_project_path",
    "language": "detected_language",
    "framework": "detected_framework",
    "type": "standalone|worktree|submodule|monorepo"
  },
  "context_sources": {
    "issue_context": "path_or_null",
    "plan_md": "boolean",
    "claude_md": "path_or_null",
    "coordination_files": ["list_of_files"],
    "documentation": ["discovered_docs"]
  },
  "loaded_context": {},
  "todos_generated": [],
  "phase": "initialization"
}
```

STEP 2: Project environment analysis and classification

Think deeply about the optimal context loading strategy based on project complexity and development workflow patterns.

PROCEDURE analyze_project_environment():

- EXTRACT project metadata from Context section
- DETERMINE project classification and development workflow
- IDENTIFY primary development tasks and coordination needs
- ASSESS context loading priorities

CASE project_context:
WHEN "issue_branch_detected":

- PRIORITIZE: Issue context loading, acceptance criteria extraction
- FOCUS: Branch-specific development tasks and requirements
- EXTRACT: Issue labels, related PRs, acceptance criteria

WHEN "main_branch_development":

- PRIORITIZE: PLAN.md coordination, recent commits analysis
- FOCUS: General development workflow and project overview
- EXTRACT: Development commands, testing strategies, documentation

WHEN "worktree_coordination":

- PRIORITIZE: Multi-agent coordination files, task assignments
- FOCUS: Parallel development coordination and conflict avoidance
- EXTRACT: Worktree status, agent assignments, shared state

WHEN "complex_monorepo":

- PRIORITIZE: Subproject analysis, dependency mapping
- FOCUS: Cross-project impacts and integration points
- EXTRACT: Workspace configuration, build dependencies, service mesh

STEP 3: Intelligent context discovery and loading

IF $ARGUMENTS provided:

- FOCUS context loading on specified area or component
- PRIORITIZE relevant documentation and coordination files
- FILTER context to reduce noise and increase relevance
  ELSE:
- EXECUTE comprehensive context discovery across all available sources
- LOAD all relevant project context systematically

Use parallel sub-agents for comprehensive context analysis:

- **Agent 1**: Project Structure and Configuration Analysis
  - Analyze build files, dependencies, and project structure
  - Extract development commands and testing strategies
  - Identify key directories and architectural patterns

- **Agent 2**: Documentation and Coordination File Processing
  - Load and parse PLAN.md, CLAUDE.md, README.md
  - Process coordination files in /tmp/PROJECT/
  - Extract documentation from docs/ directories

- **Agent 3**: Git History and Branch Context Analysis
  - Analyze recent commits and branch patterns
  - Load issue context if available
  - Extract development workflow patterns

- **Agent 4**: Environment and Service Discovery
  - Detect Docker services and port configurations
  - Identify database connections and external dependencies
  - Analyze deployment and infrastructure setup

TRY:

- EXECUTE parallel context discovery across all identified sources
- PROCESS and organize context by functional area
- SYNTHESIZE findings into comprehensive project understanding
- GENERATE appropriate todos based on discovered context
- UPDATE session state: phase = "context_loaded"

CATCH (missing_context_sources):

- PROVIDE detailed context source recommendations
- CREATE placeholder coordination files for future use
- DOCUMENT context gaps and suggest improvements
- GENERATE basic project setup todos

CATCH (complex_project_analysis_required):

- USE extended thinking for deep architectural analysis
- BREAK down complex project structure into manageable components
- IMPLEMENT progressive context loading with checkpoints
- CREATE hierarchical project understanding

CATCH (coordination_file_conflicts):

- ANALYZE conflicting information across sources
- PRIORITIZE context sources based on recency and authority
- RESOLVE conflicts through intelligent merging strategies
- DOCUMENT resolution decisions for transparency

STEP 4: Context synthesis and todo generation

PROCEDURE synthesize_project_context():

- CONSOLIDATE findings from all context sources
- CREATE unified project understanding
- IDENTIFY key development workflows and entry points
- EXTRACT actionable development tasks

PROCEDURE generate_intelligent_todos():

CASE project_state:
WHEN "issue_branch_with_context":

```typescript
// Generate issue-specific todos
const issueTodos = [
  {
    content: `Review issue #${issueNumber}: ${issueTitle}`,
    status: "pending",
    priority: "high",
  },
  ...acceptanceCriteria.map((criterion) => ({
    content: `Implement: ${criterion}`,
    status: "pending",
    priority: "high",
  })),
];
```

WHEN "coordination_workflow":

```typescript
// Generate coordination-based todos
const coordTodos = [
  {
    content: "Check coordination files for task assignments",
    status: "pending",
    priority: "medium",
  },
  {
    content: "Sync with other agents through shared state files",
    status: "pending",
    priority: "medium",
  },
];
```

WHEN "standard_development":

```typescript
// Generate standard development todos
const devTodos = [
  {
    content: "Run test suite to verify setup",
    status: "pending",
    priority: "medium",
  },
  {
    content: "Start development services if needed",
    status: "pending",
    priority: "low",
  },
];
```

STEP 5: Environment setup validation and recommendations

PROCEDURE validate_development_environment():

- CHECK port availability for detected services
- VALIDATE required dependencies and tools
- VERIFY Docker services and external connections
- ASSESS development workflow readiness

IF port_conflicts_detected:

- SUGGEST alternative port configurations
- PROVIDE environment variable overrides
- DOCUMENT port conflict resolution strategies

IF missing_dependencies_detected:

- LIST required tools and installation commands
- PROVIDE setup instructions for detected framework
- SUGGEST development environment improvements

STEP 6: Session completion and context summary

FINALLY:

- UPDATE session state: phase = "complete"
- GENERATE comprehensive context loading summary
- SAVE context cache for future sessions: `/tmp/auto-context-cache-$SESSION_ID.json`
- CLEAN UP temporary analysis files
- CREATE todo list with TodoWrite tool based on discovered context

## Context Loading Patterns

### Branch-Based Context Detection:

**Issue Branch Pattern** (`feature/123-description`, `fix/456-bug`):

- Load issue context from `/tmp/PROJECT/BRANCH-issue-context.md`
- Extract issue number, labels, and acceptance criteria
- Generate issue-specific todos and development focus
- Prioritize related documentation and test files

**Coordination Branch Pattern** (in worktree environment):

- Load coordination files from `/tmp/PROJECT/`
- Parse agent assignments and task distribution
- Check worktree status and parallel development state
- Generate coordination-specific todos

**Main Branch Development**:

- Focus on PLAN.md and general project documentation
- Load recent commit history for context
- Generate standard development workflow todos
- Prioritize project overview and setup tasks

### Documentation Priority Hierarchy:

1. **CLAUDE.md** (project-specific) - Highest priority development guidelines
2. **PLAN.md** - Multi-agent coordination and task breakdown
3. **Issue context files** - Branch-specific development requirements
4. **README.md** - General project overview and setup
5. **docs/** directory - Additional technical documentation
6. **.claude/** directory - Project-specific Claude configurations

### Environment Analysis:

**Development Command Extraction:**

- Deno projects: Extract from `deno.json` tasks
- Node.js projects: Extract from `package.json` scripts
- Rust projects: Use `cargo` commands
- Go projects: Use `go` toolchain commands
- Java projects: Use Maven/Gradle build tools

**Service Discovery:**

- Docker Compose services and port configurations
- Database connections and external dependencies
- API endpoints and service mesh configurations
- Development vs production environment differences

**Testing Strategy Detection:**

- Test framework identification (Jest, Vitest, Deno test, etc.)
- Test file patterns and coverage configuration
- Integration and E2E testing setup
- CI/CD pipeline integration points

## Advanced Context Loading Strategies

### Multi-Agent Context Discovery:

For complex projects or when comprehensive analysis is needed:

```markdown
Think harder about optimal context loading strategies for this project complexity level.

Use 4 parallel agents for thorough context discovery:

1. **Structure Agent**: Project architecture and build configuration
2. **Documentation Agent**: All documentation sources and coordination files
3. **History Agent**: Git history, branch patterns, and development workflow
4. **Environment Agent**: Services, dependencies, and deployment configuration
```

### State Management Schema:

**Session State Files:**

- `/tmp/auto-context-$SESSION_ID.json` - Main session state
- `/tmp/auto-context-workspace-$SESSION_ID/` - Analysis workspace
- `/tmp/auto-context-cache-$SESSION_ID.json` - Context cache for performance
- `/tmp/auto-context-todos-$SESSION_ID.json` - Generated todo analysis

**Context Loading Checkpoints:**

- `project_detected` - Basic project information extracted
- `sources_discovered` - All context sources identified
- `context_loaded` - Documentation and files processed
- `todos_generated` - Action items created
- `environment_validated` - Development setup verified

### Integration Patterns:

**Workflow Integration:**

- **Pre-development**: Run automatically at session start
- **Branch switching**: Re-run to update context for new branch
- **Coordination**: Integrate with worktree and multi-agent workflows
- **Documentation**: Keep context fresh with project evolution

**Command Composition:**

- **Before `/start`**: Ensures comprehensive project understanding
- **After `/new-worktree`**: Loads branch-specific context automatically
- **With `/plan`**: Provides context for strategic planning
- **Replaces**: Multiple manual `/context:*` command invocations

### Expected Outcomes:

**Immediate Project Orientation:**

- Complete understanding of project structure and technology stack
- Awareness of current development context (issues, coordination, etc.)
- Ready-to-use development commands and environment setup
- Prioritized todo list based on project state and requirements

**Enhanced Development Workflow:**

- Seamless context switching between projects and branches
- Automatic coordination with multi-agent development workflows
- Intelligent environment setup and conflict resolution
- Comprehensive project documentation awareness

**Smart Context Management:**

- Adaptive loading based on project complexity and type
- Efficient caching for performance in large projects
- Conflict resolution for overlapping context sources
- Progressive disclosure of context complexity

The auto context loader transforms project onboarding from a manual, error-prone process into an intelligent, automated workflow that adapts to any project structure and development context.
