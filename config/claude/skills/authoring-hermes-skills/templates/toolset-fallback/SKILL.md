---
name: TODO-skill-name
description: >
  TODO one-sentence summary. This skill acts as a fallback when the TODO
  toolset is unavailable, providing a degraded-but-functional alternative.
version: 0.1.0
metadata:
  hermes:
    category: TODO-category
    tags: [TODO, fallback, TODO-domain]
    fallback_for_toolsets: [TODO-toolset-name]
---

# TODO Skill Title (Fallback)

## When to Use

Automatically surfaces when the `TODO-toolset-name` toolset is not available
in the current Hermes session. Provides a reduced-capability path to
accomplish TODO: primary goal.

## Procedure

1. TODO: confirm the preferred toolset is genuinely unavailable (check
   `/tools` or infer from prior failures).
2. TODO: fall back to TODO alternative approach.
3. TODO: flag any differences from the preferred path so the user knows what
   they're missing.

## Pitfalls

- Don't use this skill when the preferred toolset IS available — Hermes will
  hide it automatically, but if you invoke it explicitly you'll get inferior
  results.
- TODO: specific fallback-mode limitations.

## Verification

- TODO: how to confirm the fallback achieved the user's goal.
