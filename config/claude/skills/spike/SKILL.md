---
name: spike
description: Quick prototype in an isolated git worktree. Creates a worktree, spawns agents to explore a technical approach, and opens a draft PR with findings. Use for time-boxed technical exploration, feasibility testing, or library evaluation. Keywords: spike, prototype, worktree, explore, feasibility, proof of concept, PoC, try, experiment, can we use
context: fork
disable-model-invocation: true
argument-hint: [description-of-what-to-explore]
allowed-tools: Read, Grep, Glob, Bash, Write, Edit
---

# Spike: Worktree-Based Prototyping

Quickly prototype a technical approach in an isolated git worktree. The spike produces working (or instructively failing) code and a draft PR documenting what was learned.

## When to Use

- "Can we use library X for this?"
- "What would it take to migrate from A to B?"
- "Is this API fast enough for our use case?"
- "How hard would it be to add feature Y?"
- Time-boxed exploration where the goal is learning, not production code

## Workflow

### 1. Parse the Exploration Goal

Read `$ARGUMENTS` to understand what the user wants to explore. Identify:

- **Goal**: What question are we answering?
- **Scope**: What's the minimum work to answer it?
- **Success criteria**: How do we know if the approach works?

### 2. Create an Isolated Worktree

Create a git worktree so the spike is fully isolated from the main working tree:

```bash
# Determine repo root and spike name
REPO_ROOT=$(git rev-parse --show-toplevel)
SPIKE_SLUG=$(echo "$ARGUMENTS" | tr '[:upper:]' '[:lower:]' | tr -cs 'a-z0-9' '-' | head -c 40 | sed 's/-$//')
SPIKE_DIR="${REPO_ROOT}/../spike-$(date +%Y%m%d-%H%M%S)"
BRANCH_NAME="spike/${SPIKE_SLUG}"

# Create worktree on a new branch from current HEAD
git worktree add "$SPIKE_DIR" -b "$BRANCH_NAME"
```

**Important**: All subsequent work happens in `$SPIKE_DIR`, not the main working tree. Use absolute paths for all file operations.

### 3. Prototype the Approach

Work in the worktree to answer the exploration question:

**If evaluating a library or tool:**
1. Add the dependency (npm install, pip install, cargo add, nix add, etc.)
2. Write a minimal integration that exercises the key functionality
3. Run it and capture the results
4. Note any compatibility issues, rough edges, or surprises

**If exploring an architecture change:**
1. Sketch the new structure with real (but minimal) code
2. Identify the hardest part and implement that first
3. Note what breaks, what's easy, and what's unexpectedly hard
4. List the files/modules that would need to change in a real implementation

**If testing feasibility or performance:**
1. Write a minimal benchmark or test case
2. Run it and capture numbers
3. Compare against requirements or current baseline
4. Note scaling characteristics (linear, quadratic, etc.)

### 4. Document Findings in the Worktree

Create a `SPIKE.md` file in the worktree root with structured findings:

```markdown
# Spike: [Title from $ARGUMENTS]

## Question
[What we set out to answer]

## Approach
[What we tried, in 2-3 sentences]

## Results

### What Worked
- [Finding 1]
- [Finding 2]

### What Didn't Work
- [Issue 1]
- [Issue 2]

### Surprises
- [Unexpected finding]

## Key Code Snippets

[Include the most instructive code from the spike]

## Recommendation
[One of: **Proceed**, **Proceed with caveats**, **Pivot**, **Abandon**]

### Rationale
[Why this recommendation, in 2-3 sentences]

### If Proceeding, Next Steps
1. [Step 1]
2. [Step 2]
3. [Step 3]

### Estimated Effort for Full Implementation
[Rough scope: small (hours), medium (days), large (weeks)]
```

### 5. Commit and Push

```bash
cd "$SPIKE_DIR"

# Stage everything
git add -A

# Commit with descriptive message
git commit -m "spike: [brief description of what was explored]

Explored: [1-line summary]
Result: [Proceed/Pivot/Abandon]
See SPIKE.md for full findings."

# Push the spike branch
git push -u origin "$BRANCH_NAME"
```

### 6. Open a Draft PR

```bash
cd "$SPIKE_DIR"

gh pr create \
  --draft \
  --title "Spike: [concise title]" \
  --body "$(cat <<'EOF'
## Spike Summary

**Question**: [What we explored]
**Result**: [Proceed / Proceed with caveats / Pivot / Abandon]

## Key Findings
- [Finding 1]
- [Finding 2]
- [Finding 3]

## Recommendation
[Brief recommendation and rationale]

---
*This is a spike PR for exploration purposes. Code is intentionally rough.
See `SPIKE.md` in the branch for full details.*
EOF
)"
```

### 7. Report Back

Return to the user with:
1. The draft PR URL
2. A brief summary of findings
3. The recommendation (proceed/pivot/abandon)
4. Cleanup instructions (see below)

## Cleanup

When the spike is done and findings are captured, the user can clean up:

```bash
# Remove the worktree (from the main repo)
git worktree remove ../spike-YYYYMMDD-HHMMSS

# Delete the remote branch (optional, after PR is closed)
git push origin --delete spike/description

# Delete the local branch
git branch -D spike/description
```

**Or keep it**: If the spike is worth continuing, the user can merge the draft PR or continue working in the worktree.

## Tips for Good Spikes

- **Time-box mentally**: A spike should answer "can we?" not "let's build it." Aim for the minimum code to learn.
- **Fail fast**: If something doesn't work in the first 10 minutes, that's a valid finding. Document it and move on.
- **Don't polish**: Spike code is disposable. Skip tests, linting, error handling. The output is knowledge, not code.
- **Commit messy**: One big commit is fine for a spike. The PR is for sharing findings, not for code review.
- **Include negative results**: "Library X doesn't support feature Y" is valuable. Document it.

## Example Invocations

**Library evaluation:**
```
/spike Can we use Tanstack Query to replace our custom data fetching layer?
```

**Architecture exploration:**
```
/spike What would it take to split the monolith's user service into its own package?
```

**Performance feasibility:**
```
/spike Can SQLite handle our read workload if we switch from Postgres for the config service?
```

**Migration scoping:**
```
/spike How hard is it to migrate from Jest to Vitest in the frontend package?
```

## Anti-Patterns

- **Don't build production code in a spike**: The worktree is for learning. Rewrite cleanly if proceeding.
- **Don't skip the SPIKE.md**: The whole point is documented findings. Code without context is useless after a week.
- **Don't spike in the main worktree**: Always use a git worktree. Keeps the main tree clean and the spike isolated.
- **Don't forget cleanup instructions**: Worktrees and branches left around cause confusion.
- **Don't spike without a clear question**: "Explore X" is too vague. "Can X do Y within constraint Z?" is actionable.
