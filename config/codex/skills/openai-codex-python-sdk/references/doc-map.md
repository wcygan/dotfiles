---
canonical_url: https://github.com/openai/codex/tree/main/sdk/python
last_verified: 2026-06-05
---

# Codex Python SDK Documentation Map

Use the official OpenAI `openai/codex` repository as the source of truth for the Python SDK.

## Strict SDK Sources

These files were present under `sdk/python` when checked on 2026-06-05:

- README: https://github.com/openai/codex/blob/main/sdk/python/README.md
- Getting started: https://github.com/openai/codex/blob/main/sdk/python/docs/getting-started.md
- API reference: https://github.com/openai/codex/blob/main/sdk/python/docs/api-reference.md
- FAQ: https://github.com/openai/codex/blob/main/sdk/python/docs/faq.md
- Examples index: https://github.com/openai/codex/blob/main/sdk/python/examples/README.md

## Adjacent Runtime Source

- Python runtime package: https://github.com/openai/codex/blob/main/sdk/python-runtime/README.md

Treat `sdk/python-runtime` as adjacent packaging context. It explains the runtime dependency used by the Python SDK, but it is not part of the strict `sdk/python` docs tree.

## Reading Order

1. Start with the README for the package purpose, install command, quickstart, auth entry points, and built-in help.
2. Read Getting Started for a runnable multi-turn flow, sandbox presets, thread continuation, and async usage.
3. Read the API reference before naming exact classes, methods, keyword arguments, result fields, or imported types.
4. Read the FAQ for stability, runtime-package, retry, migration, and common failure behavior.
5. Read the Examples index before writing sample code or selecting a pattern for a real app.

## Verification Rules

- If the user needs exact current behavior, fetch the linked source before answering.
- If a local `openai/codex` checkout is available, inspect its `sdk/python` files instead of relying on this map.
- If GitHub docs and installed package behavior conflict, verify the installed `openai_codex.__version__`, package metadata, and the runtime package version before changing application code.
