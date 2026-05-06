---
canonical_url: https://developers.openai.com/codex/config-basic
last_verified: 2026-05-06
---

# Config Basics

Use this reference when the user asks where Codex config lives, how config precedence works, or how to set common local options.

Key points from the official docs:

- User configuration lives at `~/.codex/config.toml`.
- Project overrides live in `.codex/config.toml`.
- CLI and IDE extension share the same configuration layers.
- Project `.codex/` layers load only when the project is trusted.

Precedence, highest first:

1. CLI flags and `--config` overrides.
2. Profile values from `--profile <name>`.
3. Project `.codex/config.toml` files from repo root to current working directory, closest wins, trusted projects only.
4. User config at `~/.codex/config.toml`.
5. System config at `/etc/codex/config.toml` on Unix, if present.
6. Built-in defaults.

Common options:

```toml
model = "gpt-5.5"
approval_policy = "on-request"
sandbox_mode = "workspace-write"
default_permissions = ":workspace"
web_search = "cached"
model_reasoning_effort = "high"
personality = "pragmatic"
```

Windows sandbox:

```toml
[windows]
sandbox = "elevated"
```

TUI keymap example:

```toml
[tui.keymap.global]
open_transcript = "ctrl-t"

[tui.keymap.composer]
submit = ["enter", "ctrl-m"]
```

When editing config, prefer the smallest relevant layer. Use user config for personal defaults and project config only for repository-specific behavior.
