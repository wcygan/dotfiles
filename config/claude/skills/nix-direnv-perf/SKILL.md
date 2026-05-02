---
name: nix-direnv-perf
description: Diagnose and prevent slow/contending nix-direnv rebuilds in this dotfiles repo. Use when a `flake.lock` update triggers concurrent rebuilds, terminals hang on `direnv export`, or fish/Nix daemon troubleshooting. Keywords nix-direnv, flake.lock, direnv export, nix-daemon, concurrent rebuild, .envrc.
---

# nix-direnv Performance & Troubleshooting

Repo-specific guidance for the `~/Development/dotfiles` flake. Loaded when terminals hang on direnv, the Nix daemon misbehaves, or you're about to bump `flake.lock`.

## Concurrent Rebuild Problem

When `flake.lock` changes, every open terminal with direnv tries to rebuild simultaneously:

- Lock contention (Nix serializes operations)
- Redundant downloads (each shell fetches the same closures)
- 3-10x slower rebuilds, high CPU/memory

Detect with:

```bash
ps aux | grep -E 'direnv export|nix.*print-dev-env'
# Multiple sessions = contention
```

## Prevention

**1. Close extra terminals before flake updates.** Keep ONE terminal in `dotfiles/` while running `nix flake update` or editing `flake.lock`. Reopen others after the rebuild completes.

**2. Prime the cache manually:**

```bash
cd ~/Development/dotfiles
nix build --no-link '.#devShells.aarch64-darwin.default'
```

**3. Optional `--impure` for faster eval:**

```bash
echo 'use flake --impure' > .envrc
direnv allow
```

## Emergency Fix (rebuild already in progress)

```bash
pkill -f 'direnv export'
pkill -f 'nix.*print-dev-env'
ps aux | grep -E 'direnv|nix.*print-dev-env' | grep -v grep   # verify
# Close extra dotfiles terminals; the remaining one resumes
```

## General Nix/direnv Troubleshooting

- Source daemon: `. /nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh`
- Fish not seeing Nix? `exec fish -l` and confirm `config/fish/conf.d/10-nix.fish`
- Fedora: keep SELinux enforcing; the Determinate installer ships the policy
- Direnv not loading? `direnv status` and ensure `.envrc` is allowed
- macOS installer issues? System Settings → Privacy & Security for blocked components

## Best Practices When Bumping Packages

- `nix flake update` from ONE terminal with others closed
- Pre-build with `nix build` before opening multiple shells
- First post-update build takes 2-5 min; subsequent shells are instant
