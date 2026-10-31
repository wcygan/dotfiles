---
name: nightly-nix-updates
description: Configure, verify, repair, and reconfigure this dotfiles repository's local nightly Nix updater on macOS and systemd Linux. Use for its 3 AM schedule, seven-day observation quarantine, scheduler health, missed runs, update logs, and rollback.
---

# Nightly Nix updates

Keep the optional local updater working through the repository's supported
installation and verification paths. Use `$dotfiles-operations` alongside this
skill; use `$cross-platform-guardian` for platform-sensitive implementation
changes, `$nix-manager` for profile mechanics, and `$nix-update` for an intentional
input update. This project-local skill does not belong in the global catalog.

## Operating contract

- Explicit first opt-in: `make nightly-enable`. Normal `./bootstrap.sh install`
  remembers that choice and reconciles the scheduler, including incomplete setup.
- Schedule: 03:00 local; work is restricted to 03:00–04:00. Missed nights are
  acceptable. No wake request or daytime catch-up is intended. A late scheduler
  delivery is rejected by the runtime window guard.
- Quarantine: seven complete days since this machine first observed an immutable
  Nix input snapshot. It is not individual package release age or commit age,
  does not guarantee protection from zero-days, and can delay security fixes.
- Candidate checks precede profile application. Successful updates leave a local
  `flake.lock` change for review. No automatic pull, commit, push, or global
  skill update occurs.
- One checkout owns the per-user schedule and shared setup mutation lock. Human
  edits can pause updates; updater-owned lock changes/backups can be retried.
  Enabling records the current source/lock baseline, so review local edits first.
- Installation probes the actual scheduler through `bootstrap.sh nightly-probe`.
  Strict `verify` is read-only and checks configuration, registration, and the
  recorded matching probe. Neither proves a future overnight update succeeded.

## Choose a journey

Read the [feature and journey index](references/journeys.md) for exact commands,
prerequisites, expected effects, evidence capture, and cleanup:

1. Inspect an existing installation without changing it.
2. Enable or repair a remembered installation and prove scheduler reachability.
3. Verify daytime rejection and diagnose a missed night.
4. Change schedule, quarantine, environment, or checkout ownership.
5. Verify candidate/application behavior and handle a failed update.

Start with `git status --short`, `make nightly-status`, and
`./bootstrap.sh recover`. Confirm the owning checkout and intended enabled state
before a mutation. Do not run a second scheduler against the same HOME/profile
for testing. Use a disposable OS instance for destructive lifecycle checks.

## Configuration ownership

Read [configuration and platform support](references/configuration.md) before
changing behavior. The renderer and runtime are the source of truth; generated
plist/unit files and private JSON are outputs, not configuration interfaces.
There is currently no supported CLI flag for changing the hour or quarantine.

After source changes, run the relevant gates, then use the supported enable or
normal-install operation to reconcile the scheduler and refresh its baseline.
Do not silently bless unrelated edits by refreshing ownership metadata.

Report observed scheduler health separately from actual update outcomes. Name
the platform exercised, real versus simulated boundaries, last-run evidence,
cleanup, untested journeys, recovery state, and commit/push status. Never infer
macOS acceptance from Docker or declare overnight success from a probe alone.
