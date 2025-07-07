---
allowed-tools: Bash(gh:*), Bash(git:*), Bash(jq:*), Bash(gdate:*), Bash(osascript:*), Write, Read
description: Comprehensive PR status monitoring with CI/CD state analysis and merge readiness validation
---

## Context

- Session ID: !`gdate +%s%N 2>/dev/null || date +%s%N 2>/dev/null || echo "$(date +%s)$(jot -r 1 100000 999999 2>/dev/null || shuf -i 100000-999999 -n 1 2>/dev/null || echo $RANDOM$RANDOM)"`
- Current directory: !`pwd`
- Current branch: !`git branch --show-current 2>/dev/null || echo "no-git-repo"`
- Git status: !`git status --porcelain 2>/dev/null | wc -l | tr -d ' ' || echo "0"` files changed
- Remote origin: !`git remote get-url origin 2>/dev/null | sed 's/.*github.com[:/]\([^/]*\/[^.]*\).*/\1/' || echo "no-remote"`
- Available PRs: !`gh pr list --json number,title,state 2>/dev/null | jq length 2>/dev/null || echo "0"`
- Open PRs by author: !`gh pr list --author @me --state open --json number 2>/dev/null | jq length 2>/dev/null || echo "0"`
- Default branch PR: !`gh pr view --json number,state 2>/dev/null | jq -r '.number // "none"' 2>/dev/null || echo "none"`
- GitHub CLI status: !`gh auth status 2>/dev/null | head -1 || echo "Not authenticated"`

## Your Task

Provide comprehensive pull request status monitoring and analysis using systematic evaluation of CI/CD state, review status, and merge readiness.

STEP 1: Initialize PR monitoring session and parameter validation

- CREATE session state file: `/tmp/pr-check-state-$SESSION_ID.json`
- SET initial state:
  ```json
  {
    "sessionId": "$SESSION_ID",
    "timestamp": "$(gdate -Iseconds 2>/dev/null || date -Iseconds)",
    "pr_number": null,
    "monitoring_mode": "single_check",
    "analysis_depth": "standard"
  }
  ```

- PARSE command arguments from $ARGUMENTS:
  - IF $ARGUMENTS contains PR number: Extract and validate PR exists
  - ELSE IF current branch has associated PR: Auto-detect PR number
  - ELSE: List available PRs for selection

- VALIDATE GitHub CLI authentication and repository access
- UPDATE session state with validated PR number and context

STEP 2: Comprehensive PR status analysis with intelligent depth detection

Think deeply about the optimal analysis strategy based on PR complexity, CI/CD pipeline depth, and merge requirements.

- DETERMINE analysis scope based on PR characteristics:
  - **Simple PRs**: Basic status, reviews, checks
  - **Complex PRs**: Extended analysis with CI/CD deep dive
  - **Enterprise PRs**: Full compliance and security analysis

- ANALYZE PR metadata and determine monitoring requirements:
  ```bash
  gh pr view $PR_NUMBER --json state,mergeable,mergeStateStatus,statusCheckRollup,reviewDecision,reviews,author,createdAt,updatedAt,additions,deletions,changedFiles
  ```

- ASSESS CI/CD pipeline complexity:
  ```bash
  gh pr checks $PR_NUMBER --json name,state,conclusion,startedAt,completedAt
  ```

STEP 3: Multi-dimensional PR status evaluation with conditional analysis

CASE analysis_depth:
WHEN "standard":

- EXECUTE core status evaluation:
  1. **Basic PR Information**:
     ```bash
     gh pr view $PR_NUMBER --json title,author,state,createdAt,updatedAt,additions,deletions,changedFiles
     ```

  2. **Review Status Assessment**:
     ```bash
     gh pr view $PR_NUMBER --json reviewDecision,reviews
     ```

  3. **CI/CD Checks Overview**:
     ```bash
     gh pr checks $PR_NUMBER
     ```

  4. **Merge Readiness Validation**:
     ```bash
     gh pr view $PR_NUMBER --json mergeable,mergeStateStatus
     ```

WHEN "comprehensive":

- Think harder about comprehensive analysis patterns for complex PRs
- EXECUTE extended analysis with detailed CI/CD monitoring:
  1. **Full Status Check Rollup**:
     ```bash
     gh pr view $PR_NUMBER --json statusCheckRollup
     ```

  2. **Detailed Check Analysis**:
     ```bash
     gh api repos/{owner}/{repo}/commits/$(gh pr view $PR_NUMBER --json headRefOid -q .headRefOid)/check-runs
     ```

  3. **Workflow Run Analysis**:
     ```bash
     gh run list --branch $(gh pr view $PR_NUMBER --json headRefName -q .headRefName) --json databaseId,status,conclusion,createdAt
     ```

  4. **Branch Protection Analysis**:
     ```bash
     gh api repos/{owner}/{repo}/branches/$(gh pr view $PR_NUMBER --json baseRefName -q .baseRefName)/protection
     ```

