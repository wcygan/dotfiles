# Migration History

Read this reference before changing compatibility guarantees, restoring retired
behavior, or replacing a setup boundary. Add an entry when a breaking change is
intentional, alongside focused migration tests.

## 2026-10-31 — Migrate CLI tools from Homebrew in verified groups

The Nix profile now owns the two requested CLI groups. The first group uses
the stable input. Hyperfine, Typst, Graphviz, OCRmyPDF, FFmpeg, and yt-dlp use
the existing newer input where supported; Intel macOS retains stable packages.
The yt-dlp dependency closure includes Deno, without restoring the retired
global Deno configuration.

`scripts/check-cli-migration.py` exercises real behavior using the installed
profile, a PATH without Homebrew, and disposable fixtures. Run `--group first`
and `--group next` before and after removing matching Homebrew formulae.
The first group requires Docker. It starts only a temporary localhost Temporal
server and does not contact a Kubernetes cluster. The second group verifies
local rendering, OCR, media encoding, metadata, and a localhost download; it
does not establish compatibility with every external video site.

On this Mac, Graphviz intentionally moves from Homebrew 16.1.0 to Nix 15.1.1
after rendering checks, as explicitly requested. Retain Homebrew FFmpeg while
FreeRDP and unpaper require it. Disable Homebrew autoremove during migration
so unrelated dependencies and state remain intact.

A Nix profile rollback restores the previous package generation but does not
reinstall removed Homebrew formulae. To restore Homebrew ownership, reinstall
the affected formulae explicitly and verify PATH precedence.

## 2026-10-31 — Use upstream security packages and retire Deno

The main package set now follows `nixos-26.05`, which retains Intel macOS
support and includes patched certificates, Go and Node. A second locked
`nixpkgs-unstable` input supplies uv and Zed on the other three systems. Intel macOS uses stable Zed and retains upstream uv 0.13.4
because unstable no longer supports that platform. Bun is temporarily pinned
to its patched 1.4.4 release on all systems; nixpkgs still supplies older
versions. Live checks showed that Bun 1.4.2 accepted an affected chain even
with the newer trust store.

The remaining Comodo root filter and curl CA settings protect clients using
the profile trust store. The previous emSign root exclusion is no longer
needed because the upstream bundle has removed that root.

The profile provides `zed` alongside nixpkgs' `zeditor` command. On macOS,
the application is available under `~/.nix-profile/Applications/Zed.app`.
Existing Homebrew installations are retained; check `command -v zed` after
installation to confirm command precedence.

Deno is no longer a top-level profile tool or configured by the repository. Its managed-link inventory entry,
Fish wrappers, abbreviations and completions have been removed. Existing
machine-local Deno installations and the old `~/.config/deno` link are not
deleted automatically.

Managed Fish/Bash/zsh configuration and the development shell set default
`SSL_CERT_FILE`, `SSL_CERT_DIR` and `NIX_SSL_CERT_FILE` values for clients
such as Python and wget. Open a new shell after installation. Explicit CA
environment overrides remain supported.

Apply with `make profile`, then run `make verify` and
`python3 scripts/check-emudhra.py` from a new shell. The live check requires
certificate rejection for both incident hosts and successful HTTPS to
example.com. DNS failures and timeouts fail the check. Apple tools, other
applications and previously built binaries need their own verification.
`nix profile rollback` restores the previous packages and certificate policy.

## 2026-10-15 — Reconcile removed files inside pinned skills

`agent-skills --prune` now archives installed provider-owned skill trees containing
files absent from the target pin before reinstalling those skills through GitHub
CLI. This addresses overlay installs retaining deleted demos. Archives remain
outside discovery roots and preserve the entire previous tree. Normal installation
and read-only verification still reject obsolete files; unrelated shared-user
skills remain untouched unless the existing explicit reset mode is requested.

## 2026-10-14 — Reconcile catalog retirements and support explicit reset

The provider archived its 116-skill catalog and retained `uv-python`, `just`,
and `design-loop`. Updating the pin is insufficient because GitHub CLI does not
remove retired local skills. `agent-skills --check` now rejects stale copies
owned by the pinned provider. Authorized `agent-skills --prune` archives those
copies before completing verification; skills from other sources remain intact.

An explicitly requested `agent-skills --reset --yes` archives every shared user
skill outside the pinned catalog, including foreign and untracked local skills.
Both operations use the existing user mutation lock and journal, validate each
accepted directory tree and move it to a dated XDG-state archive outside skill
discovery. Failed acceptance restores prior directories when safe; interrupted
operations retain recovery state and archive paths. Global built-in/plugin skills
and project-local skills are outside this shared-directory reset.

