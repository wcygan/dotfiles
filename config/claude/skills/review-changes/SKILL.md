---
name: review-changes
description: Orchestrate multiple review agents for a comprehensive pre-PR code review. Analyzes diff, verifies intent alignment with linked issues, and checks for broader codebase impacts. Use before opening a PR to catch bugs, security issues, silent failures, and performance problems. Keywords: review, code review, pre-PR, diff review, check changes, audit changes
disable-model-invocation: true
context: fork
---

# Pre-PR Code Review

Orchestrate parallel review agents to comprehensively analyze staged and unstaged changes before opening a PR. Each agent reviews through a different lens, producing prioritized findings.

## Workflow

### 1. Gather Context

Collect all information needed for review:

```bash
# Get the current branch
BRANCH=$(git branch --show-current)

# Get unstaged changes
git diff

# Get staged changes
git diff --staged

# Get all commits on this branch not on main
git log --oneline main..HEAD

# Full diff against main
git diff main...HEAD
```

If on a branch with an existing PR, read the PR description:

```bash
gh pr view --json title,body,labels,milestone 2>/dev/null
```

If the PR or commits reference issues, read them:

```bash
# Extract issue numbers from PR body or commit messages
gh issue view <NUMBER> --json title,body,labels,comments 2>/dev/null
```

### 2. Spawn Parallel Review Agents

Use the Task tool to spawn 4 parallel sub-agents. Pass each agent the full diff context.

#### Agent 1: Code Reviewer

Focus: Bugs, logic errors, security, code quality.

```
Review this diff for:
- Logic errors and off-by-one bugs
- Null/undefined safety issues
- Resource leaks (unclosed handles, missing cleanup)
- Race conditions or concurrency issues
- Security vulnerabilities (injection, XSS, CSRF, auth bypass)
- Code quality (naming, duplication, complexity)
- API contract violations
Report each finding with: severity, file:line, description, suggestion.
```

#### Agent 2: Silent Failure Hunter

Focus: Error handling, swallowed errors, bad fallbacks.

```
Review this diff for silent failure patterns:
- Empty catch blocks or catch-and-ignore
- Missing error propagation (errors caught but not re-thrown or logged)
- Fallback values that mask bugs (default empty arrays, null coalescing to wrong values)
- Missing null checks before operations that will fail silently
- Promises without .catch() or missing await
- try/catch blocks that swallow important context
- Logging that drops error details (logging message but not the error object)
- Missing validation that causes downstream silent corruption
Report each finding with: severity, file:line, description, what could go wrong.
```

#### Agent 3: Performance Analyst

Focus: Algorithmic complexity, bottlenecks, resource usage.

```
Review this diff for performance concerns:
- O(n^2) or worse algorithms (nested loops over collections)
- N+1 query patterns
- Missing pagination on unbounded queries
- Large allocations in hot paths
- Synchronous I/O blocking async flows
- Missing caching opportunities for expensive operations
- Regex patterns vulnerable to ReDoS
- Unbounded growth (maps/arrays that grow without limit)
Report each finding with: severity, file:line, description, estimated impact.
```

#### Agent 4: Type Design Analyzer

Focus: Type design quality, encapsulation, invariants.

```
Review this diff for type design issues:
- Overly broad types (any, unknown, Record<string, any>)
- Missing discriminated unions where variants exist
- Stringly-typed values that should be enums or branded types
- Mutable state that should be readonly
- Leaky abstractions exposing internal details
- Missing invariant enforcement (constructor validation, factory methods)
- Type assertions (as) that bypass safety
- Optional fields that should be required or vice versa
Report each finding with: severity, file:line, description, suggested improvement.
```

### 3. Cross-Reference Intent

After all agents report back, cross-reference findings against the stated intent:

- **Does the diff match the PR/issue description?** Flag changes that seem unrelated to the stated goal.
- **Are there missing changes?** If the issue says "fix X and Y" but only X is addressed, flag it.
- **Are there scope creep changes?** Refactors or feature additions mixed into a bug fix.

### 4. Check Broader Impact

Look for changes that could break callers or contracts:

- **Exported function signatures changed?** Check for callers in the codebase.
- **Database schema changes?** Check for migrations and backward compatibility.
- **Config format changes?** Check for dependent services or deployment configs.
- **API response shape changed?** Check for consumers.

```bash
# For each changed exported symbol, search for usages
rg "functionName" --type-add 'src:*.{ts,js,py,go,rs}' -t src
```

### 5. Output Format

Present findings as a structured report:

```markdown
## Code Review: [branch-name]

### Intent Alignment
- [PASS/WARN] Changes match stated intent: [summary]
- [WARN] Missing: [anything the issue/PR mentions but isn't addressed]
- [WARN] Out of scope: [changes not related to stated intent]

### Critical
- [FILE:LINE] Description of critical issue
  Suggestion: how to fix

### Warning
- [FILE:LINE] Description of warning
  Suggestion: how to fix

### Info
- [FILE:LINE] Description of informational finding
  Suggestion: optional improvement

### Broader Impact
- [PASS/WARN] No breaking changes to public API / [description of impact]

### Summary
X critical, Y warnings, Z info findings across N files.
```

## Notes

- Adapt agent prompts to the language/framework detected in the diff.
- If there are no staged or unstaged changes, review commits on the branch vs main.
- If there is no PR yet, skip the intent alignment section.
- Keep findings actionable: every finding should include a specific suggestion.
