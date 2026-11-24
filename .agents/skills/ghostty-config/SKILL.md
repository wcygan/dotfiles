---
name: ghostty-config
description: Change or troubleshoot Ghostty fonts, themes, keybindings, shell integration, and window behavior in this dotfiles repository.
---

# Configure Ghostty

Edit [config/ghostty/config](../../../config/ghostty/config). Keep custom theme
files in `config/ghostty/themes/`. For a keybinding, check the existing trigger
and action before adding another binding. For a font change, check the family
Ghostty can resolve with `ghostty +list-fonts`.

Use the [Ghostty reference](REFERENCE.md) for examples. For settings or actions
that depend on the installed version, consult the
[configuration reference](https://ghostty.org/docs/config/reference) or
[keybinding guide](https://ghostty.org/docs/config/keybind).

## Verify the change

From the repository root, validate the file you edited:

```sh
ghostty +validate-config --config-file=config/ghostty/config
```

On macOS, if the CLI is outside `PATH`, use the executable inside the
installed Ghostty app. For a visual change, inspect the affected window when
available. For a shortcut, try the key in its intended context. Report which
behavior you observed and whether verification covered only the config parser.

## Repair a host link

The [managed-link inventory](../../../src/dotfiles_setup/links.py) already
includes Ghostty. A settings edit needs only the repository source. If the
request also covers a missing or incorrect host link, use
[dotfiles-operations](../dotfiles-operations/SKILL.md). Preview the changes
with `./bootstrap.sh link --dry-run` and apply `./bootstrap.sh link` when
authorized.
