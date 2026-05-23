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

      denoVersion = "2.8.0";
      denoArtifacts = {
        "x86_64-linux" = {
          target = "x86_64-unknown-linux-gnu";
          hash = "sha256-viyLU8jKHWa+dv65saUkQZ2nCLANTKB0z1xjPIHBYns=";
        };
        "aarch64-linux" = {
          target = "aarch64-unknown-linux-gnu";
          hash = "sha256-kzpqfSmFlXJxzSCFpaWhgyOYqiIaNU2qtWNRls8su64=";
        };
        "x86_64-darwin" = {
          target = "x86_64-apple-darwin";
          hash = "sha256-1utkO38a+yITn0qhfE2Xv33atOAeGCDtyzC5rlw6c5E=";
        };
        "aarch64-darwin" = {
          target = "aarch64-apple-darwin";
          hash = "sha256-26gTuLadYhjP+xElK55OYDbKLJ15hDzeNntLNpqvljQ=";
        };
      };

      mkPinnedDeno =
        pkgs:
        let
          inherit (pkgs) lib stdenv;
          artifact = denoArtifacts.${stdenv.hostPlatform.system};
        in
        stdenv.mkDerivation {
          pname = "deno";
          version = denoVersion;

          src = pkgs.fetchurl {
            url = "https://dl.deno.land/release/v${denoVersion}/deno-${artifact.target}.zip";
            hash = artifact.hash;
          };
          sourceRoot = ".";

          nativeBuildInputs =
            [ pkgs.unzip ]
            ++ lib.optionals stdenv.hostPlatform.isLinux [ pkgs.autoPatchelfHook ];
          buildInputs = lib.optionals stdenv.hostPlatform.isLinux [
            stdenv.cc.cc.lib
          ];

          dontConfigure = true;
          dontBuild = true;

          installPhase = ''
            runHook preInstall

            install -Dm755 deno "$out/bin/deno-unwrapped"
            printf '%s\n' \
              '#!/bin/sh' \
              'if [ "''${1:-}" = upgrade ]; then' \
              '  echo "deno is managed by the dotfiles Nix profile; update flake.nix instead." >&2' \
              '  exit 1' \
              'fi' \
              "exec \"$out/bin/deno-unwrapped\" \"\$@\"" \
              > "$out/bin/deno"
            printf '%s\n' \
              '#!/bin/sh' \
              "exec \"$out/bin/deno-unwrapped\" x \"\$@\"" \
              > "$out/bin/dx"
            chmod +x "$out/bin/deno"
            chmod +x "$out/bin/dx"

            runHook postInstall
          '';

          doInstallCheck = stdenv.buildPlatform.canExecute stdenv.hostPlatform;
          installCheckPhase = ''
            "$out/bin/deno" --version | grep "deno ${denoVersion}"
            upgradeLog="$(mktemp)"
            ! "$out/bin/deno" upgrade 2>"$upgradeLog"
            grep "managed by the dotfiles Nix profile" "$upgradeLog"
          '';

          meta = {
            homepage = "https://deno.com/";
            changelog = "https://deno.com/blog/v2.8";
            description = "Secure runtime for JavaScript and TypeScript";
            license = lib.licenses.mit;
            mainProgram = "deno";
            platforms = allSystems;
            sourceProvenance = with lib.sourceTypes; [ binaryNativeCode ];
          };
        };

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
                # Pinned until nixos-unstable carries Deno 2.8.
                (mkPinnedDeno pkgs)
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
