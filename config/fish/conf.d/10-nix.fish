# Priority PATH setup - Nix profile packages take precedence
# Load order: Nix > user paths > brew/dnf > system paths

# IMPORTANT: fish_add_path adds to fish_user_paths which persists across sessions
# We use --path to only modify PATH for this session, and --move so existing
# inherited paths are moved to the requested priority.

# 1. Add system and user-installed binaries as fallback paths.
# macOS: Homebrew paths
if test -d /opt/homebrew/bin
  fish_add_path --path --move --prepend /opt/homebrew/bin
else if test -d /usr/local/bin
  fish_add_path --path --move --prepend /usr/local/bin
end

# Bun binaries are a fallback to the user-local npm prefix below. Both may
# install the same CLI, and ~/.local/bin is the repo-managed npm location.
if test -d $HOME/.bun/bin
  fish_add_path --path --move --prepend $HOME/.bun/bin
end

# User-specific binary locations (for manual installs)
if test -d $HOME/.local/bin
  fish_add_path --path --move --prepend $HOME/.local/bin
end
if test -d $HOME/bin
  fish_add_path --path --move --prepend $HOME/bin
end

# TiUP binaries (installed by https://tiup-mirrors.pingcap.com/install.sh)
if test -d $HOME/.tiup/bin
  fish_add_path --path --move --prepend $HOME/.tiup/bin
end

# Cargo/Rust binaries
if test -d $HOME/.cargo/bin
  fish_add_path --path --move --prepend $HOME/.cargo/bin
end

# Go binaries
if test -d $HOME/go/bin
  fish_add_path --path --move --prepend $HOME/go/bin
end

# 2. Prefer Nix profile bins for reproducible tools.
# Add system-wide Nix profile first so the user profile can take precedence.
if test -d /nix/var/nix/profiles/default/bin
  fish_add_path --path --move --prepend /nix/var/nix/profiles/default/bin
end

# Ensure user Nix bins are on PATH (works for both single- and multi-user).
if test -d $HOME/.nix-profile/bin
  fish_add_path --path --move --prepend $HOME/.nix-profile/bin
end

# Set flake features at the process level (good default)
set -gx NIX_CONFIG 'experimental-features = nix-command flakes'

# If multi-user daemon profile exists, import environment once per shell.
# We avoid sourcing bash in fish; instead, we ask bash to print env and we import it.
if test -f /nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh
  # Prevent repeated imports in the same session
  if not set -q __nix_env_imported
    for line in (bash -lc 'source /nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh >/dev/null 2>&1; env' | string split0)
      set kv (string split -m1 '=' -- $line)
      set -l k $kv[1]
      set -l v $kv[2]
      # Only set variables that aren't already exported by fish or that we know we want
      if test -n "$k"; and test -n "$v"
        # Skip PATH here; fish_add_path handles ordering better
        if test $k != PATH
          set -gx $k $v
        end
      end
    end
    set -g __nix_env_imported 1
  end
end

# Handy abbr/aliases (fish native)
abbr -a nix-update 'nix flake update && nix profile upgrade --no-write-lock-file'
abbr -a nix-search 'nix search nixpkgs'
abbr -a nix-list   'nix profile list'
abbr -a nix-clean  'nix-collect-garbage -d'
abbr -a nix-shell-pure 'nix-shell --pure'
abbr -a nix-build-dry 'nix build --dry-run --no-write-lock-file'
