# /changelog

Generate comprehensive changelog from git commits, pull requests, and release tags following conventional changelog standards.

## Usage

```
/changelog [version or date range]
```

## Changelog Generation Process

### 1. Gather Commit History

```bash
# Get commits since last tag
git log $(git describe --tags --abbrev=0)..HEAD --oneline

# Get commits between dates
git log --since="2024-01-01" --until="2024-12-31" --pretty=format:"%h %s"

# Get commits with full details
git log --pretty=format:"%h|%an|%ad|%s|%b" --date=short

# Include merge commits and PR references
git log --merges --grep="Merge pull request" --pretty=format:"%s"
```

### 2. Analyze Commit Types

```bash
# Find commits by conventional type
git log --grep="^feat:" --pretty=format:"- %s"
git log --grep="^fix:" --pretty=format:"- %s"
git log --grep="^BREAKING CHANGE:" --pretty=format:"- %s"

# Extract PR numbers
git log --grep="#[0-9]" -E --pretty=format:"%s" | grep -oE "#[0-9]+"

# Get author contributions
git shortlog -sn --since="last-tag"
```

### 3. Changelog Format

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- New features added but not yet released

### Changed

- Changes in existing functionality

### Deprecated

- Soon-to-be removed features

### Removed

- Removed features

### Fixed

- Bug fixes

### Security

- Security vulnerabilities fixed

## [1.2.0] - 2024-12-15

### Added

- feat: Add user authentication system (#123)
- feat: Implement dark mode toggle (#125)
- feat: Add CSV export functionality (#128)

### Changed

- refactor: Improve database query performance (#124)
- chore: Update dependencies to latest versions (#126)

### Fixed

- fix: Resolve memory leak in background workers (#122)
- fix: Correct timezone handling in reports (#127)

### Security

- fix: Patch XSS vulnerability in user inputs (#129)

## [1.1.0] - 2024-11-01

...
```

### 4. Commit Classification

```typescript
interface CommitClassification {
  breaking: RegExp[];
  features: RegExp[];
  fixes: RegExp[];
  performance: RegExp[];
  refactor: RegExp[];
  docs: RegExp[];
  style: RegExp[];
  test: RegExp[];
  chore: RegExp[];
}

const patterns: CommitClassification = {
  breaking: [/^BREAKING CHANGE:/, /^feat!:/, /^fix!:/],
  features: [/^feat:/, /^feature:/, /add/i, /implement/i],
  fixes: [/^fix:/, /^bugfix:/, /fix/i, /resolve/i, /patch/i],
  performance: [/^perf:/, /performance/i, /optimize/i],
  refactor: [/^refactor:/, /refactor/i, /restructure/i],
  docs: [/^docs:/, /documentation/i, /README/],
  style: [/^style:/, /formatting/i, /lint/i],
  test: [/^test:/, /^tests:/, /testing/i],
  chore: [/^chore:/, /^build:/, /^ci:/, /dependencies/i],
};
```

### 5. Automated Generation Script

```typescript
// generate-changelog.ts
import { $ } from "https://deno.land/x/dax/mod.ts";

async function generateChangelog(since: string, until = "HEAD") {
  // Get all commits in range
  const commits = await $`git log ${since}..${until} --pretty=format:"%H|%h|%s|%b|%an|%ae"`.text();

  const sections = {
    breaking: [] as string[],
    added: [] as string[],
    changed: [] as string[],
    deprecated: [] as string[],
    removed: [] as string[],
    fixed: [] as string[],
    security: [] as string[],
  };

  // Parse and classify commits
  for (const line of commits.split("\n")) {
    const [hash, short, subject, body, author] = line.split("|");

    if (subject.match(/^BREAKING CHANGE:|^.*!:/)) {
      sections.breaking.push(`- ${subject} (${short})`);
    } else if (subject.match(/^feat:/)) {
      sections.added.push(`- ${subject.replace(/^feat:\s*/, "")} (${short})`);
    } else if (subject.match(/^fix:/)) {
      sections.fixed.push(`- ${subject.replace(/^fix:\s*/, "")} (${short})`);
    }
    // ... more classifications
  }

  // Generate markdown
  let changelog = `## [${await getNextVersion()}] - ${new Date().toISOString().split("T")[0]}\n\n`;

  if (sections.breaking.length > 0) {
    changelog += `### ⚠️ BREAKING CHANGES\n${sections.breaking.join("\n")}\n\n`;
  }

  if (sections.added.length > 0) {
    changelog += `### Added\n${sections.added.join("\n")}\n\n`;
  }

  // ... more sections

  return changelog;
}
```

### 6. PR and Issue Integration

```bash
# Extract PR information
git log --grep="Merge pull request" --pretty=format:"%s" | \
  sed 's/Merge pull request #\([0-9]*\).*/PR #\1/'

# Get issue references
git log --grep="#[0-9]" --pretty=format:"%s" | \
  grep -oE "(closes|fixes|resolves) #[0-9]+"

# Include co-authors
git log --pretty=format:"%s%n%b" | \
  grep "Co-authored-by:" | sort | uniq
```

### 7. Version Determination

```typescript
async function determineVersionBump(commits: string[]): Promise<string> {
  const current = await $`git describe --tags --abbrev=0`.text();
  const [major, minor, patch] = current.replace("v", "").split(".").map(Number);

  let newMajor = major, newMinor = minor, newPatch = patch;

  if (commits.some((c) => c.match(/^BREAKING CHANGE:|^.*!:/))) {
    newMajor++;
    newMinor = 0;
    newPatch = 0;
  } else if (commits.some((c) => c.match(/^feat:/))) {
    newMinor++;
    newPatch = 0;
  } else if (commits.some((c) => c.match(/^fix:/))) {
    newPatch++;
  }

  return `${newMajor}.${newMinor}.${newPatch}`;
}
```

### 8. Release Notes Generation

```markdown
## Release Notes - v1.2.0

### Highlights

🎉 **User Authentication**: Full authentication system with JWT tokens
🌙 **Dark Mode**: Toggle between light and dark themes
📊 **Export Features**: Export your data as CSV files

### Breaking Changes

None in this release

### Migration Guide

No migration required

### Contributors

Thanks to all contributors who made this release possible:

- @user1 (5 commits)
- @user2 (3 commits)
- @user3 (2 commits)

### Full Changelog

https://github.com/org/repo/compare/v1.1.0...v1.2.0
```

## Output Format

```markdown
# Changelog for [Version/Range]

## Summary

- **Version**: X.Y.Z
- **Date**: YYYY-MM-DD
- **Commits**: N
- **Contributors**: M

## Changes

### ⚠️ Breaking Changes

[List if any]

### ✨ Features

- Description (commit-hash) [#PR]

### 🐛 Bug Fixes

- Description (commit-hash) [#PR]

### 🔧 Improvements

- Description (commit-hash)

### 📚 Documentation

- Description (commit-hash)

### 🏠 Internal

- Dependency updates
- Build improvements
- Test additions

## Contributors

[List of contributors with commit counts]

## Links

- [Full Diff](link-to-diff)
- [Release](link-to-release)
```

## Changelog Standards

1. **Group by type** (features, fixes, etc.)
2. **Order by importance** within groups
3. **Include commit hash** for traceability
4. **Reference PRs/issues** when available
5. **Highlight breaking changes** prominently
6. **Credit contributors**
7. **Link to full details**

## Guidelines

- Use conventional commit format
- Keep descriptions user-focused
- Explain impact, not implementation
- Group related changes
- Maintain consistent formatting
- Update with each release
