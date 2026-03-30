---
name: post-merge-sweeper
description: Scan recently merged PRs for unaddressed review comments and create follow-up GitHub issues. Designed for /loop usage to continuously catch things that slipped through the merge. Keywords: merged PR, review comments, unresolved, follow-up, sweep, post-merge
disable-model-invocation: true
allowed-tools: Read, Grep, Glob, Bash
---

# Post-Merge Sweeper

Scan merged PRs for unaddressed review comments and create follow-up issues.
Designed for `/loop 10m /post-merge-sweeper`.

## Pre-loaded Context

**Repo:** !`gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || echo 'unknown'`

**Recently merged PRs (last 10):**
!`gh pr list --state merged --limit 10 --json number,title,mergedAt,author 2>/dev/null || echo '[]'`

**Already processed PRs:**
!`REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null | tr '/' '-'); cat "/tmp/.sweeper-processed-${REPO}" 2>/dev/null || echo '(none)'`

## Step 1: Filter Merged PRs

Using the pre-loaded data above:
- Filter to PRs merged in the **last 24 hours** only
- Skip PRs authored by bots (login contains `[bot]` or `dependabot` or `renovate`)
- Skip PRs whose number appears in the "Already processed" list
- If no unprocessed PRs remain, report "No new merged PRs to scan" and stop
- Derive OWNER/REPO_NAME from the repo name for API calls and tracker path

## Step 2: Analyze Review Comments

For each unprocessed PR, fetch:

```bash
gh api repos/{owner}/{repo}/pulls/{number}/comments
gh api repos/{owner}/{repo}/pulls/{number}/reviews
gh api repos/{owner}/{repo}/issues/{number}/comments
```

Identify **actionable unaddressed** comments — those that are:
- Explicitly marked unresolved in a review thread
- Questions that never received a reply from the PR author
- Requested changes with no evidence of follow-up commits
- Code suggestions (`suggestion` blocks) that were neither applied nor declined

**SKIP** comments that are:
- "nit", "optional", "nice to have", "minor", "take it or leave it"
- Emoji-only or thumbs-up reactions
- Purely conversational ("looks good", "thanks", "agreed")
- Already addressed by subsequent commits in the PR

## Step 3: Create Follow-Up Issues

**Max 3 issues per iteration** to avoid flooding.

Before creating, check for duplicates:
```bash
gh issue list --search "Follow-up from PR #<number>" --state open --json number,title
```

For each actionable comment, create an issue:

```bash
gh issue create \
  --title "Follow-up from PR #<number>: <brief description>" \
  --body "<body>" \
  --label "follow-up"
```

If the `follow-up` label doesn't exist, create it first:
```bash
gh label create follow-up --description "Unaddressed review comment" --color "c5def5" 2>/dev/null
```

Issue body should include:
- Link to the original PR comment (permalink URL)
- Quote of the reviewer's comment
- The relevant code context
- Brief explanation of what was requested

**Present each created issue to the user** with its URL and a one-line summary.

## Step 4: Track & Report

After processing each PR, append its number to `$TRACKER`:
```bash
echo "<number>" >> "$TRACKER"
```

Final report:
```
Scanned N merged PRs, created M follow-up issues.
[list created issues with URLs]
```
