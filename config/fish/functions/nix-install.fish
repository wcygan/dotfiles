function nix-install
  if test (count $argv) -lt 1
    echo "Usage: nix-install <package>"
    return 1
  end
  set pkg $argv[1]
  echo "Searching for package: $pkg"
  nix search nixpkgs $pkg | head -n 20
  read -P "Install package? (y/n) " -l reply
  if string match -qi 'y*' -- $reply
    nix profile install "nixpkgs#$pkg"
  end
end
