# Sub-Agents Guide

Custom sub-agents for Claude Code. Each `.md` file in this directory defines a specialized agent that Claude auto-delegates to based on its `description` field.

Reference: https://code.claude.com/docs/en/sub-agents

## How Sub-Agents Work

Sub-agents are **isolated Claude instances** with their own context window, system prompt, and tool access. When Claude encounters a task matching a sub-agent's description, it delegates automatically. The sub-agent works independently and returns a summary.

Key differences from skills:
- **Skills** load instructions into the *current* conversation context (stateless, on-demand)
- **Sub-agents** run in a *separate* context window with their own system prompt (isolated, potentially stateful)
- Sub-agents can have **persistent memory** that accumulates across sessions
- Sub-agents can have **skills preloaded** into their context at startup

## File Format

```yaml
---
name: my-agent              # Required. Lowercase + hyphens, max 64 chars
description: When to use me  # Required. Claude uses this for auto-delegation
tools: Read, Grep, Glob      # Optional. Inherits all tools if omitted
disallowedTools: Write, Edit  # Optional. Denylist (removed from inherited set)
model: sonnet                 # Optional. sonnet | opus | haiku | inherit (default)
memory: user                  # Optional. user | project | local
skills:                       # Optional. Preloaded into context at startup
  - skill-name
permissionMode: default       # Optional. default | acceptEdits | plan | bypassPermissions
maxTurns: 20                  # Optional. Limits agentic turns
hooks:                        # Optional. Lifecycle hooks scoped to this agent
  PreToolUse: [...]
---

Markdown body becomes the system prompt.
Sub-agents receive ONLY this prompt + environment info, NOT the full Claude Code system prompt.
```

## Frontmatter Fields Reference

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Unique ID (lowercase, hyphens). Becomes the delegation target |
| `description` | Yes | When Claude should use this agent. Include "use proactively" for auto-delegation |
| `tools` | No | Allowlist of tools. Omit to inherit all from parent session |
| `disallowedTools` | No | Denylist. Removed from inherited/specified tools |
| `model` | No | `sonnet`, `opus`, `haiku`, or `inherit` (default) |
| `memory` | No | `user` (cross-project), `project` (repo-specific, VCS-safe), `local` (repo-specific, gitignored) |
| `skills` | No | Skills injected into context at startup (full content, not just available) |
| `permissionMode` | No | `default`, `acceptEdits`, `dontAsk`, `plan`, `bypassPermissions` |
| `maxTurns` | No | Cap on agentic turns before stopping |
| `hooks` | No | `PreToolUse`, `PostToolUse`, `Stop` hooks scoped to this agent |
| `color` | No | Background color in UI for identifying which agent is running |

## Design Principles

### 1. Choose the Right Model

Cost and latency matter. Match model to task complexity:

```yaml
# Read-only exploration — fast and cheap
model: haiku

# Analysis requiring judgment — balanced
model: sonnet

# Complex multi-step reasoning — use the session's model
model: inherit
```

**Real example:** `codebase-oracle` uses `haiku` (read-only exploration), `quality-reviewer` uses `sonnet` (needs judgment), `ship-it` uses `inherit` (makes commit/PR decisions).

### 2. Restrict Tools to the Minimum

Don't give write access to agents that only need to read:

```yaml
# Read-only agent (exploration, review, analysis)
tools: Read, Grep, Glob, Bash

# Read-write agent (implementation, fixing, shipping)
tools: Read, Grep, Glob, Bash, Write, Edit
```

**Real example:** `quality-reviewer` has `Read, Grep, Glob, Bash` — it reports findings but never edits code. `ship-it` has full tools because it commits and creates PRs.

### 3. Use Memory Deliberately

Memory scope determines where knowledge persists:

| Scope | Location | Use When |
|-------|----------|----------|
| `user` | `~/.claude/agent-memory/<name>/` | Knowledge applies across all projects (commit style, review preferences) |
| `project` | `.claude/agent-memory/<name>/` | Knowledge is repo-specific and shareable (architecture, patterns) |
| `local` | `.claude/agent-memory-local/<name>/` | Repo-specific but private (personal notes, local config) |

**Real example:** `codebase-oracle` uses `project` memory (architecture is repo-specific). `quality-reviewer` uses `user` memory (review preferences carry across projects).

Include explicit memory instructions in the agent's system prompt:

```markdown
## Auto-Memory
After each invocation, update your memory with:
- [what to save]

Consult your memory before starting each run to apply accumulated knowledge.
```

### 4. Preload Skills for Domain Knowledge

The `skills` field injects skill content into the agent's system prompt at startup. The agent always has those conventions in mind — it doesn't need to discover or load them.

```yaml
skills:
  - review-changes    # Agent knows the review workflow from the start
  - security-review   # Agent knows OWASP checks from the start
```

**Key distinction:** Skills loaded this way are part of the system prompt, not invoked via the Skill tool. The agent receives the full skill content as context, not just the skill's description.

