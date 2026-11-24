---
name: zellij-config
description: Change or troubleshoot Zellij keybindings, modes, layouts, themes, and pane behavior in this dotfiles repository.
---

# Configure Zellij

For settings and shortcuts, edit
[config/zellij/config.kdl](../../../config/zellij/config.kdl). Check the
binding in the mode where the user presses it. The same key can do something
different in another mode. Use `zellij setup --dump-config` to read the defaults
for the installed version when comparing behavior.

For a layout, edit the corresponding file under
[config/zellij/layouts/](../../../config/zellij/layouts/). The
[development layout](../../../config/zellij/layouts/dev.kdl) shows how this
repository names tabs, sets initial focus, and assigns sizes. Keep custom themes
in `config/zellij/themes/`. See the [KDL examples](REFERENCE.md) for individual
actions, layout properties, and theme syntax.

## Verify the change

From the repository root, check that Zellij reads the tracked configuration:

```sh
zellij --config-dir config/zellij --config config/zellij/config.kdl setup --check
```

Look for the tracked filename and `[CONFIG FILE]: Well defined.` For a shortcut,
exercise the key in its intended mode when a test session is available. For a
layout, open the changed file in a separate test session and check the requested
tabs, focus, and pane arrangement. Inspect any commands the layout launches
before starting it. Report which behavior you saw or which check you could run.

## Repair a host link

The [managed-link inventory](../../../src/dotfiles_setup/links.py) already
includes the Zellij directory. For a request to repair its host destination,
use [dotfiles-operations](../dotfiles-operations/SKILL.md). Preview the
changes with `./bootstrap.sh link --dry-run` and apply `./bootstrap.sh link`
when authorized.
