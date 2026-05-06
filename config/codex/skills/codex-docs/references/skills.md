---
canonical_url: https://developers.openai.com/codex/skills
last_verified: 2026-05-06
---

# Skills

Use this reference when creating, updating, installing, or explaining Codex skills.

Key points from the official docs:

- Skills extend Codex with task-specific capabilities through instructions, resources, and optional scripts.
- Skills are the reusable workflow format; plugins are the installable distribution unit for reusable skills and apps.
- Codex supports skills in the CLI, IDE extension, and Codex app.
- Skill loading uses progressive disclosure: name, description, and path are listed first; full `SKILL.md` loads only when Codex chooses the skill.
- A skill directory requires `SKILL.md` with `name` and `description` frontmatter.
- Optional folders include `scripts/`, `references/`, `assets/`, and `agents/openai.yaml`.
- Triggering can be explicit with `$skill-name`, `/skills`, or the skill picker, or implicit when the task matches the description.
- Descriptions should front-load the trigger use case and stay concise because large skill lists may be shortened.
- Codex detects skill edits automatically; restart if a change does not appear.
- Codex supports symlinked skill folders and follows their targets.

Discovery locations:

- Repository skills: `.agents/skills` from current directory up to repo root.
- User skills: `$HOME/.agents/skills`.
- Admin skills: `/etc/codex/skills`.
- System skills: bundled with Codex.

Dotfiles note:

This repo intentionally uses `config/codex/skills` as the source of truth and links it to `~/.codex/skills`. Keep user-authored global Codex skills there.
