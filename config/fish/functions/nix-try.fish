function nix-try
  if test (count $argv) -lt 1
    echo "Usage: nix-try <package>"
    return 1
  end
  set pkg $argv[1]
  nix-shell -p $pkg --run "$pkg --version || $pkg --help || echo 'Loaded: $pkg'"
end
