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
