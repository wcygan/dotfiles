---
name: pi-coding-agent
description: Use the pi coding agent CLI (@earendil-works/pi-coding-agent) and navigate its docs and source. Covers interactive/print/json/rpc modes, model & tool flags, sessions, custom models.json (local llama.cpp/Ollama/vLLM), skills, extensions, and the pi-mono monorepo layout. Use when running `pi`, driving it headlessly/programmatically, configuring local models, writing pi extensions/skills, or answering "how does pi do X". Keywords pi, pi.dev, pi coding agent, earendil, pi-mono, llamacpp, models.json, rpc mode, json mode, qwen.
---

# pi coding agent

`pi` is a minimal terminal coding harness: an LLM with `read`/`bash`/`edit`/`write` tools (plus opt-in `grep`/`find`/`ls`), extensible through TypeScript extensions, Agent-Skills-standard skills, prompt templates, and themes. It runs against many providers — including a **locally served OpenAI-compatible endpoint**, which is this machine's primary setup.

Core philosophy: keep the harness small, push workflow behavior into extensions/skills/packages. It deliberately ships **no** built-in MCP, sub-agents, permission popups, plan mode, to-dos, or background bash — build or install those as extensions.

## Local sources of truth (prefer over the web)

- **CLI itself**: `pi --help` (exhaustive flag list + env vars + built-in tool names). Version: `pi --version` (currently 0.70.2).
- **Cloned repo** (`pi-mono`): `/Users/wcygan/Development/pi` — branch `main`.

> Package-name note: this machine's binary is installed as **`@mariozechner/pi-coding-agent`** (bun global, at `~/.bun/install/global/node_modules/@mariozechner/pi-coding-agent`). The public docs and the cloned repo use the scope **`@earendil-works/pi-coding-agent`**. Same project — author is Mario Zechner (badlogic) — published under two npm scopes. Use whichever scope matches the install you're touching.
- **Docs in-source** (mirror of pi.dev/docs): `/Users/wcygan/Development/pi/packages/coding-agent/docs/*.md`. Read these directly; they are authoritative and offline.
- **Canonical web docs** (use if the clone is stale/absent): https://pi.dev/docs/latest

When asked "how does pi do X", read the matching doc file in the clone first, then the source under `packages/`. See [references/navigation.md](references/navigation.md) for the doc-to-file and monorepo map.

## This machine's setup (verify, don't assume)

- Models are served locally by **llama.cpp** (`llama serve -hf unsloth/Qwen3.6-27B-MTP-GGUF:BF16`) at `http://127.0.0.1:8080/v1` (OpenAI Chat Completions API).
- pi config lives in `~/.pi/agent/`: `models.json` (custom local providers), `settings.json` (`defaultProvider`/`defaultModel`), `auth.json`, `sessions/`, `skills/`.
- **Gotcha already present here:** `~/.pi/agent/models.json` lists model `id`s (e.g. `unsloth/Qwen3.6-27B-GGUF:UD-Q4_K_XL`, `qwen3.6-27b-mtp`) that do **not** match what `/v1/models` actually serves (`unsloth/Qwen3.6-27B-MTP-GGUF:BF16`). It works because llama.cpp ignores the `model` field and routes to the one loaded model — but the displayed name is fiction. Confirm the live id with `curl -s http://127.0.0.1:8080/v1/models | jq -r '.data[].id'` before trusting config.

Before driving pi locally, confirm the server is up:
```bash
curl -s --max-time 2 http://127.0.0.1:8080/v1/models | jq -r '.data[].id' || echo "llama.cpp not serving on :8080"
```

## Running pi — the 20% you need most

```bash
pi                                  # interactive, in cwd, uses default provider/model
pi "Summarize this repo"            # interactive with an initial prompt
pi @README.md @src/app.ts "Review"  # @-prefixed files are attached to the message
pi -p "List all .ts files in src/"  # PRINT mode: process and exit (scripting)
cat notes.md | pi -p "Summarize"    # print mode merges piped stdin into the prompt
pi --tools read,grep,find,ls -p "Review the code"   # READ-ONLY: no edit/write/bash
```

Pick the model explicitly (overrides settings):
```bash
pi --provider llamacpp --model "unsloth/Qwen3.6-27B-GGUF:UD-Q4_K_XL" -p "..."
pi --model llamacpp/qwen3.6-27b-mtp "..."     # provider/id shorthand
curl -s http://127.0.0.1:8080/v1/models | jq -r '.data[].id'  # what's served (pi --list-models is broken here, see local-models.md)
```

Sessions persist to `~/.pi/agent/sessions/` (per cwd):
```bash
pi -c            # continue most recent session
pi -r            # browse & resume
pi --no-session  # ephemeral
```

In interactive mode: `/` opens commands, `@` fuzzy-finds files, `!cmd` runs a shell command and feeds output to the model (`!!cmd` runs it silently), `Ctrl+L`/`/model` switches models, `Shift+Tab` cycles thinking level. Full command and key tables are in [references/cli.md](references/cli.md).

## Driving pi from other programs

- **`--mode json`** — every event as one JSON line on stdout. Best for one-shot observation/automation. Parse with `jq`.
- **`--mode rpc`** — bidirectional JSONL over stdin/stdout: send `prompt`/`steer`/`abort`/`set_model`/... commands, receive `response` + streamed events. Best for embedding pi as a long-lived controlled subprocess.
- **SDK** — embed the agent in a Node.js app via `@earendil-works/pi-coding-agent`.

Details, event/command catalogs, and copy-paste clients: [references/programmatic.md](references/programmatic.md).

## Customizing pi

| Want to… | Do this | Reference |
|----------|---------|-----------|
| Add a local/self-hosted model | edit `~/.pi/agent/models.json` (no restart; reloads on `/model`) | [references/local-models.md](references/local-models.md) |
| Add a tool/command/flag/UI/provider | write a TypeScript extension | [references/extensions.md](references/extensions.md) |
| Add a reusable capability (markdown + scripts) | drop a `SKILL.md` skill under `~/.pi/agent/skills/` (Agent Skills standard; pi can also read `~/.claude/skills`) | [skills doc](file:///Users/wcygan/Development/pi/packages/coding-agent/docs/skills.md) |
| Change defaults (model, theme, compaction, retry) | edit `~/.pi/agent/settings.json` | [settings doc](file:///Users/wcygan/Development/pi/packages/coding-agent/docs/settings.md) |
| Install shared resources | `pi install <npm-or-git-source>`, `pi list`, `pi config` | [usage doc](file:///Users/wcygan/Development/pi/packages/coding-agent/docs/usage.md) |

## Reference index

- [references/cli.md](references/cli.md) — full flag reference, modes, slash commands, keybindings, env vars, message queue.
- [references/local-models.md](references/local-models.md) — `models.json` schema, llama.cpp/Ollama/vLLM recipes, Qwen thinking format, this machine's config and its quirks.
- [references/programmatic.md](references/programmatic.md) — json mode, rpc protocol (commands + events), SDK, with runnable examples.
- [references/extensions.md](references/extensions.md) — extension factory, registration API (tools/commands/flags/providers), lifecycle events, minimal examples.
- [references/navigation.md](references/navigation.md) — doc-file index and the pi-mono monorepo source map (where things actually live).
