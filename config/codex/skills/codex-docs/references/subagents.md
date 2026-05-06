---
canonical_url: https://developers.openai.com/codex/subagents
last_verified: 2026-05-06
---

# Subagents

Use this reference when the user asks about spawning agents, custom agents, parallel work, or agent-specific config.

Key points from the official docs:

- Current Codex releases enable subagent workflows by default.
- Subagent activity is visible in the Codex app and CLI; IDE visibility is documented as coming soon.
- Codex only spawns subagents when explicitly asked.
- Subagents are useful for work that can run in parallel, such as codebase exploration or multi-part PR review.
- Subagents use additional tokens because each agent performs its own model and tool work.
- The CLI `/agent` command can switch between active agent threads.
- Users can steer, stop, or close running subagents by asking Codex.
- Subagents inherit the current sandbox policy.
- Runtime overrides from the parent turn, including approval and sandbox changes, apply when Codex spawns a child.

Built-in agents:

- `default`: general-purpose fallback.
- `worker`: implementation and fixes.
- `explorer`: read-heavy codebase exploration.

Custom agents:

- Personal custom agents live under `~/.codex/agents/`.
- Project custom agents live under `.codex/agents/`.
- Each custom agent is a standalone TOML file.
- Required fields are `name`, `description`, and `developer_instructions`.
- Optional fields can include model, reasoning effort, sandbox mode, MCP servers, and skills configuration.

Global settings live under `[agents]`, including open thread caps, spawn depth, and default worker job runtime.
