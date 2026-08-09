---
name: global-skill-creator
description: "Route reusable Codex skill requests from dotfiles to the authoritative agent-skills repository. Use when a request mentions a global skill, reusable workflow, or legacy global command."
---

# Global Skill Creator Compatibility Skill

## Outcome

Keep this repository free of global-skill source packaging and vendoring.
Reusable skills belong in the dedicated `agent-skills` repository;
dotfiles-specific operating skills belong in `.agents/skills/`; the global
catalog is consumed here only through `$agent-skills-integration`.

## Workflow

1. Classify the workflow. Use `.agents/skills/<name>/` only when it is specific
   to this dotfiles repository.
2. For a portable workflow, direct the work to the authoritative
   `agent-skills` repository. Do not recreate its source catalog or add vendor
   metadata in this repository.
3. Follow the selected repository's current skill-authoring and validation
   instructions. Use `$agent-skills-integration` for the separate dotfiles pin,
   installation, and verification workflow. Installed Codex and Pi state is
   machine-local.
4. Validate a dotfiles-local skill with the narrowest relevant repository
   checks, normally `make test-pre`.

## Migration Note

The historical dotfiles-owned source catalog and linked installer were retired.
This compatibility skill preserves the old name while routing reusable source
to `agent-skills` and catalog consumption to the pinned integration.
