# Model Selection Reference

Detailed model comparison for M5 Max 128GB. See also: hardware.md for memory constraints.

## ⭐ Preferred Default: Qwen3.6-35B-A3B

**35B total / 3B active MoE, multimodal (text + vision), 256K native context (1M via YaRN).** This is the preferred daily-driver model on this hardware for four reasons:

1. **Lossless is affordable.** BF16 weights are only 69.4 GB — you can run the flagship at full precision and still have ~50 GB free for a 256K KV cache plus OS and apps. Almost no other model in this intelligence tier fits at BF16 on consumer Apple Silicon.
2. **MoE speed.** Only 3B active params per token → generation speed in the Qwen3-Coder-30B-A3B ballpark (~100-130 t/s at Q5/Q4, ~50-70 t/s at BF16 — bandwidth-bound).
3. **Multimodal.** Includes vision (mmproj files), unlike the 30B-A3B class it supersedes.
4. **Agentic-friendly.** Supports `/think` and `/no_think` modes; default `enable_thinking:true` can be disabled for tool loops.

**Gotchas**
- **Ollama is currently broken** for this model — mmproj vision files aren't handled. Use llama.cpp (llama-server) or MLX directly.
- **Thinking mode on by default** — pass `--chat-template-kwargs '{"enable_thinking":false}'` for agentic/coding use.
- If you see gibberish at long context, add `--cache-type-k bf16 --cache-type-v bf16`.

**Quant picks (Unsloth Dynamic 2.0 GGUFs)**

| Quant | Size | Use when |
|-------|------|----------|
| **BF16** | 69.4 GB | Flagship lossless quality; room for 256K ctx; ~50-70 t/s |
| **UD-Q5_K_XL** | 26.6 GB | Speed + quality balance, dual-model setups, 1M-token YaRN context |
| UD-Q4_K_XL | 22.4 GB | Maximum speed / minimum footprint |
| UD-IQ4_XS | 17.7 GB | Edge case — co-load with a large second model |

**Sampling**
- Thinking mode: `--temp 0.6 --top-p 0.95 --top-k 20 --min-p 0.0`
- Non-thinking: `--temp 0.7 --top-p 0.8 --top-k 20 --min-p 0.0`

## Tier 1: Maximum Power (Push the Limits)

| Model | Total | Active | Type | Quant | Size | t/s | Notes |
|-------|-------|--------|------|-------|------|-----|-------|
| **Qwen3-235B-A22B** | 235B | 22B | MoE | Q4 | ~124 GB | 15-25 | The king. Largest that fits via MLX |
| **Devstral 2 123B** | 123B | 123B | Dense | Q4_K_M | ~73 GB | 10-16 | Top coding (76.2% SWE-bench) |
| **Mistral Large 2 123B** | 123B | 123B | Dense | Q4_K_M | ~73 GB | 10-16 | Strong general reasoning |
| **Llama 4 Scout** | 109B | 17B | MoE | Q4 | ~55 GB | 30-45 | 10M context, multimodal |
| **GLM-4.5 Air 106B** | 106B | ~106B | Dense | Q4_K_M | ~63 GB | 15-20 | Strong general, 128K context |

## Tier 2: High Power, Great Performance (Daily Drivers)

| Model | Total | Active | Type | Quant | Size | t/s | Notes |
|-------|-------|--------|------|-------|------|-----|-------|
| **Qwen3-72B** | 72B | 72B | Dense | Q4_K_M | ~42 GB | 18-25 | Excellent general reasoning |
| **Llama 3.3 70B** | 70B | 70B | Dense | Q6_K | ~55 GB | 18-25 | Battle-tested, Q8 (~75 GB) feasible |
| **Llama 4 Scout** | 109B | 17B | MoE | Q8 | ~100 GB | 25-35 | Better quality at Q8 |

## Tier 3: Sweet Spot for Developers (Fast + Smart)

