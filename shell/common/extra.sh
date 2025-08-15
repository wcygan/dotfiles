##############################################################################
#   Filename: .extra.sh                                                      #
# Maintainer: Will Cygan <wcygan.io@gmail.com>                              #
#        URL: http://github.com/wcygan/dotfiles                             #
#                                                                            #
# Sections:                                                                  #
#   01. Git Configuration ........ Universal Git settings                   #
#   02. Shell Configuration ...... ZSH and Bash specific settings           #
#   03. Tool Integrations ......... FZF, direnv, and development tools      #
##############################################################################

##############################################################################
# 01. Git Configuration                                                      #
##############################################################################

# Git configuration (universal)
GIT_AUTHOR_NAME="Will Cygan"
GIT_COMMITTER_NAME="$GIT_AUTHOR_NAME"
git config --global user.name "$GIT_AUTHOR_NAME"
GIT_AUTHOR_EMAIL="wcygan.io@gmail.com"
GIT_COMMITTER_EMAIL="$GIT_AUTHOR_EMAIL"
git config --global user.email "$GIT_AUTHOR_EMAIL"

##############################################################################
# 02. Shell Configuration                                                    #
##############################################################################

# Shell-specific configurations
if [ -n "$ZSH_VERSION" ]; then
    # ZSH-specific configurations
    
    # zsh completion configuration
    zstyle ':completion:*' matcher-list '' 'm:{a-zA-Z}={A-Za-z}' 'r:|=*' 'l:|=* r:|=*'
    autoload -Uz compinit && compinit

    # zsh syntax highlighting (if available)
    if [ -f /opt/homebrew/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh ]; then
        source /opt/homebrew/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
    fi

    # mise activation for zsh
    if command -v mise >/dev/null 2>&1; then
        eval "$(/opt/homebrew/bin/mise activate zsh)"
    fi

elif [ -n "$BASH_VERSION" ]; then
    # Bash-specific configurations
    
    # mise activation for bash
    if command -v mise >/dev/null 2>&1; then
        eval "$(/opt/homebrew/bin/mise activate bash)"
    fi
    
    # Additional bash completion sources
    if command -v brew >/dev/null 2>&1; then
        # Git completion for bash
        if [ -f "$(brew --prefix)/etc/bash_completion.d/git-completion.bash" ]; then
            source "$(brew --prefix)/etc/bash_completion.d/git-completion.bash"
        fi
        
        # Docker completion for bash
        if [ -f "$(brew --prefix)/etc/bash_completion.d/docker" ]; then
            source "$(brew --prefix)/etc/bash_completion.d/docker"
        fi
    fi
fi

##############################################################################
# 03. Tool Integrations                                                      #
##############################################################################

# Universal tool integrations (work in both shells)

# fzf key bindings (universal)
if command -v fzf >/dev/null 2>&1; then
    # Universal fzf environment variables
    export FZF_DEFAULT_OPTS='--height 40% --layout=reverse --border'
    
    # Set up fzf for file search
    if command -v fd >/dev/null 2>&1; then
        export FZF_DEFAULT_COMMAND='fd --type f --hidden --follow --exclude .git'
        export FZF_CTRL_T_COMMAND="$FZF_DEFAULT_COMMAND"
    fi
    
    # Ensure fzf keybindings are available and loaded
    if [ -n "$BASH_VERSION" ]; then
        # Generate fzf keybindings file if missing
        if [ ! -f ~/.fzf.bash ]; then
            if fzf --bash > ~/.fzf.bash 2>/dev/null; then
                echo "✓ Generated fzf keybindings at ~/.fzf.bash"
            else
                echo "⚠️  Failed to generate fzf keybindings. Run: fzf --bash > ~/.fzf.bash"
            fi
        fi
        # Always try to source the keybindings
        if [ -f ~/.fzf.bash ]; then
            source ~/.fzf.bash
        fi
    elif [ -n "$ZSH_VERSION" ]; then
        # Generate fzf keybindings file if missing
        if [ ! -f ~/.fzf.zsh ]; then
            if fzf --zsh > ~/.fzf.zsh 2>/dev/null; then
                echo "✓ Generated fzf keybindings at ~/.fzf.zsh"
            else
                echo "⚠️  Failed to generate fzf keybindings. Run: fzf --zsh > ~/.fzf.zsh"
            fi
        fi
        # Always try to source the keybindings
        if [ -f ~/.fzf.zsh ]; then
            source ~/.fzf.zsh
        fi
    fi
else
    # Warn if fzf is not installed
    if [ "$DOTFILES_DISTRO" = "fedora" ]; then
        echo "⚠️  fzf is not installed. Install with: sudo dnf install fzf"
    elif [ "$DOTFILES_OS" = "macos" ]; then
        echo "⚠️  fzf is not installed. Install with: brew install fzf"
    elif [ "$DOTFILES_PACKAGE_MANAGER" = "apt" ]; then
        echo "⚠️  fzf is not installed. Install with: sudo apt install fzf"
    else
        echo "⚠️  fzf is not installed. Please install it for enhanced shell features."
    fi
fi

# direnv integration (if available)
if command -v direnv >/dev/null 2>&1; then
    if [ -n "$ZSH_VERSION" ]; then
        eval "$(direnv hook zsh)"
    elif [ -n "$BASH_VERSION" ]; then
        eval "$(direnv hook bash)"
    fi
fi
