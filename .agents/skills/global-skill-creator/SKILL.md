---
name: global-skill-creator
description: "Route reusable Codex skill requests from dotfiles to the authoritative agent-skills repository. Use when a request mentions a global skill, reusable workflow, or legacy global command."
---

# Global Skill Creator Compatibility Skill

## Outcome

Keep this repository free of global-skill packaging, installation, validation,
and vendoring. Reusable skills belong in the dedicated `agent-skills`
repository; dotfiles-specific operating skills belong in `.agents/skills/`.

## Workflow

1. Classify the workflow. Use `.agents/skills/<name>/` only when it is specific
   to this dotfiles repository.
2. For a portable workflow, direct the work to the authoritative
   `agent-skills` repository. Do not create a global catalog, modify an
   installer, or add vendor metadata in this repository.
3. Follow the selected repository's current skill-authoring and validation
   instructions. Machine-local Codex and Pi state is outside this repository.
4. Validate a dotfiles-local skill with the narrowest relevant repository
   checks, normally `make test-pre`.

## Migration Note

The historical global-skill installer and linked catalog were retired. This
compatibility skill preserves the old name while preventing new work from being
placed in dotfiles.
