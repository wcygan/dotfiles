---
name: authoring-hermes-skills
description: >
  Author Hermes Agent skills (SKILL.md files) for ~/.hermes/skills/ or
  dotfiles-tracked external skill dirs. Covers frontmatter, conditional
  activation via toolset fallbacks, progressive disclosure with references/
  and templates/, and the hermes skills CLI. Use when creating, editing, or
  reviewing Hermes skills, or setting up shared skill directories.
  Keywords: hermes skill, hermes agent, nous research, SKILL.md, ~/.hermes/skills,
  skill_manage, external_dirs, fallback_for_toolsets, hermes skills CLI
---

# Authoring Hermes Skills

Hermes Agent (by Nous Research, `hermes-agent.nousresearch.com`) has its own
skill system. It shares the "SKILL.md + frontmatter + progressive disclosure"
philosophy with Claude Code skills, but the **frontmatter fields, discovery
mechanics, and CLI tooling are different**. Do not copy Claude Code skill
patterns blindly.

Last verified against docs: 2026-04-05. If fields below stop matching the
live docs, re-fetch `https://hermes-agent.nousresearch.com/docs/user-guide/features/skills/`
via the `hermes-docs` skill before trusting this file.

## Hermes vs Claude Code skills — quick diff

| Concern | Claude Code | Hermes |
|---|---|---|
| File | `SKILL.md` | `SKILL.md` |
| Required frontmatter | `name`, `description` | `name`, `description` |
| Auto-invocation control | `disable-model-invocation`, `user-invocable` | N/A — agent reasons from `skills_list` |
| Tool restriction | `allowed-tools` | N/A (toolsets are global) |
| Execution context | `context: fork`, `agent:` | N/A (Hermes has subagents via `/background`) |
| Conditional visibility | — | `fallback_for_toolsets`, `requires_toolsets`, `platforms` |
| Env vars | — | `required_environment_variables` (interactive prompt) |
| Filesystem category | Flat (`skills/<name>/`) | Category-nested (`skills/<category>/<name>/`) |
| Progressive disclosure | SKILL.md body + references | Level 0 `skills_list`, Level 1 `skill_view`, Level 2 `skill_view(name, path)` |
| Hub/distribution | — | `hermes skills browse/install` from skills.sh, GitHub taps, well-known endpoints |

**Rule of thumb**: when in doubt, start with a minimal SKILL.md containing
only `name` + `description` + body. Add optional fields only when you have a
concrete reason.

## Where Hermes skills live

```
~/.hermes/skills/
├── <category>/
│   └── <skill-name>/
│       ├── SKILL.md           # required
│       ├── references/        # optional — loaded on demand (Level 2)
│       ├── templates/         # optional
│       ├── scripts/           # optional
│       └── assets/            # optional
├── .hub/                      # hub state (don't touch)
└── .bundled_manifest
```

The **category directory is load-bearing** — it's a real filesystem path, not
just metadata. Categories visible on a typical install include `devops`,
`research`, `software-development`, `data-science`, `creative`, `media`,
`productivity`, `mcp`, etc. Use an existing category when possible.

### External (read-only) skill directories

Hermes can scan additional directories via `~/.hermes/config.yaml`:

```yaml
skills:
  external_dirs:
    - ~/Development/dotfiles/config/hermes/skills
    - /home/shared/team-skills
    - ${SKILLS_REPO}/skills
```

Paths support `~` and `${VAR}` expansion. External directories are **read-only**
from the agent's perspective — `skill_manage` always writes to
`~/.hermes/skills/`. Local skills shadow external ones with identical names.

**This repo uses this pattern** — curated, git-tracked Hermes skills live
under `config/hermes/skills/<category>/<name>/SKILL.md` and are registered as
an external dir by `scripts/setup-hermes-skills.sh`. See
[references/dotfiles-integration.md](references/dotfiles-integration.md).

## Minimum viable SKILL.md

```yaml
---
name: my-skill
description: One sentence on what it does and when to use it.
---

# My Skill

## When to Use
...

## Procedure
...
```

That's it. Everything else is optional.

## Adding structure progressively

Add fields only when you need them. Work down this list in order:

