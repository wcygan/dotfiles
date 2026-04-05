# Dotfiles Integration

How Hermes skills are kept in git in this dotfiles repo and loaded by Hermes
without copying or symlinking into `~/.hermes/skills/`.

## Layout

```
dotfiles/
├── config/
│   └── hermes/
│       └── skills/
│           └── <category>/
│               └── <skill-name>/
│                   ├── SKILL.md
│                   └── references/  (optional)
└── scripts/
    └── setup-hermes-skills.sh
```

## How it's wired

`scripts/setup-hermes-skills.sh` (invoked by `install.sh`) idempotently adds
the dotfiles skills directory to `~/.hermes/config.yaml` under
`skills.external_dirs`:

```yaml
skills:
  external_dirs:
    - ~/Development/dotfiles/config/hermes/skills
```

Hermes treats external directories as **read-only**, which is exactly what we
want:

- Git stays the source of truth.
- `hermes skills` commands and the agent's `skill_manage` tool can't mutate
  these files.
- No copy step, no symlink — the path is read directly on every
  `skills_list` call.

## Why not symlink into `~/.hermes/skills/`?

- Symlink support in `~/.hermes/skills/` isn't documented.
- Mixes git-tracked skills with hub-installed ones and agent-created ones in
  one namespace — confusing ownership.
- `hermes skills update/uninstall` might touch git-tracked files.

## Why not copy via install.sh?

- Creates drift: edits on either side silently diverge.
- Requires re-running installer after every `git pull`.
- Loses the read-only guarantee.

## Adding a new skill

1. `mkdir -p config/hermes/skills/<category>/<name>/`
2. Write `SKILL.md` (see [../templates/](../templates/))
3. Commit.
4. On any machine with the dotfiles cloned and `setup-hermes-skills.sh` run,
   `hermes skills list` will show the new skill immediately — no re-run needed.

## Removing a skill

`git rm -r config/hermes/skills/<category>/<name>/` and commit. Hermes picks
up the removal on next `skills_list`.

## Shadowing

If you want to override a git-tracked skill locally (e.g., experiment without
committing), copy its directory into `~/.hermes/skills/<category>/<name>/` and
edit. Local skills shadow external ones with the same name.

## Multiple machines

The dotfiles repo path is the same on every machine (assuming the user clones
to `~/Development/dotfiles/`). If you clone elsewhere, edit the
`external_dirs` entry in `~/.hermes/config.yaml` or set an env var and use
`${VAR}` expansion in the config.
