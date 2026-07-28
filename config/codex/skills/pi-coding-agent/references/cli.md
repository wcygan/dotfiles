# Pi CLI reference

Treat `pi --help` as authoritative for the installed version. This page is a
task-oriented map, not a frozen exhaustive flag list.

## Invocation and modes

```text
pi [options] [@files...] [messages...]
```

| Mode | Typical use |
| --- | --- |
| default interactive TUI | human-guided repository work |
| `-p`, `--print` | run a prompt, print the result, exit |
| `--mode json` | emit session and agent events as JSONL |
| `--mode rpc` | accept commands and emit responses/events as JSONL |
| `--export <input> [output]` | export a saved session |

`@file` arguments attach files to the first message. Piped stdin is incorporated
in print mode.

## Reproducible model selection

Use `--provider <name>`, `--model <id-or-pattern>`, and `--thinking <level>` as
supported by the installed version. Prefer environment variables or Pi's
credential store over `--api-key`, because command-line secrets may be exposed
through shell history and process listings.

Run `pi --list-models [search]` only after checking the installed help. If it
fails, inspect the redacted custom model configuration and the provider's model
endpoint instead of assuming that no models exist.

## Tool boundaries

Pi commonly provides `read`, `bash`, `edit`, and `write`, with additional
read-only discovery tools such as `grep`, `find`, and `ls`. Confirm the current
built-ins with `pi --help`.

```bash
pi --tools read,grep,find,ls --no-session -p "Review the repository"
pi --exclude-tools bash,edit,write --no-session -p "Inspect only"
```

An allowlist is clearer than an exclusion list for safety-sensitive inspection.

## Sessions

Sessions normally live under `${PI_CODING_AGENT_DIR:-$HOME/.pi/agent}/sessions`.

```bash
pi -c                    # continue the latest session
pi -r                    # select a session to resume
pi --session <path-or-id>
pi --fork <path-or-id>
pi --no-session
pi --name <display-name>
```

Use `--no-session` for smoke tests and automation that should not retain history.

## Resources and context

Current releases expose flags for extensions, skills, prompt templates, themes,
and context-file discovery. Verify exact spellings in `pi --help`.

Pi discovers project instructions such as `AGENTS.md` and `CLAUDE.md` unless
context discovery is disabled. Explicit resource flags may still load a single
resource when general discovery is disabled.

## Interactive navigation

Common behavior includes:

- `/` command completion;
- `@` file discovery;
- `!command` shell execution;
- model and thinking-level switching;
- session resume, tree, fork, clone, compact, export, and reload commands; and
- steering or follow-up messages while an agent is running.

Keybindings and commands change over time. Read the installed or matching source
docs under `packages/coding-agent/docs/usage.md` and `keybindings.md`.

## Package commands

`pi install`, `remove`, `update`, `list`, and `config` manage Pi resource
packages. They mutate global or project Pi state; inspect first and run them only
when the user requested the corresponding change.

## Important environment variables

Verify the current list in `pi --help`. Frequently relevant variables include:

- `PI_CODING_AGENT_DIR`: global Pi configuration directory;
- `PI_CODING_AGENT_SESSION_DIR`: session storage override;
- `PI_PACKAGE_DIR`: package directory override;
- `PI_OFFLINE`: suppress startup network operations;
- `PI_SKIP_VERSION_CHECK`: suppress the update check;
- provider-specific API-key variables; and
- `VISUAL` or `EDITOR` for external editing.

For restricted execution, create a temporary directory and set
`PI_CODING_AGENT_DIR` for read-only CLI discovery so Pi does not touch the
user's live configuration.
