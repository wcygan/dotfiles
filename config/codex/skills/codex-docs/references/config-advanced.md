---
canonical_url: https://developers.openai.com/codex/config-advanced
last_verified: 2026-05-06
---

# Advanced Config

Use this reference when the user asks about profiles, one-off CLI overrides, state locations, model providers, MCP, shell environment policy, telemetry, or analytics.

Key points from the official docs:

- Advanced config is for providers, policies, integrations, and finer control.
- Use config basics first when the user only needs common settings.
- Check the official config reference when exact keys, defaults, or supported values matter.

Profiles:

- Profiles are experimental.
- Profiles live under `[profiles.<name>]` in `config.toml`.
- Use `codex --profile <name>` to select a profile.
- Set `profile = "<name>"` at the top level to make one profile the default.
- Profiles can override keys such as model, reasoning effort, approval policy, and model catalog path.

Example:

```toml
model = "gpt-5.4"
approval_policy = "on-request"

[profiles.deep-review]
model = "gpt-5-pro"
model_reasoning_effort = "high"
approval_policy = "never"

[profiles.lightweight]
model = "gpt-4.1"
approval_policy = "untrusted"
```

One-off overrides:

```bash
codex --model gpt-5.4
codex --config model='"gpt-5.4"'
codex --config sandbox_workspace_write.network_access=true
codex --config 'shell_environment_policy.include_only=["PATH","HOME"]'
```

Notes:

- `--config` values are parsed as TOML.
- Dot notation can set nested keys.
- Quote values carefully so the shell does not split them.

State locations:

- `CODEX_HOME` defaults to `~/.codex`.
- Common files include `config.toml`, credentials or keychain references, `history.jsonl`, logs, and caches.
- Do not link the whole `~/.codex` directory into dotfiles unless intentionally tracking runtime state.

Telemetry and analytics:

- Codex can export OpenTelemetry logs/traces/metrics when configured.
- Anonymous health and usage metrics are enabled by default unless disabled.

Disable analytics:

```toml
[analytics]
enabled = false
```

When giving advice, avoid inventing unsupported keys. Fetch the official page or config reference for exact syntax.