**Real example:** `ship-it` preloads `review-changes`, `commit`, and `create-pr` — it knows all three workflows from its first turn without needing to discover them.

### 5. Write Descriptions for Auto-Delegation

Claude uses the `description` to decide when to delegate. Write it like you're teaching Claude when to reach for this agent:

```yaml
# Good — tells Claude exactly when to delegate
description: Expert code quality reviewer. Use proactively after writing or modifying code, before committing, or when asked to review changes.

# Bad — too vague, Claude won't know when to use it
description: Reviews code
```

Include "use proactively" if the agent should be auto-delegated without the user asking.

### 6. Foreground vs Background

- **Foreground** (default): blocks main conversation, can prompt for permissions
- **Background**: runs concurrently, auto-denies unpre-approved permissions

Ask Claude to "run this in the background" or press `Ctrl+B` to background a running agent. Background agents can't use MCP tools.

## Our Agent Roster

### Skill-Composing Agents (with memory)

These agents compose multiple skills and learn over time:

| Agent | Model | Memory | Skills | Delegates When |
|-------|-------|--------|--------|----------------|
| `quality-reviewer` | sonnet | user | review-changes, security-review | After code changes, "review this" |
| `codebase-oracle` | haiku | project | onboard | "How does X work?", codebase questions |
| `ship-it` | inherit | user | review-changes, commit, create-pr | "Ship it", "commit and PR" |

### Domain Expert Agents

Focused agents with deep expertise in a single domain:

| Agent | Model | Focus |
|-------|-------|-------|
| `security-auditor` | inherit | Threat modeling, OWASP, vulnerability analysis |
| `performance-analyst` | inherit | Algorithmic complexity, bottlenecks, caching |
| `reliability-engineer` | inherit | Failure modes, error handling, observability |
| `test-strategist` | inherit | Test design, coverage gaps, flaky tests |
| `tech-lead` | inherit | Architecture decisions, code review, mentoring |
| `api-designer` | inherit | Interface ergonomics, API/CLI design |
| `domain-modeler` | inherit | Data modeling, DDD, state machines |
| `devils-advocate` | inherit | Challenging assumptions, simplicity advocacy |
| `refactoring-strategist` | inherit | Code smells, refactoring plans, tech debt |
| `implementation-investigator` | inherit | Reverse-engineering, tracing code paths |

### Infrastructure Agents

| Agent | Focus |
|-------|-------|
| `kubernetes-architect` | K8s cluster design, networking, security |
| `skaffold-deployment-expert` | Skaffold config, K8s dev workflows |
| `fedora-sysadmin` | Fedora Linux administration, SELinux, systemd |

## Patterns

### Read-Only Reviewer

Restrict tools so the agent can only observe, never modify:

```yaml
---
name: my-reviewer
description: Reviews X for quality. Use proactively after changes.
tools: Read, Grep, Glob, Bash
model: sonnet
---
```

### Learning Expert

Combine skills + memory for an agent that improves over time:

```yaml
---
name: my-expert
description: Expert in X. Use proactively when...
tools: Read, Grep, Glob, Bash
model: sonnet
memory: user
skills:
  - relevant-skill-1
  - relevant-skill-2
---

[System prompt]

## Auto-Memory
After each invocation, save:
- Patterns discovered
- Conventions learned
- False positives to avoid

Consult memory before starting each run.
```

### Hook-Guarded Agent

Use hooks for conditional tool validation:

```yaml
---
name: db-reader
description: Read-only database queries
tools: Bash
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-readonly.sh"
---
```

## Creating New Agents

1. Create `config/claude/agents/<name>.md` with frontmatter + system prompt
2. The dotfiles link script symlinks to `~/.claude/agents/` automatically
3. Restart Claude Code or run `/agents` to load immediately
4. Test with: "Use the <name> agent to..."

### Checklist

- [ ] `name` is lowercase-hyphenated and unique
- [ ] `description` tells Claude exactly when to delegate (include "use proactively" if appropriate)
- [ ] `tools` restricted to minimum needed (read-only agents don't get Write/Edit)
- [ ] `model` chosen deliberately (haiku for speed, sonnet for judgment, inherit for complex tasks)
- [ ] `memory` scope matches knowledge portability (user = cross-project, project = repo-specific)
- [ ] `skills` preloaded if the agent needs domain knowledge from existing skills
- [ ] System prompt includes auto-memory instructions if memory is enabled
- [ ] System prompt has clear "When Invoked" steps and structured output format

## Limitations

- Sub-agents **cannot spawn other sub-agents** (no nesting)
- Sub-agents receive only their system prompt, not the full Claude Code system prompt
- Background agents auto-deny permissions not pre-approved and can't use MCP tools
- Memory files persist based on `cleanupPeriodDays` setting (default: 30 days)
- Auto-compaction triggers at ~95% context capacity (override with `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE`)
