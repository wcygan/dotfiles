# Platform Key FamilyDisplayName Warning

Fix "warning: unhandled Platform key FamilyDisplayName" error when using git/lazygit in Nix development environments.

## Problem

When running git commands or lazygit in the dotfiles directory, you see:

```
warning: unhandled Platform key FamilyDisplayName
```

This warning appears in stderr and can cause lazygit to crash with:

```
*fs.PathError chdir warning: unhandled Platform key FamilyDisplayName: no such file or directory
```

**Root cause:** Nix's development environment sets `DEVELOPER_DIR` to its own SDK, which includes an outdated `xcbuild` from 2019. When git or lazygit invoke `xcrun`, this old version cannot parse modern Xcode platform plist files (introduced in recent macOS versions).

## Solution

Override `DEVELOPER_DIR` in `.envrc` to use the system's CommandLineTools instead of Nix's SDK.

Add to `.envrc`:

```bash
use flake

# Override Nix's DEVELOPER_DIR to use system Xcode tools
# Fixes "Platform key FamilyDisplayName" warning from old xcbuild
# See: https://github.com/jetify-com/devbox/issues/2754
if [ -d /Library/Developer/CommandLineTools ]; then
  export DEVELOPER_DIR=/Library/Developer/CommandLineTools
fi
```

After editing `.envrc`:

```bash
direnv allow
```

The environment will automatically reload with the fix applied.

## Verification

1. Check that `DEVELOPER_DIR` is correctly set:
   ```bash
   echo $DEVELOPER_DIR
   # Should output: /Library/Developer/CommandLineTools
   ```

2. Test git commands:
   ```bash
   git status
   # Should run without the warning
   ```

3. Test lazygit:
   ```bash
   lg
   # Should launch without errors
   ```

## Related Files

- `.envrc` - Direnv environment configuration
- `flake.nix` - Nix development environment definition

## References

- [jetify-com/devbox#2754](https://github.com/jetify-com/devbox/issues/2754) - Original issue report
- [jesseduffield/lazygit#5013](https://github.com/jesseduffield/lazygit/issues/5013) - Lazygit crash report
- [IlanCosman/tide#611](https://github.com/IlanCosman/tide/issues/611) - Similar issue in Fish shell prompt
