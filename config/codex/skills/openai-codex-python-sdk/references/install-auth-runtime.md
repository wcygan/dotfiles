---
canonical_url: https://github.com/openai/codex/blob/main/sdk/python/docs/getting-started.md
last_verified: 2026-06-05
---

# Install, Auth, and Runtime

Use this reference for setup, authentication, and packaging questions. Re-check the linked docs before precise version guidance.

## Install

- Published package: `openai-codex`
- Import package: `openai_codex`
- Python requirement observed in the docs: `>=3.10`
- Basic install command:

```sh
python -m pip install openai-codex
```

The docs describe `openai-codex` as a public beta. While beta releases are the only published releases, normal pip install selects the latest beta; after a stable release exists, prerelease opt-in may require `--pre`.

## Authentication

The SDK reuses existing Codex authentication when one is available. Explicit login flows are available from `Codex`:

- `login_chatgpt()` starts browser login and returns a handle with an `auth_url`.
- `login_chatgpt_device_code()` starts device-code login and returns a `verification_url` plus `user_code`.
- `login_api_key(...)` authenticates synchronously with an API key.
- Interactive login handles expose `wait()` for completion and `cancel()` to stop that attempt.
- `account()` reads current account state, and `logout()` clears it.

Do not write real API keys into examples, tests, docs, or shell commands. Use placeholders only when documenting the API shape, and prefer environment variables or existing Codex auth for runnable code.

## Runtime Package

The SDK installs a compatible `openai-codex-cli-bin` runtime dependency automatically. The SDK and runtime packages are versioned independently, and each SDK release pins one compatible runtime package.

The adjacent runtime README says `openai-codex-cli-bin` is wheel-only and is staged during release so the SDK can pin an exact Codex CLI version without committing platform binaries to the repository.

## Checkout Development

For contributors running checked-in examples from the repository, the examples README says to work from `sdk/python` and install development dependencies:

```sh
uv sync --extra dev
source .venv/bin/activate
```

The checked-in examples bootstrap local SDK imports from `sdk/python/src`. If the pinned runtime is missing for the active interpreter, the bootstrap installs the matching runtime package and cleans temporary files afterward.
