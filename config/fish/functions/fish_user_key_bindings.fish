function fish_user_key_bindings
    if command -s fzf-share >/dev/null
        source (fzf-share)/key-bindings.fish
    end

    fzf_key_bindings
end
