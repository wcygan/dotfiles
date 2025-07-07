---
allowed-tools: Task, Bash(gh pr view:*), Bash(gh pr list:*), Bash(gh pr review:*), Bash(gh pr diff:*), Bash(gh pr checks:*), Bash(gh pr edit:*), Bash(gh api:*), Bash(git branch:*), Bash(rg:*), Bash(delta:*), Bash(jq:*), Bash(gdate:*)
description: Review and manage pull requests with comprehensive analysis and smart recommendations
---

## Context

- Session ID: !`gdate +%s%N`
- Current branch: !`git branch --show-current 2>/dev/null || echo "detached-head"`
- Current branch PR: !`gh pr list --head "$(git branch --show-current 2>/dev/null || echo none)" --json number,title,state | jq -r '.[0].number // "none"' 2>/dev/null || echo "none"`
- PRs for review: !`gh pr list --search "review-requested:@me" --json number,title,author | jq length 2>/dev/null || echo "0"`
- Mentioned in PRs: !`gh pr list --search "mentions:@me" --json number,title | jq length 2>/dev/null || echo "0"`
- Open PRs count: !`gh pr list --state open --json number | jq length 2>/dev/null || echo "0"`
- Repository: !`gh repo view --json nameWithOwner,url | jq -r '.nameWithOwner // "unknown"' 2>/dev/null || echo "unknown"`
- GitHub auth status: !`gh auth status 2>&1 | head -1 || echo "Not authenticated"`

## Your task

STEP 1: Initialize PR review session

- CREATE session state: `/tmp/pr-review-state-$SESSION_ID.json`
- INITIALIZE review session with timestamp and context
- PARSE arguments from $ARGUMENTS for action and PR number
- SET session data:
  ```json
  {
    "sessionId": "$SESSION_ID",
    "timestamp": "ISO_8601_TIMESTAMP",
    "action": "auto-detect",
    "prNumber": null,
    "repository": "auto-detect",
    "reviewPhase": "initialization",
    "analysisResults": {},
    "reviewDecisions": [],
    "errorLog": []
  }
  ```

STEP 2: Parse arguments and determine review action

IF $ARGUMENTS is empty:

- SET action = "discover_prs"
- FOCUS on PRs assigned for review and current branch PR

ELSE IF $ARGUMENTS starts with action keyword (approve|comment|request-changes|diff|checks|files):

- EXTRACT action and optional PR number
- SET review_action = detected action

ELSE IF $ARGUMENTS is numeric:

- SET prNumber = $ARGUMENTS
- SET action = "review_specific_pr"

ELSE:

- LOG invalid arguments to session state
- PROVIDE usage examples and available PRs

STEP 3: Execute PR discovery or direct review

CASE action:
WHEN "discover_prs":

TRY:

- FETCH PRs assigned for review: `gh pr list --search "review-requested:@me" --json number,title,author,createdAt`
- FETCH current branch PR: `gh pr list --head $(git branch --show-current) --json number,title,state`
- FETCH mentioned PRs: `gh pr list --search "mentions:@me" --json number,title,state`
- DISPLAY interactive PR selection with priorities:
  1. PRs explicitly assigned for review (highest priority)
  2. Current branch PR (if exists)
  3. PRs where mentioned (lowest priority)
- SAVE PR list to session state

WHEN "review_specific_pr":

- VALIDATE PR number exists and is accessible
- PROCEED to comprehensive PR analysis

CATCH (github_api_error):

- LOG API errors to session state
- CHECK GitHub authentication status
- PROVIDE troubleshooting guidance
- FALLBACK to manual PR specification

STEP 4: Comprehensive PR analysis (with sub-agent delegation for complex PRs)

Think deeply about the optimal review strategy based on PR characteristics and complexity.

TRY:

- FETCH PR metadata: `gh pr view $PR_NUMBER --json title,body,state,author,assignees,labels,milestone,files`
- ANALYZE PR complexity based on:
  - File count and change volume
  - Code patterns and languages involved
  - Security implications
  - Testing requirements

IF PR complexity is high (>20 files OR >1000 lines changed OR security-sensitive):

