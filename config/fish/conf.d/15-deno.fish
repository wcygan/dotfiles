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
