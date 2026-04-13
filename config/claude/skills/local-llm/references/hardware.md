# M5 Max 128GB Hardware Reference

## Specs

| Feature | M5 Max | Impact |
|---|---|---|
| Memory bandwidth | 614 GB/s | Token generation speed (bandwidth-bound) |
| Neural Accelerators | 40 (1/GPU core) | 3.3-4x faster prefill vs M4 |
| GPU cores | 40 | Metal compute |
| Unified memory | 128 GB | ~90-100 GB usable for models |
| SSD throughput | up to 14.5 GB/s | Enables SSD-streamed MoE |
| CPU cores | 18 (6P+12E) | "World's fastest CPU core" |

## Why It Matters for LLMs

- **Unified memory** = full 128GB available to GPU, no PCIe bottleneck, no CPU-to-GPU copy
- **614 GB/s** determines generation speed (LLM inference is memory-bandwidth-bound)
- **Neural Accelerators** deliver 3.3-4x faster TTFT — long-context agent workflows finally responsive
- **Usable memory** after macOS + browser + editor: ~90-100 GB

## Key Tradeoff

Enormous *capacity* (128GB) but moderate *bandwidth* (614 GB/s):
- **Dense models**: generation speed limited by bandwidth. 70B at ~40GB → ~20-30 t/s
- **MoE models**: only active params need compute per token. 400B MoE with 17B active → generates like 17B dense. **MoE is the sweet spot**

## What 128GB Actually Runs

| Model | Quant | Size | Prefill (t/s) | Generation (t/s) |
|---|---|---|---|---|
| Qwen 3.5 35B-A3B MLX | 4-bit | ~20 GB | ~1000 | 112-130 |
| Gemma 4 26B MoE | Q4_K_M | ~20 GB | 800-1000 | 80-100+ |
| Gemma 4 31B Dense | Q8_0 | ~39 GB | 500-700 | 25-35 |
| Gemma 4 31B Dense | Q4_K_M | ~26 GB | 700-900 | 35-45 |
| Qwen 3.5 72B | Q4_K_M | ~45 GB | 300-500 | 10-15 |
| Qwen3 235B-A22B | Q4 | ~130 GB | painful | 5-10 |
| Kimi K2.5 (1T MoE) | 1.8-bit SSD | ~230 GB disk | — | 7.5 |

## Multi-Model Setups

| Setup | Memory | Headroom |
|-------|--------|----------|
| GLM-4.7-Flash Q8 + Gemma 4 31B Q8 | ~77 GB | ~41 GB free |
| Qwen3-Coder 30B-A3B Q8 + Llama 3.3 70B Q4 + Gemma 4 E4B Q8 | ~90 GB | ~28 GB |

## Where It Excels

- Portable offline/private inference (only laptop where 70B runs at interactive speed)
- Context-switching between dev work and LLM inference (unified memory, no VRAM juggling)
- Coding agents with privacy constraints (Gemma 4 31B Q8 + Aider/Claude Code/OpenCode via Ollama)

## Honest Tradeoffs

1. **Battery**: 60-90W under inference → 60-90 min unplugged
2. **Desktop GPUs faster for small models**: RTX 4090 = 1008 GB/s, RTX 5090 ≈ 1.8 TB/s
3. **Mac Studio M3 Ultra 512GB** dominates high end: 819 GB/s, 4x memory ceiling
4. **128GB ≠ 128GB for models**: 90-100 GB usable after OS + apps
5. **Cloud API economics**: MBP cost ≈ 2-3 years of Claude Pro + API credits

## Quantization Rule of Thumb

Use the highest quant that fits with room for context:
- **Q8** for 30B-class models
- **Q4-Q6** for 70B models
- **Q4 or lower** for 100B+ models
- **~0.6 GB per 1B params** at 4-bit

## Sources

- ideas/macbook-pro-m5-max-128gb-local-llms.md
- ideas/m5-max-128gb-most-powerful-local-models.md
