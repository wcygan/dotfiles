# Feature and journey index

Run commands from the owning checkout. Capture evidence outside the repository:

```bash
nightly_evidence=$(mktemp -d "${TMPDIR:-/tmp}/nightly-verification.XXXXXX")
git status --short > "$nightly_evidence/git-before.txt"
make nightly-status > "$nightly_evidence/status-before.txt" 2>&1
./bootstrap.sh recover > "$nightly_evidence/recovery-before.txt" 2>&1
```

Keep this shell variable in the same shell when using the following commands.
Inspect exit codes as well as logs. Preserve logs on failure. These are real
commands, not dry-runs: enable/disable/install mutate state; status/verify/recover
without `--apply` inspect it. The production updater has no dry-run option.

## 1. Inspect installed health

Prerequisite: existing installed checkout. No scheduler launch is required for
this read-only journey; the permanent scheduler should already be registered.

```bash
./bootstrap.sh verify > "$nightly_evidence/verify.txt" 2>&1
make nightly-status > "$nightly_evidence/status.txt" 2>&1
```

For an opted-in installation, require strict verify exit 0 and status with
`enabled: true`, `healthy: true`, the resolved owning repository, expected window,
and observation age. Read `last_run` separately; an empty result means no completed
nightly run was recorded, not that installation failed. Disabled/unconfigured is
valid only if that matches the user's intended state. Cleanup: no resources were
created except retained evidence. This journey does not test fresh reachability.

## 2. Enable, repair, and probe reachability

Prerequisites: installation/profile is usable, checkout is inside HOME, no pending
recovery, and scheduler ownership is understood. Preserve unrelated edits. This
journey is appropriate for requested setup/repair or rechecking an already enabled
installation; inspection alone does not authorize a first opt-in.

```bash
make nightly-enable > "$nightly_evidence/enable.txt" 2>&1
./bootstrap.sh verify > "$nightly_evidence/verify-after-enable.txt" 2>&1
make nightly-status > "$nightly_evidence/status-after-enable.txt" 2>&1
./bootstrap.sh recover > "$nightly_evidence/recovery-after.txt" 2>&1
```

Require all commands to succeed, healthy enabled status, matching owner, and no
pending recovery. Enable internally launches a real ephemeral scheduler job that
executes `bootstrap.sh nightly-probe` with a fresh token. It waits for a matching
acknowledgement before reporting success, then removes/stops its transient job.
The probe writes private health state and scheduler output, but performs no Nix
input update or profile installation.

Inspect native registration and confirm no leftover probes:

```bash
# macOS: permanent job must exist; no .probe-* job should remain.
launchctl print "gui/$(id -u)/com.wcygan.dotfiles.nightly" \
  > "$nightly_evidence/launch-agent.txt" 2>&1
launchctl list > "$nightly_evidence/launch-jobs.txt"
```

```bash
# Linux: permanent timer must be enabled/active with a next run.
systemctl --user status dotfiles-nightly.timer \
  > "$nightly_evidence/timer.txt" 2>&1
systemctl --user list-units --all 'dotfiles-nightly-probe-*' \
  > "$nightly_evidence/probe-units.txt"
```

Run only the block for the current OS. For remembered opt-in repair, use
`./bootstrap.sh install` instead of enable: it must report the nightly operation
and pass strict verification after a fresh probe. Test deliberate unload/stop and
repair only in a disposable instance or within explicit disruption scope. Require
verify to fail before repair and pass afterward.

Cleanup preserves the intended permanent enabled schedule and captured proof.
If first enable was temporary, run `make nightly-disable`, check disabled status,
and verify the permanent job is unloaded/timer inactive. Disabled generated files
and historical private state are retained. Do not disable an originally enabled
installation merely to clean up a verification run. Failed mutations require
read-only recovery inspection before another attempt; follow operations guidance
for any authorized recovery apply.

## 3. Daytime rejection and missed nights

Prerequisite: current local hour is outside 03; do not run this command at 03
unless an actual update is intended. Capture `date` first.

```bash
date > "$nightly_evidence/local-time.txt"
git hash-object flake.lock > "$nightly_evidence/lock-before.txt"
nix profile list --json > "$nightly_evidence/profile-before.json"
./bootstrap.sh nightly-run > "$nightly_evidence/daytime.txt" 2>&1
git hash-object flake.lock > "$nightly_evidence/lock-after.txt"
nix profile list --json > "$nightly_evidence/profile-after.json"
diff "$nightly_evidence/lock-before.txt" "$nightly_evidence/lock-after.txt"
diff "$nightly_evidence/profile-before.json" "$nightly_evidence/profile-after.json"
```

Require a skipped-outside-window message, exit 0, unchanged lock/profile, and no
update activity. No cleanup beyond preserving proof. For missed runs, inspect
status, native scheduler logs, last-run files, login/user-manager availability,
checkout ownership, and recovery. A sleeping/offline/logged-out machine may miss
a night; do not add daytime catch-up. Late macOS delivery may occur but the
runtime guard must reject it outside the window.

## 4. Reconfigure and reconcile

Prerequisites: a concrete requested policy change and reviewed current source and
state. Follow the [configuration map](configuration.md#reconfiguration-map).
Edit owning source and tests, run the relevant gates, then execute journey 2 using
normal install or enable to regenerate files and refresh the reviewed baseline.
Run journey 1 and inspect both generated content and native registration. Repeat
native acceptance on each affected OS; report unavailable platforms as gaps.
Cleanup removes only owned disposable test resources. Preserve production opt-in,
observations, rollback backups, evidence, and unrelated work.

## 5. Candidate, application, and failure recovery

Fast regression check:

```bash
nix --extra-experimental-features 'nix-command flakes' \
  develop --no-write-lock-file .#default \
  --command uv run --locked pytest tests/test_nightly.py -q
```

The focused tests simulate Nix/profile/network boundaries where needed;
they exercise age, deadlines, checkout guards, candidate/rollback and recovery
behavior but do not establish a real package upgrade or overnight delivery.

Real update acceptance requires a naturally mature observation, a healthy owning
checkout, network access, and the actual nighttime window. Let the scheduled job
run. Preserve `last-run.json`, `last-run.log`, scheduler diagnostics, before/after
lock and profile identities, strict verification, and recovery inspection. Require
candidate checks to succeed before application, the recorded installed result,
expected profile/lock changes, and strict verification afterward. During warmup,
an observed result without installation is expected. Do not backdate observations
or change the host clock to manufacture maturity.

On failure, inspect the journal and real lock/profile before retrying. The updater
attempts profile/guarded-lock restoration; interruption or later human edits may
require recovery. `./bootstrap.sh recover` is inspection; applying recovery needs
reviewed scope. Manual `nix profile rollback` affects profile generations, not the
lockfile; use `$nix-manager` and restore only the reviewed matching lock state.
No automatic backup deletion or Git publication is part of cleanup.

## Evidence limits

At initial implementation on 2026-10-31, native macOS enable/probe, deliberate
unload detection, normal-install repair, and daytime rejection passed. A disposable
OrbStack Ubuntu VM exercised the production systemd enable/probe, stop detection,
repair, and disable lifecycle; that VM was deleted afterward. Ubuntu/Fedora
containers exercised focused tests and setup acceptance, not native scheduler
delivery. Actual overnight update, real sleep/wake, and a seven-day production
quarantine/application cycle were not yet observed. Recheck live state and report
new evidence rather than treating this historical record as current health.
