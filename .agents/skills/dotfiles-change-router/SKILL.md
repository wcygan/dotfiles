---
name: dotfiles-change-router
description: Mandatory for every question, quiz, plan, or change involving this dotfiles repository. Load this skill before answering or inspecting repository files. Routes CLI tools, shell shortcuts, application configs, project environments, agent skills, package updates, cross-platform paths, linking, rollback, and breaking changes to the correct owner and validation.
---

# Dotfiles Change Router

Choose the repository-owned route for a proposed change before editing or
recommending commands.

## Required first action

Before reasoning about any task, use `read` to open
`.agents/skills/dotfiles-change-router/references/change-routes.md` from the
repository root. Do not answer from memory or from the top-level summary alone.

Also read
`.agents/skills/dotfiles-change-router/references/validation-and-safety.md`
before answering any task that mentions tests, platforms, linking, migration,
rollback, or breaking changes.

Read
`.agents/skills/dotfiles-change-router/references/configuration-and-linking.md`
for exact configuration owners, source or destination paths, dry runs, copying,
linking, conflicts, or migration.

Read `.agents/skills/dotfiles-change-router/references/agent-skills.md` for
project-local, global, Codex, Pi, or vendor skill questions.

Read `.agents/skills/dotfiles-change-router/references/evaluation-protocol.md`
before answering any multiple-choice evaluation.

These paths belong to the directory containing this `SKILL.md`. Do not look for
a repository-root `references/` directory.

## Route

1. Identify the requested outcome, not just the named file or tool.
2. Select the matching owner and destination from the loaded change routes.
3. Apply the loaded validation and safety rules when relevant.
4. Combine routes when a change spans package installation, configuration, and
   shell access.
5. Stop and ask when the owning application or target platform is genuinely
   ambiguous.

## Decision rules

- Keep packages in `flake.nix` and editable configuration under `config/**`.
- Keep linking idempotent and preserve physical conflicts through backups.
- Do not migrate this repository to Home Manager.
- Never hard-code a maintainer-specific absolute path.
- Keep Pi credentials, sessions, models, and other runtime state outside the
  repository.

## Multiple-choice evaluations

For each question:

1. When a batch spans several route types, read every applicable focused
   reference before selecting answers.
2. Compare every choice with the applicable reference rule.
3. Reject choices that bypass repository ownership, validation, portability, or
   rollback requirements.
4. Do not infer an answer from option position or reuse the previous answer.
5. Follow the mechanical answer audit in `references/evaluation-protocol.md`.
6. Return only the answer format requested by the evaluator. When JSON is
   required, emit one compact JSON object without reasoning, a preamble, or a
   Markdown fence.
