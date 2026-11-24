---
name: agent-skills-integration
description: "Maintain the pinned agent-skills provider/consumer integration. Use when changing the external skill repository or pin, installing or verifying the Codex user catalog, troubleshooting skill collisions or recovery, or changing the dotfiles integration contract."
---

# Agent Skills Integration

The provider repository owns the reusable catalog. Dotfiles owns the exact
commit in `agent-skills.lock.toml` and the consumer installer. Project-only
skills live in this repository's `.agents/skills/`. Use
[dotfiles-operations](../dotfiles-operations/SKILL.md) alongside this skill.

## Choose the requested operation

- **Author or review a reusable skill.** Work in the provider checkout.
  Source review and editing can proceed independently of installation.
- **Audit the installed catalog.** Run `./bootstrap.sh agent-skills --check`.
  It reads the installed files and the pinned GitHub tree. Report the commit,
  count, destination, and any mismatch it identifies.
- **Install the recorded pin on a fresh host or restore it.** Read
  `agent-skills.lock.toml` and run the authorized `./bootstrap.sh agent-skills`.
  It installs that exact commit through GitHub CLI and verifies the result.
  A pinned reinstall preserves the lock even when newer releases exist.
- **Install or publish work from a provider checkout.** Inspect
  `git status --short` in both repositories. Read the provider's
  `.agents/skills/really-fast-reinstall/SKILL.md`. Get the go-ahead for
  `just install` there, disclosing any other pending provider work included
  in the commit. It installs the checkout, archives retired provider skills,
  pins dotfiles, and pushes both repositories. Use `just install --wait` when
  the user wants publication confirmed. A default run starts its pushes in
  the background. A requested GitHub-backed audit of the new pin can follow
  once the provider commit reaches the remote.
- **Advance the pin without a provider checkout.** Resolve the requested
  provider revision and review the changes from the existing pin. With
  authorization to update the lock, set only its commit to the reviewed full
  lowercase 40-character SHA. When installation is also requested, run the
  pinned installer and audit the result. Commit and push only when authorized.

## Collisions, stale copies, and recovery

The installer refuses duplicate locations or a same-name skill from another
source. Report the conflicting name, source, and path. For a stale provider
skill or obsolete files in a retained skill, an explicitly authorized
`./bootstrap.sh agent-skills --prune` archives the affected trees outside
skill discovery and reinstalls the pinned catalog. A separately authorized
`--reset --yes` includes unrelated shared-user skills. Use read-only
`./bootstrap.sh recover` to inspect an interruption. Recovery apply needs
its own go-ahead. See the [pinned skills runbook](../dotfiles-operations/references/operations.md#pinned-global-agent-skills)
for reconciliation and legacy-copy cleanup.

## Change the integration

The dotfiles installer uses `gh skill install` with `--dir`, `--all`, and
`--pin` and resolves the lock's shared directory under the current home. Keep
this operation explicit, serialized, and journaled. The provider installer is
a separate writer. Keep the shared audit read-only and lock-free.

The audit checks each expected provider skill's source, custom-directory
scope, exact version, pinned flag, path, files, and source attestation. It also
detects retired provider entries. GitHub CLI refreshes `updatedAt` when it
reinstalls unchanged skills. Compare the normalized provider inventory and
installed contents across reruns. Other providers may have skills in the same
directory.

For integration code changes, inspect `src/dotfiles_setup/agent_skills.py`,
its CLI and recovery paths, and `tests/test_agent_skills.py`. Run the focused
tests and the [applicable validation gates](../dotfiles-operations/references/operations.md#validation-matrix).
Use `make agent-skills-check` for live acceptance. It runs the same read-only
audit as `./bootstrap.sh agent-skills --check`.
