# Template for Fish function
# Save to: ~/.config/fish/functions/function-name.fish

function function-name --description 'Brief description here'
    # Optional: Named arguments
    # --argument-names arg1 arg2

    # Optional: Wrap another command for completions
    # --wraps='original-command'

    # Check argument count
    if test (count $argv) -eq 0
        echo "Usage: function-name <arguments>"
        return 1
    end

    # Local variables
    set -l local_var "value"

    # Process arguments
    for arg in $argv
        echo "Processing: $arg"
    end

    # Error handling
    if not some_command
        echo "Error: command failed"
        return 1
    end

    # Success
    return 0
end
