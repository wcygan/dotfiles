# Nix Manager Reference Guide

Advanced patterns, troubleshooting, and Determinate Systems best practices.

## Flake Architecture Deep Dive

### Input Patterns

#### Following Inputs

Prevent duplicate dependencies by making inputs follow each other:

```nix
inputs = {
  nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  home-manager.url = "github:nix-community/home-manager";
  home-manager.inputs.nixpkgs.follows = "nixpkgs";  # Use same nixpkgs

  flake-utils.url = "github:numtide/flake-utils";
};
```

**Benefits:**
- Reduces closure size (no duplicate nixpkgs)
- Faster evaluation
- Consistent package versions across inputs

#### Input Types

```nix
inputs = {
  # GitHub repository
  nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  # Git repository
  my-repo.url = "git+https://git.example.com/repo.git?ref=main";

  # Local path (useful for development)
  local-flake.url = "path:../other-project";

  # Tarball
  my-package.url = "https://example.com/package.tar.gz";

  # Indirect (flake registry)
  nixpkgs-stable.url = "nixpkgs/nixos-23.11";
};
```

### Output Patterns

#### Multi-System Helper

**forAllSystems pattern (used in this repo):**

```nix
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
in {
  packages = forAllSystems ({ pkgs }: {
    default = pkgs.hello;
  });
}
```

**Alternative using flake-utils:**

```nix
{
  inputs.flake-utils.url = "github:numtide/flake-utils";

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let pkgs = import nixpkgs { inherit system; };
      in {
        packages.default = pkgs.hello;
        devShells.default = pkgs.mkShell { };
      }
    );
}
```

#### Common Output Types

**Packages:**
```nix
packages = forAllSystems ({ pkgs }: {
  default = pkgs.hello;
  custom-tool = pkgs.callPackage ./packages/custom-tool.nix { };
});
```

**Development Shells:**
```nix
devShells = forAllSystems ({ pkgs }: {
  default = pkgs.mkShell {
    packages = with pkgs; [ nodejs python3 ];
    shellHook = ''
      echo "Welcome to dev environment"
      export PROJECT_ROOT=$(pwd)
    '';
  };

  # Multiple shells for different purposes
  ci = pkgs.mkShell {
    packages = with pkgs; [ git gh ];
  };
});
```

**Apps (runnable executables):**
```nix
apps = forAllSystems ({ pkgs }: {
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
});
```

**Checks (CI validation):**
```nix
checks = forAllSystems ({ pkgs }: {
  package-builds = self.packages.${system}.default;

  format-check = pkgs.runCommand "format-check" {} ''
    ${pkgs.nixpkgs-fmt}/bin/nixpkgs-fmt --check ${./.}
    touch $out
  '';

  tests = pkgs.runCommand "run-tests" {} ''
    ${pkgs.nodejs}/bin/npm test
    touch $out
  '';
});
```

**Formatter:**
```nix
formatter = forAllSystems ({ pkgs }: pkgs.nixpkgs-fmt);
# Or: pkgs.alejandra for alternative formatter
```

## Advanced Package Management

### Overlays for Customization

**Problem**: Need bleeding-edge package from unstable while using stable channel

**Solution**: Use overlays

```nix
{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-23.11";
    nixpkgs-unstable.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs, nixpkgs-unstable }: {
    packages = forAllSystems ({ system }:
      let
        pkgs = import nixpkgs {
          inherit system;
          overlays = [
            # Replace specific packages with unstable versions
            (final: prev: {
              neovim = nixpkgs-unstable.legacyPackages.${system}.neovim;
              ripgrep = nixpkgs-unstable.legacyPackages.${system}.ripgrep;
            })
          ];
        };
      in {
        default = pkgs.buildEnv { paths = [ pkgs.neovim pkgs.ripgrep ]; };
      }
    );
  };
}
```

### Package Overrides

**Modify package attributes:**

```nix
{
  packages.default = pkgs.buildEnv {
    paths = [
      # Override Neovim with plugins
      (pkgs.neovim.override {
        configure = {
          packages.myPlugins = with pkgs.vimPlugins; {
            start = [ vim-nix telescope-nvim ];
          };
        };
      })

      # Override Python with specific packages
      (pkgs.python3.withPackages (ps: with ps; [
        requests
        numpy
        pandas
      ]))
    ];
  };
}
```

