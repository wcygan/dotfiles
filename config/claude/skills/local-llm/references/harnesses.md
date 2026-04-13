# Coding Agent Harness Reference

A "harness" is the agent scaffolding around a model — tool-calling loop, prompt templates, file editing, diff application, recovery. **When local tool calls fail, ~80% of the time it's the harness, not the model.**

## What a Harness Does

1. Builds system prompt (tool descriptions, file context, repo map)
2. Parses streamed output for tool calls (JSON function-calling, XML tags, pythonic)
3. Executes tools (shell, edit, read, grep) and feeds results back
4. Manages loop, context trimming, recovery from bad output
5. Applies diffs to filesystem

## Landscape

### OpenCode (Recommended Daily Driver)

```bash
ollama launch opencode --model gemma4:26b
```

Config (`~/.config/opencode/opencode.json`):
```json
{
  "provider": {
    "ollama": {
      "base_url": "http://localhost:11434/v1",
      "models": {
        "gemma4:31b": { "context_length": 65536 }
      }
    }
  }
}
```

- First-class local support, 75+ providers
- MLX lead (Awni Hannun) publishes reference config
- GitHub Copilot fallback via `/connect`

### Claude Code (Best UX)

```bash
ollama launch claude --model gemma4:31b
```

Manual setup:
```bash
export ANTHROPIC_BASE_URL="http://localhost:11434"
export ANTHROPIC_AUTH_TOKEN="ollama"
export ANTHROPIC_API_KEY=""
claude --model gemma4:31b
```

Persistent (`~/.claude/settings.json`):
```json
{
  "env": {
    "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1",
    "ANTHROPIC_AUTH_TOKEN": "ollama",
    "ANTHROPIC_API_KEY": "",
    "ANTHROPIC_BASE_URL": "http://localhost:11434"
  },
  "model": "gemma4:31b"
}
```

VS Code: add to `claudeCode.environmentVariables` in settings.json. **Requires full VS Code restart.**

Onboarding bypass (`~/.claude.json`):
```json
{"hasCompletedOnboarding": true, "primaryApiKey": "sk-dummy-key"}
```

### Hermes Agent (Long Autonomous Runs)

```bash
hermes model  # select ollama interactively
# or in config.yaml:
# model:
#   default: qwen3.5:27b
#   provider: custom
#   base_url: http://localhost:11434/v1
```

- Per-model tool-call parsers (`--parser hermes`) dramatically reduce parse failures
- Best for unattended, long-running sessions

### Aider (Git-Native)

```bash
aider --model ollama_chat/gemma4:31b
aider --model openai/gemma4:31b --openai-api-base http://localhost:11434/v1 --openai-api-key ollama
```

- Auto-commits changes with meaningful messages
- Understands repo structure, multi-file edits
- Less autonomous — you're the driver

### Codex CLI

Config (`~/.codex/config.toml`):
```toml
[model_providers.mlx]
name = "MLX"
base_url = "http://localhost:8080/v1"
wire_api = "chat"

[profiles.qwen]
model = "mlx-community/Qwen3.5-35B-A3B-4bit"
model_provider = "mlx"
```

Run: `codex --profile qwen`

### Cline (VS Code Extension)

1. Install "Cline" from VS Code Marketplace
2. Settings → "Ollama" as provider
3. Base URL: `http://localhost:11434`
4. Select model

Plan mode analyzes without modifying; Act mode executes with approval at each step.

### Continue.dev (VS Code Extension)

Config (`~/.continue/config.yaml`):
```yaml
models:
  - name: Gemma 4 31B (Chat)
    provider: ollama
    model: gemma4:31b
    roles: [chat, edit, apply]
  - name: Gemma 4 26B MoE (Autocomplete)
    provider: ollama
    model: gemma4:26b
    roles: [autocomplete]
```

Multi-model strategy: fast 26B MoE for autocomplete, 31B Dense for chat/reasoning.

## Decision Framework

| Need | Use |
|------|-----|
| CC UX with local model | Claude Code + `ollama launch claude` |
| Most flexible agentic CLI | **OpenCode** |
| Max tool-call reliability | **Hermes Agent** with `--parser hermes` |
| OpenAI CLI, known config | Codex CLI with `--oss` |
| Terminal + git, you're the driver | Aider |
| Embedded in editor | Continue.dev |

## Best Practices

- **Context window**: Set `num_ctx 65536` in Ollama Modelfile (default 4096 is unusable for agents)
- **`/no_think` for agentic loops** — thinking mode for planning, no_think for execution
- **Strip `<think>` blocks from history** — OpenCode and Hermes do this; simpler wrappers don't
- **One harness per project** while learning quirks
- **Define per-model profiles** so you can swap Qwen/Gemma/GLM without re-editing config

## Sources

- ideas/llm-harnesses-for-local-models.md
- ideas/local-llm-coding-agents.md
