---
name: openai-codex-python-sdk
description: Use when building, reviewing, debugging, or documenting Python applications that use the OpenAI Codex Python SDK, especially the openai-codex package, openai_codex imports, Codex or AsyncCodex clients, threads, turns, streaming, login flows, sandbox access, SDK examples, or the openai-codex-cli-bin runtime package. Use this skill for Codex Python SDK questions even when the user only says "Codex SDK" in a Python context.
---

# OpenAI Codex Python SDK

Use this skill for Python work against the public beta OpenAI Codex SDK. Keep exact API claims source-backed because the SDK is beta and may change before 1.0.

## Workflow

1. Identify the task surface: install/auth/runtime, threads and turns, streaming or turn controls, async parity, multimodal or structured input, examples, or troubleshooting.
2. Read the smallest relevant reference file from the map below.
3. Verify current details before precise API, install, or version claims:
   - Prefer a local `openai/codex` checkout when the user is working inside one.
   - Otherwise fetch the official GitHub sources listed in `references/doc-map.md`.
4. Inspect the target application code before editing. Match its Python package manager, async style, logging style, and test pattern.
5. Use public SDK exports from `openai_codex` and `openai_codex.types`. Avoid private modules unless the task is explicitly about SDK internals.
6. Choose the client deliberately: `Codex` for sync programs and `AsyncCodex` with `async with` for async programs.
7. Choose the turn primitive deliberately: `thread.run(...)` for common cases and `thread.turn(...)` when streaming, steering, interrupting, or custom event handling is needed.
8. Set `sandbox=` intentionally on thread starts and sensitive turns. Do not assume filesystem access from examples.
9. Keep secrets out of code, docs, tests, shell history, and committed config. Prefer existing Codex auth or user-managed environment variables for API keys.

## Reference Map

- `references/doc-map.md`: official source links, strict `sdk/python` file list, and verification rules.
- `references/install-auth-runtime.md`: package install, Python requirement, login flows, and runtime package behavior.
- `references/threads-turns-sandbox.md`: clients, thread lifecycle, turns, streaming, result fields, kwargs, and sandbox presets.
- `references/examples-patterns.md`: official example folders and when to copy each pattern.
- `references/troubleshooting.md`: beta caveats, migration notes, constructor failures, hanging turns, retries, and runtime mismatch checks.

## Quality Rules

- Treat the SDK as beta. Re-check the source before encoding exact signatures or long-lived guidance.
- Prefer the official checked-in examples over invented minimal snippets when implementing real workflows.
- Distinguish conversation state from execution: a `Thread` holds state; a turn is one model execution inside that thread.
- Prefer `run()` unless the application genuinely needs event-by-event behavior.
- Use `stream()` only when the app will keep consuming notifications until the matching turn completes.
- Do not retry all failures. Retry only transient overload failures with the SDK-supported retry helper or an equivalent bounded policy.
- Keep public keyword arguments in Python `snake_case`; the SDK maps wire-level names internally.

## Fast Commands

```sh
python -m pip install openai-codex
python -m pydoc openai_codex
python -m pydoc openai_codex.Codex
```
