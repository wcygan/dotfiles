---
canonical_url: https://github.com/openai/codex/blob/main/sdk/python/examples/README.md
last_verified: 2026-06-05
---

# Examples and Patterns

Use the checked-in examples before inventing SDK usage. Each example folder contains `sync.py` for `Codex` and `async.py` for `AsyncCodex`.

## General Pattern

- Use plain strings for text-only turns.
- Use typed input objects for multimodal or structured input lists.
- Use only public exports from `openai_codex` and `openai_codex.types`.
- From a checkout, run examples from `sdk/python`.

Recommended first run:

```sh
python examples/01_quickstart_constructor/sync.py
python examples/01_quickstart_constructor/async.py
```

## Example Index

- `01_quickstart_constructor/`: first run and sanity check.
- `02_turn_run/`: inspect full turn output fields.
- `03_turn_stream_events/`: stream a turn with a curated event view.
- `04_models_and_metadata/`: discover visible models for the connected runtime.
- `05_existing_thread/`: resume an existing thread created in-script.
- `06_thread_lifecycle_and_controls/`: thread lifecycle and control calls.
- `07_image_and_text/`: remote image URL plus text multimodal turn.
- `08_local_image_and_text/`: local image plus text multimodal turn using a generated sample image.
- `09_async_parity/`: parity-style sync flow with async equivalent patterns elsewhere.
- `10_error_handling_and_retry/`: overload retry pattern and typed error handling.
- `11_cli_mini_app/`: interactive chat loop.
- `12_turn_params_kitchen_sink/`: structured output with advanced `turn(...)` configuration.
- `13_model_select_and_turn_params/`: list models, choose model and reasoning effort, run turns, and print usage.
- `14_turn_controls/`: separate `steer()` and `interrupt()` demos.
- `15_login_and_account/`: browser-login handle lifecycle, cancellation, and account inspection.

## Pattern Selection

- For quick scripts or backend jobs, start from quickstart plus `02_turn_run`.
- For UI progress or dashboards, start from `03_turn_stream_events`.
- For existing conversation state, start from `05_existing_thread`.
- For user-controlled chat apps, start from `11_cli_mini_app`.
- For schemas or advanced turn settings, start from `12_turn_params_kitchen_sink`.
- For account onboarding or auth troubleshooting, start from `15_login_and_account`.
