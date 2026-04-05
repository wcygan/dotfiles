# Integrations — Routing

Base: `https://hermes-agent.nousresearch.com`. Integrations are split between `/docs/integrations/` and the feature pages they document — follow the table.

## Symptom → URL

| User situation | Fetch |
|---|---|
| "What integrations does Hermes support?" (orientation) | `/docs/integrations/` |
| Which LLM providers work (OpenRouter, Anthropic, OpenAI, Google, Nous, DeepSeek, GitHub Copilot, custom OpenAI-compatible) | `/docs/integrations/providers` |
| Provider routing rules (cost/speed/quality) | `/docs/user-guide/features/provider-routing` |
| Fallback between providers on error | `/docs/user-guide/features/fallback-providers` |
| Credential pools / multi-key rotation | `/docs/user-guide/features/credential-pools` |
| MCP servers (GitHub, databases, files, external APIs) | `/docs/user-guide/features/mcp` |
| How to actually wire an MCP server into Hermes | `/docs/guides/use-mcp-with-hermes` |
| Web search backends (Firecrawl, Parallel, Tavily, Exa) | `/docs/integrations/` (then follow footer) |
| Browser automation providers (cloud + local) | `/docs/user-guide/features/browser` |
| TTS + STT providers | `/docs/user-guide/features/tts` |
| Voice mode end-to-end | `/docs/user-guide/features/voice-mode` |
| Voice mode how-to setup | `/docs/guides/use-voice-mode-with-hermes` |
| IDE integration (VS Code, Zed, JetBrains) | `/docs/user-guide/features/acp` |
| OpenAI-compatible API server (expose Hermes to other frontends) | `/docs/user-guide/features/api-server` |
| Honcho (AI-native user memory) | `/docs/user-guide/features/honcho` |
| Batch processing / RL training data | `/docs/user-guide/features/batch-processing`, `/docs/user-guide/features/rl-training` |
| Messaging: Telegram, Discord, WhatsApp, Slack | `/docs/user-guide/messaging/` |
| Discord specifics | `/docs/user-guide/messaging/discord` |

## Providers quick-reference (verified 2026-04-04)

Routing use only — always WebFetch `/docs/integrations/providers` for current list and auth shape.

- **OpenAI-native**: OpenAI, Anthropic, Google, OpenRouter, Nous, Groq, DeepSeek, GitHub Copilot
- **Custom**: any OpenAI-compatible endpoint (base_url override)
- **Auth storage**: API keys → `.env`; OAuth (Nous Portal, ChatGPT/Codex) → `auth.json`
- **Selection**: `hermes model` interactive picker, or `--model`/`--provider` flags, or `config.yaml`
