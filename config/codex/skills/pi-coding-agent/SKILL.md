---
name: pi-coding-agent
description: "Use and investigate the Pi coding agent CLI. Covers interactive, print, JSON, and RPC modes; model and tool flags; sessions; local OpenAI-compatible models; skills; extensions; and the pi monorepo. Use when running `pi`, automating it, configuring models.json, writing Pi extensions or skills, or answering how Pi implements a behavior."
---

# Pi Coding Agent

Use this skill to operate Pi or trace its behavior from documentation and source.

## Evidence order

Pi changes quickly, so establish the relevant version before relying on a flag,
schema, or source path:

1. Run `command -v pi` and `pi --version` for the installed CLI.
2. Run `pi --help` for version-current flags and environment variables. If Pi
   tries to initialize writable state in a restricted environment, retry with an
   isolated `PI_CODING_AGENT_DIR` under a temporary directory.
3. Locate a source checkout from the current workspace or ask the user for its
   path. Do not assume a machine-specific clone location.
4. Compare the checkout's `packages/coding-agent/package.json` version with the
   installed version before treating its docs or source as matching runtime
   behavior.
5. Use the canonical docs at `https://pi.dev/docs/latest` when local sources are
   absent or stale.

State which source supports the answer and call out version mismatches.

See [references/navigation.md](references/navigation.md) for the documentation
and monorepo map.

## Safe operating rules

- Treat Pi prompts, tool access, commits, pushes, and external writes as separate
  authority. A request to explain Pi does not authorize running an agent that can
  edit the user's checkout.
- For inspection, prefer `--tools read,grep,find,ls` and `--no-session`.
- Never print or copy `auth.json`, API keys, or provider credentials.
- Inspect `models.json` structurally with redaction; do not expose `apiKey`,
  headers, or command-backed secrets.
- Verify local model endpoints before launching a long agent run.
- Do not mutate Pi settings, install packages, or remove resources unless the
  user requested that change.

## Common commands

```bash
pi                                      # interactive in the current directory
pi "Summarize this repository"          # interactive with an initial prompt
pi @README.md @src/app.ts "Review"      # attach files to the message
pi --no-session -p "List TypeScript files"  # one-shot print mode
pi --tools read,grep,find,ls --no-session -p "Review this code"
pi -c                                   # continue the latest session
pi -r                                   # browse and resume a session
```

Use `--provider` and `--model` when reproducibility matters:

```bash
pi --provider <provider> --model <model-id> --no-session -p "<prompt>"
```

Read [references/cli.md](references/cli.md) before composing less common
invocations.

## Local and custom models

Pi reads custom providers from `${PI_CODING_AGENT_DIR:-$HOME/.pi/agent}/models.json`.
Do not assume that a configured model ID matches what a local server currently
serves. Query the server's model endpoint, compare it with the redacted config,
then run a minimal `--no-session -p` smoke test.

Use [references/local-models.md](references/local-models.md) for schemas, local
server examples, secret handling, and verification.

## Programmatic use

- Plain `-p`: one-shot answer for shell scripts.
- `--mode json`: JSONL event stream for observing a one-shot run.
- `--mode rpc`: bidirectional JSONL for controlling a long-lived subprocess.
- SDK: in-process TypeScript integration.

Use the smallest surface that meets the request. See
[references/programmatic.md](references/programmatic.md) for event handling and
client patterns.

## Extensions and skills

Use a Pi skill for reusable instructions and bundled resources. Use a TypeScript
extension when the behavior needs tools, commands, flags, lifecycle hooks, UI, or
provider integration.

Read [references/extensions.md](references/extensions.md), then verify the
current API against the matching installed docs or source before writing code.

## Completion

Report:

- the installed Pi version and source/docs version used;
- the exact command, config path, or source files inspected;
- whether the operation was read-only or mutated Pi/user state;
- validation performed; and
- any version mismatch, unavailable endpoint, or unverified assumption.