| Model | Total | Active | Type | Quant | Size | t/s | Notes |
|-------|-------|--------|------|-------|------|-----|-------|
| **Qwen3-Coder 30B-A3B** | 30B | 3B | MoE | Q8 | ~32 GB | 100-134 | Best coding MoE, feels instant |
| **GLM-4.7-Flash** | ~30B | ~3.8B | MoE | Q8 | ~38 GB | 80-100 | #1 coding index (25.9), community fav |
| **Gemma 4 31B Dense** | 30.7B | 30.7B | Dense | Q8 | ~33 GB | 25-35 | Strong reasoning, 256K ctx, Apache 2.0 |
| **Devstral Small 2 (24B)** | 24B | 24B | Dense | Q8 | ~26 GB | 35-45 | 68% SWE-bench Verified |
| **Gemma 4 26B MoE** | 25.2B | 3.8B | MoE | Q8 | ~27 GB | 60-100+ | Speed demon, perfect for autocomplete |

## Tier 4: Vision / Multimodal

| Model | Total | Active | Quant | Size | t/s | Vision |
|-------|-------|--------|-------|------|-----|--------|
| **Gemma 4 31B Dense** | 30.7B | 30.7B | Q8 | ~39 GB | 25-35 | Text + Image |
| **Llama 4 Scout** | 109B | 17B | Q4 | ~62 GB | 30-45 | Text + Image + Video, 10M ctx |
| **Qwen2.5-VL-72B** | 72B | 72B | Q4 | ~50 GB | 18-25 | Strong vision-language |
| **Gemma 4 E4B** | ~8B | 4.5B | Q8 | ~10 GB | 100+ | Edge-class, ultra-fast |

## Top 5 Picks (Summary)

1. **⭐ Qwen3.6-35B-A3B (BF16 or UD-Q5_K_XL)** — Preferred daily driver. 35B/3B MoE, vision, 256K ctx. BF16 fits losslessly (69 GB). ~50-130 t/s depending on quant
2. **Qwen3-235B-A22B (Q4, MLX)** — Most powerful that fits. Frontier knowledge, 22B active. ~15-25 t/s
3. **GLM-4.7-Flash (Q8)** — Best pure-coding model. ~80-100 t/s. Excellent tool calling
4. **Devstral 2 123B (Q4_K_M)** — Best SWE-bench (76.2%). ~10-16 t/s. Serious engineering tasks
5. **Llama 4 Scout (Q4-Q8)** — Best multimodal at scale. 109B MoE, 17B active. ~30-45 t/s. 10M context

## What Does NOT Fit (or Fits Poorly)

| Model | Params | Why Not |
|-------|--------|---------|
| DeepSeek V3.2 / R1 (671B) | 671B | ~131GB at 1.58-bit, ~3-5 t/s. Unusable |
| Llama 4 Maverick (402B) | 402B | ~122GB at 1.78-bit. Quality degraded |
| Any model >235B MoE at Q4+ | Varies | Memory ceiling reached |

## Recommended Setups

### Fast + Quality Dual Model (~77 GB)

| Role | Model | Quant | Memory |
|------|-------|-------|--------|
| Fast coding | GLM-4.7-Flash | Q8 | ~38 GB |
| Deep reasoning | Gemma 4 31B Dense | Q8 | ~39 GB |

### Maximum Variety (~90 GB)

| Role | Model | Quant | Memory |
|------|-------|-------|--------|
| Speed | Qwen3-Coder 30B-A3B | Q8 | ~38 GB |
| Quality | Llama 3.3 70B | Q4_K_M | ~42 GB |
| Vision | Gemma 4 E4B | Q8 | ~10 GB |

## Sampling Parameters (Qwen3.5 Reference)

| Mode | temperature | top_p | top_k | presence_penalty |
|------|-------------|-------|-------|-----------------|
| Thinking (/think) | 1.0 | 0.95 | 20 | 1.5 |
| Coding | 0.6 | 0.95 | 20 | — |
| Instruct (/no_think) | 0.7 | 0.8 | 20 | 1.5 |

## Sources

- ideas/m5-max-128gb-most-powerful-local-models.md
- ideas/macbook-pro-m5-max-128gb-local-llms.md
- ideas/mlx-qwen35-35b-a3b-setup.md
