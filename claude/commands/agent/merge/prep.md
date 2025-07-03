---
allowed-tools: Bash(git:*), Bash(gh:*), Bash(rg:*), Bash(fd:*), Bash(jq:*), Read, Grep, Write, TodoWrite
description: Prepare branches for merging across multiple worktrees and coordinate integration
---

# /agent:merge:prep

Prepares branches from multiple worktrees for clean merging by checking for conflicts, running tests across affected code, generating merge strategies, and creating integration checklists. Essential for multi-agent development workflows.

## Live Repository Context

- **Current branch**: !`git branch --show-current`
- **Active worktrees**: !`git worktree list | grep -v "bare" | wc -l | xargs -I {} echo "{} active worktrees"`
- **Worktree details**: !`git worktree list | grep -v "bare" | awk '{print $1 " → " $3}' | sed 's/\[//g' | sed 's/\]//g'`
- **Uncommitted changes**: !`git status --porcelain | wc -l | xargs -I {} echo "{} files"`
- **Behind/ahead main**: !`git rev-list --left-right --count origin/main...HEAD 2>/dev/null | awk '{print "Behind: " $1 ", Ahead: " $2}' || echo "No upstream"`

## Coordination Status

- **Project name**: !`basename "$(git rev-parse --show-toplevel)"`
- **Coordination files**: !`PROJECT=$(basename "$(git rev-parse --show-toplevel)"); if [ -d "/tmp/$PROJECT" ]; then ls -1 /tmp/$PROJECT/*.json 2>/dev/null | wc -l | xargs -I {} echo "{} JSON files"; else echo "None"; fi`
- **Active PRs**: !`gh pr list --state open --limit 10 --json number,title,headRefName | jq -r '.[] | "#\(.number): \(.title) (\(.headRefName))"' | head -5`

## Usage

```bash
# Prepare current branch for merging with main
/agent:merge:prep

# Prepare specific branches for integration
/agent:merge:prep feature-auth feature-api

# Prepare all worktree branches for coordinated merge
/agent:merge:prep --all-worktrees

# Generate integration plan without making changes
/agent:merge:prep --dry-run
```

## Arguments

$ARGUMENTS

## Workflow

### 1. Worktree Discovery

```bash
# Get all active worktrees and their branches
WORKTREES=$(git worktree list --porcelain | grep -E "^worktree|^branch" | paste -d' ' - - | sed 's/worktree //;s/branch refs\/heads\//: /')

# Parse arguments to determine target branches
if [[ "$ARGUMENTS" == *"--all-worktrees"* ]]; then
  TARGET_BRANCHES=$(git worktree list | grep -v "bare" | awk '{print $3}' | sed 's/\[//g' | sed 's/\]//g')
elif [[ -n "$ARGUMENTS" && "$ARGUMENTS" != *"--"* ]]; then
  TARGET_BRANCHES="$ARGUMENTS"
else
  TARGET_BRANCHES=$(git branch --show-current)
fi
```

### 2. Pre-Merge Validation

**For each target branch:**

```bash
# Check for uncommitted changes
cd "$WORKTREE_PATH"
if [[ $(git status --porcelain | wc -l) -gt 0 ]]; then
  echo "⚠️  Branch $BRANCH has uncommitted changes"
  NEEDS_COMMIT=true
fi

# Ensure branch is up-to-date with remote
git fetch origin
LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/$BRANCH 2>/dev/null || echo "")
if [[ "$LOCAL" != "$REMOTE" && -n "$REMOTE" ]]; then
  echo "⚠️  Branch $BRANCH differs from origin/$BRANCH"
  NEEDS_PUSH=true
fi

# Check if branch is behind main
BEHIND=$(git rev-list --count HEAD..origin/main)
if [[ $BEHIND -gt 0 ]]; then
  echo "⚠️  Branch $BRANCH is $BEHIND commits behind main"
  NEEDS_REBASE=true
fi
```

