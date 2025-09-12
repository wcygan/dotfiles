function which-version --description 'Show which version of a command will be used (system vs Nix)'
    if test (count $argv) -eq 0
        echo "Usage: which-version <command>"
        echo "Shows which version of a command will be used (system vs Nix)"
        return 1
    end

    set -l cmd $argv[1]
    set -l cmd_path (which $cmd 2>/dev/null)

    if test -z "$cmd_path"
        echo "Command '$cmd' not found"
        return 1
    end

    echo "Active: $cmd_path"

    # Check source
    if string match -q "*/nix/*" $cmd_path; or string match -q "*/.nix-profile/*" $cmd_path
        echo "Source: Nix package"
    else if string match -q "*/opt/homebrew/*" $cmd_path; or string match -q "*/usr/local/*" $cmd_path
        echo "Source: Homebrew"
    else if string match -q "$HOME/.local/bin*" $cmd_path; or string match -q "$HOME/bin*" $cmd_path
        echo "Source: User install"
    else if string match -q "$HOME/.cargo/bin*" $cmd_path
        echo "Source: Cargo"
    else if string match -q "$HOME/go/bin*" $cmd_path
        echo "Source: Go"
    else
        echo "Source: System package"
    end

    # Show all available versions
    echo ""
    echo "All available:"
    for loc in (which -a $cmd 2>/dev/null)
        echo "  $loc"
    end
end
