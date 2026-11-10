# Homebrew configuration for macOS
# This file loads before 10-nix.fish, which then moves the Nix profile and
# user bin directories ahead of Homebrew on PATH.

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

    # Retain the existing shellenv fallback for nonstandard Homebrew installs.
    if command -v brew >/dev/null 2>&1; and begin
        not set -q HOMEBREW_PREFIX; or test (command -s brew) != "$HOMEBREW_PREFIX/bin/brew"
    end
        # Get any additional environment variables from brew shellenv
        for line in (brew shellenv | string match -r '^export .*' | string replace -r '^export ' '')
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
