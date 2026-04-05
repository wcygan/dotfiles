# Hermes profile worked examples

Concrete walkthroughs for common profile scenarios. Prefer these when the
user wants a recipe, not a flag reference.

## Table of contents

- [1. Spin up a dedicated coding assistant](#1-spin-up-a-dedicated-coding-assistant)
- [2. Back up your current setup before risky changes](#2-back-up-your-current-setup-before-risky-changes)
- [3. Run two Telegram bots simultaneously](#3-run-two-telegram-bots-simultaneously)
- [4. Fork a profile for experiments](#4-fork-a-profile-for-experiments)
- [5. Move a profile to another machine](#5-move-a-profile-to-another-machine)
- [6. Reset a profile without losing keys](#6-reset-a-profile-without-losing-keys)
- [7. Temporarily run one command under a profile](#7-temporarily-run-one-command-under-a-profile)

---

## 1. Spin up a dedicated coding assistant

Goal: a profile named `coder` with its own model config, SOUL, and history.

```
hermes profile create coder --clone
hermes profile use coder
coder config set model.model anthropic/claude-sonnet-4
$EDITOR ~/.hermes/profiles/coder/SOUL.md      # personality
coder chat
```

The `--clone` pulls the active profile's `config.yaml`, `.env`, and
`SOUL.md` so you start from known-good settings rather than blank.

After creation, `coder` is available as a top-level command via the
auto-generated `~/.local/bin/coder` wrapper.

## 2. Back up your current setup before risky changes

```
hermes profile export default -o ~/backups/default-$(date +%F).tar.gz
```

To restore later:

```
hermes profile import ~/backups/default-2026-04-05.tar.gz --name default-restored
hermes profile use default-restored
```

Importing under a new name avoids clobbering the current `default`.

## 3. Run two Telegram bots simultaneously

Each bot lives in its own profile with its own `.env` and gateway service.

```
hermes profile create assistant --clone
hermes profile create researcher --clone

$EDITOR ~/.hermes/profiles/assistant/.env     # TELEGRAM_BOT_TOKEN=xxx
$EDITOR ~/.hermes/profiles/researcher/.env    # TELEGRAM_BOT_TOKEN=yyy (different!)

assistant gateway install
researcher gateway install
```

This creates two independent services (`hermes-gateway-assistant` and
`hermes-gateway-researcher`) that never share state. If you accidentally
reuse the same token, the second `gateway install` fails with a conflict
error naming the other profile — see `gotchas.md`.

## 4. Fork a profile for experiments

You want to test new skills against the real memory and history of
`coder`, without risking the working setup:

```
hermes profile create coder-experiment --clone-all --clone-from coder
hermes profile use coder-experiment
# poke around, test skills, change config freely
hermes profile use coder                      # back to the real one
hermes profile delete coder-experiment --yes  # discard the fork
```

`--clone-all` includes memories, sessions, skills, cron jobs, and plugins
so the fork behaves like a real continuation, not a blank shell.

## 5. Move a profile to another machine

On the source machine:

```
hermes profile export coder -o coder.tar.gz
scp coder.tar.gz newbox:~/
```

On the destination:

```
hermes profile import ~/coder.tar.gz
hermes profile use coder
```

Secrets in `.env` travel inside the archive — handle accordingly. Model
provider keys will work out of the box; anything machine-specific (local
paths in `config.yaml`, custom MCP server endpoints) may need editing.

## 6. Reset a profile without losing keys

You want fresh memory and sessions but keep `.env` and `config.yaml`:

```
hermes profile export coder -o coder-backup.tar.gz     # safety net
hermes profile create coder-fresh --clone --clone-from coder
hermes profile use coder-fresh
hermes profile rename coder coder-old
hermes profile rename coder-fresh coder
hermes profile delete coder-old --yes
```

`--clone` (not `--clone-all`) copies only config, env, and SOUL — leaving
memory and sessions empty in the new profile.

## 7. Temporarily run one command under a profile

No sticky switch needed:

```
hermes -p coder doctor
hermes --profile=researcher chat -q "summarize my pinned papers"
```

Equivalent to using the alias:

```
coder doctor
researcher chat -q "summarize my pinned papers"
```

Use this form in scripts where you don't want to depend on whichever
profile happens to be active.
