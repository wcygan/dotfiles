# Change Routes

Use the narrowest matching route. Combine rows when one request spans multiple
responsibilities.

| Requested outcome | Repository owner and route |
| --- | --- |
| Add a workstation CLI package | Add it to `flake.nix`; install through the repository Nix profile workflow. |
| Add a Fish abbreviation or alias for a tool | Use `config/fish/conf.d/40-aliases.fish`; guard optional tools with `type -q <tool>`. |
| Add a reusable Fish function | Create `config/fish/functions/<name>.fish`. |
| Add or change XDG-compliant application configuration | Put editable files under `config/**` and wire an idempotent link in `scripts/link-config.sh`. |
| Configure a legacy non-XDG program | Verify its native location instead of forcing `~/.config`; tmux uses `~/.tmux.conf`. |
| Add one project's development environment | Use the repository's documented nix-direnv pattern rather than adding project-only dependencies globally. |
| Add an external agent skill | Add `<owner>/<repo>@<skill>` to `SKILLS` in `scripts/install-skills.sh`, accept only an official publisher, then run `make install-skills`. |
| Add a project-local Pi skill | Put it under `.agents/skills/<name>/`; noninteractive Pi must trust project resources, normally with the one-run `--approve` flag. |
| Add a repository-authored global Pi skill | Put a `SKILL.md`-rooted directory under `config/pi/skills/<name>/`; link only that skills leaf to `~/.pi/agent/skills`. |
| Add a reusable global Codex workflow skill | Put it under `config/codex/skills/<name>/` and validate the catalog with `./tests/test-codex-skills.sh`. |
| Update the Nix package set | Run `make update`; do not edit or recreate `flake.lock` by hand. |
| Preview config links | Run `make link-dry`; it invokes `scripts/link-config.sh --dry-run`. |

## Configuration owners

- Fish: `config/fish/`
- Ghostty: `config/ghostty/`
- lazygit: `config/git/lazygit/`
- Neovim: `config/nvim/`
- Starship: `config/starship.toml`
- Zed: `config/zed/`
- Zellij: `config/zellij/`

Use the owning configuration route first. Add cross-platform review when a
change introduces executable paths, shell startup behavior, platform
conditionals, or package-availability assumptions.

For exact source and destination paths, especially lazygit, tmux, Bun, Deno,
Codex, Pi, and VS Code, read `configuration-and-linking.md`.
