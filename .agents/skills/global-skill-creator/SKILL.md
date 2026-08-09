---
name: global-skill-creator
description: "Create global Codex skills distributed through this dotfiles repository. Use when adding reusable Codex workflows under config/codex/skills or adapting a project-local skill for global use."
---

# Global Skill Creator

## Goal

Create a portable global Codex skill under `config/codex/skills/`.

Success means the skill has valid Codex frontmatter, useful trigger language, focused instructions, optional resources only when they add value, and a passing local validator run.

Stop when the skill is created or updated, validation passes, and the user has a concrete invocation example.

## Workflow

1. Read the current Codex skill-authoring instructions exposed in the session, then inspect an active tracked skill and `tests/test-codex-skills.sh`. Do not depend on the system-managed, gitignored `config/codex/skills/.system` directory.
2. Ask for the skill's reusable purpose, trigger scenarios, and whether it needs references, scripts, templates, or assets.
3. Create `config/codex/skills/<skill-name>/` with a matching `SKILL.md` frontmatter `name`.
4. Use concise `description` text that front-loads the key task and trigger words.
5. Keep detailed docs in `references/`, deterministic helpers in `scripts/`, and output resources in `assets/`.
6. Add `agents/openai.yaml` when UI metadata or explicit-invocation policy is useful. Keep it to the supported `interface` and `policy` fields used by active skills.
7. Add the skill to the expected inventory in `tests/test-codex-skills.sh` and run:

```bash
./tests/test-codex-skills.sh
```

8. Run `make test-pre` for every global skill change.

## Dotfiles Context

This repository tracks global Codex skills in `config/codex/skills`. `scripts/link-config.sh` links that directory into `${CODEX_HOME:-~/.codex}/skills`.

Keep global skills project-agnostic. Use `.codex/skills` for workflows that only make sense inside this dotfiles repository.
