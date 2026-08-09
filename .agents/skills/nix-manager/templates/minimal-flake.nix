# Minimal Flake Template
# Single-package flake for simple projects

{
  description = "Minimal flake template";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      # Supported systems
      systems = [
        "x86_64-linux"
        "aarch64-linux"
        "x86_64-darwin"
        "aarch64-darwin"
      ];

      # Helper to generate attributes for all systems
      forAllSystems = f:
        nixpkgs.lib.genAttrs systems (system:
          f {
            pkgs = import nixpkgs {
              inherit system;
              config.allowUnfree = true;
            };
          }
        );
    in
    {
      # Default package
      packages = forAllSystems ({ pkgs }: {
        default = pkgs.hello;  # Replace with your package
      });

      # Development shell
      devShells = forAllSystems ({ pkgs }: {
        default = pkgs.mkShell {
          packages = with pkgs; [
            # Development tools
            git
          ];
        };
      });

      # Formatter for `nix fmt`
      formatter = forAllSystems ({ pkgs }: pkgs.nixpkgs-fmt);
    };
}
