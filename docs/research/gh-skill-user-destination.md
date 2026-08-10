# GitHub CLI skill destination for Codex

**Research date:** 2026-08-09
**Question:** How can `gh skill install` place the reusable catalog in
`~/.agents/skills` instead of `~/.codex/skills`?

**Status:** Implemented on 2026-08-09. The current integration uses the custom
directory for installation and verification. The analysis below preserves the
evidence and migration plan from before implementation.

## Answer

With the installed GitHub CLI (`gh` 2.96.0), pass an explicit custom
directory:

```sh
gh skill install wcygan/agent-skills \
  --all \
  --pin f8aec055dd18e4c3ae18f58db39ebb9012592e4b \
  --force \
  --dir "$HOME/.agents/skills"
```

`--dir` is the supported per-command override. It takes precedence over both
`--agent` and `--scope`; it is not a persisted GitHub CLI default. The
install command has no documented configuration or environment setting for a
custom default destination, and v2.96.0 resolves a Codex user installation
from a static host registry rather than configurable Codex state. See the
[official install manual](https://cli.github.com/manual/gh_skill_install) and
the [v2.96.0 `--dir` resolution](https://github.com/cli/cli/blob/v2.96.0/pkg/cmd/skills/install/install.go#L1026-L1031).

For a non-custom-destination form, GitHub CLI's `universal` host maps its
user scope to `~/.agents/skills`:

```sh
gh skill install wcygan/agent-skills \
  --all \
  --pin f8aec055dd18e4c3ae18f58db39ebb9012592e4b \
  --force \
  --agent universal \
  --scope user
```

That is **not** the Codex host mapping. It makes GitHub CLI track the skills
as installed for `universal`, so existing dotfiles verification that queries
`gh skill list --agent codex --scope user` will not see them.

## Why the previous command used `~/.codex/skills`

At the research date, the installed command was `gh` 2.96.0. In that release's
registry, the Codex host maps project scope to `.agents/skills` but user scope to
`.codex/skills` [direct source](https://github.com/cli/cli/blob/v2.96.0/internal/skills/registry/registry.go#L69-L73).
The registry joins the selected host's `UserDir` to the home directory; the
only special environment override in that code is for Claude Code, not Codex
[direct source](https://github.com/cli/cli/blob/v2.96.0/internal/skills/registry/registry.go#L399-L424).

This explained the live inventory at the research date. `gh skill list --agent
codex --scope user` reported the pinned catalog under `~/.codex/skills`.

## Codex's current documented discovery location

OpenAI's current Codex documentation says that user skills are loaded from
`$HOME/.agents/skills`, and that symlinked skill folders are supported
[official documentation](https://developers.openai.com/codex/skills#where-codex-loads-local-skills).
That differs from the GitHub CLI v2.96.0 registry, so this is an upstream
compatibility drift rather than an installation failure.

The documentation also says Codex scans repository-local `.agents/skills`.
This repository's project-specific skills therefore remain correctly located
under its tracked `.agents/skills/`; this research only concerns the separate
user-wide catalog.

## Migration plan recorded at the research date

These commands were intentionally not run before migration authorization. A
second install would have created another copy without removing the existing
`~/.codex/skills` catalog. Both locations could have exposed duplicate names.

The adopted migration changed the consumer integration as one coherent unit:

1. Install with `--dir "$HOME/.agents/skills"` (the explicit, truthful
   destination), rather than pretending the Codex host default has changed.
2. Verify with `gh skill list --dir "$HOME/.agents/skills" --json ...`.
   `gh skill list` treats `--dir` as a custom scope and does not allow it to
   be combined with `--agent` or `--scope`
   [direct source](https://github.com/cli/cli/blob/v2.96.0/pkg/cmd/skills/list/list.go#L143-L162).
3. Keep the same custom directory on direct GitHub CLI maintenance commands:
   `gh skill update --dir "$HOME/.agents/skills" ...`. The update command
   explicitly exposes `--dir` to scan a custom directory
   [official update manual](https://cli.github.com/manual/gh_skill_update).
4. Validate actual Codex discovery on the installed desktop or CLI before
   retiring `~/.codex/skills`. At the research date, the live session exposed
   skills from that legacy location.
5. Treat removal of the old catalog as a separately authorized, recoverable
   user-file migration after the new catalog and discovery result have been
   independently verified.

The cleaner long-term option is for GitHub CLI to update its `codex` user
mapping to match OpenAI's documented `$HOME/.agents/skills`. Once that ships,
the existing `--agent codex --scope user` contract can remain intact and no
custom-directory special case is needed. Until then, neither `CODEX_HOME` nor
`--scope user` changes GitHub CLI's Codex default.

## Sources and local evidence

- GitHub CLI 2.96.0 [install manual](https://cli.github.com/manual/gh_skill_install)
  and [source registry](https://github.com/cli/cli/blob/v2.96.0/internal/skills/registry/registry.go#L48-L73).
- GitHub CLI v2.96.0 [installation destination resolver](https://github.com/cli/cli/blob/v2.96.0/pkg/cmd/skills/install/install.go#L989-L1031)
  and [custom-directory listing behavior](https://github.com/cli/cli/blob/v2.96.0/pkg/cmd/skills/list/list.go#L143-L162).
- GitHub CLI [update manual](https://cli.github.com/manual/gh_skill_update).
- OpenAI [Codex local skill discovery documentation](https://developers.openai.com/codex/skills#where-codex-loads-local-skills).
- Local read-only checks on 2026-08-09: `gh --version`, `gh skill install
  --help`, `gh skill list --agent codex --scope user --json ...`, and
  `./bootstrap.sh agent-skills --check` (50 pinned skills at
  `/Users/wcygan/.codex/skills`).
