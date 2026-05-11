# Deno configuration for Fish shell
# Adds Deno to PATH and sets up completions

# Add Deno to PATH if installed (ensure it takes priority over Nix)
if test -d $HOME/.deno/bin
    # Remove any existing Deno path entries and add with highest priority
    set -l deno_path $HOME/.deno/bin
    set -gx PATH (string match -v $deno_path $PATH)
    set -gx PATH $deno_path $PATH
end

# Set Deno environment variables
set -gx DENO_INSTALL $HOME/.deno
set -gx DOTFILES_DENO_COOLDOWN_CONFIG $HOME/.config/deno/deno.jsonc

function __dotfiles_find_deno_config --description 'Find the nearest Deno project config'
    set -l dir $PWD

    while test -n "$dir"; and test "$dir" != /
        if test -f "$dir/deno.json"; or test -f "$dir/deno.jsonc"
            return 0
        end

        set dir (dirname "$dir")
    end

    test -f /deno.json; or test -f /deno.jsonc
end

function __dotfiles_deno_has_dependency_config_arg --description 'Detect Deno args that override cooldown config'
    for arg in $argv
        switch $arg
            case --minimum-dependency-age '--minimum-dependency-age=*' --config '--config=*' -c --no-config
                return 0
        end
    end

    return 1
end

function deno --wraps deno --description 'Run Deno with dotfiles dependency cooldown defaults'
    switch "$argv[1]"
        case install add update outdated x
            if __dotfiles_deno_has_dependency_config_arg $argv; or __dotfiles_find_deno_config; or not test -f "$DOTFILES_DENO_COOLDOWN_CONFIG"
                command deno $argv
            else
                command deno $argv[1] --config "$DOTFILES_DENO_COOLDOWN_CONFIG" $argv[2..-1]
            end
        case '*'
            command deno $argv
    end
end

# Set up dx alias for running package binaries (Deno 2.6+)
# dx is the Deno equivalent to npx
if command -v deno >/dev/null 2>&1
    alias dx='deno x'
end

# Generate and source Deno completions if deno is available
if command -v deno >/dev/null 2>&1
    # Only generate completions if they don't exist or are outdated
    set -l completions_file $HOME/.config/fish/completions/deno.fish
    set -l deno_binary $HOME/.deno/bin/deno

    # Create completions directory if it doesn't exist
    if not test -d $HOME/.config/fish/completions
        mkdir -p $HOME/.config/fish/completions
    end

    # Generate completions if file doesn't exist or deno binary is newer
    if not test -f $completions_file; or test $deno_binary -nt $completions_file
        deno completions fish > $completions_file 2>/dev/null
    end
end
