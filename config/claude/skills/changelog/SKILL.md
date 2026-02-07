---
name: changelog
description: Generate a changelog or release notes from git history between two refs (tags, commits, or branches). Use when preparing a release, summarizing changes, or creating release notes. Keywords: changelog, release notes, release, changes, what changed, version, tag, diff, history, summary
context: fork
agent: Explore
disable-model-invocation: true
argument-hint: [from-ref] [to-ref]
allowed-tools: Read, Grep, Glob, Bash(git *)
---

# Changelog Generator

Generate structured release notes from git history between two refs. Categorizes commits by type, reads diffs for significant changes, and outputs a conventional changelog.

## When to Use

- Preparing a new release and need release notes
- Summarizing what changed between two tags or commits
- Creating a CHANGELOG.md entry for a version bump
- Reviewing what shipped since the last deploy

## Workflow

### 1. Determine the Ref Range

Parse `$ARGUMENTS` for from-ref and to-ref. Handle these cases:

**Two args provided** (e.g., `/changelog v1.2.0 v1.3.0`):
```bash
FROM_REF="$1"  # e.g., v1.2.0
TO_REF="$2"    # e.g., v1.3.0
```

**One arg provided** (e.g., `/changelog v1.2.0`):
```bash
FROM_REF="$1"  # e.g., v1.2.0
TO_REF="HEAD"
```

**No args provided** (e.g., `/changelog`):
```bash
# Auto-detect: latest tag to HEAD
FROM_REF=$(git describe --tags --abbrev=0 2>/dev/null)
TO_REF="HEAD"

# If no tags exist, use first commit
if [ -z "$FROM_REF" ]; then
  FROM_REF=$(git rev-list --max-parents=0 HEAD)
fi
```

**Validate the refs exist:**
```bash
git rev-parse --verify "$FROM_REF" >/dev/null 2>&1 || echo "ERROR: $FROM_REF is not a valid ref"
git rev-parse --verify "$TO_REF" >/dev/null 2>&1 || echo "ERROR: $TO_REF is not a valid ref"
```

### 2. Gather Commit History

```bash
# Full commit list with hashes
git log --oneline "$FROM_REF".."$TO_REF"

# With author and date for context
git log --format="%h %s (%an, %ad)" --date=short "$FROM_REF".."$TO_REF"

# Stats summary
git diff --stat "$FROM_REF".."$TO_REF"

# Number of contributors
git log --format="%an" "$FROM_REF".."$TO_REF" | sort -u
```

### 3. Categorize Commits

Parse each commit message and categorize using conventional commit prefixes:

| Category | Prefixes | Priority |
|----------|----------|----------|
| **Breaking Changes** | `BREAKING CHANGE`, `breaking:`, `!:` | 1 (always first) |
| **Features** | `feat:`, `add:`, `feature:` | 2 |
| **Bug Fixes** | `fix:`, `bugfix:`, `bug:` | 3 |
| **Performance** | `perf:`, `performance:` | 4 |
| **Documentation** | `docs:`, `doc:` | 5 |
| **Refactoring** | `refactor:`, `refact:` | 6 |
| **Tests** | `test:`, `tests:` | 7 |
| **Build/CI** | `ci:`, `build:`, `chore:` | 8 |
| **Other** | Anything that doesn't match | 9 |

**For commits without conventional prefixes**, read the commit message body and diff to infer the category:

```bash
# Read full commit message and diff for ambiguous commits
git show --stat <hash>
git show <hash> -- '*.rs' '*.ts' '*.py' '*.go'  # filter to source files
```

### 4. Enrich Significant Changes

For commits tagged as features or breaking changes, read the actual diff to write a better summary than the commit message alone:

```bash
# Read the diff for a significant commit
git show <hash> --stat
git diff <hash>~1..<hash> -- '*.rs' '*.ts' '*.py' '*.go' '*.js' '*.java'
```

Write a one-line human-readable summary that describes **what changed for the user**, not implementation details.

**Good**: "Add bulk export of user data as CSV"
**Bad**: "Add exportUsers function to UserService"

### 5. Detect Version and Date

