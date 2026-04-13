# Ollama API Reference

**Base URL:** `http://localhost:11434`

All endpoints accept/return JSON. Streaming endpoints default to `stream: true` (NDJSON).

## Generate Completion

**`POST /api/generate`**

| Field | Type | Required | Description |
|---|---|---|---|
| `model` | string | yes | Model name |
| `prompt` | string | no | Input text |
| `suffix` | string | no | Fill-in-the-middle suffix |
| `images` | string[] | no | Base64-encoded images |
| `format` | string/object | no | `"json"` or a JSON schema object |
| `system` | string | no | System prompt |
| `stream` | boolean | no | Stream partial responses (default: true) |
| `think` | boolean/string | no | Enable thinking (`true`, `"high"`, `"medium"`, `"low"`) |
| `raw` | boolean | no | Skip prompt templating |
| `keep_alive` | string/number | no | How long to keep model loaded (e.g. `"5m"`, `0` to unload) |
| `options` | object | no | Runtime parameters (see below) |

**Response fields:** `model`, `created_at`, `response`, `thinking`, `done`, `done_reason`, `total_duration`, `load_duration`, `prompt_eval_count`, `prompt_eval_duration`, `eval_count`, `eval_duration` (durations in nanoseconds).

## Chat

**`POST /api/chat`** — Multi-turn conversation.

| Field | Type | Required | Description |
|---|---|---|---|
| `model` | string | yes | Model name |
| `messages` | array | yes | `[{role, content, images?, tool_calls?}]` |
| `stream` | boolean | no | Default: true |
| `format` | string/object | no | `"json"` or JSON schema |
| `tools` | array | no | Function/tool definitions |
| `think` | boolean/string | no | Enable thinking output |
| `keep_alive` | string | no | Model keep-alive duration |
| `options` | object | no | Runtime parameters |

Roles: `system`, `user`, `assistant`, `tool`.

## Embeddings

**`POST /api/embed`**

| Field | Type | Required | Description |
|---|---|---|---|
| `model` | string | yes | Embedding model name |
| `input` | string/string[] | yes | Text(s) to embed |
| `truncate` | boolean | no | Truncate if exceeding context (default: true) |
| `dimensions` | integer | no | Desired embedding dimensionality |

**Response:** `{ "embeddings": [[...]], "total_duration": ..., "load_duration": ..., "prompt_eval_count": ... }`

## Model Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET /api/tags` | List local models | Returns `{ "models": [...] }` with name, size, digest, details |
| `POST /api/show` | Show model details | `{ "model": "name", "verbose": true }` → parameters, license, template, capabilities |
| `POST /api/pull` | Download model | `{ "model": "name" }` — streams progress |
| `POST /api/push` | Upload model | `{ "model": "user/name" }` |
| `POST /api/create` | Create/derive model | `{ "model": "name", "from": "base", "system": "...", "parameters": {...} }` |
| `POST /api/copy` | Duplicate model | `{ "source": "a", "destination": "b" }` |
| `DELETE /api/delete` | Remove model | `{ "model": "name" }` |

## Running Models

**`GET /api/ps`** — Show currently loaded models.

Response includes: `name`, `model`, `size`, `digest`, `details`, `expires_at`, `size_vram`, `context_length`.

## Runtime Options

Passed in the `options` object:

| Parameter | Type | Description |
|-----------|------|-------------|
| `seed` | int | Reproducible output |
| `temperature` | float | Randomness |
| `top_k` | int | Limit to K most likely tokens |
| `top_p` | float | Nucleus sampling |
| `min_p` | float | Minimum probability threshold |
| `stop` | string/array | Stop sequence(s) |
| `num_ctx` | int | Context window size (tokens) |
| `num_predict` | int | Max tokens to generate |

## Thinking Mode

Enabled by default for supported models. Binary toggle (on/off).

```bash
# CLI
ollama run qwen3.5:27b --think=false
ollama run qwen3.5:27b --think

# In-session
/set nothink
/set think

# API
{"model": "qwen3.5:27b", "messages": [...], "think": false}
```

`--think` only works with `ollama run`, not `ollama launch`. Use `/set nothink` inside launch sessions.

## MLX Backend (0.19+)

Automatically used on Apple Silicon Macs with 32GB+ unified memory. No config needed.

Performance on Qwen3.5-35B-A3B:

| Metric | Ollama 0.18 | Ollama 0.19 (MLX) |
|--------|------------|-------------------|
| Prefill | 1,154 t/s | 1,810 t/s (~1.6x) |
| Decode | 58 t/s | 112 t/s (~1.9x) |

## Coding Agent Integration

```bash
# Zero-config agent launch
ollama launch claude --model gemma4:31b
ollama launch opencode --model gemma4:26b

# Manual env vars for Claude Code
export ANTHROPIC_BASE_URL="http://localhost:11434"
export ANTHROPIC_AUTH_TOKEN="ollama"
export ANTHROPIC_API_KEY=""
claude --model gemma4:31b
```

## Error Codes

| Status | Meaning |
|--------|---------|
| 200 | Success |
| 400 | Bad request |
| 404 | Model not found |
| 429 | Rate limited |
| 500 | Internal error |

## Version

**`GET /api/version`** → `{ "version": "0.19.x" }`

## Source

- Docs: https://docs.ollama.com/api/introduction
- MLX blog: https://ollama.com/blog/mlx
