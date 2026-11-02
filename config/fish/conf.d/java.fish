if not set -q JAVA_HOME; and command -q brew
    set -l java_prefix
    if set -q HOMEBREW_PREFIX; and test (command -s brew) = "$HOMEBREW_PREFIX/bin/brew"
        set java_prefix "$HOMEBREW_PREFIX/opt/openjdk"
    else
        set java_prefix (brew --prefix openjdk 2>/dev/null)
    end
    if test -d "$java_prefix"
        set -gx JAVA_HOME "$java_prefix"
        fish_add_path --path "$JAVA_HOME/bin"
    end
end
