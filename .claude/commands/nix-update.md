---
description: Update Nix packages and show version changes summary
---

Update all packages in the flake to their latest versions and provide a clear summary of what changed.

**Workflow:**

1. **Update flake.lock**
   - Run `make update` to fetch latest nixpkgs
   - Capture the old and new nixpkgs commit hashes

2. **Compare package versions**
   - Extract old and new nixpkgs commits from git diff
   - For key packages in flake.nix, compare versions:
     - Version control: git, gh, lazygit
     - Languages: rustup, go, python3, deno, bun
     - Shell/Terminal: fish, zsh, tmux, starship, zellij
     - CLI tools: ripgrep, fd, bat, eza, delta, fzf, jq, yq
     - Editors: neovim, codex, claude-code
     - Dev tools: direnv, nix-direnv
     - Containers: docker-client, docker-compose, lazydocker, k9s
     - System: htop, btop, ncdu
     - Other: just, buf, grpcurl, dogdns
   - Use: `nix eval "github:NixOS/nixpkgs/COMMIT#PACKAGE.version" --raw`

3. **Verify the update**
   - Run `make test-pre` to ensure flake is still valid
   - Run `nix build .#default --dry-run` to check if packages can be built
   - If dry-run fails with build errors, recommend reverting: `git checkout HEAD -- flake.lock`
   - Report any failures with clear error messages

4. **Present summary**
   - Show upgraded packages in a clear table format
   - Highlight notable updates (major/minor version bumps)
   - Display nixpkgs commit range and date span
   - Provide GitHub compare link for full nixpkgs changelog

**Output format:**

```
✅ Flake updated successfully!

📦 Package Updates (MMM DD → MMM DD):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PACKAGE         OLD VERSION  →  NEW VERSION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
git             2.51.0       →  2.51.2
go              1.25.2       →  1.25.3
fish            4.1.2        →  4.2.0  ⭐ (major)
...

🔗 Full nixpkgs changelog:
https://github.com/NixOS/nixpkgs/compare/OLD_HASH..NEW_HASH

📊 Summary:
- X packages updated
- Y major updates, Z minor updates

✅ Verification: make test-pre passed

💡 Next steps:
git add flake.lock
git commit -m "chore: update flake.lock to nixpkgs MMM DD"
```

**Error handling:**
- If `make update` fails, explain the error and suggest fixes
- If version comparison fails for a package, mark as "N/A" and continue
- If tests fail, show the failure and recommend rolling back

**Performance:**
- Run version comparisons in parallel when possible
- Only check packages that are actually in flake.nix
- Cache nixpkgs commit hashes to avoid re-parsing

**User experience:**
- Keep output concise but informative
- Use emojis sparingly for visual scanning
- Provide actionable next steps
- Include the commit message suggestion

**IMPORTANT - Final reminder:**
After the user commits the flake.lock changes, remind them to actually install the updated packages:
```bash
make install-packages
```
or:
```bash
nix profile install . --priority 5
```

This step is REQUIRED to upgrade the installed packages to match the new flake.lock. Simply updating flake.lock does NOT upgrade installed packages.
