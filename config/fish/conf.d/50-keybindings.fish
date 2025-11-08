# config/fish/conf.d/50-keybindings.fish
#
# Custom keybindings for Fish shell

# Only set keybindings in interactive mode
status is-interactive; or exit

# Option+Backspace: Delete word backward (macOS standard behavior)
# macOS terminals typically send \e\b or \e\x7f for Option+Backspace
bind \e\b backward-kill-word
bind \e\x7f backward-kill-word

# Option+Delete: Delete word forward (if needed)
bind \e\[3\;9~ kill-word

# Ctrl+W: Also delete word backward (alternative)
# Fish default is backward-kill-path-component, but you might prefer backward-kill-word
# Uncomment the line below if you want Ctrl+W to delete entire words instead of path components
# bind \cw backward-kill-word
