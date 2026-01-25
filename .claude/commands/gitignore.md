---
description: Intelligently scan and update .gitignore with appropriate patterns
---

You are helping manage the `.gitignore` file for this repository. Your goal is to analyze what's tracked, untracked, and potentially sensitive, then create or update `.gitignore` with appropriate patterns.

**User context (if provided):** $ARGUMENTS

# Analysis Process

## Step 1: Gather Intelligence

Run these commands to understand the current state:

```bash
# What's currently being tracked by git?
git ls-files

# What's untracked (candidates for gitignore)?
git status --porcelain | grep '^??' | cut -c4-

# Current .gitignore contents (if exists)
cat .gitignore 2>/dev/null || echo "No .gitignore exists"

# Check for common sensitive/generated patterns
fd -H -t f -e env -e pem -e key -e sqlite -e db 2>/dev/null | head -20
fd -H -t d -name node_modules -o -name __pycache__ -o -name .direnv -o -name target -o -name dist -o -name build 2>/dev/null | head -20
```

## Step 2: Classify Files

Categorize discovered files into:

### Always Ignore (Security/Privacy)
- `.env`, `.env.*` - Environment variables with secrets
- `*.pem`, `*.key`, `*.p12` - Private keys and certificates
- `*.sqlite`, `*.db` - Local databases
- `.credentials`, `credentials.json` - API credentials
- `*.secret`, `secrets/` - Explicitly marked secrets
- `.netrc`, `.npmrc` (if contains tokens)

### Always Ignore (Generated/Build Artifacts)
- `node_modules/`, `vendor/` - Package dependencies
- `__pycache__/`, `*.pyc` - Python bytecode
- `target/`, `dist/`, `build/`, `out/` - Build outputs
- `.next/`, `.nuxt/`, `.cache/` - Framework caches
- `*.log`, `logs/` - Log files
- `coverage/`, `.nyc_output/` - Test coverage

### Always Ignore (Editor/IDE)
- `.idea/`, `.vscode/` (except shared settings)
- `*.swp`, `*.swo`, `*~` - Editor temp files
- `.DS_Store`, `Thumbs.db` - OS files

### Always Ignore (Nix/Direnv)
- `.direnv/` - direnv cache
- `result`, `result-*` - Nix build outputs

### Probably Ignore (Review Case-by-Case)
- Lock files (depends on project policy)
- Generated documentation
- Local configuration overrides

### Never Ignore (Should Be Tracked)
- Source code
- Configuration templates
- Documentation
- Tests
- `flake.nix`, `flake.lock` (in Nix projects)
- `.envrc` (direnv config - no secrets)

## Step 3: Generate Patterns

Create patterns that are:
1. **General, not specific** - Use `*.log` not `debug.log`
2. **Directory-aware** - Use `node_modules/` with trailing slash
3. **Well-organized** - Group by category with comments
4. **Negation-capable** - Use `!` for exceptions when needed

## Step 4: Output Format

Present findings in this structure:

```
## Current State Summary
- Tracked files: X
- Untracked files: Y
- Current .gitignore patterns: Z

## Recommended Changes

### Files That Should Be Ignored (currently untracked)
[List with reasoning]

### Files That Might Be Accidentally Tracked
[List any tracked files that look like they shouldn't be]

### Proposed .gitignore Update
[Show the new/updated .gitignore content]
```

# Gitignore Template Structure

When writing `.gitignore`, use this organization:

```gitignore
# ===== OS =====
.DS_Store
Thumbs.db

# ===== Editors =====
.idea/
.vscode/
*.swp
*~

# ===== Secrets & Credentials =====
.env
.env.*
*.pem
*.key
.credentials

# ===== Dependencies =====
node_modules/
vendor/
__pycache__/

# ===== Build Outputs =====
dist/
build/
target/
*.o
*.a

# ===== Caches =====
.cache/
.direnv/
.pytest_cache/

# ===== Logs =====
*.log
logs/

# ===== Project Specific =====
# [Add project-specific patterns here]
```

# Safety Checks

Before finalizing:

1. **Verify no source code will be ignored** - Check patterns don't match `.ts`, `.py`, `.go`, etc.
2. **Check for overly broad patterns** - Avoid `*` without extension
3. **Warn about already-tracked files** - `git rm --cached` may be needed
4. **Preserve existing custom patterns** - Don't remove user's intentional entries

# User Interaction

- If `$ARGUMENTS` specifies "update" or "add", modify the existing `.gitignore`
- If `$ARGUMENTS` specifies "check" or "audit", only report findings without changes
- If `$ARGUMENTS` is empty, ask: "Should I (1) audit and report, or (2) update .gitignore?"
- If potentially sensitive files are already tracked, warn and suggest remediation

# After Completion

1. Show diff of changes (if any)
2. Remind about `git rm --cached <file>` if tracked files need untracking
3. Suggest running `git status` to verify
4. Note any patterns that might need project-specific adjustment

Now analyze this repository and proceed with gitignore management.
