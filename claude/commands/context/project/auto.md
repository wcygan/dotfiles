---
allowed-tools: Read, Grep, Glob, Bash(git:*), Bash(rg:*), Bash(fd:*), Bash(jq:*), Bash(bat:*), Bash(eza:*), TodoWrite
description: Automatically detect and load comprehensive project context based on environment
---

# /context:project:auto

Automatically detects and loads the most relevant project context based on the current directory, branch name, project type, and available coordination files. This command is designed to quickly orient Claude to any project without requiring manual specification.

## Live Repository Context

- **Current directory**: !`pwd`
- **Git branch**: !`git branch --show-current 2>/dev/null || echo "Not a git repository"`
- **Project name**: !`basename "$(git rev-parse --show-toplevel 2>/dev/null || pwd)"`
- **Recent commits**: !`git log --oneline -5 2>/dev/null || echo "No git history"`
- **Uncommitted changes**: !`git status --porcelain 2>/dev/null | wc -l | xargs -I {} echo "{} files with changes"`
- **Active worktrees**: !`git worktree list 2>/dev/null | wc -l | xargs -I {} echo "{} worktrees"`

## Project Detection

- **Language**: !`if [ -f "deno.json" ] || [ -f "deno.jsonc" ]; then echo "Deno/TypeScript"; elif [ -f "package.json" ]; then echo "Node.js"; elif [ -f "Cargo.toml" ]; then echo "Rust"; elif [ -f "go.mod" ]; then echo "Go"; elif [ -f "pom.xml" ]; then echo "Java/Maven"; elif [ -f "build.gradle" ] || [ -f "build.gradle.kts" ]; then echo "Java/Gradle"; elif [ -f "requirements.txt" ] || [ -f "pyproject.toml" ]; then echo "Python"; else echo "Unknown"; fi`
- **Framework**: !`if [ -f "deno.json" ] && grep -q "@fresh/core" deno.json 2>/dev/null; then echo "Fresh"; elif [ -f "package.json" ] && grep -q "next" package.json 2>/dev/null; then echo "Next.js"; elif [ -f "package.json" ] && grep -q "react" package.json 2>/dev/null; then echo "React"; elif [ -f "Cargo.toml" ] && grep -q "axum" Cargo.toml 2>/dev/null; then echo "Axum"; elif [ -f "Cargo.toml" ] && grep -q "actix-web" Cargo.toml 2>/dev/null; then echo "Actix Web"; elif [ -f "go.mod" ] && grep -q "connect-go" go.mod 2>/dev/null; then echo "ConnectRPC"; elif [ -f "go.mod" ] && grep -q "gin-gonic" go.mod 2>/dev/null; then echo "Gin"; elif [ -f "pom.xml" ] && grep -q "spring-boot" pom.xml 2>/dev/null; then echo "Spring Boot"; else echo "See dependencies"; fi`
- **Testing**: !`if [ -f "deno.json" ] && grep -q "test" deno.json 2>/dev/null; then echo "Deno test"; elif [ -f "package.json" ] && grep -q "jest" package.json 2>/dev/null; then echo "Jest"; elif [ -f "package.json" ] && grep -q "vitest" package.json 2>/dev/null; then echo "Vitest"; elif [ -f "Cargo.toml" ]; then echo "cargo test"; elif [ -f "go.mod" ]; then echo "go test"; else echo "Unknown"; fi`

## Context Sources Available

- **Issue context**: !`BRANCH=$(git branch --show-current 2>/dev/null); PROJECT=$(basename $(git rev-parse --show-toplevel 2>/dev/null || pwd)); if [ -f "/tmp/$PROJECT/$BRANCH-issue-context.md" ]; then echo "✓ Available"; else echo "✗ None"; fi`
- **Coordination files**: !`PROJECT=$(basename $(git rev-parse --show-toplevel 2>/dev/null || pwd)); if [ -d "/tmp/$PROJECT" ]; then ls -1 /tmp/$PROJECT 2>/dev/null | wc -l | xargs -I {} echo "{} files found"; else echo "None"; fi`
- **PLAN.md**: !`if [ -f "PLAN.md" ]; then echo "✓ Available"; else echo "✗ None"; fi`
- **CLAUDE.md**: !`if [ -f "CLAUDE.md" ]; then echo "✓ Project-specific"; elif [ -f "$HOME/.claude/CLAUDE.md" ]; then echo "✓ Global only"; else echo "✗ None"; fi`

