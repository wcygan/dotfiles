# Nix + Dotfiles (Cross‑Platform)

Reproducible tooling via **Nix (flakes)**, portable configs via **symlinks**.

* **Platforms**: macOS (Intel/Apple Silicon), Ubuntu, Fedora
* **Installer**: [Determinate Systems Nix Installer](https://github.com/DeterminateSystems/nix-installer)
* **Shells supported**: fish (native), bash/zsh (via `config/shell-nix.sh`)

---

## Prerequisites

* macOS 12+ or a recent Ubuntu/Fedora
* `curl` and a POSIX shell available (default on all three)
* For Ubuntu/Fedora: user must be in the `sudoers` group

> The Determinate installer handles `/nix` mount setup, users/groups, and SELinux policy (Fedora) automatically.

---

## Quick Start

### 1) Install Nix (all platforms)

```bash
# Determinate Systems – single, cross‑platform command
curl --proto '=https' --tlsv1.2 -sSf -L https://install.determinate.systems/nix | sh -s -- install
```

**After install**: open a **new shell** or source the daemon profile if present:

```bash
# multi‑user daemon (preferred on macOS + most Linux)
[ -f /nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh ] \
  && . /nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh
```

Verify:

```bash
nix --version
```

### 2) Clone and bootstrap

```bash
# Clone this repo
REPO_DIR="$HOME/nix-dotfiles"   # change if you want
git clone <YOUR-REPO-URL> "$REPO_DIR"
cd "$REPO_DIR"

# One‑shot: install Nix (if missing), install packages, link configs
./install.sh
```

What `./install.sh` does:

1. Runs `scripts/install-nix.sh` (idempotent) using Determinate installer
2. Installs packages from `flake.nix` via `scripts/install-packages.sh`
3. Symlinks configs via `scripts/link-config.sh`

### 3) Shell integration

**fish (recommended)**

* Config is symlinked into `~/.config/fish` (see `config/fish/*`).
* Open a new **login** fish, or run:

```fish
exec fish -l
```

---

## Project Layout

```
config/
  fish/                 # fish config (conf.d, functions, config.fish)
  shell-nix.sh          # bash/zsh helper to load Nix env
scripts/
  install-nix.sh        # Determinate Nix installer wrapper
  install-packages.sh   # install packages from flake.nix
  link-config.sh        # symlink configs into ~/.config and $HOME
flake.nix               # package set (cross‑platform)
install.sh              # orchestrated installer
Makefile                # common tasks (install, test, update, etc.)
```

---

## Uninstall / Clean Up (Selective)

* Remove symlinks only:

```bash
make uninstall
```

* Reclaim space from old package generations:

```bash
nix-collect-garbage -d
```

> Full Nix removal differs by OS; use the official uninstaller from Determinate/NixOS docs if you truly want to remove `/nix`.

---
