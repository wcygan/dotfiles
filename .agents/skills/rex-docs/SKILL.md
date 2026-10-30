---
name: rex-docs
description: "Look up Rex (Superlogical's terminal multiplexer) behavior in its official docs and the installed rex CLI before answering or changing Rex setup in this repository. Use for Rex config (init.lua, rex.bind, rex.action, modes, layouts), agent integration (rex skill setup, hooks), PATH or shell issues inside Rex, remote hosts, or any 'how does Rex do X' question. Keywords: rex, superlogical, init.lua, rex skill, rex config, multiplexer, session, block, pane"
---

# Rex Docs

## Goal

Answer Rex questions and make Rex changes from evidence: the official docs for
intent and the installed `rex` binary for what this machine actually supports.
Rex is in beta and changes quickly, so never rely on memory for action names,
flags, or Lua APIs.

## Where the docs are

The docs are built for agents. Prefer these over scraping HTML pages.

| Need | Source |
| --- | --- |
| Page index with one-line summaries | `https://www.superlogical.com/rex/docs/llms.txt` |
| One page as markdown | Append `.md` to any docs URL, e.g. `.../rex/docs/customize/config.md` |
| Search by topic | `uv run scripts/search.py "QUERY" [-n LIMIT]`, which wraps `.../rex/docs/search.json?q=` |
| Every page in one file | `https://www.superlogical.com/rex/docs/llms-full.txt` (large; search first) |

Fetch with `curl -sL`. Start with `scripts/search.py`, then read the whole page
on each hit's `page:` line.

Pages you will need most often:

- `customize/config.md`: where `init.lua` lives, `check` and `reload`, `require`
- `customize/keyboard-shortcuts.md`, `key-sequences.md`, `key-modes.md`, `actions.md`
- `reference/lua.md`: the full Lua API
- `automate/agent-skill.md`: `rex skill setup`, hooks, supported agents
- `automate/cli.md`: CLI targets, environment variables, and the PATH and Nix sections
- `linux/remote-access.md`: network listeners and their security model

## Ask the installed binary

The docs describe the latest release. The local binary is the truth for this
machine. Check it before writing config:

```sh
rex version                       # version and API revision
rex <command> --help              # flags for this version
rex actions                       # server and block actions
rex -C <client> actions           # actions the Mac app offers (rex client ls for labels)
rex config check [PATH]           # validate init.lua or a draft without applying it
rex keymap                        # merged bindings from the running server
rex skill status                  # agent skill and hook install state
rex skill show                    # the guide Rex's own skill gives agents
rex api                           # server API methods
```

Read-only commands still start a missing local server unless you pass
`--autostart=false`.

## Facts verified on this setup

- `rex keymap` lists only bindings from `init.lua`. The Mac app's built-in
  shortcuts aren't in it; check the app's Settings for those before binding
  over a Cmd shortcut.
- Fonts, themes, and appearance live in the Mac app, not in `init.lua`.
- `rex.on` event handlers only work in scripts run with `rex do`, not in
  `init.lua`.
- Rex starts each terminal with the account's login shell, `/bin/zsh`.
  `~/.zshrc` then runs `exec fish -l`, so Rex panes run fish just as Ghostty does.
- Fish startup moves Nix and other paths ahead of `$REX_BIN_DIR`. The last
  block of `config/fish/config.fish` moves it back to the front;
  `tests/test_fish_rex_path.py` covers it. Keep that block last.
- `rex skill setup` has been run for Claude Code, Codex, OpenCode, and Pi. It
  owns `~/.claude/skills/rex`, `~/.agents/skills/rex`, and a `SessionStart`
  hook in `~/.claude/settings.json` and `~/.codex/hooks.json`. Those are
  machine-local; rerun `rex skill setup` on each machine instead of copying
  them. `~/.agents/skills` is also the `agent-skills` catalog root; see
  `$agent-skills-integration` before treating `rex` there as stale.
- Codex filters the environment its shell commands get
  (`[shell_environment_policy]` in the machine-local `~/.codex/config.toml`).
  It must pass `REX_*` through and put Rex's bin directory on its fixed `PATH`,
  or Codex reports `rex: command not found` inside Rex. The repo's Codex
  template has no such section, so check this on each new machine.

Recheck these against the current binary and docs when they matter. They were
true when written, not necessarily now.

## Changing Rex config in this repository

`config/rex/` is a managed link to `~/.config/rex` (see
`src/dotfiles_setup/links.py`). `config/rex/init.lua` keeps the Ghostty
shortcuts from `config/ghostty/config` so switching terminals keeps the same
keys.

1. Edit `config/rex/init.lua`. Split large configs with `require("name")` and
   a sibling `name.lua`.
2. Validate: `rex config check config/rex/init.lua`.
3. Apply: `rex config reload` on the machine running the server. Reload is
   refused over a remote connection.
4. Confirm: `rex -C <client> keymap` shows each binding with its `init.lua`
   line and reports actions the client doesn't have.

The Linux and FreeBSD server reads the same file, so include
`$cross-platform-guardian` when a binding or action is macOS-specific.

## Completion

Report which doc pages and CLI output support the answer, the Rex version
checked, and anything the docs and the local binary disagreed on.
