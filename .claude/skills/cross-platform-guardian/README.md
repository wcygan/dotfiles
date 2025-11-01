# Cross-Platform Guardian Skill

**Agent skill for maintaining cross-platform compatibility across macOS, Ubuntu, and Fedora in this dotfiles repository.**

## What This Skill Does

Automatically activates when you:
- Add new scripts, configs, or Nix packages
- Update `flake.nix` or `flake.lock`
- Mention platform issues ("works on Mac but not Linux")
- Request compatibility checks or cross-platform testing

**Capabilities**:
- 🔍 **Audit**: Scans for hardcoded paths, platform-specific commands, missing guards
- 🔧 **Auto-fix**: Applies fixes for common issues (dynamic paths, conditionals, guards)
- 🧪 **Test**: Validates Nix flake across all 4 architectures
- 📦 **Update**: Manages `flake.lock` updates with platform testing

## Quick Start

### Run Compatibility Audit

```bash
./.claude/skills/cross-platform-guardian/scripts/audit-compatibility.sh
```

**Checks**:
- Hardcoded user paths (`/Users/wcygan`)
- Platform-specific commands without conditionals (`open` vs `xdg-open`)
- Shebang correctness (bash features with `#!/bin/sh`)
- Unguarded tool usage in Fish configs
- Nix flake architecture support
- CI test matrix coverage

### Test Nix Flake Platforms

```bash
./.claude/skills/cross-platform-guardian/scripts/test-platform-compatibility.sh
```

**Tests**:
- x86_64-linux (Intel/AMD Linux)
- aarch64-linux (ARM Linux)
- x86_64-darwin (Intel Mac)
- aarch64-darwin (Apple Silicon)

## File Structure

```
.claude/skills/cross-platform-guardian/
├── SKILL.md                    # Main skill instructions (loaded by Claude)
├── REFERENCE.md                # Detailed technical reference
├── README.md                   # This file
└── scripts/
    ├── audit-compatibility.sh          # Scans for compatibility issues
    └── test-platform-compatibility.sh  # Tests Nix flake across platforms
```

## Integration with Repository

### Git Hooks (Optional)

Add to `.git/hooks/pre-commit`:
```bash
#!/usr/bin/env bash
./.claude/skills/cross-platform-guardian/scripts/audit-compatibility.sh || exit 1
```

### Makefile Integration

Already integrated via:
- `make test-pre` → Pre-flight checks
- `make test-docker` → Docker matrix (Ubuntu + Fedora)

### CI/CD

Runs automatically in GitHub Actions:
- `.github/workflows/ci.yml` → Full test matrix

## Common Usage Patterns

### Before Adding New Feature

```bash
# 1. Audit current state
./.claude/skills/cross-platform-guardian/scripts/audit-compatibility.sh

# 2. Implement feature...

# 3. Re-audit
./.claude/skills/cross-platform-guardian/scripts/audit-compatibility.sh

# 4. Run full tests
make test-pre && make test-docker
```

### After Updating Nix Flake

```bash
# 1. Update flake
nix flake update

# 2. Test all platforms
./.claude/skills/cross-platform-guardian/scripts/test-platform-compatibility.sh

# 3. Run Docker matrix
make test-docker

# 4. Commit if passing
git add flake.lock
git commit -m "chore(nix): update flake.lock"
```

### Debugging Platform-Specific Failure

```bash
# 1. Check CI logs to identify failing platform

# 2. Audit for issues
./.claude/skills/cross-platform-guardian/scripts/audit-compatibility.sh

# 3. Test specific platform locally via Docker
docker build -f tests/Dockerfile.ubuntu -t test .
docker run -it test bash

# 4. Apply fixes and re-test
```

## Skill Activation Examples

**User requests that trigger this skill**:
- "Check if this works on Ubuntu"
- "Make sure this is cross-platform compatible"
- "Update the Nix flake"
- "Why is CI failing on Fedora?"
- "Add support for Alpine Linux"
- "Fix this hardcoded path"

**Claude will automatically**:
1. Run audit to identify issues
2. Apply auto-fixes where possible
3. Report findings with file:line references
4. Suggest manual fixes for complex cases
5. Validate via test scripts

## Supported Platforms

| Platform | Test Method | Status |
|----------|-------------|--------|
| macOS (Intel) | CI native | ✅ Fully supported |
| macOS (ARM) | CI native | ✅ Fully supported |
| Ubuntu 22.04+ | CI Docker | ✅ Fully supported |
| Fedora 40 | CI Docker | ✅ Fully supported |
| Other Linux | Untested | ⚠️ Partial support |
| WSL2 | Untested | ❌ Not supported |

## How Compatibility is Achieved

1. **Nix as Universal Package Manager**
   - Single `flake.nix` for all platforms
   - Binary cache shared across architectures
   - Reproducible from `flake.lock`

2. **Platform Detection Layers**
   - Bash: `$OSTYPE` variable
   - Fish: `uname` command
   - Container: `/.dockerenv` check

3. **Path Standardization**
   - XDG Base Directory compliance where possible
   - Platform-specific overrides for non-compliant tools (VSCode, tmux)

4. **Testing Infrastructure**
   - Pre-flight: Syntax validation
   - Isolated: Ephemeral HOME testing
   - Docker: Ubuntu + Fedora full simulation
   - CI: Native ubuntu-latest + macos-latest

## Keeping Systems Up-to-Date

### Nix Package Updates

```bash
# Weekly update cycle
nix flake update
./.claude/skills/cross-platform-guardian/scripts/test-platform-compatibility.sh
make test-docker
git commit -m "chore(nix): update flake.lock"
```

### Config Synchronization

Configs are symlinked from repo → `~/.config/`:
```bash
# Re-link after pulling changes
make link

# Or full reinstall
./install.sh  # Idempotent, safe to re-run
```

### Dockerfile Updates

Update base images monthly:
```bash
# tests/Dockerfile.ubuntu
FROM ubuntu:25.04  # Update version

# tests/Dockerfile.fedora
FROM fedora:40     # Update version
```

## Troubleshooting

### "Audit script reports false positive"

Edit `.claude/skills/cross-platform-guardian/scripts/audit-compatibility.sh` to refine detection logic.

### "Platform test fails but package exists"

```bash
# Check nixpkgs directly
nix search nixpkgs <package-name>
nix eval nixpkgs#<package>.meta.platforms
```

### "CI passes but local Docker fails"

```bash
# Rebuild Docker without cache
docker build --no-cache -f tests/Dockerfile.ubuntu .
```

## References

- **Main skill**: `SKILL.md` (loaded by Claude when activated)
- **Technical details**: `REFERENCE.md` (comprehensive guide)
- **Repository docs**: `AGENTS.md` (workflow and standards)
- **User preferences**: `~/.claude/CLAUDE.md` (personal dev methodology)

---

**Maintained by**: Cross-platform compatibility skill (auto-invoked by Claude)
**Last updated**: 2025-11-01
