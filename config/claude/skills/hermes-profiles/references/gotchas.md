# Hermes profile gotchas & non-obvious behaviors

Facts the CLI help won't tell you. Check here when something "should work"
but doesn't, or when a user is about to do something with a sharp edge.

## Table of contents

- [Deletion refuses the active profile](#deletion-refuses-the-active-profile)
- [`--clone` vs `--clone-all`](#--clone-vs---clone-all)
- [`hermes update` touches every profile](#hermes-update-touches-every-profile)
- [`hermes uninstall` is total](#hermes-uninstall-is-total)
- [Profile name charset is strict](#profile-name-charset-is-strict)
- [Bot token collisions across profiles](#bot-token-collisions-across-profiles)
- [Rename does not migrate gateway services](#rename-does-not-migrate-gateway-services)
- [The default profile is `~/.hermes`, not `~/.hermes/profiles/default`](#the-default-profile-is-hermes-not-hermesprofilesdefault)
- [Alias collisions with existing binaries](#alias-collisions-with-existing-binaries)
- [`HERMES_HOME` is the switch](#hermes_home-is-the-switch)

---

## Deletion refuses the active profile

`hermes profile delete <name>` errors out if `<name>` is the currently
active profile. Switch first:

```
hermes profile use default
hermes profile delete old-profile --yes
```

There is no `--force` that bypasses this check. The constraint exists so
that deletion never leaves Hermes pointing at a nonexistent directory.

## `--clone` vs `--clone-all`

They are *not* just verbose vs terse. They copy different things:

| What is copied        | `--clone` | `--clone-all` |
| --------------------- | --------- | ------------- |
| `config.yaml`         | yes       | yes           |
| `.env` (keys, tokens) | yes       | yes           |
| `SOUL.md`             | yes       | yes           |
| memory files          | no        | yes           |
| session history       | no        | yes           |
| skills directory      | no        | yes           |
| cron jobs             | no        | yes           |
| plugins               | no        | yes           |
| state database        | no        | yes           |

Default case: use `--clone` for "new agent, same provider setup." Use
`--clone-all` only when you genuinely want a snapshot fork of a live
agent (experiments, backups).

## `hermes update` touches every profile

Running `hermes update` syncs newly bundled skills into **every** profile,
not just the active one. There is no `--profile` scope for updates. If
you've manually edited bundled skills inside a profile, they may be
overwritten — move customizations into your own skills directory first.

## `hermes uninstall` is total

Removes Hermes itself, default configuration, **and every profile**. No
per-profile exclusion flag. If you want to keep profile data:

```
hermes profile export coder -o ~/coder.tar.gz
hermes profile export researcher -o ~/researcher.tar.gz
hermes uninstall
# ...later, reinstall, then:
hermes profile import ~/coder.tar.gz
```

## Profile name charset is strict

Allowed: ASCII letters, digits, `-`, `_`. Rejected: spaces, `/`, dots,
unicode, punctuation. Names are used as directory names and shell
wrapper names, so the restriction is mechanical, not stylistic.

## Bot token collisions across profiles

Each profile has its own `.env`, but platform bot tokens are globally
unique identities. If two profiles hold the same `TELEGRAM_BOT_TOKEN`
(or Discord / Slack / WhatsApp / Signal equivalent), the second gateway
to start will refuse with an error naming the conflicting profile.

Fix: rotate one of the tokens, or run only one gateway at a time for
that platform.

## Rename does not migrate gateway services

`hermes profile rename old new` updates the directory and regenerates
`~/.local/bin/new`, but an installed systemd/launchd unit named
`hermes-gateway-old` is **not** renamed. After renaming:

```
old gateway stop            # may fail if alias already gone
hermes profile rename old new
new gateway install         # creates hermes-gateway-new
# manually remove the stale hermes-gateway-old service file
```

## The default profile is `~/.hermes`, not `~/.hermes/profiles/default`

Existing installs don't migrate into a `profiles/` subdirectory. The
"default" profile always lives at `~/.hermes` directly; new profiles live
under `~/.hermes/profiles/<name>/`. This means:

- `hermes profile list` shows `default` as a first-class entry, but its
  files are a level up from the rest.
- Path-based tooling targeting "any profile" needs to handle both
  `~/.hermes/*` and `~/.hermes/profiles/*/*`.

## Alias collisions with existing binaries

Profile creation drops a wrapper at `~/.local/bin/<name>`. If `<name>`
matches an existing command on PATH, resolution order decides which
wins — usually the one earlier in PATH. Two workarounds:

```
hermes profile alias coder --remove           # drop the wrapper
hermes profile alias coder --name hcoder      # use a prefixed name
```

Then invoke explicitly with `hermes -p coder ...` or `hcoder ...`.

## `HERMES_HOME` is the switch

All isolation ultimately flows from `HERMES_HOME`. Setting it manually
before invoking `hermes` has the same effect as using a profile:

```
HERMES_HOME=~/.hermes/profiles/coder hermes chat
```

Useful in scripts, cron jobs, or systemd units that predate profile
support. The generated `~/.local/bin/<name>` wrapper is doing exactly
this under the hood.