## 2026-08-29 — Require physical destination parents and no-replace renames

Managed mutations now validate every destination parent through a descriptor
walk. A symlinked ancestor of a managed destination, such as a synced
`~/.config`, fails with an unsafe-parent error. Replace the symlink with a
real directory before you install.

Atomic replacement now uses no-replace renames. Linux needs `renameat2` with
`RENAME_NOREPLACE` filesystem support. macOS needs `renameatx_np`. A
filesystem without support fails with `ENOTSUP`. Move the managed
destinations to a filesystem with no-replace support.

Created directories now install with mode `0755` by default; a caller may
declare a stricter mode. The transactional rewrite had created
`~/.local/bin` and `~/.local/lib` with mode `0700`. Replace those
directories if the restrictive mode matters to you.

## 2026-08-29 — Reject inactive checkout profile elements

Profile setup now upgrades only an active element from the current checkout.
If the matching element is inactive, remove it with `nix profile remove NAME`.
Then run `./bootstrap.sh profile` to add a new active element. This prevents an
inactive profile record from hiding the active installation state.

## 2026-08-29 — Retain verified legacy skill quarantines

Legacy skill cleanup now moves each accepted tree to a hidden quarantine in
the same directory. It does not delete the accepted contents. Inspect the
reported paths after cleanup. Move retained trees to the platform trash only
after the shared catalog passes `./bootstrap.sh agent-skills --check`.

## 2026-08-10 — Move global instructions to shared agent configuration

`config/agents/AGENTS.md` is now the authoritative global instruction source.
The managed inventory links it to both `~/.agents/AGENTS.md` and
`${CODEX_HOME:-~/.codex}/AGENTS.md`, deduplicating the destination when
`CODEX_HOME` is `~/.agents`. `config/codex/AGENTS.md` remains a compatibility
link, while `config/codex/config.toml` retains its machine-local template
behavior. Existing physical destinations continue to use the standard backup
before replacement.

## 2026-08-08 — Retire the dotfiles-owned global skill catalog

The repository stopped linking or validating its former Codex skill catalog,
custom agents, and Claude configuration. Dotfiles-specific operating skills
remain under `.agents/skills/`; reusable source moved to the dedicated
`agent-skills` repository.

## 2026-08-09 — Consume a pinned external agent-skill catalog

The explicit `./bootstrap.sh agent-skills` command consumes
`agent-skills.lock.toml`, uses `gh skill install` for Codex user scope, refuses
conflicting same-name skills, and verifies source plus pin. Installed copies and
GitHub CLI tracking state are machine-local. The command remains outside the
default install, and skills removed upstream require separate review because
GitHub CLI does not prune them.

## 2026-08-09 — Move the shared catalog to the Agent Skills user directory

GitHub CLI's Codex host profile still maps user installs to `~/.codex/skills`,
but Codex now documents `~/.agents/skills` as the shared user discovery root.
The consumer lock moved to schema version 2 with a portable relative directory,
and the installer now supplies that directory with `gh skill install --dir` and
verifies it with `gh skill list --dir`. A guarded, explicit legacy cleanup is
available only after the shared catalog verifies. It quarantines exact matching
legacy copies and does not prune foreign or stale skills.

## 2026-08-09 — Replace setup orchestration with Python

`bootstrap.sh` became the supported setup entry point. It obtains Nix only when
explicitly authorized on Linux/WSL, enters `nix develop`, and runs `uv run
--locked python -m dotfiles_setup`. The default install leaves Bash and zsh
startup files unchanged; shell handoff is explicit.

## 2026-08-09 — Separate advisory and strict verification

`doctor` is advisory and exits successfully after reporting host or
not-yet-installed warnings. `verify` is strict, read-only post-installation
acceptance, and `install` runs it last. Ambient development-shell health checks
use `doctor`.

## 2026-08-09 — Add the transactional setup boundary

Mutating setup commands are serialized by a fail-fast per-user lock and write a
content-free operation manifest under XDG state. Link, npm, Codex-template, and
shell-file changes are journaled and atomic. Interrupted operations block later
mutations until recovery is inspected; applying recovery requires `--apply
--yes`. External profile and agent-skill state is inspected and acknowledged,
not automatically reversed.

## 2026-08-09 — Make repository targets canonical CI acceptance

Linux CI invokes repository Make targets for locked quality, syntax,
four-system evaluation, and the Docker runtime matrix. Documentation builds on
pull requests and deploys only from `main`. Native Apple Silicon runs weekly or
manually; Intel macOS runs manually. Workflows remain bounded, least-privilege,
SHA-pinned, report-retaining, and cleanliness-checking.
