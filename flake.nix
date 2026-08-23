{
  description = "System packages";

  inputs = {
    # The final nixpkgs release branch that supports Intel macOS.
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-26.05-darwin";
  };

  outputs =
    { self, nixpkgs }:
    let
      allSystems = [
        "x86_64-linux"
        "aarch64-linux"
        "x86_64-darwin"
        "aarch64-darwin"
      ];
      bunVersion = "1.4.0";

      # nixpkgs' `bun` package lags upstream releases. Pin it to a newer
      # upstream build until nixpkgs catches up, then drop this overlay.
      # See: .agents/skills/nix-update/SKILL.md
      bunOverlay = final: prev: {
        bun = prev.bun.overrideAttrs (old: {
          version = bunVersion;
          src =
            {
              aarch64-darwin = final.fetchurl {
                url = "https://github.com/oven-sh/bun/releases/download/bun-v${bunVersion}/bun-darwin-aarch64.zip";
                hash = "sha256-xmnpf2Fk4cluBwF0jbmN+ndJKQjL2DlMdVcTSnNd44E=";
              };
              x86_64-darwin = final.fetchurl {
                url = "https://github.com/oven-sh/bun/releases/download/bun-v${bunVersion}/bun-darwin-x64.zip";
                hash = "sha256-HQIRuPHcmRGCNEaHrRXnLuhvFUhFpff6R3mUzTQd2bA=";
              };
              aarch64-linux = final.fetchurl {
                url = "https://github.com/oven-sh/bun/releases/download/bun-v${bunVersion}/bun-linux-aarch64.zip";
                hash = "sha256-SxozLuhhmD65O8/m93D/+U4+MbLDiL2uo8jtNeWO7Q4=";
              };
              x86_64-linux = final.fetchurl {
                url = "https://github.com/oven-sh/bun/releases/download/bun-v${bunVersion}/bun-linux-x64.zip";
                hash = "sha256-LQP7X7g6yLVnrKCigbLOGhoZ1Ij1bClo2Iw/Jekv5FI=";
              };
            }.${final.stdenv.hostPlatform.system} or old.src;
        });
      };

      forAllSystems =
        f:
        nixpkgs.lib.genAttrs allSystems (
          system:
          f {
            pkgs = import nixpkgs {
              inherit system;
              config.allowUnfree = true;
              overlays = [ bunOverlay ];
            };
          }
        );
    in
    {
      packages = forAllSystems (
        { pkgs }:
        {
          default =
            with pkgs;
            buildEnv {
              name = "system-packages";
              paths = [
                # Version control
                git
                gh
                lazygit

                # Build tools
                gnumake
                cmake
                pkg-config
                just

                # Programming languages
                rustup
                go
                python313
                uv
                nodejs
                deno
                bun

                # Shell and terminal
                fish
                zsh
                tmux
                starship

                # Coding agents - installed via Homebrew for latest versions
                # codex         # brew install --cask codex
                # claude-code   # brew install --cask claude-code

                # Modern CLI tools
                curl
                wget
                jq
                yq
                fzf
                ripgrep
                fd
                bat
                eza
                delta
                zoxide
                atuin

                # Development tools
                neovim
                direnv
                nix-direnv

                # Container tools
                docker-client
                docker-compose
                lazydocker

                # Nix development
                nil
                nixd
                nixpkgs-fmt

                # System monitoring
                htop
                btop
                ncdu

                # Network tools
                nmap
                mtr
                httpie

                # Media tools
                immich-go

                # File management
                tree
                unzip
                zip
                rsync
                repomix
                broot
                dust
                ast-grep
                sd
                dive

                # Kubernetes
                k9s

                # gRPC tools
                grpcurl
                grpcui
                buf

                # DNS tools
                doggo

                # Terminal multiplexer
                zellij
              ] ++ lib.optionals stdenv.isLinux [
                # Runtime for uv-managed binary wheels such as DuckDB.
                stdenv.cc.cc.lib
              ];
            };
        }
      );

      devShells = forAllSystems (
        { pkgs }:
        {
          default = pkgs.mkShell {
            packages = with pkgs; [
              self.packages.${pkgs.stdenv.hostPlatform.system}.default
              fish
              nixpkgs-fmt
              shellcheck
            ];
            shellHook = ''
              echo "🐠 Dotfiles development environment"
              echo "Run: make test-pre"
            '';
          };
        }
      );

      formatter = forAllSystems ({ pkgs }: pkgs.nixpkgs-fmt);
    };
}
