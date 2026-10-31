{
  description = "System packages";

  inputs = {
    # The final nixpkgs release branch that supports Intel macOS.
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-26.05";
    unstable.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
  };

  outputs =
    { self, nixpkgs, unstable }:
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
            let
              # Some clients do not apply NSS intermediate-certificate distrust.
              cacert = pkgs.cacert.override {
                blacklist = [ "Comodo AAA Services root" ];
              };
              curl = pkgs.curl.overrideAttrs (old: {
                configureFlags = builtins.filter (flag: flag != "--without-ca-bundle" && flag != "--without-ca-path") old.configureFlags ++ [
                  "--with-ca-bundle=${cacert}/etc/ssl/certs/ca-bundle.crt"
                  "--with-ca-path=${cacert.hashed}/etc/ssl/certs"
                ];
              });
              modern = if pkgs.stdenv.hostPlatform.system == "x86_64-darwin" then pkgs else
              import unstable {
                system = pkgs.stdenv.hostPlatform.system;
                config.allowUnfree = true;
              };
              inherit (modern) hyperfine typst graphviz ocrmypdf ffmpeg yt-dlp;
              # Unstable no longer supports Intel macOS; retain its uv binary fallback.
              uv = if pkgs.stdenv.hostPlatform.system != "x86_64-darwin" then modern.uv else
              pkgs.stdenvNoCC.mkDerivation {
                pname = "uv";
                version = "0.13.4";
                src = pkgs.fetchurl {
                  url = "https://github.com/astral-sh/uv/releases/download/0.13.4/uv-x86_64-apple-darwin.tar.gz";
                  hash = "sha256-e+Lc0xYSL0s+Wgp4ifYkgmbBRCU3ThBf99yXeRhGA6Y=";
                };
                dontConfigure = true;
                dontBuild = true;
                installPhase = "install -Dm755 uv uvx -t $out/bin";
                meta = pkgs.uv.meta;
              };
              zed = pkgs.symlinkJoin {
                name = "zed-${modern.zed-editor.version}";
                paths = [ modern.zed-editor ];
                postBuild = "ln -s zeditor $out/bin/zed";
              };
              # nixpkgs still ships Bun before its certificate security fix.
              bun = modern.bun.overrideAttrs {
                version = "1.4.4";
                src = pkgs.fetchurl {
                  url = "https://github.com/oven-sh/bun/releases/download/bun-v1.4.4/bun-${{
                      aarch64-darwin = "darwin-aarch64";
                      x86_64-darwin = "darwin-x64";
                      aarch64-linux = "linux-aarch64";
                      x86_64-linux = "linux-x64-baseline";
                  }.${pkgs.stdenv.hostPlatform.system}}.zip";
                  sha256 = {
                    aarch64-darwin = "c240d7f0ccb90c263a849fcdb09b7ee62630d921348ed6aafda86b9d577bc510";
                    x86_64-darwin = "50a3491f73abc2fe81673171a85762d3bc2cc1680ccecadd983de99adf77977e";
                    aarch64-linux = "baa6bb36f51d6e58561e02bbea825038a9df454f673d6d776e8bbf86f8c7850e";
                    x86_64-linux = "e0446eb55995772eb9894bebae9a6be368d985a8b9271ee124486f9946eedd76";
                  }.${pkgs.stdenv.hostPlatform.system};
                };
              };

            in
            with pkgs;
            buildEnv {
              name = "system-packages";
              paths = [
                # Version control
                git
                gh
                lazygit
                jujutsu

                # Build tools
                gnumake
                cmake
                pkg-config
                act
                just

                # Programming languages
                rustup
                go
                python313
                uv
                nodejs
                bun
                pnpm

                # Shell and terminal
                fish
                zsh
                tmux
                starship

                # Coding agents - installed via Homebrew for latest versions
                # codex         # brew install --cask codex
                # claude-code   # brew install --cask claude-code

                # Modern CLI tools
                cacert
                cacert.hashed
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
                hyperfine
                atuin

                # Development tools
                neovim
                zed
                direnv
                nix-direnv
                temporal-cli

                # Container tools
                docker-client
                docker-compose
                lazydocker
                crane
                skaffold

                # Nix development
                nil
                nixd
                nixpkgs-fmt

                # System monitoring
                htop
                btop
                ncdu

                # Encryption
                age
                sops

                # Network tools
                nmap
                mtr
                httpie

                # Media and document tools
                immich-go
                ffmpeg
                yt-dlp
                exiftool
                poppler-utils
                ocrmypdf
                typst
                graphviz

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
                kubectl
                kubent

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
              export NIX_SSL_CERT_FILE="''${NIX_SSL_CERT_FILE-${self.packages.${pkgs.stdenv.hostPlatform.system}.default}/etc/ssl/certs/ca-bundle.crt}"
              export SSL_CERT_FILE="''${SSL_CERT_FILE-${self.packages.${pkgs.stdenv.hostPlatform.system}.default}/etc/ssl/certs/ca-bundle.crt}"
              export SSL_CERT_DIR="''${SSL_CERT_DIR-${self.packages.${pkgs.stdenv.hostPlatform.system}.default}/etc/ssl/certs}"
              echo "🐠 Dotfiles development environment"
              echo "Run: make test-pre"
            '';
          };
        }
      );

      formatter = forAllSystems ({ pkgs }: pkgs.nixpkgs-fmt);
    };
}
