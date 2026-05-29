# pi CLI reference

Contents: Invocation shape · Modes · Model selection · Tools · Sessions · Resources · System prompt · Package subcommands · Slash commands · Editor & message queue · Environment variables.

Authoritative source is `pi --help` (it prints the full, version-current flag list, env vars, and built-in tool names). This file is a curated summary. Doc: `packages/coding-agent/docs/usage.md` in the clone.

## Invocation shape

```
pi [options] [@files...] [messages...]
```

- `@file` arguments are attached to the (first) message: `pi @a.ts @b.ts "compare these"`. Works with images too: `pi -p @shot.png "what's here?"`.
- Multiple quoted strings become multiple messages.

## Modes

| Flag | Behavior |
|------|----------|
| (default) | interactive TUI |
| `-p`, `--print` | non-interactive: run the prompt, print result, exit. Reads piped stdin and merges it into the prompt. |
| `--mode json` | emit every event as a JSON line (see programmatic.md) |
| `--mode rpc` | JSONL request/response + event protocol over stdin/stdout (see programmatic.md) |
| `--export <in> [out]` | export a session `.jsonl` to HTML and exit |

## Model selection

| Flag | Notes |
|------|-------|
| `--provider <name>` | e.g. `llamacpp`, `anthropic`, `openai`, `google` |
| `--model <pattern>` | id, `provider/id`, or fuzzy pattern; optional `:<thinking>` suffix (`sonnet:high`) |
| `--api-key <key>` | overrides env/auth.json |
| `--thinking <level>` | `off`, `minimal`, `low`, `medium`, `high`, `xhigh` |
| `--models <patterns>` | comma list for `Ctrl+P` cycling; globs + fuzzy (`"claude-*,gpt-4o"`) |
| `--list-models [search]` | list reachable models (fuzzy filter optional). ⚠️ crashes on this machine in 0.70.2 — see local-models.md |

## Tools

Built-in: `read`, `bash`, `edit`, `write` (on by default) and `grep`, `find`, `ls` (read-only, off by default).

| Flag | Effect |
|------|--------|
| `-t`, `--tools <list>` | allowlist exactly these (built-in + extension + custom) |
| `-xt`, `--exclude-tools <list>` | disable specific tools |
| `-nbt`, `--no-builtin-tools` | drop built-ins, keep extension/custom tools |
| `-nt`, `--no-tools` | disable all tools |

Read-only review pattern: `pi --tools read,grep,find,ls -p "..."`.

## Sessions

Saved to `~/.pi/agent/sessions/` (organized by cwd). Override dir with `--session-dir`, `PI_CODING_AGENT_SESSION_DIR`, or `sessionDir` in settings.

| Flag | Effect |
|------|--------|
| `-c`, `--continue` | continue most recent session |
| `-r`, `--resume` | browse & select |
| `--session <path\|id>` | open specific file or partial UUID |
| `--fork <path\|id>` | fork into a new session |
| `--no-session` | ephemeral |
| `-n`, `--name <name>` | set display name at startup |

## Resources (extensions / skills / prompts / themes / context)

| Flag | Effect |
|------|--------|
| `-e`, `--extension <src>` | load extension (path/npm/git); repeatable |
| `--skill <path>` | load skill; repeatable, additive even with `--no-skills` |
| `--prompt-template <path>` | load prompt template; repeatable |
| `--theme <path>` | load theme; repeatable |
| `--no-extensions` / `--no-skills` / `--no-prompt-templates` / `--no-themes` | disable discovery |
| `-nc`, `--no-context-files` | skip `AGENTS.md` / `CLAUDE.md` discovery |

Combine `--no-*` with explicit `-e/--skill` to load *exactly* one resource: `pi --no-extensions -e ./x.ts`.

## System prompt & misc

| Flag | Effect |
|------|--------|
| `--system-prompt <text>` | replace default prompt (context files + skills still appended) |
| `--append-system-prompt <text\|file>` | append; repeatable |
| `--verbose` | force verbose startup |
| `--offline` | no startup network ops (same as `PI_OFFLINE=1`) |

## Package management subcommands

These manage pi *packages* (bundled extensions/skills/prompts/themes), not the pi install.

```bash
pi install <source> [-l]   # -l = project-local (.pi/) instead of global (~/.pi/agent/)
pi remove <source> [-l]    # alias: pi uninstall
pi update [source|self]    # update all / one; --self updates pi, --extensions updates packages
pi list                    # list installed packages
pi config                  # TUI to enable/disable package resources
```

## Slash commands (interactive)

Type `/` to autocomplete. Skills appear as `/skill:name`; prompt templates as `/templatename`.

| Command | Purpose |
|---------|---------|
| `/login`, `/logout` | manage OAuth / API-key credentials |
| `/model`, `/scoped-models` | switch model / pick cycling set |
| `/settings` | thinking level, theme, delivery, transport |
| `/new`, `/resume`, `/name <n>`, `/session` | session lifecycle & info |
| `/tree`, `/fork`, `/clone` | navigate / branch / duplicate session history |
| `/compact [prompt]` | manually compact context |
| `/copy`, `/export [file]`, `/share` | copy last msg / export HTML / upload gist |
| `/reload` | reload keybindings, extensions, skills, prompts, context files |
| `/hotkeys`, `/changelog`, `/quit` | help / version history / exit |

## Editor & message queue (interactive)

- `@` fuzzy file ref, `Tab` path completion, `Shift+Enter` newline, `Ctrl+V` paste image, `Ctrl+G` external `$EDITOR`.
- `!cmd` runs shell and sends output to model; `!!cmd` runs without sending output.
- **Enter** queues a *steering* message (delivered after current tool batch). **Alt+Enter** queues a *follow-up* (after all work). **Esc** aborts and restores queued text. Delivery tuned via `steeringMode`/`followUpMode` settings.

## Key environment variables

| Var | Purpose |
|-----|---------|
| `PI_CODING_AGENT_DIR` | config dir (default `~/.pi/agent`) |
| `PI_CODING_AGENT_SESSION_DIR` | session storage (overridden by `--session-dir`) |
| `PI_PACKAGE_DIR` | override package dir (Nix/Guix store paths) |
| `PI_OFFLINE` | disable all startup network ops |
| `PI_SKIP_VERSION_CHECK` | skip the pi.dev latest-version check |
| `PI_CACHE_RETENTION=long` | extended prompt cache where supported |
| `<PROVIDER>_API_KEY` | e.g. `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `GEMINI_API_KEY` (full list in `pi --help`) |
| `VISUAL` / `EDITOR` | external editor for `Ctrl+G` |

Keybindings are fully customizable; see `packages/coding-agent/docs/keybindings.md`.
