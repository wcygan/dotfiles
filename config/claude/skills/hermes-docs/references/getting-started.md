# Getting Started — Routing

All URLs relative to `https://hermes-agent.nousresearch.com`. WebFetch the best match; do not answer from memory.

## Symptom → URL

| User situation | Fetch |
|---|---|
| "I want to try Hermes" / "how do I install it" / "first-run tutorial" | `/docs/getting-started/quickstart` |
| "I need detailed install options" / "what about package managers" | `/docs/getting-started/installation` |
| "I'm on NixOS" / "install via Nix / flake" | `/docs/getting-started/nix-setup` |
| "how do I upgrade Hermes" / "update to latest" | `/docs/getting-started/updating` |
| "where should I start reading the docs" / "learning order" | `/docs/getting-started/learning-path` |

## Ground-truth facts (verified 2026-04-04)

Use these only to decide routing, not as authoritative answers. Always fetch before quoting specifics.

- Install one-liner (quickstart): `curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash`
- Post-install: `source ~/.bashrc` or `source ~/.zshrc`, then `hermes`
- Model picker: `hermes model` (supports 15+ providers: OpenAI, Anthropic, OpenRouter, DeepSeek, GitHub Copilot, Nous, custom endpoints)
- Platforms: Linux, macOS, WSL2, Windows (via WSL2)

## Common follow-ups

After the user gets past install, they usually ask about: CLI flags (`references/user-guide.md`), config (`references/user-guide.md`), or picking a model (`/docs/integrations/providers`).
