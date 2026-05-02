---
name: hermes-profiles
description: Manage Hermes Agent profiles — isolated `~/.hermes/profiles/<name>/` envs with per-profile config, SOUL.md, memory, sessions, gateway. Use for create/clone/switch/export/import profiles or configuring per-profile messaging gateways. Keywords hermes profile, -p, --profile, HERMES_HOME, gateway install.
---

# Hermes Profiles

Canonical reference for Hermes Agent (Nous Research) profiles. Authoritative
when the user asks how profiles behave, what a subcommand does, or how to
run multiple isolated agents on one machine. Fall back to live docs at
`hermes-agent.nousresearch.com/docs/user-guide/profiles/` only for anything
not covered here.

Scope note: this skill is narrower than `hermes-docs`. Use it for
profile-specific questions; use `hermes-docs` for any other Hermes topic.

## What a profile is

A profile is a fully isolated Hermes environment rooted at
`~/.hermes/profiles/<name>/`. Each profile owns its:

- `config.yaml` — model, provider, toolsets, settings
- `.env` — API keys, bot tokens
- `SOUL.md` — personality and instructions
- memory files, session history, skills directory
- state database, gateway PID files, logs, cron jobs

The **default** profile lives at `~/.hermes` itself (no migration needed
for existing installs). Isolation works by setting `HERMES_HOME` before
Hermes launches — 119+ internal file paths resolve via `get_hermes_home()`,
so everything scopes automatically.

## Three ways to target a profile

Ordered by stickiness:

1. **One-shot flag** — `hermes -p <name> <cmd>` or `--profile=<name>`.
   Overrides the active profile for a single invocation.
2. **Generated alias** — every profile creates a wrapper at
   `~/.local/bin/<name>`, so `coder chat` is equivalent to
   `hermes -p coder chat`.
3. **Sticky default** — `hermes profile use <name>` changes the active
   profile until you switch again.

## Quick command cheatsheet

| Task                       | Command                                            |
| -------------------------- | -------------------------------------------------- |
| List profiles              | `hermes profile list` (active marked `*`)          |
| Show details               | `hermes profile show <name>`                       |
| Switch sticky default      | `hermes profile use <name>`                        |
| Create blank               | `hermes profile create <name>`                     |
| Clone config only          | `hermes profile create <name> --clone`             |
| Clone everything           | `hermes profile create <name> --clone-all`         |
| Clone from specific source | `... --clone --clone-from <src>`                   |
| Rename                     | `hermes profile rename <old> <new>`                |
| Delete                     | `hermes profile delete <name> [--yes]`             |
| Export archive             | `hermes profile export <name> [-o <path.tar.gz>]`  |
| Import archive             | `hermes profile import <archive> [--name <n>]`     |
| Regenerate alias           | `hermes profile alias <name> [--remove]`           |
| Install gateway service    | `<name> gateway install`                           |

For exact flag behavior, argument validation, and every subcommand option,
load `references/commands.md`.

## When to load which reference

| User question                                         | Load                    |
| ----------------------------------------------------- | ----------------------- |
| "What does `--clone-all` copy vs `--clone`?"          | `references/commands.md`|
| "How do I set up a separate coder profile?"           | `references/examples.md`|
| "Why can't I delete this profile?"                    | `references/gotchas.md` |
| "Why did my second Telegram bot fail to start?"       | `references/gateways.md`|
| "Clone my whole setup as a backup"                    | `references/examples.md`|
| "What's the service name after `gateway install`?"    | `references/gateways.md`|
| "Does `hermes update` touch every profile?"           | `references/gotchas.md` |

Each reference is self-contained and linked from this file only — no
nested references. Read them with Read, not `head`, so you get the full
table of contents.

## Core constraints (always applicable)

- Profile names: alphanumeric plus `-` and `_` only.
- Cannot delete the currently active profile — switch first with
  `hermes profile use <other>`.
- Profiles share no state. A change to one profile's `config.yaml` never
  affects another.
- `hermes update` syncs newly bundled skills into **every** profile.
- `hermes uninstall` removes **all** profiles; there is no bulk "keep
  profile X" escape hatch — export first.

## Fallback

If a user question isn't covered by this skill or its references,
WebFetch the live docs:

- `https://hermes-agent.nousresearch.com/docs/user-guide/profiles/`
- `https://hermes-agent.nousresearch.com/docs/reference/profile-commands`

Last verified: 2026-04-05.
