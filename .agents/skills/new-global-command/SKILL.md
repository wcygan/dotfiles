---
name: new-global-command
description: "Convert a reusable command idea into a global Codex skill in config/codex/skills. Legacy name for users who ask to create global slash commands; create skills instead."
---

# New Global Command Compatibility Skill

## Goal

Turn a reusable workflow idea into a global Codex skill under `config/codex/skills/`.

Success means no `config/codex/commands/` file is created, the new workflow is represented as a valid skill, and the user has a `$skill-name` invocation example.

Stop when the global skill is created or the user has a draft ready for review.

## Context

Codex uses skills as the durable authoring format for reusable workflows. Treat requests for a "global command" or "slash command" as requests for a global skill unless the user explicitly asks for built-in slash-command documentation.

Prefer `$global-skill-creator` for new work. Use this skill as a compatibility path for the old command name and for migrating command-style prompt templates.

## Requirements To Gather

Ask only for missing information that cannot be inferred:

1. Skill name: lowercase, hyphen-case, and specific.
2. Purpose: the recurring task the skill performs.
3. Scope: confirm it is project-agnostic enough for `config/codex/skills/`.
4. Inputs: what the user will provide in the prompt after `$skill-name`.
5. Resources: whether it needs references, scripts, templates, or assets.

## Workflow

1. Read `config/codex/skills/.system/skill-creator/SKILL.md`.
2. If useful, read `.codex/skills/global-skill-creator/SKILL.md` for this repo's global-skill conventions.
3. Validate that the proposed workflow is broadly useful across projects.
4. If it is project-specific, recommend `.codex/skills/<skill-name>/` instead.
5. Create `config/codex/skills/<skill-name>/SKILL.md` with required `name` and `description` frontmatter.
6. Keep the `description` concise and trigger-rich.
7. Move long checklists, templates, or examples into `references/`.
8. Add scripts only for deterministic work that is safer to run than to retype.
9. Validate the skill:

```bash
uv run --with pyyaml config/codex/skills/.system/skill-creator/scripts/quick_validate.py config/codex/skills/<skill-name>
```

10. Run `make test-pre` if the change affects shared skill infrastructure, link behavior, install scripts, or repo tests.

## Good Global Skill Candidates

- Code explanation and teaching workflows.
- Generic code review methods.
- Security review checklists.
- Performance analysis workflows.
- Refactoring advisors.
- Test strategy design.
- Debugging methodology.
- Documentation generation and review.
- Git workflow helpers.

## Use Project-Local Skills Instead For

- Deployment flows tied to one repo.
- Build commands tied to one stack.
- Database operations tied to a schema.
- API tests tied to specific endpoints.
- Environment setup tied to one project.

## Output

When complete, report:

- Skill path.
- Invocation example using `$skill-name`.
- Validation command and result.
- Any reason the skill was scoped globally or locally.

Reusable prompt templates from the old command workflow are available in `references/templates.md`.
