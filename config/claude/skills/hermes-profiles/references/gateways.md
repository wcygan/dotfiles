# Per-profile gateways

Each Hermes profile runs its own gateway process for messaging platforms
(Telegram, Discord, Slack, WhatsApp, Signal). Gateways are fully isolated
per profile: separate tokens, separate systemd/launchd services, separate
state.

## Table of contents

- [The mental model](#the-mental-model)
- [Starting a gateway](#starting-a-gateway)
- [Installing as a persistent service](#installing-as-a-persistent-service)
- [Service naming](#service-naming)
- [Token isolation & conflict detection](#token-isolation--conflict-detection)
- [Running N bots on one machine](#running-n-bots-on-one-machine)
- [Rename / delete hygiene](#rename--delete-hygiene)
- [Troubleshooting](#troubleshooting)

---

## The mental model

- A **profile** holds configuration (`.env` with tokens, `config.yaml`
  with model settings).
- A **gateway** is the long-running process that connects that profile
  to a messaging platform and pumps events into Hermes.
- One profile can host multiple platform gateways if its `.env` includes
  tokens for more than one platform.
- Gateways read only from their own profile's `.env`. There is no
  fallback to the default profile's secrets.

## Starting a gateway

Foreground (for debugging):

```
<profile> gateway start
# or
hermes -p <profile> gateway start
```

This runs until you Ctrl-C. Useful for verifying that the `.env` tokens
are correct and the bot authenticates before installing as a service.

## Installing as a persistent service

```
<profile> gateway install
```

Registers the gateway with the OS service manager:

- **macOS** — launchd, user-level agent.
- **Linux** — systemd, user-level unit (`systemctl --user`).

After install, the service auto-starts on login / reboot and survives
shell exits.

## Service naming

Services are named `hermes-gateway-<profile>`:

```
hermes-gateway-coder
hermes-gateway-assistant
hermes-gateway-researcher
```

Check status with the platform's usual tools:

```
# Linux
systemctl --user status hermes-gateway-coder
journalctl --user -u hermes-gateway-coder -f

# macOS
launchctl list | rg hermes-gateway
```

## Token isolation & conflict detection

Each profile's `.env` holds its own tokens. Hermes checks at gateway
startup whether another profile is already running a gateway with the
**same** bot token for the same platform. If so, the second gateway
refuses to start and prints an error naming the conflicting profile.

Supported platforms covered by this check:

- Telegram (`TELEGRAM_BOT_TOKEN`)
- Discord
- Slack
- WhatsApp
- Signal

The check exists because platforms enforce single-connection-per-bot and
silent collisions would cause message loss or auth loops.

## Running N bots on one machine

The canonical multi-bot setup:

```
hermes profile create assistant --clone
hermes profile create researcher --clone

$EDITOR ~/.hermes/profiles/assistant/.env
# TELEGRAM_BOT_TOKEN=<bot_A>
$EDITOR ~/.hermes/profiles/researcher/.env
# TELEGRAM_BOT_TOKEN=<bot_B>

assistant gateway install
researcher gateway install

# Verify
systemctl --user status hermes-gateway-assistant hermes-gateway-researcher
```

Each bot has its own model config, memory, sessions, and cron schedule —
changing one does not affect the other.

## Rename / delete hygiene

Gateway services are **not** automatically updated when you rename or
delete a profile.

Renaming:

```
old gateway stop            # stop the old service first
hermes profile rename old new
new gateway install         # creates hermes-gateway-new
# then remove the stale hermes-gateway-old service unit manually
```

Deleting:

```
old gateway stop
hermes profile delete old --yes
# also disable/remove hermes-gateway-old from systemctl or launchctl
```

The service file cleanup step is manual because Hermes doesn't track
which service manager installed the unit.

## Troubleshooting

**Gateway won't start, logs show token conflict**
Two profiles share the same bot token. Rotate one token on the platform
side (BotFather, Discord developer portal, etc.) and update the relevant
profile's `.env`.

**Gateway starts but bot doesn't respond**
Check that you started it under the right profile — a default-profile
gateway with no `TELEGRAM_BOT_TOKEN` in `~/.hermes/.env` will run but
silently do nothing. Verify with `hermes profile show <name>`.

**Service auto-restarts in a loop**
Usually bad credentials. Run `<profile> gateway start` in the foreground
to see the real error instead of scraping journald.

**Updated `.env`, changes not picked up**
Restart the gateway service — env files are read once at startup:

```
systemctl --user restart hermes-gateway-<profile>
# or launchctl kickstart -k gui/$(id -u)/hermes-gateway-<profile>
```
