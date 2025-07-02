---
allowed-tools: Bash(git:*), Bash(fd:*), Bash(rg:*), Bash(jq:*), Bash(mkdir:*), Bash(cd:*), Bash(gh:*)
description: Create git worktrees for parallel Claude Code sessions with intelligent setup
---

# /new-worktree

Creates a new git worktree with intelligent project setup and environment initialization. Git worktrees are the fastest, safest way to keep several Claude Code shells going in parallel. The cleanest long-term setup is **a per-repo `.worktrees/` folder that lives beside the main working tree** (plus a global ignore so it never reaches the remote).

## Live Repository Context

- **Current branch**: !`git branch --show-current`
- **Existing worktrees**: !`git worktree list --porcelain | grep -E "^worktree|^branch" | paste -d' ' - - | sed 's/worktree //;s/branch refs\/heads\//: /'`
- **Uncommitted changes**: !`git status --porcelain | wc -l`
- **Recent branches**: !`git branch --sort=-committerdate | head -5 | sed 's/^[* ]*//'`
- **Project name**: !`basename "$(git rev-parse --show-toplevel)"`
- **GitHub remote**: !`git remote get-url origin 2>/dev/null | sed 's/.*github.com[:/]\(.*\)\.git/\1/' || echo "No GitHub remote"`
- **Open issues**: !`gh issue list --state open --limit 5 --json number,title | jq -r '.[] | "\(.number): \(.title)"' 2>/dev/null || echo "No issues accessible"`

## Project Configuration Analysis

