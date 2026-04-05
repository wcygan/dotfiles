# `hermes profile` command reference

Full subcommand reference for the profile management surface. Authoritative
for flag-level questions. Source:
`hermes-agent.nousresearch.com/docs/reference/profile-commands`.

## Table of contents

- [list](#list)
- [show](#show)
- [use](#use)
- [create](#create)
- [delete](#delete)
- [rename](#rename)
- [alias](#alias)
- [export](#export)
- [import](#import)
- [Global `-p` / `--profile` flag](#global-p----profile-flag)
- [Shell completion](#shell-completion)

---

## list

```
hermes profile list
```

Displays every profile. Active profile is marked with `*`. No flags.

## show

```
hermes profile show <name>
```

Prints profile details: directory path, configured model, gateway status,
installed skill count. Use as the read-only diagnostic.

## use

```
hermes profile use <name>
```

Sets `<name>` as the sticky default. Subsequent `hermes ...` commands (with
no `-p`) target this profile until you switch again. Switching back is
`hermes profile use default`.

## create

```
hermes profile create <name> [--clone] [--clone-all] [--clone-from <src>]
```

**Arguments**
- `<name>` — alphanumeric plus `-` and `_`. No spaces, no slashes.

**Flags**
- `--clone` — copies `config.yaml`, `.env`, and `SOUL.md` from the currently
  active profile. Sessions, memory, skills, cron, and state start empty.
- `--clone-all` — full snapshot: config, keys, personality, memories,
  session history, skills, cron jobs, plugins. Useful for backups and
  parallel experiments.
- `--clone-from <src>` — changes the source profile for `--clone` /
  `--clone-all` from the active profile to `<src>`.

**Examples**
```
hermes profile create mybot
hermes profile create work --clone
hermes profile create backup --clone-all
hermes profile create review --clone --clone-from coder
```

## delete

```
hermes profile delete <name> [--yes|-y]
```

**Flags**
- `--yes`, `-y` — skip the confirmation prompt.

**Behavior**
- Irreversibly removes `~/.hermes/profiles/<name>/` in full (config, keys,
  memory, sessions, skills, state DB, cron, logs).
- **Refuses to delete the currently active profile.** Switch first with
  `hermes profile use <other>`.
- Also removes the `~/.local/bin/<name>` alias wrapper.

## rename

```
hermes profile rename <old> <new>
```

Renames the profile directory and updates the generated alias. Gateway
services installed under the old name must be reinstalled
(`<new> gateway install`) — the old systemd/launchd unit is not migrated.

## alias

```
hermes profile alias <name> [--remove] [--name <alt>]
```

Regenerates (or removes) the shell wrapper at `~/.local/bin/<name>`.

**Flags**
- `--remove` — delete the wrapper instead of creating one.
- `--name <alt>` — create the wrapper under a custom name (useful when a
  profile name collides with an existing command on PATH).

## export

```
hermes profile export <name> [-o|--output <path>]
```

Writes a compressed `tar.gz` containing the full profile directory.

**Flags**
- `-o`, `--output <path>` — destination file. Defaults to `<name>.tar.gz`
  in the current directory.

**Example**
```
hermes profile export coder -o ~/backups/coder-$(date +%F).tar.gz
```

## import

```
hermes profile import <archive> [--name <name>]
```

Restores a profile from a tar.gz produced by `export`.

**Flags**
- `--name <name>` — override the profile name (by default inferred from
  the archive). Use this to avoid clobbering an existing profile or to
  rename during import.

## Global `-p` / `--profile` flag

```
hermes -p <name> <command...>
hermes --profile=<name> <command...>
```

Runs any Hermes command against a specific profile without touching the
sticky default. Position-independent:

```
hermes -p coder chat
hermes chat -p coder -q "hello"
hermes --profile=coder doctor
```

Equivalent to calling the generated alias directly:

```
coder chat
coder doctor
```

## Shell completion

```
hermes completion bash   # or: zsh
```

Generates a completion script that includes profile names and subcommands.
Source or symlink into your shell rc file.
