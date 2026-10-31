# Configuration and platform support

## Source map

Paths below are relative to the repository root. Recheck them before editing.

| Concern | Owning source |
| --- | --- |
| Commands and Make wrappers | `src/dotfiles_setup/cli.py`, `Makefile` |
| Scheduler fast path using profile Python, before Nix shell startup | `bootstrap.sh` |
| Age, observations, source ownership, candidate checks, deadline, application | `src/dotfiles_setup/nightly.py` |
| Schedule rendering, stable environment, registration, enable/disable/status | `src/dotfiles_setup/nightly_schedule.py` |
| Transient bootstrap probe and read-only scheduler checks | `src/dotfiles_setup/nightly_health.py` |
| Remembered opt-in during normal install | `src/dotfiles_setup/installer.py` |
| Generated destination inventory | `nightly_files` in `src/dotfiles_setup/links.py` |
| Strict acceptance and guarded recovery | `verify.py`, `recovery.py`, mutation/journal modules |
| Focused behavioral checks | `tests/test_nightly.py` |
| User instructions | `README.md`, section on nightly updates |

## Platforms and prerequisites

Both platforms need an installed profile with `~/.nix-profile/bin/python3`, a
checkout inside HOME, Nix/Git/network access for updates, and a healthy exact
checkout profile. Jobs use an explicit PATH and HOME/XDG/CODEX environment rather
than interactive shell startup. CA paths use the stable profile when available.

| macOS | Linux |
| --- | --- |
| Per-user LaunchAgent in the logged-in user's `gui/<uid>` domain | systemd user service and timer |
| `~/Library/LaunchAgents/com.wcygan.dotfiles.nightly.plist` | `${XDG_CONFIG_HOME:-$HOME/.config}/systemd/user/dotfiles-nightly.{service,timer}` |
| Calendar hour 3, minute 0; no KeepAlive/RunAtLoad on permanent job | OnCalendar 03:00, Persistent=false, WakeSystem=false |
| Read-only registration/disabled-state check | Enabled, active timer with next realtime execution required |
| Transient LaunchAgent probe, removed afterward | `systemd-run --user` transient probe, stopped/collected afterward |

Ubuntu/Fedora compatibility requires a reachable systemd user manager. Linux/WSL
without one cannot run this scheduler. Containers do not automatically provide
it. A user timer runs while its user manager exists; running while logged out
requires a separate deliberate linger policy. This installer does not enable
linger. macOS LaunchAgents similarly depend on the user's login session.

## Private state and diagnostics

State lives in `${XDG_STATE_HOME:-$HOME/.local/state}/dotfiles/nightly`:

- `schedule.json`: requested/enabled state, owner checkout, source/lock hashes,
  matching probe token, and updater-owned backup bookkeeping.
- `observations.json`: first local observation of eligible GitHub snapshots.
- `last-health.json`: completed probe acknowledgement bound to token and checkout.
- `last-run.json`: completed run result; early skips may leave it unchanged.
- `last-run.log`: latest attempted update commands and output, replaced per run.
- `scheduler.log` / `scheduler-error.log`: macOS scheduler stdout/stderr.
  Linux diagnostics also use `journalctl --user -u dotfiles-nightly.service`.

Setup lock/journals use the shared dotfiles cache/state directories, outside this
nightly subdirectory. Never delete state to bypass ownership or recovery guards.

## Reconfiguration map

These are source changes, not supported user parameters:

| Requested change | Change together |
| --- | --- |
| Hour or nighttime window | Both platform renderings in `schedule_contents`; hour/end/deadline guards in `run_nightly` and `Commands`; Linux timeout if needed; status, health text, tests, README and this skill |
| Quarantine duration | `AGE_SECONDS`, status/enable text, age-boundary tests, README and this skill; preserve existing first-seen records unless an explicit migration requires otherwise |
| Scheduler environment | `schedule_environment`, probe parity, path/quoting tests; keep credentials machine-local |
| Generated paths or names | `links.nightly_files`, renderer, health/probe registration, recovery allowlist, migration handling and tests |
| New input type or nested input graph | Observation/ancestry/lock transformation in `nightly.py`; current support is direct GitHub branch inputs without nested dependencies |
| Different checkout | Disable from the old owner first, install/verify the new HOME-contained checkout, then enable there; do not copy old ownership hashes |

Retain observation history and guarded backups through normal reconfiguration.
Do not lower age or bypass the time guard merely to make a test install something.
For urgent intentional updates, use `$nix-update` and `make update`; this bypasses
the nightly delay by design and needs explicit update scope.

After implementation changes, run focused pytest, `make test-pre`, and the
applicable dotfiles-operations gates. Bootstrap/platform changes need shell,
syntax, all-system evaluation, Docker, and native macOS evidence. Real Linux
scheduler acceptance needs a systemd user session; Docker unit tests alone do
not establish it. Record breaking migrations in the operations migration log.
