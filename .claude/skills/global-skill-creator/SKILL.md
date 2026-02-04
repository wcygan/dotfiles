---
name: global-skill-creator
description: Create global Claude Code skills that are distributed via the dotfiles repository. Use when creating a new skill, adding a global skill, or making a skill available across all projects. Keywords: skill, global skill, create skill, new skill, SKILL.md
---

# Global Skill Creator

Creates global Claude Code skills in `config/claude/skills/` for distribution via the dotfiles repository.

## Context

This dotfiles repository manages global Claude Code configuration:

| Type | Source (dotfiles) | Target (symlink) |
|------|-------------------|------------------|
| Commands | `config/claude/commands/*.md` | `~/.claude/commands/` |
| Skills | `config/claude/skills/<name>/SKILL.md` | `~/.claude/skills/<name>/` |
| Agents | `config/claude/agents/*.md` | `~/.claude/agents/` |

**Global skills** live in `config/claude/skills/` and are symlinked to `~/.claude/skills/` by the dotfiles installation process, making them available in all projects.

## Skill Structure

Every skill is a directory with `SKILL.md` as the entrypoint:

```
config/claude/skills/<skill-name>/
├── SKILL.md           # Required - main instructions
├── REFERENCE.md       # Optional - detailed guidance  
├── scripts/           # Optional - helper scripts
│   └── helper.py
└── templates/         # Optional - file templates
    └── template.md
```

## SKILL.md Format

```yaml
---
name: skill-name
description: What it does and when to use it. Include trigger keywords.
---

# Skill Name

Instructions for Claude when this skill is activated.
```

### Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | No | Display name (defaults to directory name). Lowercase, hyphens, max 64 chars. |
| `description` | Yes | **Critical** - determines when Claude auto-loads. Include what + when + keywords. |
| `disable-model-invocation` | No | `true` = only user can invoke via `/skill-name` |
| `user-invocable` | No | `false` = only Claude can invoke (background knowledge) |
| `allowed-tools` | No | Restrict tools: `Read, Grep, Glob, Bash(git *)` |
| `context` | No | `fork` = run in isolated subagent |
| `agent` | No | Subagent type when `context: fork` (e.g., `Explore`, `Plan`) |

## Instructions

### Step 1: Gather Requirements

Ask the user:
1. What should this skill do?
2. When should Claude activate it? (trigger scenarios)
3. Should it be user-invoked only (`/skill-name`) or auto-invoked by Claude?
4. Does it need supporting files (scripts, templates, reference docs)?

### Step 2: Generate Skill Name

Rules:
- Lowercase letters, numbers, hyphens only
- Max 64 characters
- Descriptive of function (what it does, not how)
- Examples: `code-reviewer`, `test-generator`, `api-doc-creator`

### Step 3: Craft the Description

The description is **critical** - it determines when Claude activates the skill.

**Template:**
```
[Primary function]. [Secondary capabilities]. Use when [trigger scenarios]. Keywords: [comma-separated terms].
```

**Good examples:**
- "Generate comprehensive test suites with high coverage. Use when adding tests, improving coverage, or implementing TDD. Keywords: test, testing, coverage, TDD"
- "Review code for security vulnerabilities and best practices. Use when reviewing PRs or auditing code. Keywords: review, security, audit, PR"

**Bad examples:**
- "Helps with code" (too vague, no triggers)
- "Does testing stuff" (no keywords)

### Step 4: Create the Skill

1. Create directory:
   ```bash
   mkdir -p config/claude/skills/<skill-name>
   ```

2. Create `SKILL.md` with:
   - YAML frontmatter (name, description, optional fields)
   - Clear instructions for Claude
   - Expected output format
   - Examples if helpful

3. If needed, add supporting files:
   - `REFERENCE.md` for detailed documentation
   - `scripts/` for executable helpers
   - `templates/` for file templates

### Step 5: Update Symlink Script (if needed)

If `scripts/link-config.sh` doesn't already handle skills, add:

```bash
# Skills (directories)
mkdir -p ~/.claude/skills
for skill_dir in "$DOTFILES/config/claude/skills"/*; do
  if [ -d "$skill_dir" ]; then
    skill_name=$(basename "$skill_dir")
    ln -sf "$skill_dir" ~/.claude/skills/"$skill_name"
  fi
done
```

### Step 6: Test the Skill

1. Run `./scripts/link-config.sh` to create symlinks
2. Start a new Claude Code session
3. Test with a request that matches the description
4. Or invoke directly: `/skill-name`

## Output

After creating the skill:
1. Show the created file structure
2. Explain when the skill will activate
3. Provide example requests that would trigger it
4. Remind to run `./scripts/link-config.sh` to install

## Invocation Control Patterns

**User-only invocation** (for actions with side effects):
```yaml
---
name: deploy
description: Deploy to production
disable-model-invocation: true
---
```

**Claude-only invocation** (background knowledge):
```yaml
---
name: project-conventions
description: Project coding conventions and patterns
user-invocable: false
---
```

**Both user and Claude** (default):
```yaml
---
name: code-reviewer
description: Review code for issues
---
```
