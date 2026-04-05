# Features — Routing

Base: `https://hermes-agent.nousresearch.com`. 25+ feature pages live under `/docs/user-guide/features/`. Load this file first, route the user's symptom to a single page, then WebFetch.

If the user is **orienting** (just wants to know what exists), fetch `/docs/user-guide/features/overview` and summarize.

## Grouped by theme

### Core execution
| Symptom | URL |
|---|---|
| Tools, toolsets, web/terminal/file tool groups | `/docs/user-guide/features/tools` |
| Skills system (progressive disclosure, preloading with `-s`) | `/docs/user-guide/features/skills` |
| Memory (`MEMORY.md`, `USER.md`, cross-session facts) | `/docs/user-guide/features/memory` |
| Context files (`.hermes.md`, `AGENTS.md` auto-injection) | `/docs/user-guide/features/context-files` |
| `@file`, `@folder`, `@url` context references in messages | `/docs/user-guide/features/context-references` |

### Automation & orchestration
| Symptom | URL |
|---|---|
| Cron / scheduled tasks (natural language or crontab) | `/docs/user-guide/features/cron` |
| Subagent delegation, `/background`, parallel agents, restricted toolsets | `/docs/user-guide/features/delegation` |
| Code execution (Python scripts calling Hermes tools programmatically) | `/docs/user-guide/features/code-execution` |
| Lifecycle hooks (logging, alerts, guardrails) | `/docs/user-guide/features/hooks` |
| Batch processing, thousands of prompts, trajectory data | `/docs/user-guide/features/batch-processing` |
| RL trajectory export for fine-tuning | `/docs/user-guide/features/rl-training` |

### Media, vision, voice
| Symptom | URL |
|---|---|
| Voice mode end-to-end (CLI + messaging) | `/docs/user-guide/features/voice-mode` |
| Browser automation backends | `/docs/user-guide/features/browser` |
| Vision, clipboard image paste | `/docs/user-guide/features/vision` |
| Image generation (FLUX 2 Pro + upscaling) | `/docs/user-guide/features/image-generation` |
| TTS + speech-to-text providers | `/docs/user-guide/features/tts` |

### Providers & routing
| Symptom | URL |
|---|---|
| Which provider handles a request, priority, cost routing | `/docs/user-guide/features/provider-routing` |
| Automatic failover between providers on error | `/docs/user-guide/features/fallback-providers` |
| Multi-key rotation (round_robin / least_used / fill_first / random) | `/docs/user-guide/features/credential-pools` |

### Integration surfaces
| Symptom | URL |
|---|---|
| MCP (Model Context Protocol) servers | `/docs/user-guide/features/mcp` |
| OpenAI-compatible HTTP server for 3rd-party frontends | `/docs/user-guide/features/api-server` |
| IDE integration: VS Code, Zed, JetBrains via ACP | `/docs/user-guide/features/acp` |
| Honcho persistent cross-session memory | `/docs/user-guide/features/honcho` |

### Identity & customization
| Symptom | URL |
|---|---|
| SOUL.md personality / system prompt customization | `/docs/user-guide/features/personality` |
| Skins, themes, colors, spinners, branding | `/docs/user-guide/features/skins` |
| Custom plugins under `~/.hermes/plugins/` | `/docs/user-guide/features/plugins` |

## Quick decision hints

- "How do I make Hermes remember X across sessions?" → **memory** (for facts) or **honcho** (for user modeling). Skills are for *procedures*, not facts.
- "How do I run Hermes automatically each morning?" → **cron**
- "How do I add a custom tool?" → **plugins** first, then **tools** for the tool model, then **mcp** if the integration is external.
- "How do I run multiple Hermes agents in parallel?" → **delegation** (`/background`, subagents)
- "How do I wire Hermes into VS Code/Zed?" → **acp**
- "How do I expose Hermes to another chat frontend?" → **api-server**
