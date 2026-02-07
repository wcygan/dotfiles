---
name: new-agent
description: Create custom Claude Code subagents. Interactive wizard that gathers requirements, generates the agent .md file with proper frontmatter and system prompt. Use when creating a new agent, adding a subagent, or making a custom agent available globally. Keywords: agent, subagent, create agent, new agent, custom agent
disable-model-invocation: true
argument-hint: "[agent-description or leave blank for interactive]"
---

# New Agent Creator

Creates custom Claude Code subagents as `.md` files with YAML frontmatter and a system prompt.

## Agent Storage Locations

| Location | Scope | When to use |
|----------|-------|-------------|
| `.claude/agents/` | Current project | Team-shared, checked into version control |
| `~/.claude/agents/` | All projects | Personal agents across your machine |

Before creating an agent, list existing agents in the target directory to avoid name conflicts.

## Agent File Format

```markdown
---
name: agent-name
description: When Claude should use this agent. Include 2-3 <example> blocks.
color: green
model: inherit
memory: user
---

System prompt content here — this becomes the agent's entire personality and instructions.
```

### Frontmatter Fields

| Field | Required | Default | Description |
|-------|----------|---------|-------------|
| `name` | **Yes** | — | Lowercase, hyphens only. Must be unique across all agents. |
| `description` | **Yes** | — | Critical for delegation. Must include `<example>` blocks. |
| `tools` | No | All tools | Comma-separated allowlist: `Read, Grep, Glob, Bash, Write, Edit` etc. |
| `disallowedTools` | No | — | Tools to explicitly deny (removed from inherited set). |
| `model` | No | `inherit` | One of: `sonnet`, `opus`, `haiku`, `inherit`. |
| `color` | No | — | UI color: `green`, `cyan`, `bright_red`, `yellow`, `blue`, `magenta`, etc. |
| `permissionMode` | No | `default` | `default`, `acceptEdits`, `dontAsk`, `bypassPermissions`, `plan`. |
| `maxTurns` | No | — | Maximum agentic turns before stopping. |
| `memory` | No | — | Persistent memory scope: `user`, `project`, or `local`. |
| `skills` | No | — | Skills to preload into the agent's context. |
| `mcpServers` | No | — | MCP servers available to this agent. |
| `hooks` | No | — | Lifecycle hooks scoped to this agent. |

## Instructions

### Step 1: Gather Requirements

If `$ARGUMENTS` is provided, use it as the agent concept. Otherwise, ask the user:

1. **What domain does this agent specialize in?** (e.g., "database optimization", "accessibility auditing", "Rust development")
2. **What should it do when invoked?** (e.g., "review queries for performance", "audit HTML for WCAG compliance")
3. **Should it be read-only or able to modify files?**
4. **What model should it use?** (`inherit` for most, `haiku` for fast/cheap tasks, `sonnet` for balanced, `opus` for complex reasoning)
5. **Should it have persistent memory across sessions?** (recommended for agents that learn patterns over time)
6. **Where should it live?** (`.claude/agents/` for project-level, `~/.claude/agents/` for user-level)

### Step 2: Choose the Name

Rules:
- Lowercase letters, numbers, hyphens only
- Descriptive of the **role**, not the task (e.g., `accessibility-auditor` not `check-accessibility`)
- Check for conflicts with existing agents in the target directory
- Keep it short but unambiguous

### Step 3: Craft the Description

The description is **critical** — Claude uses it to decide when to delegate tasks to this agent.

**Required structure:**

```
Use this agent when [trigger scenarios]. This agent excels at [capabilities]. Examples:\n\n<example>\nContext: [situation]\nuser: "[what the user says]"\nassistant: "[how Claude delegates]"\n<commentary>\n[Why this agent is the right choice]\n</commentary>\n</example>
```

**Include 2-3 `<example>` blocks** showing realistic delegation scenarios. These are essential — Claude relies on them for pattern matching.

**Best practices:**
- Start with "Use this agent when..."
- List specific trigger scenarios, not vague domains
- Include keywords users might say naturally
- Add "Use proactively" if the agent should auto-trigger (e.g., after code changes)

