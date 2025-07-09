export PATH="/usr/local/bin:$PATH"

# Detect OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS specific paths

    # DuckDB CLI
    export PATH="$HOME/.duckdb/cli/latest:$PATH"

    # Homebrew tools
    export PATH="/opt/homebrew/opt/openjdk/bin:$PATH"
    export PATH="/opt/homebrew/opt/llvm/bin:$PATH"
    export PATH="/opt/homebrew/opt/mysql-client/bin:$PATH"

    # Rancher Desktop (managed section)
    ### MANAGED BY RANCHER DESKTOP START (DO NOT EDIT)
    export PATH="$HOME/.rd/bin:$PATH"
    ### MANAGED BY RANCHER DESKTOP END (DO NOT EDIT)

    # pnpm
    export PNPM_HOME="$HOME/Library/pnpm"
    case ":$PATH:" in
      *":$PNPM_HOME:"*) ;;
      *) export PATH="$PNPM_HOME:$PATH" ;;
    esac

elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux specific paths

    # Rust/Cargo
    if [ -d "$HOME/.cargo/bin" ]; then
        export PATH="$HOME/.cargo/bin:$PATH"
    fi

    # npm global packages (if using custom prefix)
    if [ -d "$HOME/.npm-global/bin" ]; then
        export PATH="$HOME/.npm-global/bin:$PATH"
    fi

    # System directories that might not be in default PATH
    export PATH="/usr/sbin:/sbin:$PATH"
fi

# Cross-platform development tools

# Go tools
if command -v go &> /dev/null; then
    export PATH="$PATH:$(go env GOPATH)/bin"
fi

# Kubernetes tools
export PATH="${KREW_ROOT:-$HOME/.krew}/bin:$PATH"

# Development tools
export PATH="$HOME/.jbang/bin:$PATH"
export PATH="$HOME/.deno/bin:$PATH"

# Source cargo env if it exists (handles PATH for us)
if [ -f "$HOME/.cargo/env" ]; then
    source "$HOME/.cargo/env"
fi