```bash
# If TO_REF is a tag, extract version from it
VERSION=$(echo "$TO_REF" | sed 's/^v//')

# If TO_REF is HEAD, mark as unreleased
if [ "$TO_REF" = "HEAD" ]; then
  VERSION="Unreleased"
fi

# Get the date of the TO_REF
DATE=$(git log -1 --format="%ad" --date=short "$TO_REF")
```

### 6. Generate the Changelog

Output using the conventional changelog format:

```markdown
## [VERSION] - YYYY-MM-DD

### Breaking Changes
- Description of breaking change ([`abcdef1`](commit-url))
  - **Migration**: How to update existing code/config

### Features
- Description of feature ([`abcdef2`](commit-url))
- Description of feature ([`abcdef3`](commit-url))

### Bug Fixes
- Description of fix ([`abcdef4`](commit-url))

### Performance
- Description of improvement ([`abcdef5`](commit-url))

### Documentation
- Description of docs change ([`abcdef6`](commit-url))

### Internal
- Refactoring, tests, CI changes ([`abcdef7`](commit-url))

---

**Full diff**: [`FROM_REF...TO_REF`](compare-url)
**Contributors**: @author1, @author2, @author3
```

**Rules for the output:**
- Omit empty categories (don't show "### Performance" if there are none)
- Breaking changes always come first with migration notes
- Each entry is one line with the short commit hash linked
- Group related commits if they're part of the same logical change
- Include a "Full diff" link at the bottom using GitHub compare URL format
- List contributors

### 7. Construct URLs (if GitHub remote exists)

```bash
# Detect GitHub remote
REMOTE_URL=$(git remote get-url origin 2>/dev/null | sed 's/\.git$//' | sed 's|git@github.com:|https://github.com/|')

# Commit URL pattern
# ${REMOTE_URL}/commit/${HASH}

# Compare URL
# ${REMOTE_URL}/compare/${FROM_REF}...${TO_REF}
```

If no GitHub remote, use plain hashes without links.

### 8. Output

Print the changelog to stdout. The user can then:
- Copy it into CHANGELOG.md
- Use it as GitHub release notes
- Include it in a PR description

## Handling Edge Cases

**Merge commits**: Skip merge commits unless they represent meaningful squash merges:
```bash
git log --no-merges --oneline "$FROM_REF".."$TO_REF"
```

**Monorepo / scoped changes**: If the user specifies a path, scope the log:
```bash
git log --oneline "$FROM_REF".."$TO_REF" -- path/to/package/
```

**No conventional commits**: If the repo doesn't use conventional commits, categorize by reading diffs. Group by area of the codebase instead of by type.

**Very large ranges (100+ commits)**: Summarize minor changes (docs, chore, refactor) into a single line each. Focus detail on features and breaking changes.

## Example Invocations

**Between two tags:**
```
/changelog v2.0.0 v2.1.0
```

**Since last tag to now:**
```
/changelog
```

**Since a specific commit:**
```
/changelog abc1234 HEAD
```

**Scoped to a path (mentioned in arguments):**
```
/changelog v1.0.0 v2.0.0 -- packages/api
```

## Example Output

```markdown
## [2.1.0] - 2025-03-15

### Features
- Add bulk user export as CSV download ([`a1b2c3d`](https://github.com/org/repo/commit/a1b2c3d))
- Support dark mode in settings panel ([`e4f5g6h`](https://github.com/org/repo/commit/e4f5g6h))

### Bug Fixes
- Fix race condition in webhook delivery causing duplicate events ([`i7j8k9l`](https://github.com/org/repo/commit/i7j8k9l))
- Correct timezone handling for scheduled reports ([`m0n1o2p`](https://github.com/org/repo/commit/m0n1o2p))

### Performance
- Cache user permissions lookup, reducing p99 latency by 40% ([`q3r4s5t`](https://github.com/org/repo/commit/q3r4s5t))

### Internal
- Migrate CI from CircleCI to GitHub Actions ([`u6v7w8x`](https://github.com/org/repo/commit/u6v7w8x))
- Update dependencies ([`y9z0a1b`](https://github.com/org/repo/commit/y9z0a1b))

---

**Full diff**: [`v2.0.0...v2.1.0`](https://github.com/org/repo/compare/v2.0.0...v2.1.0)
**Contributors**: @alice, @bob, @charlie
```