### Version Pinning

**Pin specific package version using Nix expressions:**

```nix
let
  # Pin to specific nixpkgs revision
  pinnedPkgs = import (fetchTarball {
    url = "https://github.com/NixOS/nixpkgs/archive/commitsha.tar.gz";
    sha256 = "0000000000000000000000000000000000000000000000000000";
  }) { inherit system; };
in
{
  packages.default = pkgs.buildEnv {
    paths = [
      pinnedPkgs.go  # Use specific Go version
      pkgs.rust      # Use current nixpkgs version
    ];
  };
}
```

## Performance Optimization

### Binary Cache Configuration

**Determinate installer sets up:**
- `cache.nixos.org` (official Nix cache)
- `cache.flakehub.com` (FlakeHub cache)
- `install.determinate.systems` (Determinate cache)

**Check cache configuration:**
```bash
cat ~/.config/nix/nix.conf
```

**Expected:**
```
substituters = https://cache.nixos.org https://cache.flakehub.com
trusted-public-keys = cache.nixos.org-1:6NCHdD59X431o0gWypbMrAURkbJ16ZPMQFGspcDShjY= ...
```

### Evaluation Caching

**Enable evaluation cache:**
```bash
nix --option eval-cache true flake show
```

**Clear evaluation cache:**
```bash
rm -rf ~/.cache/nix/eval-cache-v*
```

### Store Optimization

**Deduplicate identical files:**
```bash
nix store optimise
```

**Check store size:**
```bash
du -sh /nix/store
nix store info
```

**Aggressive cleanup:**
```bash
# Remove all old generations
nix-collect-garbage -d

# Remove unreferenced store paths
nix store gc

# Optimize after cleanup
nix store optimise
```

## Troubleshooting Guide

### Build Failures

#### Missing Dependencies

**Error:**
```
error: undefined variable 'pkg-config'
```

**Solution**: Add to `buildInputs` or package list

#### Hash Mismatch

**Error:**
```
error: hash mismatch in fixed-output derivation
  specified: sha256-AAAA...
  got:       sha256-BBBB...
```

**Solution**: Update hash to match actual value (copy from error message)

#### Platform Unsupported

**Error:**
```
error: package 'x86_64-darwin-package' is not supported on 'aarch64-darwin'
```

**Solution**: Use platform conditionals

```nix
paths = [
  # Universal packages
  git
] ++ lib.optionals (system == "x86_64-darwin") [
  # Intel Mac only
  rosetta-specific-package
];
```

### Flake Evaluation Issues

#### Infinite Recursion

**Error:**
```
error: infinite recursion encountered
```

**Common cause**: Self-referencing attributes

**Solution**: Use `rec { }` carefully or break recursion with `let` bindings

#### Type Errors

**Error:**
```
error: value is a list while a set was expected
```

**Solution**: Check attribute types, use `lib.attrsets` functions

### Lock File Problems

#### Dirty Tree

**Error:**
```
warning: Git tree '/path/to/repo' is dirty
```

**Solutions:**
```bash
# Commit changes
git add flake.nix flake.lock
git commit -m "Update flake"

# Or allow dirty (not recommended)
nix flake check --impure
```

#### Merge Conflicts

**Resolve lock file conflicts:**
```bash
# Always regenerate lock file after merge
rm flake.lock
nix flake update
git add flake.lock
```

### Network Issues

#### Cache Download Failures

**Error:**
```
error: unable to download 'https://cache.nixos.org/...'
```

**Solutions:**
1. Check network connectivity
2. Try different substituter
3. Build from source: `nix build --no-substituters`

#### GitHub Rate Limiting

**Error:**
```
error: unable to access 'https://github.com/...': GitHub API rate limit exceeded
```

**Solution**: Authenticate with GitHub

```bash
# Create GitHub token (read-only, public repos)
export GITHUB_TOKEN=ghp_...

# Or use SSH instead of HTTPS
inputs.nixpkgs.url = "git+ssh://git@github.com/NixOS/nixpkgs";
```

## Migration Scenarios

### From Imperative Nix

**Old approach:**
```bash
nix-env -iA nixpkgs.git
nix-env -iA nixpkgs.neovim
```

