# Dotfiles Flake Template
# Multi-package environment for dotfiles management

{
  description = "Dotfiles system packages";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      allSystems = [
        "x86_64-linux"
        "aarch64-linux"
        "x86_64-darwin"
        "aarch64-darwin"
      ];

      forAllSystems = f:
        nixpkgs.lib.genAttrs allSystems (system:
          f {
            pkgs = import nixpkgs {
              inherit system;
              config.allowUnfree = true;
            };
          }
        );
    in
    {
      packages = forAllSystems ({ pkgs }: {
        default = with pkgs; buildEnv {
          name = "system-packages";
          paths = [
            # Version control
            git
            gh

            # Shell and terminal
            fish
            starship
            tmux

            # Modern CLI tools
            ripgrep
            fd
            bat
            eza
            fzf

            # Development tools
            neovim
            direnv
            nix-direnv

            # Add your packages here
          ];
        };
      });

      devShells = forAllSystems ({ pkgs }: {
        default = pkgs.mkShell {
          packages = with pkgs; [
            fish
            nixpkgs-fmt
            shellcheck
          ];
          inputsFrom = [ self.packages.${pkgs.system}.default ];
          shellHook = ''
            echo "🐠 Dotfiles development environment"
          '';
        };
      });

      formatter = forAllSystems ({ pkgs }: pkgs.nixpkgs-fmt);
    };
}
