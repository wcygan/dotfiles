---
name: autoresearch
description: "Deprecated Codex compatibility name for metric-driven optimization. Use only when an older prompt explicitly invokes $autoresearch; explain the rename, then apply $hill-climbing-loop with the original goal and constraints. Do not implement a separate autoresearch loop."
---

# Autoresearch

Deprecated compatibility entry. Hill Climbing Loop is the maintained Codex workflow for metric-driven keep-or-discard experiments.

When invoked:

1. Tell the user that autoresearch remains available as a compatibility name and that Hill Climbing Loop is the preferred name.
2. Read ../loop-protocol/SKILL.md and ../hill-climbing-loop/SKILL.md completely.
3. Apply Hill Climbing Loop to the user's original request without changing its scope or permissions.
4. Use the Hill Climbing defaults when the older prompt omitted a safe field.

This shim performs no discovery, edits, commands, commits, rollback, or looping by itself. It must not reintroduce the former automatic-commit and broad-revert behavior.

The separate Claude Code autoresearch skill is retained unchanged because it has harness-specific syntax and behavior.