## Usage

```bash
# Automatically load all relevant context
/context:project:auto

# The command will intelligently:
# 1. Detect project type and framework
# 2. Load issue context if available
# 3. Parse coordination files
# 4. Extract development commands
# 5. Identify testing strategies
# 6. Create initial todo list
```

## Arguments

$ARGUMENTS

## Context Loading Strategy

### 1. Branch-Based Context Detection

```bash
BRANCH=$(git branch --show-current 2>/dev/null)
PROJECT=$(basename $(git rev-parse --show-toplevel 2>/dev/null || pwd))

# Check for issue-based branch patterns
if [[ "$BRANCH" =~ (feature|bugfix|issue|fix)/([0-9]+)- ]]; then
  ISSUE_NUMBER="${BASH_REMATCH[2]}"
  ISSUE_CONTEXT="/tmp/$PROJECT/$BRANCH-issue-context.md"
  
  if [ -f "$ISSUE_CONTEXT" ]; then
    echo "📋 Loading issue #$ISSUE_NUMBER context..."
  fi
fi

# Check for worktree coordination
WORKTREE_JSON="/tmp/$PROJECT/worktrees.json"
if [ -f "$WORKTREE_JSON" ]; then
  echo "🌿 Loading worktree coordination data..."
fi
```

### 2. Documentation Priority

