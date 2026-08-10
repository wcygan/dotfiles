# Operations Runbook

## Install and Onboard

### Existing Nix installation

```bash
./bootstrap.sh
./bootstrap.sh verify
```

The default command runs `install`: profile, managed links, pinned Rust tools,
then strict verification. It does not edit Bash or zsh startup files.

### macOS without Nix

Run `./bootstrap.sh`. The bootstrapper opens the Determinate macOS package and
stops. Complete the package installation, start a new shell, and rerun. Do not
automate past the package handoff.

### Linux or WSL without Nix

Only after explicit authorization:

```bash
./bootstrap.sh --install-nix --yes
```

The bootstrapper may then invoke the official Determinate installer.

### Optional shell handoff

```bash
./bootstrap.sh install --shell-handoff
# or independently
./bootstrap.sh shell-handoff
```

This is opt-in because it changes interactive Bash/zsh startup behavior.

### Pinned global agent skills

Use `$agent-skills-integration` for every provider-source, consumer-pin,
installation, verification, collision, stale-skill, or recovery decision. It
defines the authoritative provider/consumer/runtime boundary and pin-advance
workflow.

Install or reconcile the external `agent-skills` collection for Codex's shared
user scope through the supported root entry point:

```bash
./bootstrap.sh agent-skills
./bootstrap.sh agent-skills --check
```

The first command is mutating, serialized, and journaled. It reads the exact
commit and portable relative directory from `agent-skills.lock.toml`, refuses
same-name skills from another source or location, invokes `gh skill install
--dir "$HOME/.agents/skills"`, and verifies all pinned catalog entries afterward
through `gh skill list --dir`. The check command is read-only. Installed skill
copies and GitHub CLI tracking state are machine-local outputs. GitHub CLI's
current Codex host mapping still uses `~/.codex/skills`; this integration uses
the shared user directory documented by Codex instead. GitHub CLI does not
prune files or skill directories removed upstream, so review cleanup separately
when advancing the pin.

An unchanged rerun is catalog-state idempotent, not a byte-for-byte no-op.
Because the command uses `--force`, GitHub CLI refreshes `updatedAt` for the
managed entries in the machine-local `~/.agents/.skill-lock.json`. Treat a
timestamp-only tracking diff as expected bookkeeping. Acceptance requires the
normalized inventory, source, custom-directory scope, exact pin, installed
paths, duplicate-name count, and installed file contents to remain unchanged;
any other difference is a failed idempotency check. `$agent-skills-integration`
is authoritative for this boundary.

After a successful shared-directory install and verification, an explicitly
authorized migration may remove the prior Codex-host copies with:

```bash
./bootstrap.sh agent-skills --cleanup-legacy --yes
```

That cleanup refuses to remove any legacy entry unless every expected skill has
one matching Codex user-scope path, source, pin, and version. It is idempotent
once no matching legacy catalog remains, but it is not a general skill-pruning
command.

## Inspect and Diagnose

```bash
./bootstrap.sh doctor      # advisory; PASS/WARN
./bootstrap.sh verify      # strict and read-only; PASS/FAIL
./bootstrap.sh recover     # read-only recovery inspection
nix profile list --json    # profile identity and store outputs
```

Interpret failures from the earliest violated boundary:

1. pending recovery or mutation lock;
2. Nix availability and exact profile origin;
3. profile store-output binaries and Python version;
4. pinned Rust toolchain resolution;
5. managed links and local Codex config.

Do not repair strict verification by consulting ambient `PATH`, renaming a
profile element, changing the global rustup default, or comparing copied config
contents.

## Links, Configuration, and Cleanup

Preview before applying:

```bash
./bootstrap.sh link --dry-run
./bootstrap.sh uninstall --dry-run
```

Apply only with the requested authority:

```bash
./bootstrap.sh link
./bootstrap.sh uninstall
```

New configuration belongs under `config/**` and must be added to the inventory
in `src/dotfiles_setup/links.py`. Use XDG destinations only for XDG-compliant
programs. Add platform and HOME/XDG/CODEX override tests for path changes.

## Interrupted Operations

Always inspect first:

```bash
./bootstrap.sh recover
```

Apply only after reviewing every proposed action and receiving explicit
authorization:

```bash
./bootstrap.sh recover --apply --yes
```

Recovery is intentionally conservative. If a current destination or backup no
longer matches the journal, stop for manual intervention. Nix profile changes
are not reversed automatically:

```bash
nix profile rollback
```

An interrupted `agent-skills` command also has external state that recovery
does not reverse automatically. Inspect it with `./bootstrap.sh agent-skills
--check`; an authorized recovery apply only acknowledges that state.

