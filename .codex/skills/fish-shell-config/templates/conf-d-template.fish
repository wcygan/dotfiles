# Template for conf.d config file
# Save to: ~/.config/fish/conf.d/NN-name.fish
# where NN determines load order: 10 (early), 20, 30, 40 (late)

# Example: 10-environment.fish, 20-direnv.fish, 30-prompt.fish, 40-aliases.fish

# Guard: only run if tool/file exists
if not type -q some-tool
    exit 0
end

# OR: check for file existence
if not test -f ~/.config/some-config
    exit 0
end

# Set environment variables
set -gx SOME_VAR value

# PATH manipulation
set -gx PATH $HOME/.local/bin $PATH

# Conditional setup based on OS
switch (uname)
    case Darwin
        # macOS specific
        set -gx HOMEBREW_PREFIX /opt/homebrew
    case Linux
        # Linux specific
        set -gx LINUX_VAR value
end

# Source external config
if test -f ~/.config/external/config.fish
    source ~/.config/external/config.fish
end

# Tool initialization
if type -q starship
    starship init fish | source
end

# Create abbreviations (interactive only)
abbr -a shortcut 'full command'

# Create aliases (functions)
alias short='long command'
