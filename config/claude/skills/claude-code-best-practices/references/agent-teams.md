---
title: Agent Teams
canonical_url: https://code.claude.com/docs/en/agent-teams
fetch_before_acting: true
---

# Agent Teams

> Before setting up agent teams, WebFetch https://code.claude.com/docs/en/agent-teams for the latest.

## Summary

Agent teams coordinate multiple Claude Code sessions working together. One session leads, teammates work independently with their own context windows, and they communicate via messaging.

**Experimental** — requires `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` in settings or environment. Requires v2.1.32+.

### Best Use Cases

- Research and review (parallel investigation)
- New modules/features (each teammate owns a piece)
- Debugging competing hypotheses
- Cross-layer coordination

### How to Start

Use `TeamCreate` tool or describe the team you want. The lead assigns tasks and synthesizes results.

### Key Rules

- Never have two agents edit the same file
- Each teammate gets a clear, bounded task
- Include a devil's advocate for major decisions
- 2-3 agents typical, 4-5 for complex audits

### Communication

- `SendMessage` — direct messaging between teammates
- Teammates can message each other (not just the lead)
- User can interact with individual teammates directly

### When NOT to Use

- Sequential tasks (use one agent)
- Simple file reads (use tools directly)
- Tasks requiring shared state (use sub-agents instead)
