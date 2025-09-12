function fix-paths --description 'Reset and rebuild PATH with correct priority'
    # Clear any persistent user paths
    set -e fish_user_paths

    # Rebuild PATH in correct priority order
    # 1. System essentials
    set -l new_path /usr/local/bin /usr/bin /bin /usr/sbin /sbin

    # 2. User manual installs (highest priority)
    test -d $HOME/.deno/bin; and set new_path $HOME/.deno/bin $new_path
    test -d $HOME/go/bin; and set new_path $HOME/go/bin $new_path
    test -d $HOME/.cargo/bin; and set new_path $HOME/.cargo/bin $new_path
    test -d $HOME/.local/bin; and set new_path $HOME/.local/bin $new_path
    test -d $HOME/bin; and set new_path $HOME/bin $new_path

    # 3. Homebrew (medium priority)
    test -d /opt/homebrew/bin; and set new_path /opt/homebrew/bin $new_path
    test -d /opt/homebrew/sbin; and set new_path /opt/homebrew/sbin $new_path

    # 4. Nix (lowest priority)
    test -d $HOME/.nix-profile/bin; and set new_path $new_path $HOME/.nix-profile/bin
    test -d /nix/var/nix/profiles/default/bin; and set new_path $new_path /nix/var/nix/profiles/default/bin

    # Set the new PATH
    set -gx PATH $new_path

    echo "✅ PATH has been reset with correct priority:"
    echo ""
    echo "Current deno:"
    which deno
    deno --version 2>/dev/null || echo "Deno not found"
    echo ""
    echo "PATH order (first 10):"
    echo $PATH | tr ' ' '\n' | head -10
end
