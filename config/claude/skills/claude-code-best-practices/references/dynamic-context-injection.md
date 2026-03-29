---
title: Dynamic Context Injection
canonical_url: https://code.claude.com/docs/en/skills#inject-dynamic-context
fetch_before_acting: true
---

# Dynamic Context Injection

> Before making changes or giving definitive guidance, WebFetch https://code.claude.com/docs/en/skills for the latest.

## How it works

The `` !`<command>` `` syntax (bang-backtick) runs shell commands **before** the skill content is sent to Claude. The command output replaces the placeholder inline, so Claude receives actual data — not the command itself.

This is **preprocessing**, not something Claude executes. Claude only sees the final rendered result.

## Execution order

1. Skill is invoked (by user or Claude)
2. Each `` !`<command>` `` in the skill content executes immediately
3. Command output replaces the placeholder in-place
4. String substitutions (`$ARGUMENTS`, `${CLAUDE_SESSION_ID}`, `${CLAUDE_SKILL_DIR}`) are resolved
5. Claude receives the fully-rendered prompt

## Syntax

```markdown
!`<shell command>`
```

The command runs in the user's shell. Output (stdout) replaces the entire `` !`...` `` block.

## Examples

### Inject git state

```yaml
---
name: my-skill
---

Current branch: !`git branch --show-current`
Recent commits: !`git log --oneline -5`
```

### Inject project metadata

```yaml
---
name: my-skill
---

Project files: !`ls -1 package.json Cargo.toml go.mod pyproject.toml 2>/dev/null`
Node version: !`node --version 2>/dev/null || echo 'not installed'`
```

### Full example: PR summary skill

```yaml
---
name: pr-summary
description: Summarize changes in a pull request
context: fork
agent: Explore
allowed-tools: Bash(gh *)
---

## Pull request context
- PR diff: !`gh pr diff`
- PR comments: !`gh pr view --comments`
- Changed files: !`gh pr diff --name-only`

## Your task
Summarize this pull request...
```

### Reference bundled scripts with `${CLAUDE_SKILL_DIR}`

```yaml
---
name: analyze
---

Analysis output: !`python ${CLAUDE_SKILL_DIR}/scripts/analyze.py`
```

`${CLAUDE_SKILL_DIR}` resolves to the directory containing the skill's `SKILL.md`, so bundled scripts work regardless of the user's current working directory.

## Available string substitutions

These are resolved alongside bang-backtick commands during preprocessing:

| Variable | Description |
|----------|-------------|
| `$ARGUMENTS` | All arguments passed when invoking the skill |
| `$ARGUMENTS[N]` or `$N` | Specific argument by 0-based index |
| `${CLAUDE_SESSION_ID}` | Current session ID |
| `${CLAUDE_SKILL_DIR}` | Directory containing this skill's `SKILL.md` |

If `$ARGUMENTS` is not present in the content, arguments are appended as `ARGUMENTS: <value>`.

## Shell configuration

The `shell` frontmatter field controls which shell runs the commands:

```yaml
---
shell: bash        # default
# shell: powershell  # Windows only, requires CLAUDE_CODE_USE_POWERSHELL_TOOL=1
---
```

## Key considerations

- Commands run with the **user's permissions** in the user's shell environment
- Commands run **before** Claude sees anything — Claude cannot influence what runs
- If a command fails or produces no output, the placeholder is replaced with empty string
- Use `2>/dev/null` or `|| echo 'fallback'` to handle missing tools gracefully
- Keep commands fast — they block skill loading
- For forked skills (`context: fork`), this is the primary way to inject project state since the subagent has no conversation history
