---
description: Create a project-specific Nix flake with language-appropriate tooling
---

Create a Nix flake for a development environment in the current directory or specified path.

**Step 1: Detect Project Type**

Analyze the current directory to determine the project language:
- **Python**: Look for `pyproject.toml`, `requirements.txt`, `setup.py`, `*.py` files
- **TypeScript/JavaScript**: Look for `deno.json`, `package.json`, `tsconfig.json`, `*.ts` files
- **Java**: Look for `pom.xml`, `build.gradle`, `*.java` files
- **Rust**: Look for `Cargo.toml`, `*.rs` files
- **Go**: Look for `go.mod`, `*.go` files
- **Multiple languages**: Detect all and create multi-language environment

If unclear, ask the user what type of project this is.

**Step 2: Create Language-Specific Flake**

Generate `flake.nix` using the appropriate template below:

## Python Projects (use uv)

```nix
{
  description = "Python project with uv";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      systems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
      forAllSystems = f: nixpkgs.lib.genAttrs systems (system: f {
        pkgs = import nixpkgs { inherit system; };
      });
    in
    {
      devShells = forAllSystems ({ pkgs }: {
        default = pkgs.mkShell {
          packages = with pkgs; [
            # Python via uv (ultra-fast package manager)
            uv

            # Optional: specific Python version if needed
            # python312

            # Development tools
            git
          ];

          shellHook = ''
            echo "🐍 Python development environment (uv)"
            echo "Available commands:"
            echo "  uv init          - Initialize new project"
            echo "  uv add <pkg>     - Add dependency"
            echo "  uv run <cmd>     - Run command in venv"
            echo "  uv sync          - Sync dependencies"
            echo ""

            # Create .venv if it doesn't exist
            if [ ! -d .venv ]; then
              echo "Creating virtual environment with uv..."
              uv venv
            fi

            # Activate virtual environment
            source .venv/bin/activate
          '';
        };
      });

      formatter = forAllSystems ({ pkgs }: pkgs.nixpkgs-fmt);
    };
}
```

**Python-specific setup after flake creation:**
```bash
# Initialize uv project (if not already initialized)
uv init

# Add common dependencies
uv add ruff pytest

# Create basic pyproject.toml if missing
```

## TypeScript/JavaScript Projects (use Deno)

```nix
{
  description = "TypeScript/JavaScript project with Deno";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      systems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
      forAllSystems = f: nixpkgs.lib.genAttrs systems (system: f {
        pkgs = import nixpkgs { inherit system; };
      });
    in
    {
      devShells = forAllSystems ({ pkgs }: {
        default = pkgs.mkShell {
          packages = with pkgs; [
            # Deno runtime (includes TypeScript, formatter, linter, tester)
            deno

            # Development tools
            git
          ];

          shellHook = ''
            echo "🦕 Deno development environment"
            echo "Deno version: $(deno --version | head -1)"
            echo ""
            echo "Available commands:"
            echo "  deno run <file>      - Run TypeScript/JavaScript"
            echo "  deno task <name>     - Run task from deno.json"
            echo "  deno test            - Run tests"
            echo "  deno fmt             - Format code"
            echo "  deno lint            - Lint code"
            echo "  deno check           - Type check"
            echo ""
          '';
        };
      });

      formatter = forAllSystems ({ pkgs }: pkgs.nixpkgs-fmt);
    };
}
```

**Deno-specific setup after flake creation:**
```bash
# Create deno.json if it doesn't exist
cat > deno.json <<EOF
{
  "tasks": {
    "dev": "deno run --watch main.ts",
    "test": "deno test"
  },
  "fmt": {
    "useTabs": false,
    "lineWidth": 100,
    "indentWidth": 2
  },
  "lint": {
    "rules": {
      "tags": ["recommended"]
    }
  }
}
EOF
```

## Java Projects (use Maven)

```nix
{
  description = "Java project with Maven";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      systems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
      forAllSystems = f: nixpkgs.lib.genAttrs systems (system: f {
        pkgs = import nixpkgs { inherit system; };
      });
    in
    {
      devShells = forAllSystems ({ pkgs }: {
        default = pkgs.mkShell {
          packages = with pkgs; [
            # Java Development Kit
            jdk21  # or jdk17, jdk11, etc.

            # Maven build tool
            maven

            # Development tools
            git
          ];

          shellHook = ''
            echo "☕ Java development environment (Maven)"
            echo "Java version: $(java -version 2>&1 | head -1)"
            echo "Maven version: $(mvn --version | head -1)"
            echo ""
            echo "Available commands:"
            echo "  mvn compile          - Compile project"
            echo "  mvn test             - Run tests"
            echo "  mvn package          - Build JAR"
            echo "  mvn clean install    - Clean build and install"
            echo ""
          '';
        };
      });

      formatter = forAllSystems ({ pkgs }: pkgs.nixpkgs-fmt);
    };
}
```

