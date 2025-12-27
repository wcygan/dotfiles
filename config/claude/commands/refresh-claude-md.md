---
description: Audit CLAUDE.md for staleness and generate refreshed content with exploration agents
---

Audit the project's CLAUDE.md (or AGENTS.md) for accuracy and freshness, then propose updates.

# Overview

CLAUDE.md files become stale as codebases evolve. This command launches parallel exploration agents to verify documented claims against reality, identify missing documentation, and generate refreshed content.

# Phase 1: Discovery

First, locate the project's agent instructions file:

```
Check for (in order of precedence):
1. CLAUDE.md in project root
2. AGENTS.md in project root  
3. .claude/CLAUDE.md
4. No file exists (offer to create one)
```

Read the existing file to understand what's currently documented.

# Phase 2: Parallel Exploration Audit

Launch 4 exploration agents concurrently using the Task tool with `subagent_type='Explore'`:

## Agent 1: Repository Structure
```
Verify all file/directory claims in CLAUDE.md:
- Do documented paths exist?
- Are directory descriptions accurate?
- What major directories/files are NOT mentioned?
Output: List of ✅ accurate, 🟡 stale, ❌ missing items
```

## Agent 2: Tech Stack & Dependencies
```
Analyze actual tech stack vs documented:
- Check package files (package.json, Cargo.toml, go.mod, flake.nix, pyproject.toml, etc.)
- Identify languages, frameworks, build tools
- Compare against what CLAUDE.md claims
Output: Accurate stack summary with discrepancies noted
```

## Agent 3: Commands & Workflows
```
Verify documented commands work:
- Check Makefile, justfile, package.json scripts, etc.
- Identify key commands (build, test, lint, format, deploy)
- Compare against documented commands
Output: Validated command reference
```

## Agent 4: Patterns & Conventions
```
Identify actual patterns in the codebase:
- Code organization patterns
- Naming conventions
- Testing patterns (where tests live, how they're structured)
- CI/CD setup (.github/workflows, etc.)
Output: Observed patterns that should be documented
```

# Phase 3: Staleness Report

Compile agent findings into a staleness report:

```markdown
## Staleness Report

### ✅ Accurate (no changes needed)
- [List verified claims]

### 🟡 Stale (needs update)
- [Claim] → [Reality]

### ❌ Missing (should document)
- [Undocumented feature/pattern]

### 🗑️ Obsolete (should remove)
- [Documented things that no longer exist]
```

# Phase 4: Generate Refreshed CLAUDE.md

Based on the audit, generate a refreshed version following these principles:

## Structure (adapt sections to project)

```markdown
# CLAUDE.md (or AGENTS.md)

## Mission
[1-2 sentences: What this project does and its key goals]

## Tech Stack
[Concise list: languages, frameworks, key dependencies]

## Repo Map
[Succinct directory overview - what lives where]

## Key Commands
[Copy-pasteable commands for common tasks]
build:   <command>
test:    <command>
lint:    <command>
format:  <command>

## Patterns
[Code conventions, architecture patterns, naming rules]

## Testing
[How to run tests, where tests live, coverage expectations]

## CI/CD
[What happens on push/PR, required checks]

## Authority & Guardrails
[What agents may/must not change]
```

## Content Guidelines

1. **Be concise**: Prefer tables and bullet points over prose
2. **Be specific**: "Run `make test`" not "run the tests"
3. **Be current**: Only document what actually exists
4. **Be actionable**: Include copy-pasteable commands
5. **Omit the obvious**: Don't document standard language features
6. **Link, don't duplicate**: Reference files instead of copying content

## Anti-Patterns to Avoid

- ❌ Verbose explanations of common tools
- ❌ Example code that doesn't match reality
- ❌ Documenting aspirational features
- ❌ Copying README content
- ❌ Stale file listings

# Phase 5: Output

Present to the user:

1. **Staleness Report**: Summary of what's accurate/stale/missing
2. **Proposed CLAUDE.md**: The refreshed content
3. **Diff Summary**: Key changes from current version

Ask the user if they want to:
- Apply the changes (write the file)
- Modify specific sections first
- Keep certain existing content

# Special Cases

**No existing CLAUDE.md**: Use the `create-agents-md` command pattern to generate from scratch.

**Monorepo**: Note that subdirectories may need their own CLAUDE.md files. Offer to audit those separately.

**Minimal changes needed**: If the file is mostly accurate, provide a targeted update rather than full rewrite.

# Best Practices for Ongoing Freshness

Remind the user:
- Use `#` command during sessions to add notes Claude will incorporate
- Run this audit after major refactors or dependency updates
- Keep CLAUDE.md in version control
- Treat it as living documentation, not a one-time artifact
