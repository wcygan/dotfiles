# MLX-LM Reference

Apple's Python package for running and fine-tuning LLMs on Apple Silicon via MLX.

**Source:** https://github.com/ml-explore/mlx-lm

## Install

```bash
pip install mlx-lm            # base
pip install "mlx-lm[train]"   # adds LoRA/fine-tuning
uv tool install mlx-lm        # isolated, always on PATH
```

Requires Apple Silicon + macOS. macOS 15+ recommended for large models.

## CLI Commands

### mlx_lm.generate

```bash
mlx_lm.generate --model mlx-community/Qwen3.5-35B-A3B-4bit \
  --prompt "Write a Rust function" \
  --max-tokens 1024 --temp 0.6 --top-p 0.95
```

Key flags: `--model`, `--prompt`, `--max-tokens`, `--temp`, `--top-p`, `--max-kv-size N`, `--prompt-cache-file`, `--adapter-path`, `--trust-remote-code`.

Default model: `mlx-community/Llama-3.2-3B-Instruct-4bit`.

### mlx_lm.chat

```bash
mlx_lm.chat --model mlx-community/Qwen3.5-35B-A3B-4bit
```

Interactive REPL with preserved context. Same flags as generate.

### mlx_lm.server

```bash
mlx_lm.server --model mlx-community/Qwen3.5-35B-A3B-4bit --port 8080
```

OpenAI-compatible HTTP server. Endpoints:

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/v1/chat/completions` | Chat (streaming supported) |
| GET | `/v1/models` | List available models |

Request fields: `messages`, `max_tokens` (default 512), `stream`, `temperature`, `top_p`, `top_k`, `min_p`, `repetition_penalty`, `presence_penalty`, `frequency_penalty`, `logit_bias`, `logprobs`, `stop`, `model` (hot-swap), `adapters`, `draft_model`, `num_draft_tokens`.

### mlx_lm.convert

```bash
mlx_lm.convert --model mistralai/Mistral-7B-Instruct-v0.3 -q
mlx_lm.convert --model <model> -q --upload-repo mlx-community/my-4bit
```

Don't run on models already in `mlx-community/` — they're already MLX-format.

### mlx_lm.lora

```bash
mlx_lm.lora --model <model> --train --data <dir> --iters 600
```

Fine-tune types: `lora`, `dora`, `full`. Data: JSONL (`train.jsonl`, optional `valid.jsonl`).
Formats: chat (`{"messages": [...]}`), completion (`{"prompt": "...", "completion": "..."}`), raw (`{"text": "..."}`).

### mlx_lm.fuse

```bash
mlx_lm.fuse --model <model>                    # merge adapters → fused_model/
mlx_lm.fuse --model <model> --export-gguf       # GGUF export
mlx_lm.fuse --model <model> --upload-repo <repo> # upload
```

### mlx_lm.cache_prompt

```bash
cat prompt.txt | mlx_lm.cache_prompt --model <model> --prompt - --prompt-cache-file cached.safetensors
mlx_lm.generate --prompt-cache-file cached.safetensors --prompt "Follow-up"
```

Pre-computes KV cache for shared long contexts.

## Quantization Methods

| Command | Method | Notes |
|---------|--------|-------|
| `mlx_lm.convert -q` | Naive round-to-nearest | Fast, baseline quality |
| `mlx_lm.dwq` | Distilled Weight Quantization | Best quality, slowest |
| `mlx_lm.awq` | Activation-aware WQ | Scales/clips weights pre-quant |
| `mlx_lm.gptq` | GPTQ | Minimizes per-layer squared error |
| `mlx_lm.dynamic_quant` | Dynamic mixed-precision | Fastest learned method |

Mixed quant recipes: `mixed_2_6`, `mixed_3_4`, `mixed_3_6`, `mixed_4_6`.

## Python API

```python
from mlx_lm import load, generate, stream_generate

model, tokenizer = load("mlx-community/Qwen3.5-35B-A3B-4bit")

# One-shot
prompt = tokenizer.apply_chat_template(
    [{"role": "user", "content": "Hello"}],
    add_generation_prompt=True,
)
text = generate(model, tokenizer, prompt=prompt, verbose=True, max_tokens=512)

# Streaming
for r in stream_generate(model, tokenizer, prompt, max_tokens=512):
    print(r.text, end="", flush=True)
```

Custom `sampler=` and `logits_processors=` supported via `mlx_lm.sample_utils`.

## Performance Tips

1. **Memory wiring (macOS 15+):** `sudo sysctl iogpu.wired_limit_mb=N` where N > model size in MB
2. **Rotating KV cache:** `--max-kv-size 4096` bounds memory for long generations
3. **Prompt caching:** Use `mlx_lm.cache_prompt` for shared long contexts
4. **4-bit is the sweet spot.** DWQ gives best quality for 2-4 bit. Dynamic quant is fastest to produce
5. **Speculative decoding:** Server supports `draft_model` + `num_draft_tokens`
6. **Memory rule of thumb:** ~0.6 GB per 1B params at 4-bit

## Supported Architectures

100+ including: Llama (1-4), Mistral, Mixtral, Qwen (2/3/3.5/MoE), Gemma (1-4), DeepSeek (v1-v3), Phi (1-3), GPT-2, GPT-NeoX, StarCoder2, OLMo, Mamba, Cohere, GLM (4/4-MoE), Granite, Falcon-H1, and many more.

Models on HuggingFace under `mlx-community/` namespace.

## Gotchas

- macOS 14 and below degrade badly once model exceeds RAM
- Forgetting `tokenizer.apply_chat_template` produces bad output on instruct models
- Some models need `--trust-remote-code` (e.g. Qwen)
- LoRA requires the `[train]` extra
- Default adapter output path is `adapters/`
