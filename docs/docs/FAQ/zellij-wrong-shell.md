# Zellij Uses Wrong Shell on macOS

Zellij panes open with zsh instead of fish.

## Problem

Zellij silently falls back to the system default shell when `default_shell` points to a nonexistent path.

**Root cause:** The config uses Linux paths (`/home/wcygan/`) instead of macOS paths (`/Users/wcygan/`).

## Solution

In `config/zellij/config.kdl`, update hardcoded paths to match the current OS:

```kdl
// Linux
default_shell "/home/wcygan/.nix-profile/bin/fish"
layout_dir "/home/wcygan/.config/zellij/layouts"

// macOS (correct for this machine)
default_shell "/Users/wcygan/.nix-profile/bin/fish"
layout_dir "/Users/wcygan/.config/zellij/layouts"
```

After editing, kill and recreate the session:

```bash
zellij kill-session <name> && zellij -s <name>
```

## Verification

1. Open a new Zellij session
2. Run `echo $SHELL` or `fish --version` in a pane
3. Expected: fish shell prompt and version output

## Related Files

- `config/zellij/config.kdl` - Zellij configuration
