---
title: Session Mobility (Teleport & Remote Control)
canonical_url: https://code.claude.com/docs/en/remote-control
fetch_before_acting: true
---

# Session Mobility

> Before setting up session mobility, WebFetch https://code.claude.com/docs/en/remote-control for the latest.

## Summary

Move Claude Code sessions between terminal, web, desktop, and mobile. Two complementary features:

- **Teleport**: pull a cloud/web session into your local terminal
- **Remote Control**: drive a locally-running session from your phone, tablet, or any browser

### Teleport (Web → Terminal)

Continue a cloud session on your machine. The session keeps its full conversation history and branch.

```bash
# Interactive picker of your web sessions
claude --teleport

# Resume a specific session
claude --teleport <session-id>

# From inside an active session
/teleport
# or shorthand
/tp
```

**Requirements**: clean git state (no uncommitted changes), correct repository, branch pushed to remote, same claude.ai account.

**Workflow tip**: plan locally with `claude --permission-mode plan`, then execute remotely with `claude --remote "Execute the plan"`, then teleport back to continue locally.

### Remote Control (Terminal → Web/Mobile)

Control a locally-running session from claude.ai/code or the Claude mobile app. Claude keeps running on your machine — nothing moves to the cloud.

**Three ways to start:**

```bash
# Dedicated server mode (no local interactive session)
claude remote-control
claude remote-control --name "My Project"

# Interactive session with remote control enabled
claude --remote-control
claude --rc

# From an existing session
/remote-control
/rc
```

**Server mode flags:**

| Flag | Description |
|------|-------------|
| `--name "title"` | Custom session title visible at claude.ai/code |
| `--spawn <mode>` | `same-dir` (default) or `worktree` for concurrent sessions |
| `--capacity <N>` | Max concurrent sessions (default: 32) |
| `--verbose` | Show detailed connection logs |

**Connect from another device:**
- Open the session URL shown in terminal
- Scan the QR code (press spacebar in server mode to toggle)
- Find the session in claude.ai/code session list (green dot = online)

### Enable Remote Control for All Sessions

Run `/config` and set **Enable Remote Control for all sessions** to `true`. Every interactive session becomes remotely accessible without passing `--rc`.

### Key Differences

| Feature | Remote Control | Claude Code on the Web |
|---------|---------------|----------------------|
| Runs on | Your machine | Anthropic cloud |
| Local files/MCP | Yes | No (fresh clone) |
| Requires machine on | Yes | No |
| Best for | Steering in-progress local work | Fire-and-forget tasks |

### Security

- Outbound HTTPS only — no inbound ports opened
- All traffic routed through Anthropic API over TLS
- Short-lived, scoped credentials
- Auto-reconnects after laptop sleep or network drops

### Terminal → Web (--remote)

Start a *new* web session from your terminal:

```bash
claude --remote "Fix the authentication bug in src/auth/login.ts"
```

This creates a cloud session. Monitor with `/tasks`, or open at claude.ai/code. Combine with teleport to pull results back.
