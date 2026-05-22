{
  description = "System packages";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
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

      forAllSystems =
        f:
        nixpkgs.lib.genAttrs allSystems (
          system:
          f {
            pkgs = import nixpkgs {
              inherit system;
              config.allowUnfree = true;
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
                python3
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
