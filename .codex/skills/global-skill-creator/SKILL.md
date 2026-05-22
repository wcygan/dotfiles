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

1. Read `config/codex/skills/.system/skill-creator/SKILL.md` for the current Codex skill-authoring rules.
2. Ask for the skill's reusable purpose, trigger scenarios, and whether it needs references, scripts, templates, or assets.
3. Create `config/codex/skills/<skill-name>/` with a matching `SKILL.md` frontmatter `name`.
4. Use concise `description` text that front-loads the key task and trigger words.
5. Keep detailed docs in `references/`, deterministic helpers in `scripts/`, and output resources in `assets/`.
6. Generate `agents/openai.yaml` when UI metadata is useful:

```bash
uv run --with pyyaml config/codex/skills/.system/skill-creator/scripts/generate_openai_yaml.py config/codex/skills/<skill-name>
```

7. Validate the skill:

```bash
uv run --with pyyaml config/codex/skills/.system/skill-creator/scripts/quick_validate.py config/codex/skills/<skill-name>
```

8. Run `make test-pre` when the change affects shared skill infrastructure, install/link behavior, or repo tests.

## Dotfiles Context

This repository tracks global Codex skills in `config/codex/skills`. `scripts/link-config.sh` links that directory into `${CODEX_HOME:-~/.codex}/skills`.

Keep global skills project-agnostic. Use `.codex/skills` for workflows that only make sense inside this dotfiles repository.
