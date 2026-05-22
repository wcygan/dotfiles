---
name: nix-update
description: "Update this dotfiles flake.lock, compare key Nix package versions, verify the update, and summarize changed packages. Use for Nix flake maintenance in this repo."
---

# Nix Update

## Goal

Update this repository's Nix flake inputs and summarize important package version changes.

Success means `flake.lock` is updated, relevant packages are compared where possible, verification commands pass or failures are clearly reported, and the user knows how to install the updated profile.

Stop when the update is verified or the lockfile is restored after a failed update.

## Workflow

1. Inspect the current state:

```bash
git status --short
git diff -- flake.lock
git rev-parse HEAD:flake.lock >/dev/null 2>&1 && git show HEAD:flake.lock | rg '"rev"'
```

2. Capture the current nixpkgs commit from `flake.lock`.
3. Run the repo update command:

```bash
make update
```

4. Capture the new nixpkgs commit from `flake.lock`.
5. Read `flake.nix` and compare versions only for packages that are actually present.
6. Verify the update:

```bash
make test-pre
nix build .#default --dry-run
```

7. If verification fails because of the update, explain the failure and recommend reverting `flake.lock`. Do not revert user changes unless the user asks.

## Packages To Compare When Present

- Version control: `git`, `gh`, `lazygit`.
- Languages: `rustup`, `go`, `python3`, `deno`, `bun`.
- Shell and terminal: `fish`, `zsh`, `tmux`, `starship`, `zellij`.
- CLI tools: `ripgrep`, `fd`, `bat`, `eza`, `delta`, `fzf`, `jq`, `yq`.
- Editors and agents: `neovim`, `codex`, `claude-code`.
- Dev tools: `direnv`, `nix-direnv`.
- Containers: `docker-client`, `docker-compose`, `lazydocker`, `k9s`.
- System tools: `htop`, `btop`, `ncdu`.
- Other tools: `just`, `buf`, `grpcurl`, `dogdns`.

Use this form for version checks:

```bash
nix eval "github:NixOS/nixpkgs/<commit>#<package>.version" --raw
```

If a package cannot be evaluated, mark it `N/A` and continue.

## Version Summary

Report:

```markdown
## Flake Update

- nixpkgs: `<old>` -> `<new>`
- Compare: https://github.com/NixOS/nixpkgs/compare/<old>..<new>

## Package Updates

| Package | Old | New | Notes |
| --- | --- | --- | --- |
| git | 2.x | 2.y | patch |

## Verification

- `make test-pre`: pass/fail
- `nix build .#default --dry-run`: pass/fail

## Next Steps

- Review and commit `flake.lock`.
- Install the updated packages with `make install-packages` or `nix profile install . --priority 5`.
```

## Constraints

- Keep output concise and actionable.
- Run independent version comparisons in parallel when practical.
- Do not compare packages that are not in `flake.nix`.
- Do not imply that updating `flake.lock` updates the installed profile.
- Preserve unrelated working tree changes.
