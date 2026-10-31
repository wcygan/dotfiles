if not set -q JAVA_HOME; and command -q brew
    set -l java_prefix (brew --prefix openjdk 2>/dev/null)
    if test -d "$java_prefix"
        set -gx JAVA_HOME "$java_prefix"
        fish_add_path --path "$JAVA_HOME/bin"
    end
end
