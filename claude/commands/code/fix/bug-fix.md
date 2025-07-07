---
allowed-tools: Bash(git:*), Bash(gh:*), Read, Write, Edit, MultiEdit, Task, Bash(gdate:*)
description: Systematic bug investigation and fix workflow with GitHub integration
---

## Context

- Session ID: !`gdate +%s%N`
- Current directory: !`pwd`
- Git status: !`git status --porcelain || echo "Not a git repository"`
- Current branch: !`git branch --show-current 2>/dev/null || echo "No git repository"`
- Recent commits: !`git log --oneline -5 2>/dev/null || echo "No git history"`
- Working directory status: !`git diff --name-only 2>/dev/null | wc -l | tr -d ' ' || echo "0"` modified files
- Open issues: !`gh issue list --state open --json number,title --limit 5 2>/dev/null || echo "[]"`
- Repository info: !`git remote get-url origin 2>/dev/null || echo "No remote origin"`

## Your Task

Fix the bug described in: **$ARGUMENTS**

STEP 1: Bug Analysis and State Initialization

- Initialize session state file: /tmp/bug-fix-state-$SESSION_ID.json
- Parse bug description and extract key details
- Think deeply about potential root causes and affected systems
- FOR complex bugs: Use extended thinking to analyze the problem systematically

```json
// /tmp/bug-fix-state-$SESSION_ID.json
{
  "sessionId": "$SESSION_ID",
  "timestamp": "ISO_8601_TIMESTAMP",
  "bug": "$ARGUMENTS",
  "phase": "analysis",
  "analysis": {
    "rootCause": null,
    "affectedFiles": [],
    "reproductionSteps": [],
    "priority": "normal"
  },
  "workflow": {
    "issueNumber": null,
    "branchName": null,
    "prNumber": null,
    "fixApplied": false
  },
  "checkpoints": {
    "analysis_complete": false,
    "issue_created": false,
    "branch_created": false,
    "fix_implemented": false,
    "tests_verified": false,
    "pr_created": false
  }
}
```

STEP 2: Repository Validation and Preparation

TRY:

- Verify we're in a git repository
- Check for clean working directory OR warn about uncommitted changes
- Ensure gh CLI is authenticated: gh auth status
  CATCH (git not available):
- Exit with error: "This command requires a git repository"
  CATCH (gh not authenticated):
- Provide authentication instructions: gh auth login

STEP 3: GitHub Issue Creation

IF issue doesn't already exist:

- Create descriptive GitHub issue with bug details
- Use template format:
  ```
  ## Bug Description
  [Bug description from $ARGUMENTS]

  ## Expected Behavior
  [What should happen]

  ## Actual Behavior  
  [What currently happens]

  ## Steps to Reproduce
  1. [Step 1]
  2. [Step 2]

  ## Environment
  - Branch: [current branch]
  - Last commit: [latest commit hash]
  ```
- Update state with issue number
- Mark checkpoint: issue_created = true

STEP 4: Feature Branch Creation

- Generate branch name: bugfix/[sanitized-bug-description]
- Create and checkout branch: git checkout -b [branch-name]
- Update state with branch name
- Mark checkpoint: branch_created = true

STEP 5: Bug Investigation and Root Cause Analysis

FOR complex bugs requiring deep investigation:

- Use Task tool to delegate investigation to specialized sub-agents:
  - Code analysis agent for identifying problematic code patterns
  - Log analysis agent for examining error patterns
  - Dependency analysis agent for checking library conflicts
- Think harder about edge cases and system interactions

PROCEDURE investigate_bug():

- Search codebase for relevant files and functions
- Examine recent changes that might have introduced the bug
- Check for similar patterns in bug reports or commit history
- Identify test cases that should catch this bug
- Document findings in state file

STEP 6: Bug Fix Implementation

PROCEDURE apply_fix():

- Implement the minimal fix that addresses the root cause
- Add or update tests to prevent regression
- Verify fix doesn't break existing functionality
- Document the fix approach in commit preparation

TRY:

- Apply code changes systematically
- Run relevant tests to validate fix
- Update state: fixApplied = true, checkpoints.fix_implemented = true
  CATCH (tests fail):
- Analyze test failures
- Refine fix or update tests as needed
- Retry validation

STEP 7: Testing and Validation

PROCEDURE validate_fix():

- Run unit tests related to the bug
- Perform integration testing if applicable
- Manual testing of the specific bug scenario
- Check for potential side effects

- Update state: checkpoints.tests_verified = true

STEP 8: Commit and Push Changes

- Create semantic commit message following conventional commits:
  ```
  fix: [brief description of bug fix]

  - [Specific change 1]
  - [Specific change 2]

  Fixes #[issue-number]
  ```
- Commit changes: git commit -m "[commit message]"
- Push branch: git push -u origin [branch-name]

STEP 9: Pull Request Creation

- Create PR linking to the issue:
  ```bash
  gh pr create --title "Fix: [bug description]" --body "$(cat <<'EOF'
  ## Summary
  Fixes the bug described in #[issue-number]

  ## Changes Made
  - [Change 1]
  - [Change 2]

  ## Testing
  - [x] Unit tests pass
  - [x] Manual testing completed
  - [x] No regression detected

  ## Related Issues
  Fixes #[issue-number]
  EOF
  )"
  ```
- Update state with PR number
- Mark checkpoint: pr_created = true

STEP 10: Final State Update and Cleanup

- Update state file with completion status
- Mark all checkpoints as complete
- Set phase to "complete"
- Report success with issue/PR links

FINALLY:

- Cleanup temporary files if workflow completed successfully
- Preserve state file for 24 hours for potential debugging

## Error Recovery and Resumability

IF workflow is interrupted:

- Check state file for last completed checkpoint
- Resume from the appropriate step
- Validate current repository state matches expected state

## Advanced Bug Analysis Patterns

FOR performance bugs:

- Use profiling tools to identify bottlenecks
- Analyze memory usage patterns
- Check for algorithmic inefficiencies

FOR integration bugs:

- Examine API contracts and data flow
- Check configuration and environment differences
- Validate dependency versions and compatibility

FOR security bugs:

- Think harder about attack vectors and exploit scenarios
- Review input validation and sanitization
- Check for privilege escalation opportunities
- Ensure fix doesn't introduce new vulnerabilities

## State Management Schema

```json
{
  "sessionId": "$SESSION_ID",
  "timestamp": "2025-01-07T13:30:00Z",
  "bug": "User login fails with 500 error",
  "phase": "complete",
  "analysis": {
    "rootCause": "SQL injection vulnerability in authentication query",
    "affectedFiles": ["auth.js", "user-model.js"],
    "reproductionSteps": ["Navigate to login", "Enter malicious input"],
    "priority": "critical"
  },
  "workflow": {
    "issueNumber": 123,
    "branchName": "bugfix/user-login-500-error",
    "prNumber": 456,
    "fixApplied": true
  },
  "checkpoints": {
    "analysis_complete": true,
    "issue_created": true,
    "branch_created": true,
    "fix_implemented": true,
    "tests_verified": true,
    "pr_created": true
  },
  "session_isolation": {
    "temp_files": ["/tmp/bug-fix-state-$SESSION_ID.json"],
    "created_branches": ["bugfix/user-login-500-error"],
    "created_issues": [123],
    "created_prs": [456]
  }
}
```