1. **`version: 1.0.0`** — once the skill is stable enough to track changes.
2. **`metadata.hermes.category`** + **`metadata.hermes.tags`** — for hub discovery.
3. **`platforms: [macos, linux]`** — only if the skill genuinely breaks on
   other OSes (uses `osascript`, `apt`, etc.). Don't over-restrict.
4. **`fallback_for_toolsets: [web]`** — makes the skill appear in `skills_list`
   *only when* the listed toolset is unavailable. Canonical example: the
   built-in DuckDuckGo skill is a fallback for the `web` toolset.
5. **`requires_toolsets: [kubernetes]`** — opposite: only show when the
   toolset is available.
6. **`required_environment_variables`** — Hermes prompts the user interactively
   on first use. Use this instead of hard failures in procedure steps.

Full field reference: [references/frontmatter.md](references/frontmatter.md).
Conditional activation deep dive: [references/conditional-activation.md](references/conditional-activation.md).

## Body structure conventions

Hermes skill bodies typically use these headings. Keep them — consistency helps
the agent locate the right skill via `skills_list` summaries:

```markdown
## When to Use
(one short paragraph of trigger scenarios)

## Procedure
(numbered steps; link to references/*.md for anything long)

## Pitfalls
(things that have gone wrong before)

## Verification
(how to know the skill worked)
```

Full conventions and examples: [references/body-structure.md](references/body-structure.md).

## Progressive disclosure via references/

Hermes loads skills in three levels:

- **Level 0** — `skills_list()` returns name + description + category (~3k tokens total).
- **Level 1** — `skill_view(name)` returns SKILL.md body.
- **Level 2** — `skill_view(name, path)` returns a specific file like `references/foo.md`.

**Implication**: put long reference material in `references/*.md` and link to
it from SKILL.md with its relative path. Keep each reference file
self-contained — the agent loads them individually.

Rules of thumb, ported from Claude Code skill conventions and confirmed by
Hermes docs:

- SKILL.md body under ~500 lines.
- References one level deep (SKILL.md → `references/foo.md`, never a chain).
- Reference files >100 lines get a table of contents at the top.
- Organize references by domain, not chronology.

## Testing a new skill

```bash
# 1. Confirm Hermes sees it
hermes skills list | rg my-skill

# 2. Check the parsed metadata
hermes skills inspect my-skill

# 3. Try it in a session
hermes
> /my-skill
```

If `list` shows it but `inspect` errors, the YAML frontmatter is malformed.
Full CLI reference: [references/cli-commands.md](references/cli-commands.md).

## Templates

Three starter templates live under `templates/`:

- [`templates/minimal/SKILL.md`](templates/minimal/SKILL.md) — bare required fields.
- [`templates/toolset-fallback/SKILL.md`](templates/toolset-fallback/SKILL.md)
  — skill that activates only when a toolset is missing.
- [`templates/env-dependent/SKILL.md`](templates/env-dependent/SKILL.md) —
  skill requiring API keys via `required_environment_variables`.

Copy whichever matches your use case into
`config/hermes/skills/<category>/<name>/` and edit in place.

## Common mistakes

- **Copying Claude Code frontmatter fields** (`disable-model-invocation`,
  `context: fork`, `allowed-tools`) — these don't exist in Hermes and will be
  silently ignored or fail validation.
- **Omitting the category directory** — a skill at
  `~/.hermes/skills/my-skill/SKILL.md` (no category) is nonstandard; pick a
  category even if it feels forced.
- **Writing prose instead of pointing to references** — Level 1 loads the
  whole SKILL.md body. Keep it a router, not an encyclopedia.
- **Hardcoding absolute paths** — external_dirs skills run on whichever
  machine syncs the dotfiles repo. Use `$HOME`, `~`, or relative paths.
- **Over-using `platforms`** — only restrict when the skill genuinely can't
  run elsewhere. `platforms: [macos]` on a skill that just `curl`s an API is
  a mistake.
- **Putting dotfiles-tracked skills in `~/.hermes/skills/` directly** — the
  Hermes agent can mutate them via `skill_manage`. Use the `external_dirs`
  pattern so git stays the source of truth.

## Related

- Live Hermes docs router: the `hermes-docs` skill in this repo.
- Skills hub, taps, publishing, security scanning: [references/hub-and-distribution.md](references/hub-and-distribution.md).
- Dotfiles integration (external_dirs, setup script): [references/dotfiles-integration.md](references/dotfiles-integration.md).
