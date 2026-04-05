# Hermes Agent — Complete Documentation Sitemap

Base URL: `https://hermes-agent.nousresearch.com`

All URLs below are relative to the base. This file is a routing index, not cached content. WebFetch the URL you need.

`Last verified: 2026-04-04` (against the live site on that date).

## Getting Started — `/docs/getting-started/`

| URL | Purpose |
|---|---|
| `/docs/getting-started/quickstart` | First-run tutorial: install, select model, start chatting. Single best entry point for new users. |
| `/docs/getting-started/installation` | Detailed install options beyond the one-liner. |
| `/docs/getting-started/nix-setup` | Nix-specific installation path. |
| `/docs/getting-started/updating` | How to upgrade Hermes to a newer version. |
| `/docs/getting-started/learning-path` | Recommended order to read the docs. |

## User Guide (core) — `/docs/user-guide/`

| URL | Purpose |
|---|---|
| `/docs/user-guide/cli` | All CLI flags and usage patterns: `hermes`, `hermes chat -q`, `--model`, `--provider`, `--toolsets`, `-s`, `-c`, `-r`, `--verbose`, `-w`, `--docker`. |
| `/docs/user-guide/configuration` | `~/.hermes/config.yaml`, `.env`, `auth.json`, `SOUL.md` layout; precedence (CLI > config.yaml > .env > defaults); `${VAR}` substitution; `hermes config view/edit/set/check/migrate`. |
| `/docs/user-guide/sessions` | Auto-saved conversations in SQLite (`~/.hermes/state.db`); `--continue`, `--resume`, `hermes sessions list/rename/prune`; title generation; compression lineage. |
| `/docs/user-guide/profiles` | Named config profiles. |
| `/docs/user-guide/git-worktrees` | `-w` flag and isolated worktree runs. |
| `/docs/user-guide/docker` | `--docker`, `TERMINAL_BACKEND=docker`, container hardening. |
| `/docs/user-guide/checkpoints-and-rollback` | Pre-edit snapshots and rollback. |
| `/docs/user-guide/security` | Five-layer defense: user auth → dangerous-command approval → container isolation → MCP credential filtering → context-file scanning. `--yolo`, SSRF protection, DM pairing, tirith scanning. |
| `/docs/user-guide/messaging/` | Telegram, Discord, WhatsApp, Slack overview. |
| `/docs/user-guide/messaging/discord` | Discord-specific setup. |

## User Guide / Features — `/docs/user-guide/features/`

| URL | Purpose |
|---|---|
| `/docs/user-guide/features/overview` | Index of every feature; start here if the user is orienting. |
| `/docs/user-guide/features/tools` | Tools & toolsets (web, terminal, files, etc.). |
| `/docs/user-guide/features/skills` | Hermes' skills system (progressive disclosure). |
| `/docs/user-guide/features/memory` | Persistent `MEMORY.md`, `USER.md`. |
| `/docs/user-guide/features/context-files` | Auto-loaded `.hermes.md`, `AGENTS.md`. |
| `/docs/user-guide/features/context-references` | `@file`, `@folder`, `@url` syntax in messages. |
| `/docs/user-guide/features/mcp` | MCP server integration. |
| `/docs/user-guide/features/voice-mode` | Voice interaction across CLI and messaging. |
| `/docs/user-guide/features/personality` | SOUL.md, identity customization. |
| `/docs/user-guide/features/cron` | Scheduled tasks via cron or natural language. |
| `/docs/user-guide/features/delegation` | Subagent delegation, `/background`, parallel sessions. |
| `/docs/user-guide/features/code-execution` | Python scripts calling Hermes tools programmatically. |
| `/docs/user-guide/features/hooks` | Lifecycle event hooks. |
| `/docs/user-guide/features/batch-processing` | Bulk prompt runs, trajectory generation. |
| `/docs/user-guide/features/rl-training` | RL trajectory data export. |
| `/docs/user-guide/features/browser` | Browser automation backends. |
| `/docs/user-guide/features/vision` | Clipboard image paste, vision models. |
| `/docs/user-guide/features/image-generation` | FLUX 2 Pro image generation. |
| `/docs/user-guide/features/tts` | Text-to-speech and voice transcription. |
| `/docs/user-guide/features/provider-routing` | Fine-grained provider selection. |
| `/docs/user-guide/features/fallback-providers` | Failover between LLM providers. |
| `/docs/user-guide/features/credential-pools` | Multi-key rotation: round-robin, least-used, fill-first, random. |
| `/docs/user-guide/features/api-server` | OpenAI-compatible HTTP endpoint. |
| `/docs/user-guide/features/acp` | VS Code, Zed, JetBrains IDE integration. |
| `/docs/user-guide/features/honcho` | AI-native persistent user memory. |
| `/docs/user-guide/features/skins` | CLI themes, colors, branding. |
| `/docs/user-guide/features/plugins` | Custom tools via `~/.hermes/plugins/`. |

## Integrations — `/docs/integrations/`

| URL | Purpose |
|---|---|
| `/docs/integrations/` | Integrations landing page. |
| `/docs/integrations/providers` | OpenRouter, Anthropic, OpenAI, Google, Nous, DeepSeek, GitHub Copilot, custom OpenAI-compatible endpoints. |

## Guides (how-to recipes) — `/docs/guides/`

| URL | Purpose |
|---|---|
| `/docs/guides/tips` | Tips, gotchas, prompt-cache hygiene, `/compress` timing, `--yolo` warnings. |
| `/docs/guides/build-a-hermes-plugin` | Plugin authoring walkthrough. |
| `/docs/guides/daily-briefing-bot` | Recipe: scheduled briefing bot. |
| `/docs/guides/team-telegram-assistant` | Recipe: team Telegram assistant. |
| `/docs/guides/python-library` | Using Hermes as a Python library. |
| `/docs/guides/use-mcp-with-hermes` | Wiring MCP servers into Hermes. |
| `/docs/guides/use-soul-with-hermes` | Customizing personality via SOUL.md. |
| `/docs/guides/use-voice-mode-with-hermes` | Voice mode setup walkthrough. |
| `/docs/guides/migrate-from-openclaw` | Migration guide from openclaw. |

## Developer Guide — `/docs/developer-guide/`

| URL | Purpose |
|---|---|
| `/docs/developer-guide/architecture` | Internal architecture of Hermes. |
| `/docs/developer-guide/contributing` | Contribution workflow. |

## Reference — `/docs/reference/`

| URL | Purpose |
|---|---|
| `/docs/reference/cli-commands` | Authoritative CLI command reference. |
| `/docs/reference/slash-commands` | Every `/slash` command inside a session. |
| `/docs/reference/environment-variables` | All env vars Hermes reads. |
| `/docs/reference/faq` | FAQ & troubleshooting. |

## External

- Source: `https://github.com/NousResearch/hermes-agent`
- Community: `https://discord.gg/NousResearch`
