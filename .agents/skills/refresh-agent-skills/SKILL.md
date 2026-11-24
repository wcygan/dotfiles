---
name: refresh-agent-skills
description: Check installed agent skills, reinstall the dotfiles pin, or refresh the shared catalog from the provider checkout.
license: MIT
metadata:
  author: wcygan
  version: "0.1.0"
---

# Refresh agent skills

Use [agent-skills-integration](../agent-skills-integration/SKILL.md) and the
[dotfiles operations runbook](../dotfiles-operations/references/operations.md#pinned-global-agent-skills).
Choose the source revision from the request:

- **“Does my installation match the pin?”** Run the read-only
  `./bootstrap.sh agent-skills --check` and report its result.
- **“Reinstall the pinned skills.”** Use the commit already in
  `agent-skills.lock.toml` and the dotfiles installer. This is also the
  fresh-host and recovery path.
- **“Install my local skill changes” or “publish and refresh.”** Follow the
  provider checkout's `really-fast-reinstall` skill. Its `just install`
  commits the provider worktree and dotfiles pin, installs the catalog, and
  pushes both repositories. Inspect pending changes and confirm the request
  authorizes those effects. For a publication request, verify both pushes.
- **“Advance the pin” on a host without the provider checkout.** Follow the
  integration skill's pin-advance procedure for the reviewed provider commit.

If “refresh” could mean restoring the existing pin or publishing local edits,
inspect the pin and checkout first. Clarify the desired revision before a write
when those routes would produce different results. Use the integration skill's
separate approval rules for pruning, full reset, and recovery apply.