Use the annotated `pre-transactional-setup-recovery` tag only as the known
repository rollback point before the transactional architecture; it does not
replace user-file or Nix-generation recovery.

## Package and Toolchain Maintenance

### Add or remove a Nix package

1. Edit `flake.nix`.
2. Run focused evaluation and tests.
3. Update the managed profile:

   ```bash
   ./bootstrap.sh profile
   ./bootstrap.sh verify
   ```

Do not modify `flake.lock` merely to change the package list.

### Update nixpkgs

Use `$nix-update` and the explicit update target:

```bash
make update
make test-pre
make test-eval
./bootstrap.sh verify
```

`make update` intentionally changes `flake.lock` and then updates the profile.
Ordinary develop, profile, test, and CI consumers must retain
`--no-write-lock-file` behavior.

The selected nixpkgs branch must continue supporting all four declared
systems, including Intel macOS. A successful Linux build is not proof of that
contract; run `make test-eval` and use macOS evidence when behavior is
platform-sensitive.

### Update Rust

1. Review an official Rust release and choose an exact numeric patch version.
2. Edit `rust-toolchain.toml`.
3. Update Rust and verification tests.
4. Run:

   ```bash
   ./bootstrap.sh rustup
   ./bootstrap.sh verify
   make test-pre
   ```

Never replace the explicit `rustup which --toolchain <pin> rust-analyzer`
contract with a global default or ambient lookup.

### Update Python or uv

Keep the Python constraint aligned across `flake.nix`, `pyproject.toml`, Ruff,
tests, strict verification, Docker fixtures, and CI. Regenerate `uv.lock` only
through an intentional dependency/runtime update and verify with
`uv lock --check` through `make test-pre`.

### Update Action or container pins

- Pin every GitHub Action to a full 40-character release commit and keep its
  human-readable version comment.
- Pin every normal Docker base to a full multi-platform manifest digest.
- Keep floating `--pull` behavior confined to `freshness.yml`.
- Let Dependabot propose updates for human review; do not enable auto-merge.
- Re-run `tests/test_repository_policy.py`, the affected workflow-equivalent
  target, and the Docker matrix when image inputs change.

## Validation Matrix

| Change | Required local evidence |
| --- | --- |
| Skill or docs only | frontmatter/link check; `make test-pre`; docs build when docs change |
| Python setup behavior | focused pytest; `make test-pre`; strict verify when applicable |
| Managed links or cleanup | focused pytest; `make test-local`; `make test-pre` |
| Shell handoff or Fish | focused pytest; `make test-shell`; `make test-syntax` |
| Nix package or system declaration | `make test-pre`; `make test-eval`; profile/verify when installed |
| Cross-platform bootstrap | prior gates plus `make test-docker`; relevant macOS evidence |
| Docker or CI policy | focused policy tests; YAML parse; `make test-docker` |
| Documentation | `make docs-build` |
| Broad setup/recovery change | all non-Docker gates, Docker matrix, explicit recovery tests, live read-only verify |

`make test-eval` evaluates all four systems but does not build them. Docker
acceptance covers Ubuntu and Fedora, not macOS. Record those distinctions in
the handoff.

## CI and Scheduled Operations

### Required pull-request CI

`.github/workflows/ci.yml` runs:

- locked Ruff/pytest and syntax validation;
- native Linux install twice to prove idempotency, followed by strict verify;
- all-system flake evaluation without building;
- reproducible docs build;
- Ubuntu/Fedora Docker acceptance with separate BuildKit cache scopes;
- an always-run summary that fails unless every required job succeeded.

Each job uses explicit runners, timeouts, least-privilege permissions, pinned
actions, safe diagnostics, and a final tracked-input diff check. Keep local
Make targets canonical so CI and developer acceptance cannot drift apart.

### macOS acceptance

`.github/workflows/macos.yml` runs Apple Silicon weekly or manually in an
isolated HOME/XDG/CODEX/RUSTUP/CARGO tree. Intel macOS is manual to control
cost. Both run locked tests plus install, doctor, and strict verification.

### Upstream freshness

`.github/workflows/freshness.yml` is scheduled/manual compatibility evidence.
It removes committed Docker digests only in temporary runner files, pulls
current tags, and verifies the resulting image. It must never rewrite or
commit repository files.

### Documentation deployment

Pull requests build the Docusaurus site through `make docs-build`. Pages upload
and deployment occur only on a push to `main`, with write permissions scoped
to the deploy job.

## Operational Handoff

Always include:

- exact files and public interfaces changed;
- commands and test counts;
- actual platform evidence versus evaluation-only or workflow-defined coverage;
- lockfile and worktree state;
- interrupted-operation or backup state, if relevant;
- rollback commands or tags;
- skipped checks and residual risks;
- commit/push/deploy status.