- Think harder about comprehensive review coordination and potential architectural impacts
- USE Task tool for parallel analysis with 4 specialized sub-agents:

  1. **Code Quality Agent**: Analyze code patterns, anti-patterns, and maintainability
     - SAVE findings to: `/tmp/pr-review-$SESSION_ID/code-quality.json`
     - FOCUS: Code smells, complexity, design patterns, refactoring opportunities

  2. **Security Analysis Agent**: Perform security-focused review
     - SAVE findings to: `/tmp/pr-review-$SESSION_ID/security-analysis.json`
     - FOCUS: Vulnerability patterns, credential exposure, input validation, authorization

  3. **Performance Impact Agent**: Assess performance implications
     - SAVE findings to: `/tmp/pr-review-$SESSION_ID/performance-impact.json`
     - FOCUS: Query optimization, bundle size, memory usage, algorithmic complexity

  4. **Testing & Documentation Agent**: Evaluate test coverage and documentation
     - SAVE findings to: `/tmp/pr-review-$SESSION_ID/testing-docs.json`
     - FOCUS: Test completeness, edge cases, documentation updates, API changes

- COORDINATE: Wait for all agents to complete analysis
- SYNTHESIZE: Combine findings into comprehensive review assessment

ELSE:

- EXECUTE direct analysis using core review commands:
  - `gh pr diff $PR_NUMBER --stat`
  - `gh pr view $PR_NUMBER --json reviews,reviewDecision,statusCheckRollup`
  - `gh pr diff $PR_NUMBER | rg -i "TODO|FIXME|XXX|HACK|password|secret|token|api_key"`

CATCH (pr_analysis_failed):

- LOG analysis failures to session state
- PROVIDE manual review guidance
- SAVE partial analysis results

STEP 5: Execute review actions with smart recommendations

CASE review_action:
WHEN "approve":

- CONFIRM PR passes quality checks and CI
- EXECUTE: `gh pr review $PR_NUMBER --approve --body "LGTM! Approved based on analysis."`
- LOG approval decision to session state

WHEN "comment":

- GENERATE constructive feedback based on analysis
- EXECUTE: `gh pr review $PR_NUMBER --comment --body "Review feedback"`
- SAVE comment to session state

WHEN "request-changes":

- COMPILE specific change requests from analysis
- EXECUTE: `gh pr review $PR_NUMBER --request-changes --body "Changes requested"`
- LOG change requests to session state

WHEN "diff":

- DISPLAY enhanced diff: `gh pr diff $PR_NUMBER | delta`
- HIGHLIGHT security and performance concerns from analysis

WHEN "checks":

- MONITOR CI status: `gh pr checks $PR_NUMBER`
- ANALYZE failing checks and provide remediation guidance

WHEN "files":

- LIST changed files with analysis priorities
- HIGHLIGHT files requiring focused review attention

ELSE:

- PROVIDE interactive review recommendations based on analysis
- SUGGEST specific review actions with justification

STEP 6: Session completion and cleanup

- UPDATE session state with final review decisions
- GENERATE review summary with key findings
- ARCHIVE analysis results: `/tmp/pr-review-archive-$SESSION_ID.json`
- CLEAN UP temporary session files
- PROVIDE next action recommendations

## Implementation Details

**Smart Review Patterns:**

```bash
# Automated quality checks
gh pr diff $PR_NUMBER | rg -i "TODO|FIXME|XXX|HACK"
gh pr diff $PR_NUMBER | rg -i "password|secret|token|api_key"
gh pr view $PR_NUMBER --json files --jq '.files[] | select(.additions > 500 or .deletions > 500)'

# Enhanced diff viewing
gh pr diff $PR_NUMBER | delta

# Comprehensive status monitoring
gh pr checks $PR_NUMBER --watch
gh api repos/{owner}/{repo}/commits/$(gh pr view $PR_NUMBER --json headRefOid -q .headRefOid)/check-runs

# Review collaboration
gh pr view $PR_NUMBER --json reviewRequests,reviews
gh api repos/{owner}/{repo}/pulls/$PR_NUMBER/reviews --jq '.[] | {user: .user.login, state: .state, submitted_at: .submitted_at}'
```

**Review Comment Templates:**

- Positive: "Great implementation! The error handling is particularly well thought out."
- Constructive: "Consider extracting this logic into a separate function for better testability."
- Security: "This could potentially expose sensitive data. Please add input validation."
- Performance: "This might cause N+1 queries. Consider using eager loading here."

**Error Recovery:**

- PR not found → Lists available PRs with suggestions
- No review permissions → Checks repository access and provides guidance
- Merge conflicts → Alerts about conflicts with resolution steps
- Failed checks → Shows specific failures with remediation advice