STEP 4: Intelligent CI/CD monitoring with failure analysis

TRY:

- EXECUTE systematic CI/CD status evaluation:
  1. **Check Status Inventory**:
     ```bash
     gh pr checks $PR_NUMBER --json name,state,conclusion,startedAt,completedAt
     ```

  2. **Failing Checks Identification**:
     ```bash
     gh pr checks $PR_NUMBER --json name,state,conclusion | jq -r '.[] | select(.conclusion == "failure") | .name'
     ```

  3. **IF failing checks detected**:
     - GET detailed failure logs:
       ```bash
       gh run list --branch $(gh pr view $PR_NUMBER --json headRefName -q .headRefName) --json databaseId,status,conclusion | jq -r '.[] | select(.conclusion == "failure") | .databaseId'
       ```
     - ANALYZE failure patterns and provide remediation suggestions

  4. **Pending Checks Monitoring**:
     ```bash
     gh pr checks $PR_NUMBER --json name,state | jq -r '.[] | select(.state == "pending" or .state == "in_progress") | .name'
     ```

CATCH (ci_analysis_failed):

- LOG CI/CD analysis errors to session state
- PROVIDE manual check instructions
- CONTINUE with available status information
- SAVE fallback monitoring commands

STEP 5: Advanced merge conflict detection and resolution guidance

- EXECUTE comprehensive merge analysis:
  1. **Merge Conflict Detection**:
     ```bash
     gh pr view $PR_NUMBER --json mergeable,mergeStateStatus
     ```

  2. **IF merge conflicts detected**:
     - CREATE temporary conflict analysis:
       ```bash
       git fetch origin pull/$PR_NUMBER/head:temp-pr-$PR_NUMBER
       git checkout temp-pr-$PR_NUMBER
       git merge origin/$(gh pr view $PR_NUMBER --json baseRefName -q .baseRefName) --no-commit --no-ff
       ```
     - IDENTIFY conflicting files:
       ```bash
       git diff --name-only --diff-filter=U
       ```
     - CLEANUP temporary branch:
       ```bash
       git merge --abort; git checkout -; git branch -D temp-pr-$PR_NUMBER
       ```

  3. **Branch Protection Compliance**:
     ```bash
     gh api repos/{owner}/{repo}/branches/$(gh pr view $PR_NUMBER --json baseRefName -q .baseRefName)/protection --jq '.required_status_checks.contexts[]'
     ```

STEP 6: Comprehensive status report generation with actionable insights

- GENERATE structured status report: `/tmp/pr-check-report-$SESSION_ID.md`
- INCLUDE in report:
  - **Executive Summary**: PR readiness score and key blockers
  - **Review Status**: Approval state and required actions
  - **CI/CD Health**: Check status and failure analysis
  - **Merge Readiness**: Conflict status and requirements
  - **Action Items**: Prioritized next steps for PR advancement
  - **Compliance Check**: Branch protection and policy adherence

- SAVE detailed analysis to session state
- PROVIDE real-time monitoring options if requested

STEP 7: Conditional real-time monitoring and notification setup

IF $ARGUMENTS contains "watch" OR "monitor":

- Think deeply about optimal monitoring patterns for long-running CI/CD pipelines
- IMPLEMENT real-time monitoring loop:
  ```bash
  while true; do
    clear
    echo "PR #$PR_NUMBER Status - $(gdate '+%Y-%m-%d %H:%M:%S' 2>/dev/null || date '+%Y-%m-%d %H:%M:%S')"
    echo "=====================================\n"
    
    # Status summary
    gh pr checks $PR_NUMBER | head -10
    
    # Review decision
    echo "\nReview Status:"
    gh pr view $PR_NUMBER --json reviewDecision -q .reviewDecision
    
    # Merge readiness
    echo "\nMerge Status:"
    gh pr view $PR_NUMBER --json mergeable,mergeStateStatus | jq -r '"Mergeable: \(.mergeable) | State: \(.mergeStateStatus)"'
    
    sleep 30
  done
  ```

- OPTIONAL: Set up completion notifications:
  ```bash
  osascript -e 'display notification "PR checks completed!" with title "PR #'$PR_NUMBER'"'
  ```

FINALLY:

- UPDATE session state with completion status
- SAVE monitoring session log: `/tmp/pr-check-session-$SESSION_ID.log`
- CLEAN UP temporary files and branches

## Usage Patterns

### Basic Usage

```bash
# Check current branch PR
/pr-check

# Check specific PR
/pr-check 123

# Comprehensive analysis
/pr-check 123 comprehensive

# Real-time monitoring
/pr-check 123 watch
```

