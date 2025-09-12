# Homebrew configuration for macOS
# This file loads before 10-nix.fish to ensure Homebrew takes precedence

if test (uname) = "Darwin"
    # Apple Silicon Macs (M1/M2/M3)
    if test -d /opt/homebrew
        # Add Homebrew to PATH
        fish_add_path --path --prepend /opt/homebrew/bin
        fish_add_path --path --prepend /opt/homebrew/sbin

        # Set Homebrew environment variables
        set -gx HOMEBREW_PREFIX /opt/homebrew
        set -gx HOMEBREW_CELLAR /opt/homebrew/Cellar
        set -gx HOMEBREW_REPOSITORY /opt/homebrew

        # Add Homebrew's manpages and info
        if test -d /opt/homebrew/share/man
            set -gx MANPATH /opt/homebrew/share/man $MANPATH
        end
        if test -d /opt/homebrew/share/info
            set -gx INFOPATH /opt/homebrew/share/info $INFOPATH
        end

    # Intel Macs
    else if test -d /usr/local/Homebrew
        # Add Homebrew to PATH
        fish_add_path --path --prepend /usr/local/bin
        fish_add_path --path --prepend /usr/local/sbin

        # Set Homebrew environment variables
        set -gx HOMEBREW_PREFIX /usr/local
        set -gx HOMEBREW_CELLAR /usr/local/Cellar
        set -gx HOMEBREW_REPOSITORY /usr/local/Homebrew

        # Add Homebrew's manpages and info
        if test -d /usr/local/share/man
            set -gx MANPATH /usr/local/share/man $MANPATH
        end
        if test -d /usr/local/share/info
            set -gx INFOPATH /usr/local/share/info $INFOPATH
        end
    end

    # Homebrew shellenv equivalent for any additional paths
    # This ensures all Homebrew-installed tools are available
    if command -v brew >/dev/null 2>&1
        # Get any additional environment variables from brew shellenv
        for line in (brew shellenv | grep "^export" | sed 's/^export //')
            set kv (string split -m1 '=' -- $line)
            if test (count $kv) -eq 2
                set -l k $kv[1]
                set -l v (string trim --chars='"' $kv[2])
                # Only set if not already handled above
                if not set -q $k
                    set -gx $k $v
                end
            end
        end
    end
end