**New approach (flakes):**
```nix
# flake.nix
{
  packages.default = pkgs.buildEnv {
    paths = [ pkgs.git pkgs.neovim ];
  };
}
```

```bash
nix profile install .
```

### From Nix Channels

**Old:**
```bash
nix-channel --add https://nixos.org/channels/nixpkgs-unstable
nix-channel --update
```

**New:**
```nix
# flake.nix
inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
```

```bash
nix flake update
```

### From Home Manager Standalone

**Integrate Home Manager into flake:**

```nix
{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    home-manager.url = "github:nix-community/home-manager";
    home-manager.inputs.nixpkgs.follows = "nixpkgs";
  };

  outputs = { self, nixpkgs, home-manager }: {
    homeConfigurations."username" = home-manager.lib.homeManagerConfiguration {
      pkgs = nixpkgs.legacyPackages.x86_64-linux;
      modules = [ ./home.nix ];
    };
  };
}
```

**Note**: This repository explicitly avoids Home Manager per `AGENTS.md`

## CI/CD Patterns

### GitHub Actions

**Complete workflow:**

```yaml
name: Nix CI

on: [push, pull_request]

jobs:
  build:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest]

    steps:
      - uses: actions/checkout@v4

      - name: Setup Nix cache
        uses: DeterminateSystems/magic-nix-cache-action@v2

      - name: Install Nix
        uses: DeterminateSystems/nix-installer-action@v14

      - name: Check flake
        run: nix flake check

      - name: Build packages
        run: nix build

      - name: Run tests
        run: nix flake check -L  # -L shows build logs
```

### GitLab CI

```yaml
.nix:
  image: nixos/nix:latest
  before_script:
    - nix-channel --update
    - echo "experimental-features = nix-command flakes" >> ~/.config/nix/nix.conf

build:
  extends: .nix
  script:
    - nix flake check
    - nix build
```

### Docker Integration

**Build Docker image from flake:**

```nix
{
  packages.docker = pkgs.dockerTools.buildImage {
    name = "my-app";
    tag = "latest";
    contents = [ self.packages.${system}.default ];
    config = {
      Cmd = [ "${self.packages.${system}.default}/bin/app" ];
    };
  };
}
```

```bash
# Build and load
nix build .#docker
docker load < result
docker run my-app:latest
```

## Security Best Practices

### Verify Substituters

**Check trusted substituters:**
```bash
cat ~/.config/nix/nix.conf | grep substituters
```

**Only use trusted caches:**
- `cache.nixos.org` (official)
- `cache.flakehub.com` (Determinate Systems)
- `cache.garnix.io` (community, if needed)

### Pin Dependencies

**Always commit flake.lock:**
```bash
git add flake.lock
git commit -m "Pin dependencies"
```

**Regularly update and review:**
```bash
nix flake update
git diff flake.lock  # Review changes
```

### Audit Packages

**Check package derivation:**
```bash
nix show-derivation nixpkgs#package-name
```

**Build locally if suspicious:**
```bash
nix build --no-substituters  # Force local build
```

## Nix Language Tips

### Common Functions

```nix
# List operations
lib.lists.unique [ 1 2 2 3 ]  # [ 1 2 3 ]
lib.lists.flatten [ [ 1 2 ] [ 3 4 ] ]  # [ 1 2 3 4 ]

# Attribute set operations
lib.attrsets.filterAttrs (n: v: v != null) { a = 1; b = null; }  # { a = 1; }

# String operations
lib.strings.concatStringsSep "," [ "a" "b" ]  # "a,b"

# Conditional logic
lib.optionals condition [ packages ]  # [ packages ] if true, [] if false
```

### Debugging

**Print values:**
```nix
let
  debug = x: builtins.trace x x;  # Print and return value
in
{
  packages.default = debug pkgs.hello;
}
```

**REPL exploration:**
```bash
nix repl
:lf .  # Load flake
packages.aarch64-darwin.default  # Explore attributes
:q  # Quit
```

## Resources

- **Determinate Systems Blog**: https://determinate.systems/blog/
- **Zero to Nix**: https://zero-to-nix.com/
- **Nix Pills**: https://nixos.org/guides/nix-pills/
- **NixOS Wiki**: https://nixos.wiki/
- **Nix Package Search**: https://search.nixos.org/
- **This Repository**: /Users/wcygan/Development/dotfiles/