Automatically detect project type and setup requirements:
- **Project files**: @deno.json @package.json @Cargo.toml @go.mod @pom.xml
- **Setup scripts**: @Makefile @justfile @scripts/setup.* @scripts/init.*
- **Environment config**: @.env.example @.env.*.example @config/*.example
- **Documentation**: @README.md @CLAUDE.md @CONTRIBUTING.md @docs/setup.md
- **CI/CD config**: @.github/workflows/*.yml @.gitlab-ci.yml @Jenkinsfile

## Usage

```bash
# Auto-suggest worktree based on current work
/new-worktree

# Create from GitHub issue
/new-worktree https://github.com/wcygan/wcygan.github.io/issues/34

# Create feature branch with descriptive name
/new-worktree authentication system

# Create bugfix worktree
/new-worktree bugfix login timeout

# Natural language description
/new-worktree implement the new user profile API endpoints

# Specify branch type explicitly
/new-worktree feature/payment-integration
```

## Arguments

$ARGUMENTS

## Context-Aware Behavior

The command intelligently adapts based on project context and arguments:

- **No arguments**: Analyzes current work (uncommitted changes, recent commits, open issues) to suggest appropriate worktree
- **Issue number patterns**: Detects `issue 34`, `#34`, `gh-34` and fetches full issue context from GitHub
- **Single keyword**: Uses as branch name or feature identifier
- **Multiple keywords**: Parses for branch type + description (feature, bugfix, hotfix, refactor)
- **Natural language**: Extracts intent and creates appropriate branch name
- **Explicit branch name**: Uses provided name if it follows git conventions (feature/, bugfix/, etc.)

### GitHub Issue Integration

When an issue number is detected, the command automatically:
1. Fetches issue details using `gh issue view`
2. Extracts title, body, labels, and comments
3. Determines appropriate branch type from labels (bug → bugfix/, enhancement → feature/)
4. Creates descriptive branch name from issue title
5. Includes issue context in coordination files for Claude

## Why Worktrees for Multi-Claude Development

### Key Benefits
- **Isolated Working Directories**: Each worktree has its own HEAD and working files, preventing file conflicts between Claude instances
- **Shared Object Store**: Objects are shared, so a worktree costs only changed files—no full clone needed
- **Branch Protection**: Git blocks checking out the same branch twice, preventing accidental overlap
- **Efficient Storage**: Large-file users can still trim disk use with `git lfs prune` or symlinking blobs if needed

### Recommended Directory Structure

The cleanest approach is **`.worktrees/` beside the main repo**:

```
project/                    # Main working tree
├── .git/
├── .worktrees/            # Worktree storage (git-ignored)
│   ├── feature-auth/      # Feature branch worktree
│   ├── bugfix-login/      # Bugfix branch worktree
│   └── experiment-ai/     # Experimental branch
├── src/
└── README.md
```

**Advantages**:
- Short relative paths for tooling
- Visible in `git worktree list` 
- Survives repo moves/renames
- Easy to ignore with `.git/info/exclude`
- No naming collisions between projects

## Workflow

### 1. Pre-Creation Analysis

**Git State Check**:
- Verify repository status (!`git status --porcelain`)
- Check uncommitted changes and offer to stash if needed
- List existing worktrees (!`git worktree list`)
- Ensure `.worktrees/` directory structure exists

**GitHub Issue Detection** (if issue pattern found):
```bash
# Detect issue patterns: "issue 34", "#34", "gh-34"
if [[ "$ARGUMENTS" =~ (issue |#|gh-)([0-9]+) ]]; then
  ISSUE_NUMBER="${BASH_REMATCH[2]}"
  
  # Detect explicit repo or use current
  if [[ "$ARGUMENTS" =~ --repo[= ]([^ ]+) ]]; then
    REPO="${BASH_REMATCH[1]}"
  else
    REPO=$(git remote get-url origin | sed 's/.*github.com[:/]\(.*\)\.git/\1/')
  fi
  
  # Fetch comprehensive issue data
  ISSUE_DATA=$(gh issue view "$ISSUE_NUMBER" \
    --repo "$REPO" \
    --json title,body,state,labels,assignees,createdAt,updatedAt,comments)
  
  # Extract key information
  ISSUE_TITLE=$(echo "$ISSUE_DATA" | jq -r '.title')
  ISSUE_BODY=$(echo "$ISSUE_DATA" | jq -r '.body')
  ISSUE_LABELS=$(echo "$ISSUE_DATA" | jq -r '.labels[].name' | paste -sd,)
  
  # Determine branch type from labels
  if echo "$ISSUE_LABELS" | grep -q "bug"; then
    BRANCH_PREFIX="bugfix"
  elif echo "$ISSUE_LABELS" | grep -q "enhancement\|feature"; then
    BRANCH_PREFIX="feature"
  else
    BRANCH_PREFIX="issue"
  fi
  
  # Create branch name from issue title
  BRANCH_NAME="$BRANCH_PREFIX/$ISSUE_NUMBER-$(echo "$ISSUE_TITLE" | 
    tr '[:upper:]' '[:lower:]' | 
    sed 's/[^a-z0-9]/-/g' | 
    sed 's/--*/-/g' | 
    sed 's/^-//' | 
    sed 's/-$//' | 
    cut -c1-50)"
fi
```

**Branch Name Resolution** (for non-issue arguments):
- Parse $ARGUMENTS for branch type and description
- Auto-prefix with conventional prefixes (feature/, bugfix/, etc.)
- Convert natural language to kebab-case branch names
- Validate branch name doesn't already exist

### 2. Project Type Detection

**Automatic Detection** (in priority order):
```typescript
// Deno Project
if (exists("deno.json") || exists("deno.jsonc")) {
  projectType = "deno";
  setupCommands = extractDenoTasks();
}

// Node.js Project
else if (exists("package.json")) {
  projectType = "node";
  packageManager = detectPackageManager(); // npm, yarn, pnpm
  setupCommands = extractNpmScripts();
}

// Rust Project
else if (exists("Cargo.toml")) {
  projectType = "rust";
  setupCommands = ["cargo build", "cargo check"];
}

// Go Project
else if (exists("go.mod")) {
  projectType = "go";
  setupCommands = ["go mod download", "go build ./..."];
}

// Java Project
else if (exists("pom.xml")) {
  projectType = "maven";
  setupCommands = ["mvn install"];
} else if (exists("build.gradle") || exists("build.gradle.kts")) {
  projectType = "gradle";
  setupCommands = ["./gradlew build"];
}

