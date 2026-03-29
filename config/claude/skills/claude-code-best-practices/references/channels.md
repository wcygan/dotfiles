---
title: Channels
canonical_url: https://code.claude.com/docs/en/channels
fetch_before_acting: true
---

# Channels

> Before setting up channels, WebFetch https://code.claude.com/docs/en/channels for the latest.

## Summary

Channels push events into a running Claude Code session via MCP servers. Claude reacts to external events (CI, chat, webhooks) while you're away from the terminal. Research preview — requires v2.1.80+.

### Supported Channels

- **Telegram** — bot token via BotFather, pairing code workflow
- **Discord** — bot token via Developer Portal, pairing code workflow
- **iMessage** — macOS only, reads Messages DB directly, no token needed
- **fakechat** — localhost demo for testing

### Setup Pattern

1. Install plugin: `/plugin install <channel>@claude-plugins-official`
2. Configure token: `/<channel>:configure <token>`
3. Restart with channel: `claude --channels plugin:<channel>@claude-plugins-official`
4. Pair: send message to bot → get code → `/<channel>:access pair <code>`
5. Lock down: `/<channel>:access policy allowlist`

### Security

- Sender allowlist per channel — only approved IDs can push messages
- `--channels` flag controls which servers are enabled per session
- Team/Enterprise: `channelsEnabled` and `allowedChannelPlugins` in managed settings

### Channels vs Alternatives

| Feature | What it does |
|---------|-------------|
| Claude on web | Fresh cloud sandbox from GitHub |
| Claude in Slack | Spawns web session from @mention |
| MCP server | Claude queries on demand (pull) |
| Remote Control | Drive local session from claude.ai |
| **Channels** | External events pushed in (push) |

### Enterprise

Off by default on Team/Enterprise. Admins enable via `channelsEnabled: true` in managed settings.
