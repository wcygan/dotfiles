# Platform and shell detection utilities
# This file is sourced by both bash and zsh configurations

# Detect operating system
if [[ "$(uname)" == "Darwin" ]]; then
    export DOTFILES_OS="macos"
elif [[ "$(uname)" == "Linux" ]]; then
    export DOTFILES_OS="linux"
elif [[ "$(uname -s)" == CYGWIN* ]] || [[ "$(uname -s)" == MINGW* ]]; then
    export DOTFILES_OS="windows"
else
    export DOTFILES_OS="unknown"
fi

# Detect shell and set shell-specific environment
if [ -n "$ZSH_VERSION" ]; then
    export DOTFILES_SHELL="zsh"
    export DOTFILES_SHELL_CONFIG="$HOME/.zshrc"
    export DOTFILES_SHELL_VERSION="$ZSH_VERSION"
elif [ -n "$BASH_VERSION" ]; then
    export DOTFILES_SHELL="bash"
    export DOTFILES_SHELL_CONFIG="$HOME/.bashrc"
    export DOTFILES_SHELL_VERSION="$BASH_VERSION"
else
    export DOTFILES_SHELL="unknown"
    export DOTFILES_SHELL_CONFIG=""
    export DOTFILES_SHELL_VERSION=""
fi

# Set terminal capabilities
if [ -t 1 ]; then
    export DOTFILES_TERMINAL="interactive"
    export DOTFILES_COLORS_SUPPORTED="true"
else
    export DOTFILES_TERMINAL="non-interactive"
    export DOTFILES_COLORS_SUPPORTED="false"
fi

# Platform-specific configurations
case "$DOTFILES_OS" in
    "macos")
        # macOS specific settings
        export DOTFILES_PACKAGE_MANAGER="brew"
        if command -v brew >/dev/null 2>&1; then
            export DOTFILES_BREW_PREFIX="$(brew --prefix)"
        fi
        ;;
    "linux")
        # Linux specific settings
        if command -v apt >/dev/null 2>&1; then
            export DOTFILES_PACKAGE_MANAGER="apt"
            export DOTFILES_DISTRO="debian"
        elif command -v dnf >/dev/null 2>&1; then
            export DOTFILES_PACKAGE_MANAGER="dnf"
            if [ -f "/etc/fedora-release" ]; then
                export DOTFILES_DISTRO="fedora"
            else
                export DOTFILES_DISTRO="rhel"
            fi
        elif command -v yum >/dev/null 2>&1; then
            export DOTFILES_PACKAGE_MANAGER="yum"
            export DOTFILES_DISTRO="rhel"
        elif command -v pacman >/dev/null 2>&1; then
            export DOTFILES_PACKAGE_MANAGER="pacman"
            export DOTFILES_DISTRO="arch"
        fi
        ;;
esac

# Shell-specific optimizations
case "$DOTFILES_SHELL" in
    "bash")
        # Bash-specific environment variables
        export DOTFILES_COMPLETION_ENABLED="true"
        if [ -d "$HOME/.bash_completion.d" ]; then
            export DOTFILES_COMPLETION_DIR="$HOME/.bash_completion.d"
        fi
        ;;
    "zsh")
        # ZSH-specific environment variables  
        export DOTFILES_COMPLETION_ENABLED="true"
        if [ -d "$HOME/.zsh/completions" ]; then
            export DOTFILES_COMPLETION_DIR="$HOME/.zsh/completions"
        fi
        ;;
esac

# Development environment detection
if [ -n "$VIRTUAL_ENV" ]; then
    export DOTFILES_PYTHON_ENV="$(basename $VIRTUAL_ENV)"
fi

if [ -f "package.json" ]; then
    export DOTFILES_NODE_PROJECT="true"
fi

if [ -f "Cargo.toml" ]; then
    export DOTFILES_RUST_PROJECT="true"
fi

if [ -f "go.mod" ]; then
    export DOTFILES_GO_PROJECT="true"
fi

# Quick info function
dotfiles_info() {
    echo "🔧 Dotfiles Environment Information"
    echo "=================================="
    echo "OS: $DOTFILES_OS"
    if [ -n "$DOTFILES_DISTRO" ]; then
        echo "Distribution: $DOTFILES_DISTRO"
    fi
    echo "Shell: $DOTFILES_SHELL ($DOTFILES_SHELL_VERSION)"
    echo "Config: $DOTFILES_SHELL_CONFIG"
    echo "Terminal: $DOTFILES_TERMINAL"
    echo "Colors: $DOTFILES_COLORS_SUPPORTED"
    
    if [ -n "$DOTFILES_PACKAGE_MANAGER" ]; then
        echo "Package Manager: $DOTFILES_PACKAGE_MANAGER"
    fi
    
    if [ -n "$DOTFILES_PYTHON_ENV" ]; then
        echo "Python Environment: $DOTFILES_PYTHON_ENV"
    fi
    
    local project_types=""
    [ "$DOTFILES_NODE_PROJECT" = "true" ] && project_types="$project_types Node.js"
    [ "$DOTFILES_RUST_PROJECT" = "true" ] && project_types="$project_types Rust"
    [ "$DOTFILES_GO_PROJECT" = "true" ] && project_types="$project_types Go"
    
    if [ -n "$project_types" ]; then
        echo "Detected Projects:$project_types"
    fi
}
