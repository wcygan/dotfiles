# Fish compatibility layer for non-interactive sessions
# Handles cases where tools expect bash-style syntax

# Detect if we're in a non-interactive session that might need bash
if not status is-interactive
    # Check if the command line contains bash-style env var syntax
    if set -q argv; and string match -qr '^[A-Za-z_][A-Za-z0-9_]*=' -- $argv[1]
        # This is likely a bash-style command, redirect to bash
        exec bash -c "$argv"
    end
end

# For debugging remote execution issues (can be removed once stable)
if set -q DEBUG_REMOTE_EXEC
    echo "Fish non-interactive session debug:" >&2
    echo "  argv: $argv" >&2
    echo "  PATH: $PATH" >&2
    echo "  HOME: $HOME" >&2
end
