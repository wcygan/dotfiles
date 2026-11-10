# Interactive-only guards are fine if you want to keep prompt snappy
status is-interactive; and begin
  # general interactive-only settings can go here
end

# Added by Antigravity
fish_add_path /Users/wcygan/.antigravity/antigravity/bin

# Disable fish greeting
set -g fish_greeting ""

# Per-host bastion env (anton cluster access from secondary machines)
switch (hostname)
    case betty
        set -gx KUBECONFIG $HOME/anton/kubeconfig
        set -gx TALOSCONFIG $HOME/anton/talos/clusterconfig/talosconfig
        set -gx SOPS_AGE_KEY_FILE $HOME/anton/age.key
end

# mise activation (https://mise.jdx.dev)
if test -x $HOME/.local/bin/mise
    $HOME/.local/bin/mise activate fish | source
end

# Rex puts its matching rex CLI first on PATH; keep it there after the path
# changes above. Must stay last: https://www.superlogical.com/rex/docs/automate/cli#path
if set -q REX_BIN_DIR
    fish_add_path --path --prepend --move $REX_BIN_DIR
end

if status is-interactive
    function __configure_tv_ssh --on-event fish_prompt
        if set -q GHOSTTY_BIN_DIR; and functions -q ssh
            functions --copy ssh __ghostty_ssh
            function ssh --wraps=ssh
                if test (count $argv) -eq 1; and test "$argv[1]" = tv
                    env TERM=xterm-256color ssh tv
                else
                    __ghostty_ssh $argv
                end
            end
        end
        functions --erase __configure_tv_ssh
    end
end
