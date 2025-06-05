# Git configuration (universal)
GIT_AUTHOR_NAME="Will Cygan"
GIT_COMMITTER_NAME="$GIT_AUTHOR_NAME"
git config --global user.name "$GIT_AUTHOR_NAME"
GIT_AUTHOR_EMAIL="wcygan.io@gmail.com"
GIT_COMMITTER_EMAIL="$GIT_AUTHOR_EMAIL"
git config --global user.email "$GIT_AUTHOR_EMAIL"

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

    # fzf integration for zsh (if available)
    [ -f ~/.fzf.zsh ] && source ~/.fzf.zsh

    # mise activation for zsh
    if command -v mise >/dev/null 2>&1; then
        eval "$(/opt/homebrew/bin/mise activate zsh)"
    fi

elif [ -n "$BASH_VERSION" ]; then
    # Bash-specific configurations
    
    # fzf integration for bash (if available)
    [ -f ~/.fzf.bash ] && source ~/.fzf.bash
    
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
fi

# direnv integration (if available)
if command -v direnv >/dev/null 2>&1; then
    if [ -n "$ZSH_VERSION" ]; then
        eval "$(direnv hook zsh)"
    elif [ -n "$BASH_VERSION" ]; then
        eval "$(direnv hook bash)"
    fi
fi