1. **Project CLAUDE.md** - Highest priority for project-specific instructions
2. **PLAN.md** - Multi-agent coordination and task breakdown
3. **README.md** - General project overview
4. **docs/** directory - Additional documentation
5. **.claude/** directory - Project-specific Claude configurations

### 3. Smart Context Loading

**For Issue-Based Development:**

- Load issue description, comments, and acceptance criteria
- Extract labels to understand issue type (bug, feature, enhancement)
- Identify related issues and PRs
- Create todos from acceptance criteria

**For Feature Development:**

- Load architectural documentation
- Identify affected components
- Find related test files
- Extract API endpoints or interfaces

**For Bug Fixes:**

- Load error patterns from logs
- Find related test failures
- Identify recent changes to affected files
- Load debugging history if available

### 4. Development Environment

```bash
# Extract development commands
if [ -f "deno.json" ]; then
  DEV_CMD=$(jq -r '.tasks.dev // "deno run"' deno.json 2>/dev/null)
  TEST_CMD=$(jq -r '.tasks.test // "deno test"' deno.json 2>/dev/null)
elif [ -f "package.json" ]; then
  DEV_CMD=$(jq -r '.scripts.dev // .scripts.start // "npm start"' package.json 2>/dev/null)
  TEST_CMD=$(jq -r '.scripts.test // "npm test"' package.json 2>/dev/null)
elif [ -f "Cargo.toml" ]; then
  DEV_CMD="cargo run"
  TEST_CMD="cargo test"
elif [ -f "go.mod" ]; then
  DEV_CMD="go run ."
  TEST_CMD="go test ./..."
fi

# Check for Docker services
if [ -f "docker-compose.yml" ] || [ -f "compose.yml" ]; then
  SERVICES=$(yq '.services | keys | join(", ")' docker-compose.yml 2>/dev/null || echo "docker services")
fi
```

### 5. Port Configuration

```bash
# Detect default port
DEFAULT_PORT=$(rg -o 'port["\s:=]+(\d{4})' -r '$1' --no-heading --no-filename | head -1)

# Check if port is in use
if [ -n "$DEFAULT_PORT" ] && lsof -i ":$DEFAULT_PORT" >/dev/null 2>&1; then
  SUGGESTED_PORT=$((DEFAULT_PORT + RANDOM % 1000))
  echo "⚠️  Port $DEFAULT_PORT in use. Suggested: PORT=$SUGGESTED_PORT"
fi
```

### 6. Testing Strategy Detection

```bash
# Find test files and patterns
TEST_COUNT=$(fd -e test.ts -e spec.ts -e test.js -e spec.js -e test.rs -e test.go | wc -l)
INTEGRATION_TESTS=$(fd -p "integration|e2e" -e test.ts -e spec.ts -e test.js -e spec.js | wc -l)

# Detect test configuration
if [ -f "vitest.config.ts" ] || [ -f "jest.config.js" ]; then
  TEST_CONFIG="Custom test configuration detected"
elif [ -f "deno.json" ]; then
  TEST_CONFIG="Deno test runner"
fi
```

### 7. Auto-Generated Todo List

Based on the context loaded, automatically create an appropriate todo list:

```typescript
const todos = [];

// If issue context exists
if (issueContext) {
  todos.push({
    content: `Review issue #${issueNumber}: ${issueTitle}`,
    status: "pending",
    priority: "high",
  });

  // Parse acceptance criteria
  acceptanceCriteria.forEach((criterion) => {
    todos.push({
      content: `Implement: ${criterion}`,
      status: "pending",
      priority: "high",
    });
  });
}

// If in a worktree
if (inWorktree) {
  todos.push({
    content: "Check coordination files for task assignments",
    status: "pending",
    priority: "medium",
  });
}

// Standard development tasks
if (hasTests) {
  todos.push({
    content: "Run test suite to verify setup",
    status: "pending",
    priority: "medium",
  });
}

if (hasDocker) {
  todos.push({
    content: "Start Docker services",
    status: "pending",
    priority: "medium",
  });
}
```

## Context Loading Examples

### Example 1: Issue-Based Branch

```
🚀 Auto-Loading Project Context...

📁 Project: awesome-app
🌿 Branch: feature/34-user-authentication
🏗️  Type: Deno/TypeScript (Fresh)

📋 Issue Context Loaded:
  #34: Add user authentication
  Labels: enhancement, priority:high
  Acceptance Criteria: 4 items

⚡ Development Commands:
  Start: deno task dev
  Test: deno task test
  Build: deno task build

🔌 Services:
  Docker: postgres, redis
  Port: 8000 (available ✓)

📚 Documentation:
  ✓ CLAUDE.md (project-specific)
  ✓ README.md
  ✓ PLAN.md (coordination)

✅ Created 6 todos based on issue requirements
```

### Example 2: Main Branch Development

```
🚀 Auto-Loading Project Context...

📁 Project: backend-api
🌿 Branch: main
🏗️  Type: Go (ConnectRPC)

⚡ Development Commands:
  Start: go run ./cmd/server
  Test: go test ./...
  Proto: buf generate

📚 Key Directories:
  - /api - Protocol buffers
  - /internal - Business logic
  - /cmd - Entry points

✅ Created 3 todos for general development
```

## Integration with Other Commands

- **After `/new-worktree`**: Automatically loads issue context
- **Before `/start`**: Ensures full context understanding
- **With `/think`**: Provides context for architectural decisions
- **Replaces**: Manual use of multiple `/context:*` commands

## Smart Features

### Automatic Detection

- Project type from build files
- Framework from dependencies
- Testing strategy from config
- Development workflow from task runners

### Context Prioritization

- Issue context takes precedence for issue branches
- PLAN.md for coordinated development
- CLAUDE.md for project-specific guidelines
- Recent git history for understanding changes

### Intelligent Defaults

- Suggests available ports when conflicts detected
- Creates relevant todos based on context
- Identifies primary development commands
- Detects required services and dependencies

## Best Practices

1. **Run at session start** for immediate context
2. **Run after branch switch** to update context
3. **Check todo list** for suggested actions
4. **Note port suggestions** to avoid conflicts
5. **Review loaded context** to ensure completeness

This command eliminates the need to manually load various context sources, providing a seamless onboarding experience for any project state.
