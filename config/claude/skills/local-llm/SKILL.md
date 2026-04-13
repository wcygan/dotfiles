---
name: local-llm
description: >
  Manage and run local LLMs on Apple Silicon (M5 Max 128GB MacBook Pro). Start/stop inference servers,
  pull and configure models, benchmark performance, set up coding agent harnesses (Ollama, MLX-LM,
  llama.cpp, Hermes Agent, OpenCode, Aider), troubleshoot inference issues, and optimize for speed
  or quality. Auto-loads when working with local model inference, Ollama commands, MLX server,
  llama.cpp, GGUF quantization, model selection, coding agents with local models, or Apple Silicon
  LLM performance. Use when starting a local model, picking a model for hardware, configuring a
  coding agent harness, benchmarking inference, or troubleshooting local LLM issues.
  Keywords: ollama, mlx, mlx-lm, llama.cpp, gguf, local llm, inference, quantization, apple silicon,
  m5 max, hermes agent, opencode, aider, coding agent, model selection, benchmark, moe, prefill,
  token generation, unified memory, metal, neural accelerator.
---

# Local LLM Management — M5 Max 128GB

Manage local LLM inference on Apple Silicon. Covers model selection, server management, harness configuration, and performance optimization.

## Hardware Context

- **M5 Max 128GB**: 614 GB/s bandwidth, 40-core GPU with Neural Accelerators, ~90-100 GB usable for models
- LLM inference is **memory-bandwidth-bound** — MoE models are the sweet spot (small active params, full knowledge)
- Neural Accelerators deliver 3.3-4x faster prefill vs M4 — long-context agent workflows finally work

## Quick Commands

```bash
# Start a model with Ollama (MLX backend auto-enabled on Apple Silicon 32GB+)
ollama run qwen3.5:27b
ollama run glm-4.7-flash

# Launch a coding agent with local model
ollama launch claude --model gemma4:31b
ollama launch opencode --model gemma4:26b

# Start MLX server (fastest, OpenAI-compatible)
mlx_lm.server --model mlx-community/Qwen3.5-35B-A3B-4bit --port 8080

# Start llama.cpp server (max quant control)
llama-server -hf unsloth/gemma-4-26B-A4B-it-GGUF:UD-Q4_K_XL -c 65536 --port 8080

# Check what's running
ollama ps
curl -s http://localhost:11434/api/ps | jq
```

## Model Selection

| Use Case | Model | Quant | Size | Speed | Notes |
|----------|-------|-------|------|-------|-------|
| **Fast coding** | GLM-4.7-Flash | Q8 | ~38 GB | ~80-100 t/s | Best coding index, excellent tool calling |
| **Fast coding** | Qwen3-Coder 30B-A3B | Q8 | ~32 GB | ~100-134 t/s | Purpose-built coding MoE, feels instant |
| **Quality coding** | Gemma 4 31B Dense | Q8 | ~39 GB | ~25-35 t/s | Strong reasoning, 256K context |
| **Quality coding** | Devstral 2 123B | Q4_K_M | ~73 GB | ~10-16 t/s | 76.2% SWE-bench |
| **General reasoning** | Qwen3-72B | Q4_K_M | ~45 GB | ~18-25 t/s | 70B-class workhorse |
| **Max intelligence** | Qwen3-235B-A22B | Q4 | ~124 GB | ~15-25 t/s | Frontier-class, barely fits |
| **Multimodal** | Llama 4 Scout | Q4-Q8 | ~55-100 GB | ~30-45 t/s | 10M context, vision+text |

**Dual-model daily driver setup** (~77 GB, 41 GB free):
- GLM-4.7-Flash Q8 for fast agentic work
- Gemma 4 31B Dense Q8 for hard reasoning

## Inference Engine Decision

| Engine | Best For | Speed vs MLX |
|--------|----------|-------------|
| **MLX / mlx-lm** | Maximum speed on Apple Silicon | Baseline (fastest) |
| **Ollama (MLX backend)** | Easiest setup, agent integration | ~same (uses MLX since 0.19) |
| **llama.cpp** | Max quant control, GGUF ecosystem | ~20-30% slower |

**Default to Ollama** for agent workflows. Use raw MLX for max throughput. Use llama.cpp for exotic quants or models not yet in MLX format.

## Coding Agent Harnesses

| Harness | Setup | Best For |
|---------|-------|----------|
| **OpenCode** | `ollama launch opencode --model <model>` | Daily driver, 75+ providers |
| **Claude Code** | `ollama launch claude --model <model>` | Best UX, native Ollama support |
| **Hermes Agent** | `hermes model` → select ollama | Long autonomous runs, per-model tool parsers |
| **Aider** | `aider --model ollama_chat/<model>` | Git-native pair programming |
| **Cline** | VS Code extension → Ollama provider | Plan/act workflow in VS Code |
| **Continue.dev** | VS Code extension → config.yaml | Autocomplete + chat sidebar |

## Performance Tuning

- **Context window**: Ollama defaults to 4096. Create a Modelfile with `num_ctx 65536` for agentic work
- **Thinking mode**: `/set nothink` in Ollama for faster responses in agent loops
- **Strip `<think>` blocks** from multi-turn history — bloats context, hurts quality
- **MoE loads all experts into RAM** regardless of active params (4-bit Qwen3.5-35B-A3B = ~20 GB resident)
- **Temperature**: 0.6 for coding, 0.7 for instruct, 1.0 for thinking mode

## Quantization Quick Reference

| Quant | Quality Loss | When to Use |
|-------|-------------|-------------|
| Q8_0 | Negligible (<1%) | Default for 30B-class models |
| Q6_K | Very small (~1-2%) | Sweet spot for 70B models |
| Q4_K_M | Moderate (~3-5%) | Standard for 70B+, best for headroom |
| Q3_K_L | Noticeable (~5-8%) | Budget 100B+ models |
| 1.58-2 bit | Significant (~10-15%) | Extreme: 400B+ MoE only |

**Rule**: Use the highest quant that fits with room for your desired context length.

## Troubleshooting

- **Slow prefill?** Check Activity Monitor for memory pressure / thermal throttling
- **Tool calls failing?** Usually the harness, not the model — try a different harness
- **Model not found in Ollama?** `ollama list` to verify, `ollama pull <model>` to download
- **KV cache invalidation in Claude Code?** Set `CLAUDE_CODE_ATTRIBUTION_HEADER=0`
- **< 80 t/s on MoE models?** Something is wrong — check for other Metal consumers

## Reference Files

Detailed docs for each inference engine, harness, and hardware analysis:

References: [ollama-api](references/ollama-api.md)
References: [mlx-lm](references/mlx-lm.md)
References: [llama-cpp](references/llama-cpp.md)
References: [hermes-agent](references/hermes-agent.md)
References: [hardware](references/hardware.md)
References: [harnesses](references/harnesses.md)
References: [models](references/models.md)
