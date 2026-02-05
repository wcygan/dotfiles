# CLAUDE.md

## Core Philosophy

**Small steps, tests first, green builds, atomic commits.**

## Development Loop

1. Write test first
2. Implement minimal solution
3. Run tests (must pass)
4. Format & lint
5. Commit atomically
6. Repeat

## Commit Rules

- All tests pass
- Code formatted and linted
- Single logical change with tests

## CLI Tools

**Prefer**: `rg`, `fd`, `bat`, `eza`, `jq`, `yq`, `fzf`, `delta`, `gh`

## Sub-Agents

Use 2-3 parallel agents for: codebase exploration, research, code quality audits, bug investigation.

**Never** for: single file reads, sequential tasks, trivial operations.

## Agent Teams

Use agent teams when parallel work benefits from **inter-agent debate and coordination**. Use `/agent-team` or describe the team composition you want.

**When to use teams** (instead of sub-agents):
- Multiple perspectives that create productive tension (security vs. performance, design vs. simplicity)
- Research with competing hypotheses that should challenge each other
- Cross-layer work where frontend, backend, and tests each need an owner
- Reviews where security, performance, and correctness are evaluated simultaneously

**Team sizes**: 2-3 agents for most tasks. 4-5 for complex audits or multi-hypothesis debugging. Avoid 6+.

**Key patterns**:
- **Design Review**: api-designer + domain-modeler + devils-advocate
- **Hardening**: security-auditor + reliability-engineer + performance-analyst
- **Architecture Review**: tech-lead + security-auditor + performance-analyst + devils-advocate
- **Feature Development**: api-designer + domain-modeler + test-strategist
- **Pre-Production Audit**: security-auditor + reliability-engineer + test-strategist + performance-analyst

**Rules**:
- Use delegate mode (Shift+Tab) to keep the lead orchestrating, not implementing
- Never have two agents edit the same file — split by file ownership
- Always include a devils-advocate for major decisions
- Tell the lead to "wait for teammates to finish" if it starts implementing

## Communication

- Concise (max 4 lines unless asked)
- No preamble/postamble
- Direct answers
