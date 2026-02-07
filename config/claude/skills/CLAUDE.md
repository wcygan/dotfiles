# Skills Reference

Guide to creating, configuring, and organizing Claude Code skills.
Based on the [official spec](https://code.claude.com/docs/en/skills) and real examples from this repo.

## What Skills Are

A skill is a `SKILL.md` file with YAML frontmatter and markdown instructions.
Claude loads skill descriptions into context so it knows what's available, and loads full content when invoked.
Users invoke skills with `/skill-name`, and Claude can invoke them automatically when relevant.

Skills replaced the older `.claude/commands/` system. Existing command files keep working,
but skills add frontmatter controls, supporting file directories, and auto-invocation.

## File Structure

Each skill is a directory with `SKILL.md` as the entrypoint:

```
skills/
  my-skill/
    SKILL.md           # Required — frontmatter + instructions
    template.md        # Optional — templates Claude fills in
    examples/          # Optional — example outputs
    scripts/           # Optional — scripts Claude can execute
    REFERENCE.md       # Optional — detailed docs loaded on demand
```

Keep `SKILL.md` under 500 lines. Move detailed reference material to separate files
and link to them from SKILL.md so Claude knows when to load them.

**Real example** — `gh-cli/` uses a supporting file:

```
gh-cli/
  SKILL.md             # Quick reference and common workflows
  REFERENCE.md         # Full gh CLI documentation (loaded when needed)
```

## Where Skills Live

| Location | Path | Scope |
|----------|------|-------|
| Enterprise | Managed settings | All org users |
| Personal | `~/.claude/skills/<name>/SKILL.md` | All your projects |
| Project | `.claude/skills/<name>/SKILL.md` | This project only |
| Plugin | `<plugin>/skills/<name>/SKILL.md` | Where plugin is enabled |

Priority: enterprise > personal > project. Plugin skills use `plugin:name` namespace.

Skills in directories added via `--add-dir` are also discovered automatically.

**This repo** installs personal skills — they live under `config/claude/skills/` and get
symlinked to `~/.claude/skills/` via the dotfiles link script.

## Frontmatter Reference

```yaml
---
name: my-skill              # Display name, becomes /my-skill. Defaults to directory name.
description: What it does   # Critical — Claude uses this to decide when to load the skill.
argument-hint: [issue-num]  # Shown during autocomplete. Tells user what to pass.
disable-model-invocation: true  # Only user can invoke (prevents Claude auto-triggering).
user-invocable: false       # Only Claude can invoke (hidden from / menu).
allowed-tools: Read, Grep   # Restrict which tools Claude can use.
model: sonnet               # Override model for this skill.
context: fork               # Run in a forked subagent (isolated context).
agent: Explore              # Which agent type to use with context: fork.
hooks: ...                  # Lifecycle hooks scoped to this skill.
---
```

All fields are optional. Only `description` is recommended.

### Invocation Control Matrix

| Setting | User can invoke | Claude can invoke | When loaded |
|---------|----------------|-------------------|-------------|
| (default) | Yes | Yes | Description always, full on invoke |
| `disable-model-invocation: true` | Yes | No | Not in context until user invokes |
| `user-invocable: false` | No | Yes | Description always, full on invoke |

## String Substitutions

| Variable | Description |
|----------|-------------|
| `$ARGUMENTS` | All arguments passed after the skill name |
| `$ARGUMENTS[N]` or `$N` | Specific argument by 0-based index |
| `${CLAUDE_SESSION_ID}` | Current session ID |
| `` !`command` `` | Shell command output injected before Claude sees the prompt |

## Three Skill Patterns

### 1. Reference Skills (inline, Claude-invoked)

Background knowledge Claude applies to your current work. No `context: fork`,
no `disable-model-invocation`. Claude loads it when relevant.

**Real example** — `gh-cli` teaches Claude how to use the GitHub CLI:

```yaml
---
name: gh-cli
description: Work with GitHub from the command line using the GitHub CLI (gh)...
---

# GitHub CLI (gh)
Use the `gh` CLI to interact with GitHub directly from the terminal...
```

Claude picks this up automatically whenever you ask about GitHub operations.

**Real example** — `create-pr` provides PR workflow knowledge:

```yaml
---
name: create-pr
description: Create a pull request using git and GitHub CLI...
---
```

No `disable-model-invocation`, so Claude can use this knowledge when you say
"open a PR" without explicitly typing `/create-pr`.

### 2. Task Skills (user-invoked, inline)

Step-by-step workflows you trigger manually with `/name`.
Use `disable-model-invocation: true` to prevent Claude from auto-triggering.

**Real example** — `commit` is a manual workflow:

```yaml
---
name: commit
description: Analyze staged changes and create a well-crafted conventional commit...
disable-model-invocation: true
argument-hint: [optional message override]
---

# Smart Commit
## Workflow
### 1. Assess Working State
### 2. Analyze the Diff
### 3. Generate Commit Message
### 4. Confirm and Commit
### 5. Handle Pre-Commit Hook Failures
### 6. Post-Commit Verification
```

You wouldn't want Claude auto-committing — hence `disable-model-invocation: true`.

**Real example** — `fix-issue` runs end-to-end from issue to PR:

```yaml
---
name: fix-issue
description: Take a GitHub issue number, investigate it, implement a fix...
disable-model-invocation: true
argument-hint: [issue-number]
allowed-tools: Read, Grep, Glob, Bash, Write, Edit
---
```

Note: `allowed-tools` grants those tools without per-use approval during the skill.

### 3. Forked Skills (subagent context)

Run in an isolated subagent with `context: fork`. The skill content becomes
the subagent's task prompt. It does **not** see your conversation history.

**Real example** — `onboard` runs in a read-only Explore agent:

```yaml
---
name: onboard
description: Explore an unfamiliar codebase and generate an ARCHITECTURE.md...
context: fork
agent: Explore
disable-model-invocation: true
allowed-tools: Read, Grep, Glob, Bash(find *), Bash(wc *), Bash(ls *), Write
---
```

The `agent: Explore` field means it runs in a read-only exploration context.
Results are summarized and returned to your main conversation.

**Real example** — `diff-explain` also forks with Explore:

```yaml
---
name: diff-explain
description: Explain a diff in plain English...
context: fork
agent: Explore
allowed-tools: Read, Grep, Glob, Bash(git *), Bash(gh *)
---
```

**Real example** — `review-changes` forks without specifying an agent (uses general-purpose):

```yaml
---
name: review-changes
description: Orchestrate multiple review agents for a comprehensive pre-PR code review...
context: fork
---
```

This skill spawns its own sub-agents internally, so it needs general-purpose (the default)
rather than the read-only Explore agent.

### When to fork vs inline

| Use `context: fork` when | Keep inline when |
|--------------------------|------------------|
| Skill spawns sub-agents | Skill is reference knowledge |
| Heavy exploration that would bloat main context | Simple workflow with user interaction |
| Read-only analysis tasks | Skill needs conversation history |
| Expensive work you want isolated | Skill needs to interact with user mid-run |

## Dynamic Context Injection

The `` !`command` `` syntax runs shell commands **before** Claude sees the content.
Output replaces the placeholder.

**Real example** — a PR summary skill could inject live data:

```yaml
---
name: pr-summary
context: fork
agent: Explore
allowed-tools: Bash(gh *)
---

## Pull request context
- PR diff: !`gh pr diff`
- PR comments: !`gh pr view --comments`

## Your task
Summarize this pull request...
```

Claude only sees the rendered output, not the commands.

## Writing Good Descriptions

The description is the most important field. Claude uses it for auto-invocation
decisions and to show users what's available.

**Good patterns from this repo:**

```yaml
# Specific trigger scenarios + keywords for matching
description: >
  Take a GitHub issue number, investigate it, implement a fix, write tests,
  and open a PR. End-to-end workflow from assigned issue to merged PR.
  Keywords: fix issue, github issue, resolve issue, close issue

# Clear scope + "when to use"
description: >
  Quick prototype in an isolated git worktree. Creates a worktree, spawns
  agents to explore a technical approach, and opens a draft PR with findings.
  Use for time-boxed technical exploration, feasibility testing, or library evaluation.

# Short but sufficient for reference skills
description: >
  Work with GitHub from the command line using the GitHub CLI (gh).
  Use when managing repositories, pull requests, issues, releases, or any GitHub operations.
```

**Anti-patterns:**
- `description: Helps with code` — too vague, never triggers
- No description at all — Claude can't decide when to use it
- Novel-length descriptions — wastes context budget

## Arguments Pattern

Skills receive arguments via `$ARGUMENTS`. Design for both with-args and no-args:

```yaml
---
name: changelog
argument-hint: [from-ref] [to-ref]
---

# When both args provided: /changelog v1.0 v2.0
# When one arg: /changelog v1.0 (to HEAD)
# When no args: auto-detect latest tag to HEAD
```

For positional args, use `$ARGUMENTS[N]` or `$N`:

```yaml
Migrate the $0 component from $1 to $2.
```

If `$ARGUMENTS` isn't in the content, args are appended as `ARGUMENTS: <value>`.

## Tool Restrictions

Use `allowed-tools` to limit what Claude can do during a skill:

```yaml
# Read-only exploration
allowed-tools: Read, Grep, Glob, Bash(git *), Bash(gh *)

# Full code modification
allowed-tools: Read, Grep, Glob, Bash, Write, Edit

# Scoped bash with glob patterns
allowed-tools: Read, Grep, Glob, Bash(find *), Bash(wc *), Bash(ls *), Write
```

Omit `allowed-tools` entirely to grant all tools (the default).

## Permission Control

Three ways to control skill access:

**Deny all skills** in `/permissions`:
```
Skill
```

**Allow/deny specific skills:**
```
Skill(commit)         # Allow exact match
Skill(review-pr *)    # Allow prefix match
Skill(deploy *)       # Deny prefix match (in deny rules)
```

**Per-skill frontmatter:**
- `disable-model-invocation: true` — removes from Claude's context entirely
- `user-invocable: false` — hides from `/` menu but Claude can still use it

## Skills in This Repo

### User-Invoked Workflows (`disable-model-invocation: true`)

| Skill | Purpose | Context |
|-------|---------|---------|
| `/commit` | Smart conventional commit | inline |
| `/fix-issue [N]` | Issue-to-PR pipeline | inline |
| `/spike [desc]` | Worktree-based prototyping | fork |
| `/onboard` | Codebase exploration → ARCHITECTURE.md | fork (Explore) |
| `/review-changes` | Multi-agent pre-PR review | fork |
| `/security-review [path]` | OWASP-informed security audit | fork |
| `/diff-explain [ref]` | Plain English diff explanation | fork (Explore) |
| `/changelog [from] [to]` | Generate release notes from git history | fork (Explore) |
| `/summarize-pr [N]` | Structured PR summary | fork (Explore) |
| `/debug-team [symptom]` | Multi-hypothesis debugging with agent team | fork |
| `/new-agent [desc]` | Interactive agent creation wizard | inline |

### Reference Knowledge (Claude auto-invokes)

| Skill | Purpose |
|-------|---------|
| `gh-cli` | GitHub CLI usage patterns |
| `create-pr` | Pull request creation workflow |
| `agent-team` | Agent team composition and coordination |

## Creating a New Skill

### Minimal skill (reference)

```yaml
---
name: my-conventions
description: Coding conventions for this project
---

When writing code in this project:
- Use kebab-case for file names
- Prefer composition over inheritance
- All public functions need JSDoc
```

### Standard skill (user-invoked task)

```yaml
---
name: my-workflow
description: Does X when you need Y. Keywords: x, y, z
disable-model-invocation: true
argument-hint: [target]
---

# My Workflow

## Workflow

### 1. Gather Context
[What to read/check first]

### 2. Do the Work
[Step-by-step instructions]

### 3. Verify
[How to confirm success]

### 4. Report
[What to tell the user]
```

### Forked skill (isolated execution)

```yaml
---
name: my-analysis
description: Deep analysis of X
context: fork
agent: Explore
disable-model-invocation: true
allowed-tools: Read, Grep, Glob
---

Analyze $ARGUMENTS thoroughly:
1. Find relevant files
2. Read and understand the code
3. Report findings with file:line references
```

## Troubleshooting

**Skill not triggering?**
- Check description has matching keywords
- Verify with `What skills are available?`
- Invoke directly with `/name` to test

**Skill triggers too often?**
- Make description more specific
- Add `disable-model-invocation: true`

**Skills excluded from context?**
- Too many skills exceed the 2% context budget (16k chars fallback)
- Check `/context` for warnings
- Override with `SLASH_COMMAND_TOOL_CHAR_BUDGET` env var

**Forked skill returns nothing useful?**
- `context: fork` needs a concrete task, not just guidelines
- The subagent has no conversation history — include all necessary context in the skill

## Related Docs

- [Official skills documentation](https://code.claude.com/docs/en/skills)
- [Agent Skills open standard](https://agentskills.io)
- [Sub-agents](https://code.claude.com/docs/en/sub-agents)
- [Hooks in skills](https://code.claude.com/docs/en/hooks#hooks-in-skills-and-agents)
- [Permissions](https://code.claude.com/docs/en/permissions)