### 3. Conflict Detection

```bash
# For each branch, check potential conflicts with main
for BRANCH in $TARGET_BRANCHES; do
  echo "Checking conflicts for $BRANCH..."
  
  # Get files modified in branch
  BRANCH_FILES=$(git diff --name-only origin/main...$BRANCH)
  
  # Get files modified in main since branch point
  MERGE_BASE=$(git merge-base origin/main $BRANCH)
  MAIN_FILES=$(git diff --name-only $MERGE_BASE..origin/main)
  
  # Find overlapping files
  CONFLICTS=$(comm -12 <(echo "$BRANCH_FILES" | sort) <(echo "$MAIN_FILES" | sort))
  
  if [[ -n "$CONFLICTS" ]]; then
    echo "⚠️  Potential conflicts in:"
    echo "$CONFLICTS" | sed 's/^/    /'
  fi
done
```

### 4. Test Impact Analysis

```bash
# Identify test files affected by changes
AFFECTED_TESTS=""
for BRANCH in $TARGET_BRANCHES; do
  # Get changed files
  CHANGED_FILES=$(git diff --name-only origin/main...$BRANCH)
  
  # Find related test files
  for FILE in $CHANGED_FILES; do
    # Extract base name and look for tests
    BASE=$(basename "$FILE" | sed 's/\.[^.]*$//')
    DIR=$(dirname "$FILE")
    
    # Common test patterns
    TESTS=$(fd -t f "(${BASE}[._-]test|test[._-]${BASE}|${BASE}[._-]spec|spec[._-]${BASE})\.(ts|js|rs|go|java)$")
    AFFECTED_TESTS+="$TESTS"
  done
done

# Remove duplicates
UNIQUE_TESTS=$(echo "$AFFECTED_TESTS" | tr ' ' '\n' | sort -u | tr '\n' ' ')
```

### 5. Integration Test Strategy

```bash
# Generate test commands for affected code
cat > /tmp/$PROJECT/merge-test-plan.sh << 'EOF'
#!/bin/bash
set -e

echo "🧪 Running integration tests for merge preparation..."

# Test each branch individually
%BRANCH_TESTS%

# Test merge combinations if specified
%INTEGRATION_TESTS%

echo "✅ All tests passed!"
EOF

# Make executable
chmod +x /tmp/$PROJECT/merge-test-plan.sh
```

### 6. Generate Merge Strategy

```typescript
// Create merge-strategy.json
const mergeStrategy = {
  project: projectName,
  timestamp: new Date().toISOString(),
  branches: targetBranches.map((branch) => ({
    name: branch,
    status: {
      hasUncommittedChanges: false,
      isBehindMain: false,
      needsPush: false,
      potentialConflicts: [],
    },
    testResults: {
      passed: false,
      affectedTests: [],
      coverage: null,
    },
    mergeOrder: 0, // Will be calculated
  })),
  recommendedOrder: [],
  integrationSteps: [],
};

// Calculate optimal merge order
// Branches with fewer conflicts merge first
// Dependencies considered if found in coordination files
```

### 7. PR Preparation

```bash
# For each branch ready to merge
for BRANCH in $READY_BRANCHES; do
  cd $(git worktree list | grep "\[$BRANCH\]" | awk '{print $1}')
  
  # Check if PR exists
  PR_EXISTS=$(gh pr list --head "$BRANCH" --json number --jq '.[0].number' || echo "")
  
  if [[ -z "$PR_EXISTS" ]]; then
    # Prepare PR body with context
    cat > /tmp/pr-body.md << EOF
## Summary

Merging $BRANCH as part of coordinated integration.

## Changes

$(git log origin/main..$BRANCH --oneline | head -10)

## Testing

- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] No conflicts with other branches

## Integration Notes

Part of multi-branch integration:
$TARGET_BRANCHES

See coordination status: /tmp/$PROJECT/merge-strategy.json
EOF
    
    echo "📝 PR template created for $BRANCH"
  else
    echo "✓ PR #$PR_EXISTS already exists for $BRANCH"
  fi
done
```

