---
name: pi-docs
description: Answer questions about how the pi coding agent itself works by reading pi's bundled offline docs and citing the file. Use when asked how pi does X, how to configure pi (settings.json, models.json, providers, keybindings), what a pi flag/mode/feature does, or where a pi feature is documented. Keywords pi docs, how does pi, configure pi, pi settings, models.json, pi providers, pi extensions, pi sessions, pi modes, pi skills.
---

# pi-docs

Answer questions about **pi itself** — the coding agent you are running inside — by reading pi's bundled documentation and quoting it. Ground every answer in a file you actually read this turn: pi is niche software, so answering from memory produces wrong commands and flags. Read-only — do not edit anything.

## Step 1 — locate the docs (run this first)
```
DOCS="$HOME/Development/pi/packages/coding-agent/docs"
ls "$DOCS/index.md" 2>/dev/null || find "$HOME" -maxdepth 6 -type d -path '*coding-agent/docs' 2>/dev/null | head -1
```
- If a path containing `index.md` printed, use its directory as `$DOCS`.
- Else if `find` printed a directory, use that as `$DOCS`.
- If nothing printed, the pi source clone is missing. Print exactly `pi docs not found locally — clone pi-mono or see https://pi.dev/docs/latest` and stop.

## Step 2 — pick the one file for the question
Match the question to exactly one row, then `read` that file under `$DOCS`:

| The question is about… | File |
|---|---|
| install, auth, first run | `quickstart.md` |
| interactive use, slash commands, CLI flags, `@file`, context files | `usage.md` |
| every `settings.json` option | `settings.md` |
| keybindings | `keybindings.md` |
| providers, API keys, `auth.json`, cloud (Bedrock/Azure/Vertex/Cloudflare) | `providers.md` |
| custom models, local llama.cpp/Ollama/vLLM, `models.json` | `models.md` |
| writing a custom-provider extension | `custom-provider.md` |
| extensions API (hooks, tools, commands) | `extensions.md` |
| skills (Agent Skills standard) | `skills.md` |
| prompt templates | `prompt-templates.md` |
| themes | `themes.md` |
| packages (install/share resources) | `packages.md` |
| sessions: fork / clone / tree | `sessions.md` |
| session on-disk format | `session-format.md` |
| context compaction & branch summaries | `compaction.md` |
| json mode | `json.md` |
| rpc mode | `rpc.md` |
| programmatic SDK | `sdk.md` |
| TUI components | `tui.md` |
| building pi from source | `development.md` |
| platform setup (Windows / Termux / tmux / terminal) | `windows.md`, `termux.md`, `tmux.md`, `terminal-setup.md` |

If no row clearly fits, read `$DOCS/docs.json` (the doc index) to find the right file, or run `grep -rln "<keyword>" "$DOCS"` and read the top hit.

## Step 3 — answer
Answer using only what the file says. Quote the relevant setting / flag / command verbatim and name the file it came from (e.g. `settings.md`). If the file does not contain the answer, say so and point to `docs.json` or the grep command above — do not guess.

## Self-check before answering (revise if any item is false)
- [ ] I read at least one file under `$DOCS` this turn.
- [ ] My answer names the doc file it came from.
- [ ] Every command, flag, or setting I state is copied from that file, not recalled.
- [ ] If the file lacked the answer, I said so instead of inventing one.
