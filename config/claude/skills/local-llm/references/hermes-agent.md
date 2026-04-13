# Hermes Agent Reference

NousResearch's autonomous AI agent framework. Supports local models via Ollama/custom endpoints.

**Source:** https://hermes-agent.nousresearch.com/docs/

## Install

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
hermes doctor   # verify
hermes version
```

Prerequisites: Git only. Installer handles uv, Python 3.11, Node.js v22, ripgrep, ffmpeg.

## Directory Structure

```
~/.hermes/
  config.yaml     # Primary settings
  .env            # API keys
  SOUL.md         # Agent identity (system prompt)
  memories/       # MEMORY.md + USER.md
  skills/         # Agent skills
  sessions/       # JSONL transcripts
  state.db        # SQLite: session metadata + FTS5
  cron/           # Scheduled jobs
  logs/           # Error and gateway logs
```

## Ollama / Local Model Setup

```yaml
# ~/.hermes/config.yaml
model:
  default: qwen3.5:27b
  provider: custom          # or "ollama" (alias)
  base_url: http://localhost:11434/v1
```

**Important:** If you set custom `num_ctx` in Ollama, set matching `context_length` in Hermes — Ollama's `/api/show` reports the model max, not effective `num_ctx`. Models must support at least 64K context.

Local endpoints get extended streaming timeouts (120s → 1800s). Override: `HERMES_STREAM_READ_TIMEOUT=1800` in `.env`.

## Configuration

**Precedence:** CLI flags > config.yaml > .env > defaults.

### Agent Behavior

```yaml
agent:
  max_turns: 60
  reasoning_effort: "medium"  # xhigh | high | medium | low | minimal | none
  verbose: false
```

### Context Compression

```yaml
compression:
  enabled: true
  threshold: 0.50
  target_ratio: 0.20
  protect_last_n: 20
  summary_model: "google/gemini-3-flash-preview"
```

### Memory

```yaml
memory:
  memory_enabled: true
  user_profile_enabled: true
  memory_char_limit: 2200
  user_char_limit: 1375
  nudge_interval: 10
  flush_min_turns: 6
```

### Delegation (Subagents)

```yaml
delegation:
  model: "google/gemini-3-flash-preview"
  provider: "openrouter"
  max_iterations: 50
  default_toolsets: ["terminal", "file", "web"]
```

### Model Aliases

```yaml
model_aliases:
  opus:
    model: claude-opus-4-6
    provider: anthropic
  qwen:
    model: "qwen3.5:397b"
    provider: custom
    base_url: "https://ollama.com/v1"
```

## Providers

`auto`, `openrouter`, `nous`, `anthropic`, `openai-codex`, `copilot`, `gemini`, `zai`, `kimi-coding`, `minimax`, `huggingface`, `custom` (aliases: `lmstudio`, `ollama`, `vllm`, `llamacpp`).

## Tool-Call Parsers

For local models that don't natively handle tool calls:

| Parser | Models |
|--------|--------|
| `hermes` | Hermes-family, Qwen (default) |
| `mistral` | Mistral models |
| `llama3_json` | Llama 3 |
| `qwen3_coder` | Qwen3 Coder |
| `deepseek_v3` | DeepSeek V3/V3.1 |
| `glm45` / `glm47` | GLM-4.5/4.7 |

The `--parser hermes` flag dramatically reduces tool-call parse failures on long autonomous runs.

## Key CLI Commands

| Command | Purpose |
|---------|---------|
| `hermes` | Start interactive chat |
| `hermes chat -q "prompt"` | One-shot query |
| `hermes model` | Select provider + model |
| `hermes setup` | Full configuration wizard |
| `hermes config edit` | Open config.yaml |
| `hermes config set KEY VAL` | Set a config value |
| `hermes config check` | Validate config |
| `hermes doctor` | Diagnose issues |
| `hermes tools` | Configure toolsets |
| `hermes sessions list/export/delete` | Manage sessions |
| `hermes skills search/install/list` | Manage skills |
| `hermes cron create/list/run` | Scheduled jobs |
| `hermes logs -f agent` | Tail logs |
| `hermes profile create/use/list` | Multiple instances |
| `hermes update` | Update |

## In-Session Commands

`/model`, `/personality`, `/tools`, `/skills`, `/help`, `/save`, `/title`, `/new`, `/reset`, `/compress`, `/usage`, `/verbose`, `/voice on`, `/background <prompt>`

`Alt+Enter` for multi-line. `Ctrl+C` to interrupt. `hermes -c` to resume last session.

## Session Management

```bash
hermes --continue              # resume last
hermes -c "my project"         # resume by name
hermes --resume <session_id>   # resume by ID
hermes sessions list
hermes sessions export backup.jsonl
hermes sessions prune --older-than 30
```

## SOUL.md

`~/.hermes/SOUL.md` — agent identity (system prompt slot #1). Max 20,000 chars.

Include: tone, directness, style, uncertainty handling.
Exclude: project-specific rules (use `.hermes.md` or `AGENTS.md`).

Context file priority: `.hermes.md` > `AGENTS.md` > `CLAUDE.md` > `.cursorrules`

## Toolsets

Presets: `hermes-cli` (all), `hermes-telegram`, `hermes-discord`, `hermes-whatsapp`, `hermes-slack`.

Individual: `web`, `terminal`, `file`, `browser`, `vision`, `image_gen`, `skills`, `todo`, `memory`, `session_search`, `tts`, `cronjob`.

Override per-session: `hermes chat --toolsets terminal,web,file`