// Python Project
else if (exists("requirements.txt") || exists("pyproject.toml")) {
  projectType = "python";
  setupCommands = createVirtualEnvCommands();
}
```

### 3. Setup Command Extraction

**Search Order for Setup Commands**:

1. **deno.json tasks**:
   - Look for: `init`, `setup`, `install`, `bootstrap`
   - Example: `deno task init`

2. **package.json scripts**:
   - Look for: `postinstall`, `prepare`, `setup`, `init`
   - Example: `npm run setup`

3. **Makefile targets**:
   - Search for: `setup:`, `init:`, `install:`, `bootstrap:`
   - Example: `make setup`

4. **Docker Compose**:
   - If exists, add: `docker compose up -d` for services
   - Check for init containers or setup services

5. **Documentation parsing**:
   - README.md: Look for "Setup", "Installation", "Getting Started" sections
   - CLAUDE.md: Extract development setup instructions
   - CONTRIBUTING.md: Find developer environment setup

6. **Environment files**:
   - Copy `.env.example` → `.env`
   - Copy `.env.development.example` → `.env.development`
   - Look for other `*.example` files

### 4. Worktree Creation

```bash
# Setup .worktrees/ directory structure
REPO_ROOT=$(git rev-parse --show-toplevel)
WORKTREE_DIR="$REPO_ROOT/.worktrees/$BRANCH_NAME"

# Ensure .worktrees/ is git-ignored
if ! grep -q "^\.worktrees/" "$REPO_ROOT/.git/info/exclude" 2>/dev/null; then
  echo ".worktrees/" >> "$REPO_ROOT/.git/info/exclude"
fi

# Create the worktree
if git show-ref --verify --quiet "refs/heads/$BRANCH_NAME"; then
  # Branch exists, check it out
  git worktree add "$WORKTREE_DIR" "$BRANCH_NAME"
else
  # Create new branch
  git worktree add -b "$BRANCH_NAME" "$WORKTREE_DIR"
fi

echo "✅ Worktree created at: $WORKTREE_DIR"
```

### 5. Environment Setup

**Execute in new worktree directory**:
```bash
cd "$WORKTREE_DIR"

# Run detected setup commands in order
for cmd in "${SETUP_COMMANDS[@]}"; do
  echo "Running: $cmd"
  eval "$cmd"
done

# Additional setup based on project type
case "$PROJECT_TYPE" in
  "deno")
    deno cache deps.ts 2>/dev/null || true
    ;;
  "node")
    # Install git hooks if husky is detected
    [ -f .husky/install.sh ] && .husky/install.sh
    ;;
  "python")
    # Activate virtual environment
    source venv/bin/activate 2>/dev/null || source .venv/bin/activate
    ;;
esac
```

### 6. Coordination Support

**Create coordination files for multi-agent workflows**:

```bash
# Create project-specific coordination directory
mkdir -p "/tmp/${PROJECT_NAME}"

# Create worktree registry with issue context if available
if [[ -n "$ISSUE_NUMBER" ]]; then
  cat > "/tmp/${PROJECT_NAME}/worktrees.json" << EOF
{
  "worktrees": [
    {
      "branch": "$BRANCH_NAME",
      "directory": "$WORKTREE_DIR",
      "created": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
      "purpose": "$DESCRIPTION",
      "issueNumber": $ISSUE_NUMBER,
      "issueTitle": "$ISSUE_TITLE",
      "issueLabels": "$ISSUE_LABELS",
      "issueUrl": "https://github.com/$REPO/issues/$ISSUE_NUMBER",
      "setupCommands": $SETUP_COMMANDS_JSON
    }
  ]
}
EOF

  # Create issue context file for Claude
  cat > "/tmp/${PROJECT_NAME}/${BRANCH_NAME}-issue-context.md" << EOF
# Issue #$ISSUE_NUMBER: $ISSUE_TITLE

**Labels**: $ISSUE_LABELS
**URL**: https://github.com/$REPO/issues/$ISSUE_NUMBER

## Description
$ISSUE_BODY

## Comments
$(echo "$ISSUE_DATA" | jq -r '.comments[] | "### \(.author.login) - \(.createdAt)\n\(.body)\n"')

