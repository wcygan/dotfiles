# llama.cpp Reference

LLM inference in C/C++ with no external dependencies. Apple Silicon first-class via ARM NEON, Accelerate, and Metal.

**Source:** https://github.com/ggml-org/llama.cpp

## Install

```bash
# Homebrew (recommended)
brew install llama.cpp

# Build from source
git clone https://github.com/ggml-org/llama.cpp && cd llama.cpp
cmake -B build && cmake --build build --config Release -j 8
```

Metal is **enabled by default** on macOS. No extra flags needed.

## Key Binaries

### llama-cli — Interactive chat / completion

```bash
# Basic chat
llama-cli -m model.gguf

# From Hugging Face (auto-download)
llama-cli -hf ggml-org/gemma-3-1b-it-GGUF
llama-cli -hf ggml-org/GLM-4.7-Flash-GGUF:Q4_K_M

# Grammar-constrained output
llama-cli -m model.gguf -n 256 --grammar-file grammars/json.gbnf -p 'prompt'
```

### llama-server — OpenAI-compatible HTTP server

```bash
# Basic (127.0.0.1:8080, includes web UI)
llama-server -m model.gguf --port 8080

# From HF
llama-server -hf unsloth/gemma-4-26B-A4B-it-GGUF:UD-Q4_K_XL -c 65536

# Multi-user (4 parallel slots, 16K total context)
llama-server -m model.gguf -c 16384 -np 4

# Speculative decoding
llama-server -m model.gguf -md draft.gguf

# Embedding mode
llama-server -m model.gguf --embedding --pooling cls -ub 8192
```

### llama-bench — Benchmarking

```bash
llama-bench -m model.gguf
# Reports: pp512 (prefill t/s) and tg128 (generation t/s)
```

### llama-quantize

```bash
python3 convert_hf_to_gguf.py ./models/mymodel/
./llama-quantize input.gguf output.gguf Q4_K_M
./llama-quantize --imatrix imatrix.gguf input.gguf output.gguf Q4_K_M  # best quality
```

## Server API Endpoints

### OpenAI-Compatible

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/v1/models` | List loaded models |
| POST | `/v1/chat/completions` | Chat completions (streaming) |
| POST | `/v1/completions` | Text completions |
| POST | `/v1/embeddings` | Embeddings |
| POST | `/v1/responses` | OpenAI Responses API |

### Anthropic-Compatible

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/v1/messages` | Anthropic Messages API |

### Native

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/completion` | Raw completion |
| POST | `/tokenize` | Tokenize text |
| POST | `/detokenize` | Convert tokens to text |
| GET | `/metrics` | Prometheus metrics |
| GET/POST | `/lora-adapters` | Manage LoRA |

## GGUF Quantization Options

| Quant | Bits/Weight | Size (8B) | Quality |
|-------|-------------|-----------|---------|
| IQ2_XXS | 2.38 | 2.23 GiB | Aggressive |
| Q3_K_M | 4.00 | 3.74 GiB | Medium |
| **Q4_K_M** | **4.89** | **4.58 GiB** | **Recommended default** |
| Q5_K_M | 5.70 | 5.33 GiB | Higher quality |
| Q6_K | 6.56 | 6.14 GiB | Near-lossless |
| Q8_0 | 8.50 | 7.95 GiB | Barely quantized |
| F16 | 16.00 | 14.96 GiB | Full precision |

Use `--imatrix` for best quality on aggressive quants (Q2-Q3).

## GPU Offloading (-ngl)

```bash
-ngl 999     # all layers to Metal GPU
-ngl auto    # auto-detect (default)
-ngl 0       # CPU only
```

## Key Server Flags

| Flag | Default | Description |
|------|---------|-------------|
| `-m` | — | Model file path |
| `-hf` | — | HF repo (auto-download) |
| `-c` | 0 (from model) | Context size |
| `-ngl` | auto | GPU layers |
| `-np` | auto | Parallel slots |
| `-t` | auto | CPU threads |
| `-b` | 2048 | Logical batch size |
| `-fa` | auto | Flash attention |
| `-ctk` / `-ctv` | f16 | KV cache type |
| `--port` | 8080 | Listen port |
| `--host` | 127.0.0.1 | Listen address |
| `--api-key` | none | Auth |
| `-md` | — | Draft model (speculative) |

## Apple Silicon Tips

1. **Metal on by default** — no build flags needed
2. **Flash attention** (`-fa on`) — default auto, improves long-context throughput
3. **KV cache quantization**: `-ctk q8_0 -ctv q8_0` halves KV memory vs f16
4. **Q4_K_M is the sweet spot** for most models
5. **mmap on by default** — fast model loading via memory mapping
6. **mlock** (`--mlock`) — prevents OS from swapping model weights
7. **Parallel slots** eat context proportionally: `-c 16384 -np 4` = 4096 tokens/user
8. **MoE models**: use `-cmoe` to keep expert weights on CPU if needed
9. **Memory rule**: model GGUF size + KV cache = total memory needed
