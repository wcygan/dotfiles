---
name: babysit-pr
description: >
  Monitor open PRs and shepherd them toward merge. Checks CI status, review comments,
  merge conflicts, and takes action. Designed for /loop usage (e.g., /loop 5m /babysit-pr).
  Keywords: PR monitor, babysit, CI check, review response, merge conflict, PR status
disable-model-invocation: true
allowed-tools: Read, Grep, Glob, Bash, Edit
---

# Babysit PR

Loop-oriented workflow that monitors your open PRs and shepherds them toward merge.
Designed for `/loop 5m /babysit-pr`. Maintains state across iterations via conversation context.

## State Tracking

Track across iterations to avoid re-processing:
- **Addressed comment IDs** — skip reviews/comments already handled
- **Push count this iteration** — hard cap at 3 per iteration
- **Last seen CI status per PR** — only report changes

## Iteration Workflow

### 1. Discover Open PRs

```bash
gh pr list --author @me --state open \
  --json number,title,headRefName,statusCheckRollup,reviewDecision,mergeable
```

If no open PRs, report "No open PRs" and stop.

### 2. Evaluate Each PR (Priority Order)

Process PRs in this strict priority order. For each PR, check conditions top-to-bottom
and act on the **first** that applies:

#### Priority A: New Review Comments

Check for unaddressed review comments:

```bash
gh pr view {number} --json reviews,comments
gh api repos/{owner}/{repo}/pulls/{number}/comments
```

**Decision framework:**
- Skip comments you've already addressed (tracked by comment ID across iterations)
- Skip bot comments (dependabot, codecov, etc.)
- For actionable feedback: read the referenced code, understand the ask, then either:
  - Draft a code fix if the change is mechanical (typo, naming, missing check)
  - Draft a reply if it's a design discussion or clarification
- **PRESENT TO USER FOR APPROVAL** — show the draft response or diff, wait for confirmation

#### Priority B: CI Failures

Check `statusCheckRollup` for failed checks.

**Decision framework:**
- If status unchanged since last iteration, skip (already reported)
- Read failure logs: `gh run view {run-id} --log-failed`
- Categorize the failure:
  - **Mechanical** (lint, format, types, lockfile): prepare a fix commit, present for approval
  - **Flaky test** (passed before, non-deterministic): suggest `gh run rerun {run-id} --failed`
  - **Legitimate failure** (real test regression): diagnose root cause, report to user, stop
- If a fix attempt was already tried and failed, report diagnosis and **do not retry**

#### Priority C: Merge Conflicts

If `mergeable` is `"CONFLICTING"`:

```bash
git fetch origin
git checkout {branch}
git rebase origin/main
```

- If rebase succeeds cleanly: present result, ask before pushing
- If conflicts arise: describe each conflict clearly (file, nature of conflict), do not auto-resolve

#### Priority D: Ready to Merge

If ALL of: checks passing, reviews approved (or no reviews required), no conflicts:

- Report: "PR #{number} is ready to merge"
- **NEVER auto-merge** — user decides when to merge

### 3. Status Report

Output a brief table, then details only for PRs needing action:

```
| PR | Title | CI | Reviews | Conflicts | Action |
|----|-------|----|---------|-----------|--------|
| #42 | Add widget | passing | approved | clean | Ready to merge |
| #38 | Fix auth | failing | changes requested | clean | CI fix drafted |
```

If nothing changed since last iteration: "All PRs healthy — no changes since last check."

## Guardrails (Non-Negotiable)

1. **Max 3 pushes per iteration** across all PRs combined. Track count, stop when reached.
2. **NEVER** force-push, auto-merge, auto-approve, or post comments without user confirmation.
3. **NEVER** dismiss reviews or resolve review threads.
4. **NEVER** push code or post comments without presenting to user first.
5. If a CI fix attempt fails, report diagnosis and **stop** — no retries.
6. Track addressed comment IDs to avoid re-processing across loop iterations.
7. When drafting review responses, always show the draft and wait for user approval.

## Edge Cases

- **Multiple PRs need attention**: process highest-numbered (newest) first
- **PR in draft**: still monitor CI but skip review comment processing
- **Rate limiting**: if `gh` commands fail with 403/429, report and wait for next iteration
- **No repo context**: if not in a git repo, error immediately
- **Cross-repo PRs**: only process PRs for the current repo's remote