## Implementation Notes
- Branch: $BRANCH_NAME
- Created from issue: #$ISSUE_NUMBER
EOF
else
  # Standard worktree registry without issue context
  cat > "/tmp/${PROJECT_NAME}/worktrees.json" << EOF
{
  "worktrees": [
    {
      "branch": "$BRANCH_NAME",
      "directory": "$WORKTREE_DIR",
      "created": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
      "purpose": "$DESCRIPTION",
      "setupCommands": $SETUP_COMMANDS_JSON
    }
  ]
}
EOF
fi

# Create task coordination file if requested
if [[ "$CREATE_TASKS" == "true" ]]; then
  cat > "/tmp/${PROJECT_NAME}/${BRANCH_NAME}-tasks.md" << EOF
# Tasks for $BRANCH_NAME

## Overview
$DESCRIPTION
${ISSUE_NUMBER:+"Related to issue: #$ISSUE_NUMBER - $ISSUE_TITLE"}

## Task Assignments
- [ ] Task 1: Description
- [ ] Task 2: Description

## Dependencies
- List any dependencies between tasks
- Note any required coordination points

## Progress
- Updated by each Claude instance
EOF
fi
```

### 7. Post-Creation Output

**Display comprehensive next steps**:
```
✅ Worktree created successfully!

📍 Location: .worktrees/$BRANCH_NAME
🌿 Branch: $BRANCH_NAME
🏷️  Purpose: $DESCRIPTION
${ISSUE_NUMBER:+"🔗 Issue: #$ISSUE_NUMBER - $ISSUE_TITLE"}
${ISSUE_NUMBER:+"🏷️  Labels: $ISSUE_LABELS"}

✅ Setup completed:
  - Installed dependencies
  - Configured environment
  - Initialized development services
${ISSUE_NUMBER:+"  - Loaded issue context from GitHub"}

📋 Coordination files:
  - Worktree registry: /tmp/$PROJECT_NAME/worktrees.json
${ISSUE_NUMBER:+"  - Issue context: /tmp/$PROJECT_NAME/$BRANCH_NAME-issue-context.md"}

🚀 Quick start (copy & paste):
─────────────────────────────
cd .worktrees/$BRANCH_NAME && claude
─────────────────────────────

💡 Parallel Claude tips:
  - Each worktree gets its own Claude context (.claude/)
  - Multiple Claudes can work on different branches simultaneously
  - Git prevents checking out the same branch twice
${ISSUE_NUMBER:+"  - Issue context automatically loaded for Claude"}

🧹 Cleanup when done:
  git worktree remove .worktrees/$BRANCH_NAME
  git branch -d $BRANCH_NAME  # After merging
${ISSUE_NUMBER:+"  gh issue close $ISSUE_NUMBER  # Close the issue"}
  git worktree prune          # Remove stale worktrees
```

## Worktree Management Commands

### List all worktrees
```bash
git worktree list
```

### Remove a worktree
```bash
# From anywhere in the repo
git worktree remove .worktrees/branch-name

# Or if in the worktree directory
git worktree remove .
```

### Prune stale worktrees
```bash
git worktree prune
```

## Smart Project Setup Examples

### GitHub Issue Workflow
```bash
# Issue #34: "Add user authentication"
/new-worktree issue 34

# Creates branch: feature/34-add-user-authentication
# Fetches issue details, labels, comments
# Sets up worktree with full issue context

# Issue from different repo
/new-worktree issue 123 --repo octocat/hello-world