### 8. Create Integration Checklist

```markdown
# Integration Checklist for $PROJECT

Generated: $(date)

## Pre-Merge Requirements

### Branch Status

%BRANCH_STATUS_CHECKS%

### Conflict Resolution

%CONFLICT_CHECKS%

### Testing

- [ ] All unit tests pass on individual branches
- [ ] Integration tests pass across branches
- [ ] Performance benchmarks acceptable
- [ ] Security scans clean

## Merge Sequence

Recommended order based on conflicts and dependencies:
%MERGE_ORDER%

## Post-Merge Tasks

- [ ] Update documentation
- [ ] Run full test suite on main
- [ ] Deploy to staging
- [ ] Notify team of integration

## Rollback Plan

%ROLLBACK_STEPS%
```

### 9. Coordination File Updates

```bash
# Update worktree status
cat > /tmp/$PROJECT/merge-status.json << EOF
{
  "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "preparedBy": "$(git config user.name || echo "Claude")",
  "branches": $BRANCH_STATUS_JSON,
  "conflicts": $CONFLICTS_JSON,
  "testPlan": "/tmp/$PROJECT/merge-test-plan.sh",
  "integrationChecklist": "/tmp/$PROJECT/integration-checklist.md",
  "nextSteps": [
    "Review and resolve conflicts",
    "Run integration tests",
    "Create/update PRs",
    "Coordinate merge timing"
  ]
}
EOF
```

### 10. Summary Output

```
🔀 Merge Preparation Complete!

📊 Branch Analysis:
  ✓ feature-auth: Ready (no conflicts)
  ⚠️  feature-api: 3 potential conflicts
  ✓ bugfix-123: Ready (tests pass)

🧪 Test Requirements:
  - 15 test files need to run
  - Estimated time: 5 minutes

📋 Integration Checklist:
  Created: /tmp/awesome-app/integration-checklist.md

🔄 Recommended Merge Order:
  1. bugfix-123 (no conflicts)
  2. feature-auth (no conflicts) 
  3. feature-api (requires conflict resolution)

📝 Next Steps:
  1. Resolve conflicts in feature-api
  2. Run: /tmp/awesome-app/merge-test-plan.sh
  3. Create PRs with: gh pr create
  4. Coordinate merge timing with team

💡 Quick Commands:
  - View conflicts: cat /tmp/awesome-app/conflicts-feature-api.txt
  - Run tests: /tmp/awesome-app/merge-test-plan.sh
  - Check status: cat /tmp/awesome-app/merge-status.json
```

## Advanced Features

### Dependency Detection

If PLAN.md or coordination files specify dependencies:

- Respect task dependencies when ordering merges
- Warn about incomplete dependencies
- Suggest coordination with other agents

### Automated PR Creation

When `--create-prs` flag is used:

- Create PRs for branches without them
- Update existing PRs with integration context
- Link related PRs in descriptions
- Add integration labels

### Test Orchestration

Smart test execution:

- Run only affected tests first
- Parallelize independent test suites
- Cache test results between branches
- Generate coverage reports

## Integration Patterns

### Sequential Integration

Best for dependent features:

```
main ← feature-base ← feature-extension ← feature-ui
```

### Parallel Integration

For independent features:

```
main ← feature-auth
     ← feature-api  
     ← bugfix-perf
```

### Staged Integration

For large changes:

```
main ← integration ← feature-1
                   ← feature-2
                   ← feature-3
```

## Best Practices

1. **Run early and often** to catch conflicts before they grow
2. **Coordinate timing** with team members or other agents
3. **Test incrementally** rather than all at once
4. **Document decisions** in PR descriptions
5. **Keep branches small** for easier integration

This command streamlines the complex process of integrating multiple parallel development efforts, ensuring smooth collaboration in multi-agent workflows.
