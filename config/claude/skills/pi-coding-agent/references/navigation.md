# Navigating pi's docs & source

Clone: `/Users/wcygan/Development/pi` (`pi-mono`, branch `main`). Canonical web docs: https://pi.dev/docs/latest. Prefer the clone — it's offline and matches the installed version's source.

## Doc files (`packages/coding-agent/docs/`)

Read the file that matches the question; each maps 1:1 to a pi.dev/docs page.

| Topic | File |
|-------|------|
| Install, auth, first session | `quickstart.md` |
| Interactive mode, slash commands, message queue, context files, full CLI reference | `usage.md` |
| Providers, API keys, `auth.json`, cloud (Azure/Bedrock/Vertex/Cloudflare), resolution order | `providers.md` |
| `settings.json` — every setting | `settings.md` |
| Keybindings + customization | `keybindings.md` |
| Sessions (tree/fork/clone) | `sessions.md` · on-disk format: `session-format.md` |
| Context compaction & branch summaries | `compaction.md` |
| **Custom models / local servers** (`models.json`) | `models.md` |
| **Custom providers via extension** (OAuth, custom streaming) | `custom-provider.md` |
| **Extensions** (full API) | `extensions.md` |
| Skills (Agent Skills standard) | `skills.md` |
| Prompt templates | `prompt-templates.md` |
| Themes | `themes.md` |
| Packages (install/share resources) | `packages.md` |
| json mode | `json.md` · rpc mode | `rpc.md` · SDK | `sdk.md` · TUI components | `tui.md` |
| Platform setup | `windows.md`, `termux.md`, `tmux.md`, `terminal-setup.md`, `shell-aliases.md` |
| Building pi from source | `development.md` |

Project rules for contributing to pi itself: `/Users/wcygan/Development/pi/AGENTS.md` and `CONTRIBUTING.md`.

## Monorepo layout (`packages/`)

Four published packages; the CLI composes the lower three.

| Package | npm name | Role |
|---------|----------|------|
| `coding-agent` | `@earendil-works/pi-coding-agent` | the `pi` CLI: tools, sessions, modes, extensions host |
| `agent` | `@earendil-works/pi-agent-core` | agent runtime: agent loop, tool calling, state, transport |
| `ai` | `@earendil-works/pi-ai` | unified multi-provider LLM API + model registry |
| `tui` | `@earendil-works/pi-tui` | terminal UI with differential rendering |

### `packages/coding-agent/src/`
- `cli.ts`, `main.ts`, `config.ts` — entrypoint, arg parsing, config load.
- `cli/` — `args.ts` (flag parsing), `list-models.ts`, `session-picker.ts`, `file-processor.ts` (`@file` handling), `config-selector.ts`.
- `core/tools/` — **the built-in tools**: `read.ts`, `bash.ts`, `edit.ts`, `write.ts`, `grep.ts`, `find.ts`, `ls.ts` (+ `truncate.ts`, `file-mutation-queue.ts`). Start here to understand tool behavior.
- `core/extensions/` — **extension host**: `loader.ts`, `runner.ts`, `wrapper.ts`, `types.ts` (the `ExtensionAPI`/`ExtensionContext` contract).
- `core/` — session machinery: `agent-session*.ts`, `session-manager.ts`, `model-registry.ts`/`model-resolver.ts`, `settings-manager.ts`, `system-prompt.ts`, `skills.ts`, `slash-commands.ts`, `prompt-templates.ts`, `resource-loader.ts`, `compaction/`, `export-html/`, `sdk.ts`.
- `modes/` — `interactive/`, `print-mode.ts`, `rpc/` (`rpc-mode.ts`, `rpc-client.ts`, `rpc-types.ts`, `jsonl.ts`).
- `examples/extensions/` — **~70 runnable extension examples** (see below).

### `packages/ai/src/`
- `models.ts` + `models.generated.ts` — model catalog (regenerated per release); `env-api-keys.ts` — env-var→provider map.
- `providers/` — one file per provider streaming impl: `anthropic.ts`, `openai-completions.ts`, `openai-responses.ts`, `google.ts`, `amazon-bedrock.ts`, `mistral.ts`, `cloudflare.ts`, `azure-openai-responses.ts`, `openai-codex-responses.ts`, `register-builtins.ts`, `transform-messages.ts`. **Read these when debugging a `compat` flag** — they show exactly what each flag changes on the wire.
- `stream.ts`, `types.ts`, `oauth.ts`, `utils/` (incl. `overflow.ts` — the overflow-error patterns that trigger auto-compaction).

### `packages/agent/src/`
- `agent-loop.ts`, `agent.ts` — the core agent/tool-call loop; `harness/`, `node.ts`, `proxy.ts`, `types.ts`.

### `packages/tui/src/`
- `tui.ts`, `editor-component.ts`, `keybindings.ts`/`keys.ts`, `autocomplete.ts`, `fuzzy.ts`, `terminal-image.ts`, `components/`.

## Example extensions worth copying (`packages/coding-agent/examples/extensions/`)

Strong starting points by intent:
- Permission/safety: `permission-gate.ts`, `confirm-destructive.ts`, `protected-paths.ts`, `dirty-repo-guard.ts`, `timed-confirm.ts`, `sandbox/`.
- Workflow features pi omits by default: `plan-mode/`, `todo.ts`, `subagent/`, `git-checkpoint.ts`, `auto-commit-on-exit.ts`, `handoff.ts`, `summarize.ts`, `trigger-compact.ts`, `custom-compaction.ts`.
- Providers/payload: `custom-provider-anthropic/`, `custom-provider-gitlab-duo/`, `provider-payload.ts`, `tool-override.ts`, `dynamic-tools.ts`.
- UI/rendering: `custom-header.ts`, `custom-footer.ts`, `status-line.ts`, `message-renderer.ts`, `widget-placement.ts`, `working-indicator.ts`.
- Integration: `rpc-demo.ts`, `structured-output.ts`, `send-user-message.ts`, `event-bus.ts`, `file-trigger.ts`, `ssh.ts`, `inline-bash.ts`.
- Minimal templates: `hello.ts`, `commands.ts`, `tools.ts`, `question.ts`, `notify.ts`. (`examples/extensions/README.md` indexes them all.)

## Quick recipes for "how does pi do X?"

1. `grep -rn "<term>" /Users/wcygan/Development/pi/packages/coding-agent/docs` — find the doc.
2. For a flag's wire effect: read the matching file in `packages/ai/src/providers/`.
3. For tool behavior: read `packages/coding-agent/src/core/tools/<tool>.ts`.
4. For the extension contract: read `packages/coding-agent/src/core/extensions/types.ts`.
5. Or just ask pi itself: `pi -p "Explain how pi handles context compaction, citing files"` from inside the clone.