**Maven-specific setup after flake creation:**
```bash
# Generate Maven project structure if needed
mvn archetype:generate -DgroupId=com.example -DartifactId=myapp -DarchetypeArtifactId=maven-archetype-quickstart -DinteractiveMode=false
```

## Rust Projects

```nix
{
  description = "Rust project";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    rust-overlay.url = "github:oxalica/rust-overlay";
  };

  outputs = { self, nixpkgs, rust-overlay }:
    let
      systems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
      forAllSystems = f: nixpkgs.lib.genAttrs systems (system: f {
        pkgs = import nixpkgs {
          inherit system;
          overlays = [ rust-overlay.overlays.default ];
        };
      });
    in
    {
      devShells = forAllSystems ({ pkgs }: {
        default = pkgs.mkShell {
          packages = with pkgs; [
            # Rust stable toolchain
            rust-bin.stable.latest.default

            # Alternative: specific version
            # rust-bin.stable."1.75.0".default

            # Development tools
            rust-analyzer
            cargo-watch
            cargo-edit
            git
          ];

          shellHook = ''
            echo "🦀 Rust development environment"
            echo "Rust version: $(rustc --version)"
            echo "Cargo version: $(cargo --version)"
            echo ""
            echo "Available commands:"
            echo "  cargo build          - Build project"
            echo "  cargo test           - Run tests"
            echo "  cargo run            - Run project"
            echo "  cargo watch -x run   - Watch and run on changes"
            echo ""
          '';
        };
      });

      formatter = forAllSystems ({ pkgs }: pkgs.nixpkgs-fmt);
    };
}
```

**Rust-specific setup after flake creation:**
```bash
# Initialize Cargo project if needed
cargo init
```

## Go Projects

```nix
{
  description = "Go project";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      systems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
      forAllSystems = f: nixpkgs.lib.genAttrs systems (system: f {
        pkgs = import nixpkgs { inherit system; };
      });
    in
    {
      devShells = forAllSystems ({ pkgs }: {
        default = pkgs.mkShell {
          packages = with pkgs; [
            # Go toolchain
            go_1_23  # or go_1_22, go, etc.

            # Development tools
            gopls          # Language server
            gotools        # goimports, godoc, etc.
            golangci-lint  # Linter
            git
          ];

          shellHook = ''
            echo "🐹 Go development environment"
            echo "Go version: $(go version)"
            echo ""
            echo "Available commands:"
            echo "  go run .             - Run project"
            echo "  go build             - Build binary"
            echo "  go test ./...        - Run tests"
            echo "  golangci-lint run    - Lint code"
            echo ""
          '';
        };
      });

      formatter = forAllSystems ({ pkgs }: pkgs.nixpkgs-fmt);
    };
}
```

**Go-specific setup after flake creation:**
```bash
# Initialize Go module if needed
go mod init github.com/username/project
```

## Multi-Language Projects

For projects using multiple languages, combine the relevant packages:

```nix
{
  description = "Multi-language project";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      systems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
      forAllSystems = f: nixpkgs.lib.genAttrs systems (system: f {
        pkgs = import nixpkgs { inherit system; };
      });
    in
    {
      devShells = forAllSystems ({ pkgs }: {
        default = pkgs.mkShell {
          packages = with pkgs; [
            # Python
            uv

            # TypeScript
            deno

            # Add other languages as needed
            # go_1_23
            # rust-bin.stable.latest.default

            # Development tools
            git
          ];

          shellHook = ''
            echo "🔧 Multi-language development environment"
            echo ""
          '';
        };
      });

      formatter = forAllSystems ({ pkgs }: pkgs.nixpkgs-fmt);
    };
}
```

**Step 3: Create Supporting Files**

1. **Create `.envrc`** for direnv integration:
```bash
use flake
```

2. **Create `.gitignore`** additions:
```
# Nix
.direnv/
result
result-*

# Python
.venv/
__pycache__/
*.pyc

# Deno
.deno/

# Language-specific patterns
```

**Step 4: Initialize and Activate**

After creating the flake:

```bash
# Allow direnv (if using direnv)
direnv allow

# Or manually enter dev shell
nix develop

# Verify environment
nix flake check
nix flake show
```

**Step 5: Next Steps**

Inform the user:
1. The development environment is now reproducible across machines
2. To share with team: commit `flake.nix` and `flake.lock`
3. To update dependencies: `nix flake update`
4. To add more tools: edit `packages = with pkgs; [ ... ]` section

**Output Format:**

1. Use Write tool to create `flake.nix`
2. Use Write tool to create or update `.envrc`
3. Use Write tool to create or update `.gitignore`
4. Show the commands to run next
5. Explain what was set up and how to use it

**Repository Context:**

This follows the dotfiles repository pattern:
- Using `nixos-unstable` for latest packages
- `forAllSystems` pattern for multi-platform support
- No `--impure` flags (pure evaluation only)
- Format with `nix fmt` using nixpkgs-fmt
