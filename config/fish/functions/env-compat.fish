# Fish function to handle bash-style environment variable syntax
# This provides compatibility for tools that expect VAR=value command syntax

function env-compat --description 'Handle bash-style env var syntax in fish'
    # Parse VAR=value pairs until we hit a non-assignment
    set -l env_vars
    set -l remaining_args
    set -l found_command 0

    for arg in $argv
        if test $found_command -eq 0
            # Check if this looks like VAR=value
            if string match -qr '^[A-Za-z_][A-Za-z0-9_]*=' -- $arg
                set -a env_vars $arg
            else
                # Found the actual command
                set found_command 1
                set -a remaining_args $arg
            end
        else
            set -a remaining_args $arg
        end
    end

    # If we have env vars to set, use env command
    if test (count $env_vars) -gt 0
        env $env_vars $remaining_args
    else
        # No env vars, just run the command
        $remaining_args
    end
end
