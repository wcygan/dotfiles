# Backward Delete Word

Delete entire words with Option+Delete (backward) or Option+Fn+Delete (forward) in the terminal.

## Intended Usage

| Shortcut | Action | Description |
|----------|--------|-------------|
| Option+Delete | `backward-kill-word` | Delete word before cursor |
| Option+Fn+Delete | `kill-word` | Delete word after cursor |
| Option+← | `backward-word` | Move cursor back one word |
| Option+→ | `forward-word` | Move cursor forward one word |

## Problem

Option+Delete does not delete words.

**Root cause:** macOS terminals treat Option as the Option key rather than as Alt/Meta (for terminal escape sequences).

## Solution

### Ghostty

Add to `~/.config/ghostty/config`:

```
macos-option-as-alt = left
```

Options:
- `left` - Left Option acts as Alt, right Option types special characters
- `right` - Right Option acts as Alt, left Option types special characters
- `true` - Both Option keys act as Alt

Reload with `Cmd+Shift+R` or restart Ghostty.

### Fish Shell Keybindings

Ensure these bindings exist in `~/.config/fish/conf.d/50-keybindings.fish`:

```fish
# Option+Backspace (backward delete word)
bind \e\b backward-kill-word
bind \e\x7f backward-kill-word

# Option+Delete (forward delete word)
bind \e\[3\;9~ kill-word
```

## Verification

1. Open a new terminal
2. Type: `hello world`
3. Press Option+Delete
4. Expected: `hello ` (word "world" deleted)

## Related Files

- `config/ghostty/config` - Ghostty terminal configuration
- `config/fish/conf.d/50-keybindings.fish` - Fish shell keybindings
