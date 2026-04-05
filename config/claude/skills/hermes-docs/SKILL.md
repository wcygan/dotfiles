---
name: hermes-docs
description: Look up Hermes Agent (Nous Research) documentation at hermes-agent.nousresearch.com. Use when the user asks about Hermes CLI commands, Hermes configuration (~/.hermes/config.yaml, .env, SOUL.md), Hermes sessions, Hermes security/sandboxing, Hermes skills/memory/tools/MCP, Hermes voice mode, Hermes integrations or providers, or mentions "hermes-agent" or the hermes CLI. Keywords hermes, hermes-agent, nous research, hermes cli, hermes config, hermes sessions, hermes skills, SOUL.md, hermes mcp, hermes voice mode, ~/.hermes.
---

# Hermes Agent Documentation Navigator

Route Hermes-related questions to the correct doc URL on `hermes-agent.nousresearch.com`, WebFetch it live, and answer from the fetched content.

## When this skill applies

Activate ONLY when the user is clearly asking about **Hermes Agent by Nous Research** (the CLI tool at `hermes-agent.nousresearch.com`), not other things named "hermes" (Greek god, `python-hermes`, Hermes messaging library, etc.). Require both `hermes` AND an intent word like `cli`, `config`, `session`, `skill`, `mcp`, `docs`, `agent`, `install`, or a direct URL mention. If the context is ambiguous, ask the user to confirm before fetching.

## Operating rules

1. **Always WebFetch live.** Do not answer Hermes questions from memory — the product is evolving and cached knowledge goes stale. Fetch the routed URL, then cite it.
2. **Route before fetching.** Use the routing table below to pick the single best starting URL. If the first page doesn't answer the question, fetch at most one or two linked pages from its footer.
3. **Cite URLs in the answer.** Always link the specific `/docs/...` pages you used so the user can verify.
4. **Prefer reference pages for factual lookups** (`/docs/reference/*`) and feature pages for conceptual/how-to questions.
5. **Fallback**: if a URL 404s, WebFetch `https://hermes-agent.nousresearch.com/docs` and re-route from the live sitemap.

## Top-level routing table

| User asks about… | First URL to WebFetch |
|---|---|
| Install, first run, getting started, updating | `/docs/getting-started/quickstart` |
| Nix setup specifically | `/docs/getting-started/nix-setup` |
| CLI commands, flags, slash commands, `-c`/`--resume`/`-w`/`--docker` | `/docs/user-guide/cli` |
| Exact slash-command list | `/docs/reference/slash-commands` |
| Exact CLI command reference | `/docs/reference/cli-commands` |
| `config.yaml`, `.env`, `~/.hermes/`, API keys, model selection, precedence | `/docs/user-guide/configuration` |
| Environment variable names | `/docs/reference/environment-variables` |
| Sessions: resume, list, storage, SQLite, titles, transcripts | `/docs/user-guide/sessions` |
| Profiles (per-context config) | `/docs/user-guide/profiles` |
| Git worktrees (`-w`) | `/docs/user-guide/git-worktrees` |
| Docker sandboxing (`--docker`, `TERMINAL_BACKEND`) | `/docs/user-guide/docker` |
| Checkpoints & rollback | `/docs/user-guide/checkpoints-and-rollback` |
| Security model, dangerous-command approval, `--yolo`, SSRF, DM pairing | `/docs/user-guide/security` |
| What features exist (orientation) | `/docs/user-guide/features/overview` |
| Skills (Hermes' own skill system) | `/docs/user-guide/features/skills` |
| Tools & toolsets | `/docs/user-guide/features/tools` |
| Memory (`MEMORY.md`, `USER.md`) | `/docs/user-guide/features/memory` |
| MCP servers | `/docs/user-guide/features/mcp` |
| Voice mode | `/docs/user-guide/features/voice-mode` |
| SOUL.md, personality | `/docs/user-guide/features/personality` |
| Context files (`.hermes.md`, `AGENTS.md` auto-injection) | `/docs/user-guide/features/context-files` |
| `@` references (files/folders/URLs in messages) | `/docs/user-guide/features/context-references` |
| Cron / scheduled tasks | `/docs/user-guide/features/cron` |
| Subagent delegation, `/background` | `/docs/user-guide/features/delegation` |
| Code execution (Python scripts calling Hermes tools) | `/docs/user-guide/features/code-execution` |
| Hooks | `/docs/user-guide/features/hooks` |
| Batch processing, RL trajectory data | `/docs/user-guide/features/batch-processing` |
| Browser automation | `/docs/user-guide/features/browser` |
| Vision, image paste, image generation | `/docs/user-guide/features/vision` |
| Provider routing / fallback providers / credential pools | `/docs/user-guide/features/provider-routing` |
| OpenAI-compatible API server | `/docs/user-guide/features/api-server` |
| ACP / VS Code / Zed / JetBrains integration | `/docs/user-guide/features/acp` |
| Honcho memory | `/docs/user-guide/features/honcho` |
| Telegram / Discord / WhatsApp / Slack messaging | `/docs/user-guide/messaging/` |
| Providers list (OpenRouter, Anthropic, Nous, etc.) | `/docs/integrations/providers` |
| Integrations overview | `/docs/integrations/` |
| Tips, gotchas, best practices | `/docs/guides/tips` |
| How-to recipes (bots, plugins, migration) | `references/guides.md` (routes to `/docs/guides/*`) |
| Architecture, how Hermes works internally | `/docs/developer-guide/architecture` |
| Contributing | `/docs/developer-guide/contributing` |
| FAQ / troubleshooting | `/docs/reference/faq` |

## Deeper routing

For topic areas with many sub-pages, load the matching reference file first to pick the exact URL, then WebFetch:

- **`references/sitemap.md`** — the complete URL inventory, grouped by section. Use this when the user asks something that doesn't obviously match the top-level table.
- **`references/getting-started.md`** — install / first-run / updating paths.
- **`references/user-guide.md`** — core user-guide pages (CLI, config, sessions, security, profiles, docker, worktrees, messaging).
- **`references/features.md`** — all 25+ `/user-guide/features/*` pages grouped by theme with symptom-based routing.
- **`references/integrations.md`** — providers, MCP, browser, voice, ACP, API server.
- **`references/guides.md`** — how-to recipes and migration guides under `/docs/guides/*`.
- **`references/reference.md`** — factual reference pages (CLI commands, env vars, slash commands, FAQ).

## Disambiguation guard

If the user just says "hermes" with no Nous-Research context, ask:
> Are you asking about Hermes Agent by Nous Research (the CLI at hermes-agent.nousresearch.com)? There are other projects named Hermes — just want to confirm before I pull docs.

## Kill criterion

`Last verified: 2026-04-04.` If two consecutive WebFetch calls to the base URLs in this skill return 404 or redirect off-site, the docs have moved — tell the user and delete or update this skill rather than guessing.
