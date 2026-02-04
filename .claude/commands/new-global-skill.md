---
description: Create a new global skill in config/claude/skills/ for distribution via dotfiles
---

Create a new global skill that will be available across all projects via the dotfiles symlink system.

## Context

Global skills are stored in `config/claude/skills/<skill-name>/` and symlinked to `~/.claude/skills/` during dotfiles installation. This makes them available in every Claude Code session.

**Location:** `config/claude/skills/<skill-name>/SKILL.md`

## Process

### Step 1: Gather Information

Ask the user:
1. **Skill name** - What should this skill be called? (lowercase, hyphens, max 64 chars)
2. **Purpose** - What does this skill do?
3. **Triggers** - When should Claude automatically activate it?
4. **Invocation** - User-invoked only (`/skill-name`), Claude-invoked only, or both?
5. **Complexity** - Simple (just SKILL.md) or advanced (with scripts/templates/reference)?

### Step 2: Create Directory Structure

```bash
mkdir -p config/claude/skills/<skill-name>
```

For advanced skills:
```bash
mkdir -p config/claude/skills/<skill-name>/{scripts,templates}
```

### Step 3: Generate SKILL.md

Use this template:

```yaml
---
name: <skill-name>
description: <What it does>. <When to use it>. Keywords: <comma-separated triggers>
---

# <Skill Name>

<Brief overview>

## Instructions

<Step-by-step guidance for Claude when this skill is activated>

## Output

<Expected output format>
```

**Frontmatter options:**
- `disable-model-invocation: true` - Only user can invoke via `/skill-name`
- `user-invocable: false` - Only Claude can invoke (background knowledge)
- `allowed-tools: Read, Grep, Glob` - Restrict available tools
- `context: fork` - Run in isolated subagent
- `agent: Explore` - Subagent type (when using `context: fork`)

### Step 4: Add Supporting Files (if advanced)

- `REFERENCE.md` - Detailed documentation Claude can read when needed
- `scripts/*.sh` or `scripts/*.py` - Executable helpers
- `templates/*` - File templates Claude can use

### Step 5: Remind About Installation

After creating the skill, remind the user:

```
To install the new global skill:
1. Run: ./scripts/link-config.sh
2. Or manually: ln -sf ~/Development/dotfiles/config/claude/skills/<skill-name> ~/.claude/skills/
3. Start a new Claude Code session to pick up the skill
```

## Examples

**Simple skill (code reviewer):**
```
config/claude/skills/code-reviewer/
└── SKILL.md
```

**Advanced skill (with helpers):**
```
config/claude/skills/api-generator/
├── SKILL.md
├── REFERENCE.md
├── scripts/
│   └── validate-openapi.sh
└── templates/
    └── endpoint.ts
```

## Good Description Examples

✅ "Review code for security vulnerabilities, performance issues, and best practices. Use when reviewing PRs, auditing code, or checking for bugs. Keywords: review, security, audit, PR, code review"

✅ "Generate Nix flake configurations for development environments. Use when setting up a new project with Nix or adding devShell. Keywords: nix, flake, devShell, development environment"

❌ "Helps with code" (too vague)
❌ "Does stuff with files" (no triggers)

---

**Now ask the user what global skill they want to create and guide them through the process.**
