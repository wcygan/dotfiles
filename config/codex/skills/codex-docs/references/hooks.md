---
canonical_url: https://developers.openai.com/codex/hooks
last_verified: 2026-05-06
---

# Hooks

Use this reference when the user asks about Codex lifecycle scripts, hook events, matchers, hook JSON/TOML shape, or deterministic local automation.

Key points from the official docs:

- Hooks let users run deterministic scripts during the Codex lifecycle.
- Hooks are behind the `codex_hooks` feature flag.
- Hooks can be declared in `hooks.json` or inline `[hooks]` tables in `config.toml`.
- Hooks can be user-global or project-local; project-local hooks load only when the project `.codex/` layer is trusted.
- Matching hooks from multiple files all run.
- Multiple matching command hooks for the same event are launched concurrently.
- Prefer one representation per layer: either `hooks.json` or inline `[hooks]`.

Feature flag:

```toml
[features]
codex_hooks = true
```

Common locations:

- `~/.codex/hooks.json`
- `~/.codex/config.toml`
- `<repo>/.codex/hooks.json`
- `<repo>/.codex/config.toml`

Common events:

- `SessionStart`
- `PreToolUse`
- `PermissionRequest`
- `PostToolUse`
- `UserPromptSubmit`
- `Stop`

Matcher notes:

- Matchers are regex strings.
- `*`, empty string, or omitted matcher means match everything.
- Tool-scoped matchers apply to `PreToolUse`, `PermissionRequest`, and `PostToolUse`.
- `SessionStart` matchers filter start sources such as `startup`, `resume`, and `clear`.
- `UserPromptSubmit` and `Stop` currently ignore matcher values.

Hook command notes:

- Command hooks receive one JSON object on `stdin`.
- Commands run with the session current working directory.
- If `timeout` is omitted, Codex uses 600 seconds.
- For repo-local hooks, resolve scripts from the Git root rather than relying on the current subdirectory.
