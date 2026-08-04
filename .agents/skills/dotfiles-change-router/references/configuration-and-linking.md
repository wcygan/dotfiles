# Configuration and Linking

Use this reference when exact paths or state-handling semantics matter.

## Configuration owners

| Application or concern | Tracked source |
| --- | --- |
| Fish abbreviations and aliases | `config/fish/conf.d/40-aliases.fish` |
| Fish functions | `config/fish/functions/<name>.fish` |
| Ghostty | `config/ghostty/` |
| lazygit | `config/git/lazygit/`, not `config/lazygit/` or `config/git/config` |
| Neovim | `config/nvim/` |
| Starship | `config/starship.toml` |
| tmux | `config/tmux/tmux.conf` |
| VS Code | `config/vscode/` |
| Zed | `config/zed/` |
| Zellij | `config/zellij/` |

Add packages required by an editor or application through `flake.nix`; do not
hide an installation requirement inside application configuration.

## Important destinations

- Starship: `config/starship.toml` to `~/.config/starship.toml`.
- tmux: `config/tmux/tmux.conf` to `~/.tmux.conf`.
- Bun: `config/bunfig.toml` to both `~/.bunfig.toml` and
  `~/.config/.bunfig.toml`.
- Deno: `config/deno/` to `~/.config/deno`; shell wrappers use this global
  dependency-management configuration only when no project `deno.json` or
  `deno.jsonc` is in scope.
- VS Code: `config/vscode/` is the tracked source; `scripts/link-config.sh`
  selects the platform-specific destination.

## Generic link behavior

- `make link-dry` invokes `scripts/link-config.sh --dry-run` and changes
  nothing.
- A physical destination is moved to `<destination>.backup.<timestamp>` before
  the link is created.
- Links are created or replaced idempotently with `ln -snf`.

## Specialized state boundaries

### Codex

- `config/codex/config.toml` is a template copied only when the local file is
  missing.
- Existing local `config.toml` state, including project trust entries, is
  preserved.
- `config/codex/AGENTS.md` and `config/codex/skills/` are linked.
- When `~/.codex/skills` is a physical directory, non-conflicting entries are
  migrated into the tracked skill directory, conflicts are backed up, and the
  repository symlink is then created.

### Pi

- Pi discovers shared global skills directly from `~/.agents/skills`.
- Do not create or link `~/.pi/agent/skills`; that duplicate surface causes
  skill-name collisions.
- Credentials, models, sessions, logs, and caches remain machine-local.
