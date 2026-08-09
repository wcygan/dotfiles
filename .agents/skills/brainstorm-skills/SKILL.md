---
name: brainstorm-skills
description: "Brainstorm useful Codex skills from real project context. Use when identifying recurring workflows, drafting dotfiles-local skills, or routing portable skills to agent-skills."
---

# Brainstorm Skills

## Goal

Identify useful Codex skills for the current repository and turn selected ideas into high-quality `SKILL.md` drafts.

Success means the suggested skills solve recurring work, do not duplicate existing skills, have clear trigger descriptions, and include the right repository placement.

Stop when the user has a short ranked list of skill ideas or, if requested, validated skill files.

## Workflow

1. Read the nearest `AGENTS.md` files for project rules, commands, and conventions.
2. Scan top-level project files such as `flake.nix`, `package.json`, `Cargo.toml`, `pyproject.toml`, `Makefile`, `justfile`, `Dockerfile`, and CI workflows.
3. Review existing project skills in `.agents/skills/*/SKILL.md`.
4. For portable workflows, check the dedicated `agent-skills` repository rather
   than a dotfiles-managed global catalog.
5. Identify recurring pain points from scripts, tests, CI, docs, and config layout.
6. If the user names a focus area, prioritize that area while still checking for duplication.

## Skill Ideas

For each idea, provide:

```markdown
### <Skill Name> (`$skill-name`)
Type: Reference | Task | Background Knowledge
Invocation: User-only | Codex-only | Both
Why: <1-2 sentences on the recurring problem>
What it does: <brief behavior>
Trigger keywords: <phrases that should activate the skill>
Complexity: Simple | Advanced (needs scripts, templates, or references)
Scope: Dotfiles-local `.agents/skills/` | Portable `agent-skills` repository
```

Consider only categories that match the repository:

- Code generation and scaffolding
- Testing and verification
- Code review and project-specific quality checks
- CI, deployment, and release workflows
- Documentation workflows
- Debugging and log analysis
- Refactoring and migrations
- DevOps, infrastructure, and configuration management
- Dependency management
- Repository-specific domain workflows

## Quality Filters

Suggest a skill only when it:

- Solves a real recurring need visible in the repo or named by the user.
- Benefits from Codex reading, editing, generating, or verifying across files.
- Is not already covered by existing dotfiles-local or portable skills.
- Has a specific trigger and bounded outcome.
- Can be validated with a clear command, check, or review criterion when it edits files.

## Present Results

Present the top 5-8 ideas grouped by category. Include a brief rationale for the top 3 based on repo evidence, such as repeated scripts, config families, CI jobs, or existing docs.

Ask which skills the user wants to create before writing files unless the user already requested implementation.

## Draft Selected Skills

For each selected skill:

1. Draft the full `SKILL.md` with `name` and `description` frontmatter.
2. Choose dotfiles-local scope for workflows specific to this repo:
   `.agents/skills/<name>/`.
3. Route portable workflows to the authoritative `agent-skills` repository.
4. Add `references/`, `scripts/`, `assets/`, or `agents/openai.yaml` only when they reduce context load or make the workflow more reliable.
5. For a dotfiles-local skill, verify its frontmatter name against its directory
   and run the narrowest relevant repository test. Validate portable skills in
   their authoritative repository; do not add a catalog, installer, or vendor
   metadata here.

## Authoring Notes

- Front-load trigger keywords in `description`.
- Keep `SKILL.md` focused; move detailed material into `references/`.
- Prefer `$skill-name` examples for explicit invocation.
- Name real commands the agent should run instead of relying on slash-command argument substitution.
- Use `agents/openai.yaml` when a skill should require explicit invocation or expose UI metadata.