### Step 4: Write the System Prompt

The markdown body after the frontmatter becomes the agent's system prompt. It receives only this prompt (plus basic environment details), not the full Claude Code system prompt.

**Structure:**
1. **Opening persona** (1-2 sentences): Who the agent is and what it values
2. **Core Mindset / Principles** (bulleted): The mental model that drives decisions
3. **Detailed Methodology**: Domain-specific checklists, frameworks, or processes
4. **Output Format**: How findings/results should be structured
5. **Communication Style**: Tone and presentation guidelines
6. **Memory Guidelines** (if memory enabled): What to record across sessions

**Quality bar:**
- Be specific and actionable, not vague
- Include domain-specific frameworks relevant to the specialty
- Define output structure so results are consistent
- Include anti-patterns (what NOT to do)
- Keep it under 150 lines — agents with bloated prompts lose focus

### Step 5: Select Tool Access

Common patterns:

| Agent Type | Tools | Rationale |
|-----------|-------|-----------|
| Read-only reviewer | `Read, Grep, Glob, Bash` | Can explore and run read-only commands |
| Code modifier | All tools (default) | Full access to make changes |
| Research-only | `Read, Grep, Glob, WebSearch, WebFetch` | Can search code and web, no execution |
| Restricted executor | `Bash` + hooks | Bash with PreToolUse hook to validate commands |

If the agent should have **all tools** (the common case), omit the `tools` field entirely.

### Step 6: Create the Agent File

Write the agent `.md` file to the target directory chosen in Step 1.

### Step 7: Verify and Report

After creating the file:

1. **Show the file** — display the full content
2. **Confirm no name conflicts** — check against existing agents in the target directory
3. **Show example invocations** — 2-3 ways to trigger the agent
4. **Remind about loading** — new agents are loaded at session start; restart the session or use `/agents` to load immediately
5. **Suggest testing** — try a request that matches the description to verify delegation

## Example Agent (Reference)

A well-structured agent:

```markdown
---
name: accessibility-auditor
description: Use this agent when you need to evaluate UI code for accessibility compliance, WCAG conformance, or inclusive design. Excels at identifying missing ARIA attributes, keyboard navigation issues, color contrast problems, and screen reader compatibility.\n\n<example>\nContext: The user just built a new form component.\nuser: "Can you check if this form is accessible?"\nassistant: "I'll use the accessibility-auditor agent to evaluate your form for WCAG compliance."\n<commentary>\nForm accessibility involves labels, error announcements, focus management — specialized knowledge the accessibility-auditor provides.\n</commentary>\n</example>
color: yellow
memory: user
---

You are an accessibility specialist who ensures digital interfaces work for everyone.

## Core Mindset

- **Inclusive by default**: Every user deserves equal access to functionality
- **Programmatic first**: If assistive tech can't parse it, it's broken
- **Progressive enhancement**: Start accessible, layer on interactivity

## Methodology

When auditing code:
1. Check semantic HTML structure (headings, landmarks, roles)
2. Verify all interactive elements are keyboard-accessible
3. Confirm ARIA attributes are correct and complete
4. Evaluate color contrast ratios (WCAG AA minimum)
5. Test focus management for dynamic content

## Output Format

Organize findings by impact:

### Critical (blocks access entirely)
### Major (degrades experience significantly)
### Minor (improvement opportunities)

For each finding: **what** is wrong, **where** (file:line), **why** it matters, **fix** with code example.

## Communication Style

- Be specific — cite WCAG success criteria by number (e.g., 1.4.3 Contrast)
- Provide before/after code examples for every finding
- Acknowledge what's already done well
```

## Anti-Patterns

- **Don't create agents for one-off tasks** — use skills or the main conversation instead
- **Don't create agents with vague descriptions** — "helps with code" will never trigger
- **Don't duplicate existing agents** — check the target directory first
- **Don't give write access to pure analysis agents** — principle of least privilege
- **Don't skip the `<example>` blocks** — they're the primary delegation signal
- **Don't make the system prompt too long** — over 150 lines dilutes focus