# Creates branch based on issue labels:
# - bug label → bugfix/123-fix-login-error
# - enhancement label → feature/123-add-dark-mode
# - no labels → issue/123-update-documentation
```

### Deno Fresh Project
```typescript
// Detected from deno.json
setupCommands = [
  "deno task init",      // If exists
  "deno cache deps.ts",  // Cache dependencies
  "deno task build"      // Pre-build if needed
];
```

### Node.js with Docker
```typescript
// Detected from package.json + docker-compose.yml
setupCommands = [
  "npm install",              // Install dependencies
  "cp .env.example .env",     // Setup environment
  "docker compose up -d db",  // Start required services
  "npm run db:migrate"        // Run migrations
];
```

### Rust with Database
```typescript
// Detected from Cargo.toml + diesel.toml
setupCommands = [
  "cargo build",              // Build dependencies
  "docker compose up -d postgres",
  "diesel migration run"      // Setup database
];
```

## Integration with Other Commands

- **Before**: Use `/parallel` to analyze what can be developed in parallel
- **After**: Use `/coordinate` to manage multi-agent task assignments
- **During**: Use `/agent-start` in each worktree for specialized agents
- **Cleanup**: Use standard git worktree commands to remove completed work

## Best Practices

1. **Branch Naming**:
   - Use conventional prefixes: feature/, bugfix/, hotfix/, refactor/
   - Keep names descriptive but concise
   - Use kebab-case for consistency

2. **Worktree Organization (.worktrees/ strategy)**:
   - Always use `.worktrees/` directory beside main repo
   - Ensure `.worktrees/` is in `.git/info/exclude`
   - Clean up completed worktrees promptly with `git worktree remove`
   - Run `git worktree prune` weekly to remove stale entries

3. **Parallel Claude Development**:
   - Each worktree gets its own `.claude/` context directory
   - Create worktrees for independent features to avoid conflicts
   - Use `/coordinate` command to sync between Claude instances
   - Share state via `/tmp/{project-name}/` coordination files

4. **Environment Isolation**:
   - Each worktree gets fresh dependency installation
   - Don't share node_modules or build artifacts between worktrees
   - Use separate database schemas/containers if needed
   - Copy `.env.example` files for each worktree

5. **Storage Optimization**:
   - For large repos: `git lfs prune` to clean up LFS objects
   - Shared git objects keep storage efficient
   - Consider symlinking large assets if needed
   - Monitor disk usage with `du -sh .worktrees/*`

## Error Handling

- **Uncommitted changes**: Offers to stash before creating worktree
- **Branch exists**: Suggests alternative names or checks out existing
- **Setup failure**: Continues with remaining commands, reports failures
- **Missing dependencies**: Suggests installation commands for tools

## Advanced Usage

### Custom Setup Commands
```bash
# Override detected setup with explicit commands
/new-worktree feature/custom --setup="npm install && npm run custom:setup"
```

### Task Assignment
```bash
# Create worktree with pre-assigned tasks
/new-worktree feature/api --tasks="implement user endpoints, add authentication"
```

### Multiple Worktrees
```bash
# Create multiple related worktrees
/new-worktree frontend/redesign
/new-worktree backend/api-v2
/new-worktree docs/api-documentation
```

## Quick Reference: Parallel Claude Workflow

### Starting Multiple Claude Sessions
```bash
# Terminal 1: Main branch work
claude  # In main repo

# Terminal 2: Feature development
/new-worktree feature authentication
cd .worktrees/feature-authentication && claude

# Terminal 3: Bug fix
/new-worktree bugfix login-timeout
cd .worktrees/bugfix-login-timeout && claude

# Terminal 4: Experimental work
/new-worktree experiment ai-integration  
cd .worktrees/experiment-ai-integration && claude
```

### Why .worktrees/ is Optimal

| Approach | Pros | Cons |
|----------|------|------|
| **`.worktrees/` (recommended)** | Short paths, survives moves, easy cleanup, natural grouping | Needs `.git/info/exclude` entry |
| `~/.worktrees/` | Central location | Name collisions, long paths, harder to find |
| Bare repo + siblings | Elegant for monorepos | Non-standard, tool compatibility issues |

### Common Operations
```bash
# See all active worktrees
git worktree list

# Switch between worktrees  
cd .worktrees/feature-auth

# Clean up after merging
git worktree remove .worktrees/feature-auth
git branch -d feature-auth

# Remove all stale worktrees
git worktree prune
```

This command streamlines parallel Claude development by automating the tedious setup process while maintaining clean, collision-free worktree organization that scales with your project needs.