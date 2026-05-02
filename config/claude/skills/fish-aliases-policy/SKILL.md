---
name: fish-aliases-policy
description: Policy and reference implementation for fish aliases and abbreviations in this dotfiles repo. Use when adding shortcuts to `config/fish/conf.d/40-aliases.fish`, deciding alias vs abbr, or wiring tests. Keywords fish alias, fish abbr, 40-aliases, conf.d load order, type -q guard.
---

# Fish Aliases & Abbreviations — Policy + Implementation

Loaded when adding or reviewing shortcuts in this repo's fish config.

## When to Use What

- **Abbreviations (`abbr`)**: keystroke expansions for long flaggy commands. Purely interactive.
- **Aliases/Functions**: stable short commands that should also be callable from scripts (fish `alias` defines a function). Prefer real **functions** for anything beyond simple wrapping.

## File Layout & Load Order

```
config/fish/
  conf.d/
    10-nix.fish        # Nix env + PATH
    20-direnv.fish     # direnv hook (if installed)
    30-starship.fish   # prompt
    40-aliases.fish    # aliases + interactive abbreviations
  functions/
    nix-try.fish
    nix-install.fish
  config.fish          # interactive-only; keep light
```

`conf.d/*.fish` auto-source on interactive startup in lexical order. The `40-` prefix ensures aliases load **after** PATH and tool hooks.

## Reference Implementation: `config/fish/conf.d/40-aliases.fish`

```fish
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
abbr -a gco 'git checkout'
abbr -a gst 'git status -sb'
abbr -a glg 'git log --oneline --graph --decorate --all'
abbr -a kctx 'kubectl config use-context'

# Guard: only add k* abbr if kubectl is present
if not type -q kubectl
    abbr -e kctx 2>/dev/null
end

# Global editor default if unset
set -q EDITOR; or set -gx EDITOR nvim
```

### Why This Works

- `alias` in fish creates a **function** — callable from scripts. Gate each on `type -q` so missing tools don't pollute.
- Abbreviations are interactive-only; safe in `conf.d` since they don't affect scripts.
- All in one `40-aliases.fish` keeps reproducibility (no `funcsave`/universal var state).

## Tests (in `tests/docker-test-commands.fish`)

```fish
section "Aliases"
if functions -q g
    test_pass "alias g→git exists"
else
    test_fail "alias g missing"
end

if functions -q ll
    test_pass "alias ll→eza exists (if eza present)"
else
    echo "  ℹ️  ll absent if eza not installed"
end

section "Extra Abbreviations"
if abbr --show 2>/dev/null | grep -q 'gco'
    test_pass "abbr gco exists"
else
    test_fail "abbr gco missing"
end
```

## Local Quick Check

```fish
exec fish -l
functions g | head -n1        # should show a function called g
abbr --show | grep -E 'gco|gst|glg'
```

## Scripting Caveat

Scripts run as `fish -c` may not be interactive. Aliases are functions, so they exist; abbreviations don't trigger (by design). Keep automation using full commands (e.g., `git`) to avoid coupling to personal shortcuts.

## Adding a New Shortcut — Checklist

- [ ] Pick alias vs abbr per the policy above
- [ ] Add to `40-aliases.fish` guarded with `type -q <tool>`
- [ ] Add the package to `flake.nix` if it's a new tool
- [ ] Extend `tests/docker-test-commands.fish` to assert presence
- [ ] `make test-pre` → `make test-local`
