# Cross-Platform Guardian - Reference Guide

Detailed technical reference for maintaining cross-platform compatibility in this dotfiles repository.

## Platform Architecture

### Supported Platforms

| Platform | Architecture | Test Method | Priority |
|----------|-------------|-------------|----------|
| macOS Intel | x86_64-darwin | CI native (macos-latest) | High |
| macOS ARM | aarch64-darwin | CI native (macos-latest on M1) | High |
| Ubuntu 22.04+ | x86_64-linux | CI Docker | High |
| Fedora 40 | x86_64-linux | CI Docker | High |
| Ubuntu ARM | aarch64-linux | Untested (potential) | Medium |
| Alpine Linux | x86_64-linux (musl) | Untested | Low |
| WSL2 | x86_64-linux | Untested | Low |

## Compatibility Strategy

### 1. Universal Package Management (Nix)

**Philosophy**: Use Nix as the single source of truth for packages across all platforms.

**Benefits**:
- Binary cache shared across platforms
- Reproducible builds from `flake.lock`
- No distro-specific package managers needed
- Rollback via Nix generations

**Implementation** (`flake.nix:11-16`):
```nix
allSystems = [
  "x86_64-linux"   # Standard Linux (Ubuntu, Fedora, etc.)
  "aarch64-linux"  # ARM Linux (Raspberry Pi, AWS Graviton)
  "x86_64-darwin"  # Intel Mac
  "aarch64-darwin" # Apple Silicon (M1/M2/M3)
];
```

**Package definition** (`flake.nix:38-134`):
```nix
buildEnv {
  name = "dotfiles-env";
  paths = with pkgs; [
    # 134 packages - same list for all platforms
    git fish starship direnv ripgrep fd bat eza
    # ...
  ];
}
```

### 2. Platform Detection Layers

