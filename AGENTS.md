# AGENTS.md

## Mission

Reproducible tools with Nix; portable, editable configs via symlinks; fast onboarding and deterministic CI. Do **not** migrate dotfiles to Home Manager; keep them repo-driven and linked into `~/.config`.

## Principles

* **Idempotent**: every script safe to run twice.
* **Cross‑platform**: macOS, Ubuntu, Fedora all green.
* **Minimal surface area**: configs live under `config/**`; packages live in `flake.nix`.
* **Test-first ops**: pre-flight (local) → isolated (ephemeral HOME) → Docker matrix.
* **Rollbackable**: links backed up, package generations garbage-collectable.

## Authority & Guardrails

**You may** edit: `flake.nix`, `scripts/*.sh`, `config/**`, `Makefile`, `README.md`, `AGENTS.md`, `tests/**`, CI workflows.

**You must not**: commit secrets, hard-code machine paths, or regress OS coverage.

**Breaking changes**: require a migration note in this file and a `tests/` update.

## Decision Tree

* **Need a tool?** Add it to `flake.nix` → `nix profile install .`.
* **Need a config?** Add under `config/**` → wire in `scripts/link-config.sh`.
* **Unsure?** Prefer plain files + symlinks over bespoke derivations.

---

## Workflow

1. Branch `feat/<slug>` or `fix/<slug>`.
2. Make the smallest change that passes `make test-pre` locally.
3. If touching fish, run `make test-local` (ephemeral HOME) and `make test-docker` if available.
4. Open PR with:

   * Scope and motivation
   * Screens/logs of tests
   * Rollback plan
5. Merge only when CI *summary* job is ✅.

Rollback: re-link configs (script backs up physical dirs), or `nix profile rollback` if a package regressed.

---

## Quality Bar (PR Checklist)

* [ ] Idempotent (re-run safe)
* [ ] Cross‑platform verified (macOS, Ubuntu, Fedora)
* [ ] Tests updated (pre-flight + relevant suite)
* [ ] Docs updated (README/AGENTS)
* [ ] Rollback path obvious

---

## Troubleshooting Canon

* Source daemon: `. /nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh`
* Fish not seeing Nix? `exec fish -l` and confirm `config/fish/conf.d/10-nix.fish`.
* Fedora: keep SELinux enforcing; Determinate installer provides policy.

---

# Fish Aliases & Abbreviations (Policy + Implementation)

## When to use what

* **Abbreviations (`abbr`)**: keystroke expansions for long commands with flags. Purely interactive.
* **Aliases/Functions**: stable short commands that should be callable by scripts (become functions in fish). Prefer **functions** for anything beyond simple wrapping.

## File layout & load order

All fish startup is file-based and reproducible:

```
config/fish/
  conf.d/
    10-nix.fish        # Nix env + PATH
    20-direnv.fish     # direnv hook (if installed)
    30-starship.fish   # prompt
    40-aliases.fish    # <— NEW: aliases + interactive abbreviations
  functions/
    nix-try.fish
    nix-install.fish
  config.fish          # empty/interactive-only; keep light
```

`conf.d/*.fish` are auto-sourced on interactive startup in lexical order; the `40-` prefix ensures aliases load after PATH and tool hooks.

## Create a dedicated aliases file

**Add:** `config/fish/conf.d/40-aliases.fish`

```fish
# config/fish/conf.d/40-aliases.fish
#
# Session-safe aliases and interactive abbreviations.
# Keep wrappers tiny; prefer functions for nontrivial logic.

# ——— Aliases -> define callable functions ———
function __maybe_alias --argument-names name target
    if type -q $target
        alias $name="$target"
    end
end

# Core CLI shorthands (only if binary exists)
__maybe_alias g git
__maybe_alias k kubectl
__maybe_alias d docker
__maybe_alias dc docker-compose
__maybe_alias ll eza

# Decorated examples using functions (more robust than raw alias)
if type -q eza
    functions -q la; or function la --wraps='eza -la' --description 'list all'
        eza -la $argv
    end
end

# ——— Interactive abbreviations ———
# Use for long flaggy commands; expands on SPACE/TAB in interactive shells.
abbr -a gco 'git checkout'
abbr -a gst 'git status -sb'
abbr -a glg 'git log --oneline --graph --decorate --all'
abbr -a kctx 'kubectl config use-context'

# Guard example: only add k* abbr if kubectl is present
if not type -q kubectl
    abbr -e kctx 2>/dev/null
end

# Global editor default if unset (harmless if already set elsewhere)
set -q EDITOR; or set -gx EDITOR nvim
```

### Why this works

* `alias` in fish creates a **function** (callable from scripts too). We gate each alias on `type -q` to avoid noise on machines without the tool.
* Abbreviations are purely interactive; safe in `conf.d` since they don’t affect scripts.
* Putting both in one `40-aliases.fish` keeps reproducibility (no `funcsave`/universal var state).

## Usability tests (add to `tests/docker-test-commands.fish`)

Append these checks near the existing function/abbr sections:

```fish
# Aliases become functions; confirm a couple
section "Aliases"
if functions -q g
    test_pass "alias g→git exists"
else
    test_fail "alias g missing"
end

if functions -q ll
    test_pass "alias ll→eza exists (if eza present)"
else
    echo "  ℹ️  ll will be absent if eza is not installed"
end

# Abbreviations we added
section "Extra Abbreviations"
if abbr --show 2>/dev/null | grep -q 'gco'
    test_pass "abbr gco exists"
else
    test_fail "abbr gco missing"
end
```

## Local quick check

```fish
exec fish -l
functions g | head -n1        # should show a function called g
abbr --show | grep -E 'gco|gst|glg'
```

## Scripting caveat

* Scripts run as `fish -c` may not be *interactive*. That’s okay: aliases are functions, so they exist; abbreviations don’t trigger (by design). Keep automation using full commands (e.g., `git`) to avoid coupling to personal shortcuts.

---

## Contributor Playbooks

### Add a new CLI tool + shortcut

1. Add package to `flake.nix`.
2. Add alias/abbr in `40-aliases.fish` guarded with `type -q <tool>`.
3. Extend tests to assert presence when the tool exists.
4. Run: `make test-pre` → `make test-local`.

### Bump package set

```bash
make update
# Verify locally
make test-pre && make test-local
# Push and let CI matrix run
```

### Add a fish function

Create `config/fish/functions/<name>.fish`:

```fish
function mywrap --description 'example wrapper'
    command realcmd --flag $argv
end
```

Then reference it in docs and, if relevant, add a small test.

---

## Migrations (none outstanding)

Record any one-time steps here in future PRs.