### Advanced Monitoring

```bash
# Enterprise compliance check
/pr-check 456 enterprise

# Focus on CI/CD issues
/pr-check 789 checks

# Merge readiness assessment
/pr-check 123 mergeable
```

## Status Indicators

### PR States

- `OPEN` - PR is open and active
- `CLOSED` - PR was closed without merging
- `MERGED` - PR was successfully merged

### Check States

- `PENDING` - Check is queued or running
- `SUCCESS` - Check passed
- `FAILURE` - Check failed
- `NEUTRAL` - Check completed with warnings
- `CANCELLED` - Check was cancelled
- `SKIPPED` - Check was skipped
- `TIMED_OUT` - Check exceeded time limit

### Review States

- `APPROVED` - PR has required approvals
- `CHANGES_REQUESTED` - Changes requested by reviewers
- `REVIEW_REQUIRED` - Awaiting required reviews
- `COMMENTED` - Reviews with comments only

### Merge States

- `MERGEABLE` - Ready to merge
- `CONFLICTING` - Has merge conflicts
- `UNKNOWN` - GitHub is still calculating

## Extended Thinking Integration

**For Complex PR Analysis:**

- Use "think deeply" for multi-service PR impact analysis
- Use "think harder" for security and compliance review
- Use "ultrathink" for enterprise architecture change assessment

**Enhanced Analysis Areas:**

- Cross-repository dependency impact assessment
- Security vulnerability and compliance validation
- Performance impact analysis for large changes
- Migration strategy evaluation for breaking changes

## Examples

### Basic Status Check

```bash
# Check current branch PR
/pr-check

# Check specific PR
/pr-check 123
```

### CI/CD Monitoring

```bash
# View all checks
/pr-check checks 456

# Watch checks until completion
/pr-check watch 456
```

### Review Status

```bash
# Check review status
/pr-check reviews 789

# Full merge readiness report
/pr-check mergeable 789
```

### Conflict Resolution

```bash
# Check for conflicts
/pr-check conflicts 123

# Get detailed conflict information
gh pr view 123 --json mergeable,mergeStateStatus,potentialMergeCommit
```

## Status Indicators

### PR States

- `OPEN` - PR is open and active
- `CLOSED` - PR was closed without merging
- `MERGED` - PR was successfully merged

### Check States

- `PENDING` - Check is queued or running
- `SUCCESS` - Check passed
- `FAILURE` - Check failed
- `NEUTRAL` - Check completed with warnings
- `CANCELLED` - Check was cancelled
- `SKIPPED` - Check was skipped
- `TIMED_OUT` - Check exceeded time limit

### Review States

- `APPROVED` - PR has required approvals
- `CHANGES_REQUESTED` - Changes requested by reviewers
- `REVIEW_REQUIRED` - Awaiting required reviews
- `COMMENTED` - Reviews with comments only

### Merge States

- `MERGEABLE` - Ready to merge
- `CONFLICTING` - Has merge conflicts
- `UNKNOWN` - GitHub is still calculating

## Troubleshooting

### Common Issues

#### Stuck Checks

```bash
# Re-run failed checks
gh pr checks $PR_NUMBER --json name,state | \
  jq -r '.[] | select(.state == "FAILURE") | .name' | \
  xargs -I {} gh workflow run {} --ref $(gh pr view $PR_NUMBER --json headRefName -q .headRefName)
```

#### Missing Required Checks

```bash
# List required checks
gh api repos/{owner}/{repo}/branches/main/protection/required_status_checks

# Trigger missing checks
gh pr comment $PR_NUMBER --body "/test all"
```

#### Review Dismissal

```bash
# Check why reviews were dismissed
gh api repos/{owner}/{repo}/pulls/$PR_NUMBER/reviews | \
  jq '.[] | select(.dismissed_at != null) | {user: .user.login, dismissed_at: .dismissed_at}'
```

## Integration with Other Commands

- Use after `/pr` to monitor your new PR
- Use during `/pr-review` to check CI status
- Use before merging to ensure all requirements met
- Combine with `/pr-update` to fix failing checks

## Automation Scripts

### PR Health Dashboard

```bash
# Check all your open PRs
gh pr list --author @me --json number,title --jq '.[] | .number' | \
  xargs -I {} sh -c 'echo "PR #{}: " && gh pr checks {} | grep -E "(SUCCESS|FAILURE)" | wc -l'
```

### Notification on Completion

```bash
# Wait for checks and notify
gh pr checks $PR_NUMBER --watch && \
  osascript -e 'display notification "All checks passed!" with title "PR #'$PR_NUMBER'"'
```

## See Also

- `/pr` - Create pull requests
- `/pr-review` - Review pull requests
- `/pr-update` - Update pull requests