**Layer 1: Bash scripts** (install.sh, scripts/*.sh)
- Uses `$OSTYPE` environment variable
- Pattern: `if [[ "$OSTYPE" == "darwin"* ]]; then`
- Fallback: Check `/etc/os-release`, `/etc/fedora-release`, `/etc/lsb-release`

**Layer 2: Fish shell** (config/fish/conf.d/*.fish)
- Uses `uname` command output
- Pattern: `if test (uname) = Darwin`
- Lighter than bash, portable across shells

**Layer 3: Container detection** (scripts/install-nix.sh)
- Checks: `/.dockerenv` file, `$container` env var, systemctl availability
- Used to modify Nix installer flags (`--init none` in containers)

**Layer 4: Architecture detection** (config/fish/conf.d/05-homebrew.fish)
- Checks directory existence: `/opt/homebrew` vs `/usr/local`
- Apple Silicon uses `/opt/homebrew`, Intel uses `/usr/local`

### 3. Path Standardization

**XDG Base Directory Specification**:
- `XDG_CONFIG_HOME=${XDG_CONFIG_HOME:-$HOME/.config}`
- `XDG_DATA_HOME=${XDG_DATA_HOME:-$HOME/.local/share}`
- `XDG_STATE_HOME=${XDG_STATE_HOME:-$HOME/.local/state}`
- `XDG_CACHE_HOME=${XDG_CACHE_HOME:-$HOME/.cache}`

**Config locations by tool**:

| Tool | XDG-Compliant | macOS | Linux |
|------|---------------|-------|-------|
| Fish | ✅ | `~/.config/fish` | `~/.config/fish` |
| Starship | ✅ | `~/.config/starship.toml` | `~/.config/starship.toml` |
| Zed | ✅ | `~/.config/zed` | `~/.config/zed` |
| Direnv | ✅ | `~/.config/direnv` | `~/.config/direnv` |
| VSCode | ❌ | `~/Library/Application Support/Code/User` | `~/.config/Code/User` |
| tmux | ❌ | `~/.tmux.conf` | `~/.tmux.conf` |

**Implementation** (`scripts/link-config.sh:66-70`):
```bash
if [[ "$OSTYPE" == "darwin"* ]]; then
  VSCODE_USER_DIR="$HOME/Library/Application Support/Code/User"
else
  VSCODE_USER_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/Code/User"
fi
```

### 4. Testing Infrastructure

**Test Pyramid**:
```
           /\
          /CI\          GitHub Actions (ubuntu + macos)
         /----\
        /Docker\        Docker matrix (Ubuntu + Fedora)
       /--------\
      / Isolated \      make test-local (ephemeral HOME)
     /------------\
    /  Pre-flight  \    make test-pre (syntax, permissions)
   /----------------\
```

**Pre-flight checks** (`make test-pre`):
- Script permissions (executable)
- Bash syntax validation (`bash -n`)
- Dockerfile existence
- Fish setup verification

**Local isolated tests** (`make test-local`):
```bash
# Creates ephemeral HOME directory
export HOME=$(mktemp -d)
./install.sh
fish -lc './tests/docker-test-commands.fish'
```

**Docker matrix tests** (`make test-docker`):
- Builds: `tests/Dockerfile.ubuntu`, `tests/Dockerfile.fedora`
- Runs: Full installation + verification
- Verifies: Idempotency (re-run install.sh)

**CI native tests** (`.github/workflows/ci.yml`):
- `ubuntu-latest`: Uses GitHub Actions runner with Nix
- `macos-latest`: Uses GitHub Actions runner with Nix
- Tests actual user environment (not containerized)

### 5. Common Anti-Patterns

**❌ Hardcoded paths**:
```bash
# BAD - user-specific
DOTFILES="/Users/wcygan/Development/dotfiles"

# GOOD - dynamic resolution
DOTFILES="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
```

**❌ Unguarded platform commands**:
```bash
# BAD - macOS only
open README.md

# GOOD - conditional
if [[ "$OSTYPE" == "darwin"* ]]; then
  open README.md
else
  xdg-open README.md
fi
```

**❌ Shell-specific syntax in wrong shebang**:
```bash
# BAD - bash features with sh shebang
#!/bin/sh
declare -a packages=(git fish)  # bash-only

# GOOD - correct shebang
#!/usr/bin/env bash
declare -a packages=(git fish)
```

**❌ Assuming tools exist**:
```fish
# BAD - crashes if starship not installed
eval (starship init fish)

# GOOD - graceful degradation
if type -q starship
  eval (starship init fish)
end
```

**❌ Platform-specific package in universal list**:
```nix
# BAD - may not exist on all platforms
packages = with pkgs; [
  darwin.apple_sdk  # macOS-only, breaks Linux
];

# GOOD - conditional inclusion
packages = with pkgs; [
  git fish starship
] ++ lib.optionals stdenv.isDarwin [
  darwin.apple_sdk
];
```

## Nix Flake Management

### Update Protocol

**When to update**:
- Weekly scheduled maintenance
- Before adding new packages
- When CI reports outdated nixpkgs
- After major nixpkgs releases

**Update steps**:
```bash
# 1. Update flake.lock
nix flake update

# 2. Check what changed
git diff flake.lock

# 3. Test all platforms
./.claude/skills/cross-platform-guardian/scripts/test-platform-compatibility.sh

# 4. Run full test matrix
make test-pre
make test-docker

# 5. Test on current platform
nix profile install .
fish -lc 'echo "Smoke test passed"'

# 6. Commit if all pass
git add flake.lock
git commit -m "chore(nix): update flake.lock (nixpkgs YYYY-MM-DD)"
```

**Rollback on failure**:
```bash
# Option 1: Git rollback
git checkout HEAD -- flake.lock

# Option 2: Nix generation rollback
nix profile rollback
```

### Adding New Packages

**Process**:
1. Search for package: `nix search nixpkgs <name>`
2. Add to `flake.nix` package list (alphabetically)
3. Run platform compatibility test
4. Update tests if package requires verification
5. Document in AGENTS.md if it's a critical tool

**Platform availability check**:
```bash
# Check if package builds on all platforms
nix eval .#packages.x86_64-linux.default.name
nix eval .#packages.aarch64-linux.default.name
nix eval .#packages.x86_64-darwin.default.name
nix eval .#packages.aarch64-darwin.default.name
```

**Handling platform-specific packages**:
```nix
# In flake.nix
packages = with pkgs; [
  # Universal packages
  git fish starship

  # Conditional packages
] ++ lib.optionals stdenv.isDarwin [
  # macOS-only
] ++ lib.optionals stdenv.isLinux [
  # Linux-only
];
```

## CI/CD Integration

### GitHub Actions Workflow

**Structure** (`.github/workflows/ci.yml`):
```yaml
jobs:
  pre-checks:
    runs-on: ubuntu-latest
    # Validates scripts, syntax, Dockerfiles

  docker-matrix:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        include:
          - os: ubuntu-25.04
          - os: fedora-40
    # Full Docker build + test for each distro

  native-test:
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest]
    # Native Nix install + smoke tests

  summary:
    needs: [pre-checks, docker-matrix, native-test]
    # Aggregates results, fails if any job failed
```

**Triggering**:
- On push to main
- On pull requests
- Manual workflow dispatch
- Scheduled (weekly)

**Reading results**:
- Green check: All platforms pass
- Red X: Check job logs for specific platform failure
- Yellow dot: In progress

### Local Testing Before Push

**Recommended workflow**:
```bash
# 1. Pre-flight (fast, syntax checks)
make test-pre

# 2. Local isolated test (medium, ephemeral HOME)
make test-local

# 3. Docker matrix (slow, full simulation)
make test-docker

# 4. Platform-specific compatibility
./.claude/skills/cross-platform-guardian/scripts/audit-compatibility.sh
./.claude/skills/cross-platform-guardian/scripts/test-platform-compatibility.sh

# 5. Push if all pass
git push
```

## Auto-Fix Capabilities

### Supported Fixes

**1. Hardcoded paths → Dynamic resolution**
```bash
# Detection
grep -r "/Users/wcygan" scripts/

# Auto-fix
sed -i.bak 's|/Users/wcygan/Development/dotfiles|$(cd "$(dirname "${BASH_SOURCE[0]}")/.." \&\& pwd)|g' scripts/*.sh
```

**2. Platform commands → Conditional logic**
```bash
# Detection
grep -rn "open " scripts/ | grep -v "xdg-open"

# Auto-fix (via Edit tool)
# Replace: open README.md
# With:
if [[ "$OSTYPE" == "darwin"* ]]; then
  open README.md
else
  xdg-open README.md
fi
```

**3. Shebang corrections**
```bash
# Detection
find scripts/ -name "*.sh" -exec grep -l "^#!/bin/sh" {} \; | xargs grep -l "\[\["

# Auto-fix
sed -i.bak '1s|^#!/bin/sh|#!/usr/bin/env bash|' scripts/problematic.sh
```

**4. Fish guard additions**
```fish
# Detection
grep -n "eval (starship init fish)" config/fish/conf.d/*.fish

# Auto-fix (via Edit tool)
# Replace: eval (starship init fish)
# With:
if type -q starship
  eval (starship init fish)
end
```

### Manual Review Required

Some issues require human judgment:
- **Architecture decisions**: Should package be removed or made conditional?
- **Feature parity**: Should macOS and Linux behavior differ?
- **Performance tradeoffs**: Should Docker tests be extended (slower CI)?
- **Breaking changes**: Affects users' existing setups?

## Troubleshooting

### Issue: CI passes but fails locally

**Possible causes**:
1. Outdated `flake.lock` locally
2. Different Nix daemon version
3. Local state pollution (old symlinks)

**Debug steps**:
```bash
# Sync flake.lock
git pull origin main
nix flake update

# Clean Nix profile
nix profile list
nix profile remove <problematic-package>

# Clean symlinks
./scripts/cleanup-symlinks.sh

# Re-test
./install.sh
```

### Issue: Docker test fails but native passes

**Possible causes**:
1. Dockerfile out of sync with install.sh
2. Container-specific assumptions (systemd, sudo)
3. Missing base packages in Docker image

**Debug steps**:
```bash
# Run Docker interactively
docker build -f tests/Dockerfile.ubuntu -t dotfiles-test .
docker run -it dotfiles-test bash

# Inside container:
./install.sh  # See where it fails
make test-pre
```

### Issue: Package unavailable on one platform

**Possible causes**:
1. Package doesn't support that platform (e.g., Darwin-only)
2. Package renamed in nixpkgs
3. Binary cache miss for that platform

**Debug steps**:
```bash
# Search nixpkgs
nix search nixpkgs <package-name>

# Check platform attribute
nix eval nixpkgs#<package>.meta.platforms

# Try alternative package
nix search nixpkgs <alternative-name>
```

**Resolution**:
- If truly unavailable: Add platform conditional
- If renamed: Update package name in flake.nix
- If cache miss: Wait for Hydra to build, or build locally

## Maintenance Checklist

### Weekly
- [ ] Run `nix flake update` + test matrix
- [ ] Check CI logs for warnings
- [ ] Review GitHub Actions usage (quota)

### Monthly
- [ ] Audit new files for compatibility issues
- [ ] Update Dockerfiles to latest base images
- [ ] Review and close stale compatibility issues

### Per Feature
- [ ] Run `audit-compatibility.sh` before commit
- [ ] Add regression test if fixing platform bug
- [ ] Update AGENTS.md if changing compatibility strategy
- [ ] Test on at least 2 platforms (macOS + Linux)

### Before Release
- [ ] Full test matrix passes (pre-flight + local + docker + CI)
- [ ] No hardcoded paths in `grep -r /Users/wcygan`
- [ ] All platforms in Nix flake still supported
- [ ] CLAUDE.md and AGENTS.md reflect current state

## Additional Resources

- **Nix flakes**: https://nixos.wiki/wiki/Flakes
- **XDG Base Directory**: https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html
- **Fish shell portability**: https://fishshell.com/docs/current/
- **GitHub Actions matrix**: https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#jobsjob_idstrategymatrix
