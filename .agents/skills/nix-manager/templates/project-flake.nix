# Project Development Flake Template
# Full-featured flake with packages, dev shells, apps, and checks

{
  description = "Project development environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
          config.allowUnfree = true;
        };
      in
      {
        # Packages
        packages = {
          default = self.packages.${system}.my-app;

          my-app = pkgs.stdenv.mkDerivation {
            name = "my-app";
            src = ./.;
            buildInputs = with pkgs; [ ];
            installPhase = ''
              mkdir -p $out/bin
              cp my-app $out/bin/
            '';
          };
        };

        # Development shells
        devShells = {
          default = pkgs.mkShell {
            packages = with pkgs; [
              # Language toolchain
              nodejs
              python3

              # Development tools
              git
              gh

              # LSP and formatters
              nodePackages.typescript-language-server
              nodePackages.prettier
            ];

            shellHook = ''
              echo "🚀 Project development environment"
              echo "Node: $(node --version)"
              echo "Python: $(python3 --version)"
            '';
          };

          # CI-specific shell
          ci = pkgs.mkShell {
            packages = with pkgs; [
              nodejs
              git
            ];
          };
        };

        # Runnable apps
        apps = {
          default = {
            type = "app";
            program = "${self.packages.${system}.default}/bin/my-app";
          };

          test = {
            type = "app";
            program = "${pkgs.writeShellScript "test" ''
              ${pkgs.nodejs}/bin/npm test
            ''}";
          };
        };

        # CI checks
        checks = {
          package-builds = self.packages.${system}.default;

          format-check = pkgs.runCommand "format-check" { } ''
            ${pkgs.nixpkgs-fmt}/bin/nixpkgs-fmt --check ${./.}
            touch $out
          '';

          lint = pkgs.runCommand "lint" { } ''
            ${pkgs.nodePackages.eslint}/bin/eslint .
            touch $out
          '';
        };

        # Formatter
        formatter = pkgs.nixpkgs-fmt;
      }
    );
}
