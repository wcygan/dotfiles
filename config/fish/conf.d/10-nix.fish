# Ensure Nix bins are on PATH (works for both single- and multi-user)
if test -d $HOME/.nix-profile/bin
  fish_add_path $HOME/.nix-profile/bin
end

# Add system-wide Nix profile to PATH (for multi-user installations)
if test -d /nix/var/nix/profiles/default/bin
  fish_add_path /nix/var/nix/profiles/default/bin
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
abbr -a nix-update 'nix flake update && nix profile upgrade'
abbr -a nix-search 'nix search nixpkgs'
abbr -a nix-list   'nix profile list'
abbr -a nix-clean  'nix-collect-garbage -d'
abbr -a nix-shell-pure 'nix-shell --pure'
abbr -a nix-build-dry 'nix build --dry-run'
