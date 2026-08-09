---
name: gitignore
description: "Audit or update a repository .gitignore from tracked, untracked, generated, and sensitive files. Use for gitignore cleanup, ignore pattern design, and accidental-tracking checks."
---

# Gitignore Manager

## Goal

Analyze repository state and create or update `.gitignore` with clear, safe patterns.

Success means generated files, secrets, caches, and local runtime state are ignored while source files, templates, docs, tests, and intentional config remain trackable.

Stop when the user has either an audit report or a scoped `.gitignore` change with a diff and verification notes.

## Modes

Infer mode from the user prompt:

- Audit/report only: when the prompt says check, audit, review, inspect, or asks a question.
- Edit mode: when the prompt says update, add, fix, create, ignore, or otherwise asks for a file change.
- If the prompt is empty or ambiguous, report findings first and ask before editing.

## Gather Context

Run the narrowest useful commands:

```bash
git ls-files
git status --porcelain
cat .gitignore 2>/dev/null || true
fd -H -t f -e env -e pem -e key -e sqlite -e db 2>/dev/null | head -20
fd -H -t d -g 'node_modules' -g '__pycache__' -g '.direnv' -g 'target' -g 'dist' -g 'build' 2>/dev/null | head -20
```

Use `find` only if `fd` is unavailable.

## Classify Files

Always ignore security and privacy material:

- `.env`, `.env.*`
- `*.pem`, `*.key`, `*.p12`
- `*.sqlite`, `*.db`
- `.credentials`, `credentials.json`
- `*.secret`, `secrets/`
- `.netrc` or `.npmrc` when they contain tokens

Always ignore generated and build artifacts:

- `node_modules/`, dependency vendor directories when repo policy does not track them
- `__pycache__/`, `*.pyc`
- `target/`, `dist/`, `build/`, `out/`
- `.next/`, `.nuxt/`, `.cache/`
- `coverage/`, `.nyc_output/`
- `*.log`, `logs/`

Always ignore editor and OS runtime state:

- `.idea/`, local `.vscode/` state unless the repo intentionally tracks shared settings
- `*.swp`, `*.swo`, `*~`
- `.DS_Store`, `Thumbs.db`

Always ignore Nix and direnv outputs:

- `.direnv/`
- `result`, `result-*`

Review case by case:

- Lock files, based on project policy.
- Generated docs or generated source, based on ownership model.
- Local override configs.

Keep tracked:

- Source code, tests, docs, and templates.
- `flake.nix` and `flake.lock` in Nix projects.
- `.envrc` when it contains no secrets.
- Project config files intentionally managed by the repo.

## Pattern Rules

- Prefer general patterns such as `*.log` over one-off filenames when safe.
- Use trailing slashes for directories.
- Group patterns by category with comments.
- Preserve existing custom patterns unless they are demonstrably wrong.
- Use negation patterns for intentional exceptions.
- Avoid broad patterns that could hide source code.

Default structure:

```gitignore
# ===== OS =====
.DS_Store
Thumbs.db

# ===== Editors =====
.idea/
.vscode/
*.swp
*.swo
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

# ===== Caches =====
.cache/
.direnv/
.pytest_cache/

# ===== Logs =====
*.log
logs/

# ===== Nix =====
result
result-*

# ===== Project Specific =====
```

## Safety Checks

Before editing:

1. Check whether proposed patterns would match source, docs, tests, or tracked config.
2. Identify already-tracked files that should be untracked separately with `git rm --cached`.
3. Preserve project-specific exceptions.
4. Keep the change scoped to `.gitignore` unless the user requests cleanup.

After editing:

```bash
git diff -- .gitignore
git status --porcelain
```

## Report Format

Use this shape:

```markdown
## Current State
- Tracked files: <count>
- Untracked files: <count>
- Existing ignore patterns: <count or summary>

## Recommended Changes
- <pattern or file>: <reason>

## Accidental Tracking Risks
- <tracked file>: <why it may need git rm --cached>

## Verification
- <command>: <result>
```
