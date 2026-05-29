# Local & custom models (`models.json`)

Contents: File location & reload · Supported `api` values · Minimal local provider · This machine's llama.cpp+Qwen setup (incl. compat flags & model-ID mismatch) · Per-model thinking control · Other recipes (proxy/merge/secrets) · Verify (incl. the `--list-models` crash).

Doc: `packages/coding-agent/docs/models.md` (custom models via config) and `custom-provider.md` (custom providers via extension). Use `models.json` for anything that speaks a supported API; use an extension only when you need a non-standard API or OAuth flow.

## File location & reload

- Global: `~/.pi/agent/models.json`. The file is **re-read every time you open `/model`** — edit during a session, no restart.
- Credential resolution order: `--api-key` → `auth.json` → env var → `models.json` provider key.

## Supported `api` values

| `api` | For |
|-------|-----|
| `openai-completions` | OpenAI Chat Completions and the vast majority of local servers (llama.cpp, Ollama, LM Studio, vLLM, SGLang) |
| `openai-responses` | OpenAI Responses API |
| `anthropic-messages` | Anthropic and compatible proxies |
| `google-generative-ai` | Google Generative AI (needs explicit `baseUrl` for custom models) |

## Minimal local provider

For local servers, only `id` is required per model:

```json
{
  "providers": {
    "ollama": {
      "baseUrl": "http://localhost:11434/v1",
      "api": "openai-completions",
      "apiKey": "ollama",
      "models": [ { "id": "qwen2.5-coder:7b" } ]
    }
  }
}
```

`apiKey` is required even when the server ignores it — any non-empty string works.

## This machine: llama.cpp + Qwen3.6-27B-MTP

llama.cpp's server (`llama serve -hf <repo>`) exposes an OpenAI-compatible API at `http://127.0.0.1:8080/v1`. The current `~/.pi/agent/models.json` defines three providers pointed at it: `llamacpp`, `llamacpp-mtp`, `llamacpp-stable`. `settings.json` sets `defaultProvider: llamacpp`.

```json
{
  "providers": {
    "llamacpp-mtp": {
      "baseUrl": "http://127.0.0.1:8080/v1",
      "api": "openai-completions",
      "apiKey": "sk-none",
      "compat": {
        "supportsDeveloperRole": false,
        "supportsReasoningEffort": false,
        "thinkingFormat": "qwen-chat-template"
      },
      "models": [
        { "id": "qwen3.6-27b-mtp", "name": "Qwen3.6 27B MTP (local llama.cpp)",
          "reasoning": false, "input": ["text"],
          "contextWindow": 131072, "maxTokens": 4096 }
      ]
    }
  }
}
```

### Why these `compat` flags for a local Qwen/llama.cpp server
- `supportsDeveloperRole: false` — llama.cpp doesn't understand the `developer` role; pi sends the system prompt as a `system` message instead.
- `supportsReasoningEffort: false` — the server doesn't accept OpenAI's `reasoning_effort`.
- `thinkingFormat: "qwen-chat-template"` — for **local Qwen-compatible servers** that toggle thinking via `chat_template_kwargs.enable_thinking` (distinct from `qwen`, which is DashScope's top-level `enable_thinking`). Only meaningful when `reasoning: true`.
- Other useful local flags: `supportsUsageInStreaming: false` (server omits `stream_options.include_usage`), `maxTokensField: "max_tokens"` (vs `max_completion_tokens`), `requiresToolResultName: true`.

### ⚠️ Model-ID mismatch on this machine
`models.json` advertises ids like `unsloth/Qwen3.6-27B-GGUF:UD-Q4_K_XL` and `qwen3.6-27b-mtp`, but `/v1/models` actually serves `unsloth/Qwen3.6-27B-MTP-GGUF:BF16`. It still works because **llama.cpp ignores the request `model` field and routes to the single loaded model** — but the name pi shows is whatever you wrote in config, not what's loaded. Before trusting the label:

```bash
curl -s http://127.0.0.1:8080/v1/models | jq -r '.data[].id'
```

If you want the config to reflect reality, set the model `id` to the served id (or just treat the entries as friendly aliases and accept that the displayed name is cosmetic).

## Per-model thinking control

`thinkingLevelMap` maps pi's levels (`off,minimal,low,medium,high,xhigh`) to provider values; `null` hides a level. Example for a model that can't disable thinking: `"thinkingLevelMap": { "off": null }`.

## Other recipes

- **Override a built-in provider through a proxy** (keep its models): `{ "providers": { "anthropic": { "baseUrl": "https://proxy/v1" } } }`.
- **Merge custom models into a built-in provider**: include `models`; same-`id` replaces the built-in, new `id` is added.
- **Tweak one built-in model**: use `modelOverrides: { "<id>": { ... } }` (fields: name, reasoning, input, cost, contextWindow, maxTokens, headers, compat).
- **Secrets in keys/headers**: `"$ENV_VAR"`, `"${VAR}"`, or `"!command"` (runs at request time; `models.json` does *not* cache command output — wrap slow commands yourself). `"$$"`→`$`, `"$!"`→`!`.

## Verify what pi resolved

```bash
curl -s http://127.0.0.1:8080/v1/models | jq -r '.data[].id'         # what the server actually serves
jq -r '.providers | keys[]' ~/.pi/agent/models.json                  # providers pi will offer
pi --no-session --provider llamacpp-mtp --model qwen3.6-27b-mtp -p "say hi"   # true smoke test (verified working)
```

### ⚠️ `pi --list-models` is broken on this machine (pi 0.70.2)
`pi --list-models` throws `TypeError: Cannot read properties of undefined (reading 'toString')` in `formatTokenCount` whenever the result set is non-empty — every query I tried (`qwen`, `llamacpp`, `unsloth`, even the exact id `qwen3.6-27b-mtp`) crashes; only zero-match queries (e.g. `anthropic`) survive. Cause: a reachable model has an undefined `contextWindow`/`maxTokens` and `list-models.js` formats those for every row without guarding. The offender is the **`huggingface/pi-llama` package** (in `settings.json` → `packages`), not the local `models.json`. Filtering does **not** reliably avoid it (the fuzzy match still pulls in the bad package model). Workarounds, best first:
- Inspect models via `curl …/v1/models` and `jq` over `models.json` (above).
- Remove/disable the offending package: `pi remove huggingface/pi-llama` (or drop it from `settings.json` → `packages`).
- The interactive `/model` picker and `pi -p`/`--mode` runs are unaffected — only the `--list-models` formatter is buggy.
