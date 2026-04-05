# Hub and Distribution

How Hermes skills are discovered, installed, shared, and kept up to date.

## Sources Hermes can pull from

1. **Official** (`official/`) — skills bundled with Hermes, trusted by default.
2. **skills.sh** — public Vercel-hosted directory with search.
3. **Well-known endpoints** — any server exposing `/.well-known/skills/index.json`.
4. **GitHub taps** — direct from a GitHub repo. Default taps include OpenAI,
   Anthropic, and others; add your own with `hermes skills tap <source>`.
5. **ClawHub**, **LobeHub**, **Claude marketplace** — community hubs.

## Security scanning

Installed skills are scanned for data exfiltration patterns and prompt
injection. Findings have three severities; the `--force` flag overrides
non-dangerous findings but **does not** override `dangerous` verdicts.

```bash
hermes skills install some/source      # blocks on dangerous findings
hermes skills install some/source --force   # overrides warnings, not dangers
```

Run `hermes skills audit` periodically to re-scan installed skills.

## Update flow for hub-installed skills

```bash
hermes skills check              # what has newer versions?
hermes skills update <name>      # pull latest for one skill
hermes skills update             # update all installed
```

`version:` in frontmatter drives change detection, so bump it when you publish.

## Publishing your own

`hermes skills snapshot` creates a portable artifact; `hermes skills publish`
pushes it to a configured hub. Exact publishing targets depend on the hub
source — see `hermes skills publish --help` on your installed version.

## Distribution patterns compared

| Pattern | When to use | Trade-offs |
|---|---|---|
| `external_dirs` (dotfiles) | Personal/team skills under version control | Read-only from agent, no hub UX, manual sync via git |
| Private GitHub tap | Shared across machines with public discovery | Requires publishable layout, public by default |
| Skill snapshot + install | One-off sharing | No update tracking, recipient gets a frozen copy |
| skills.sh publish | Public distribution to everyone | Public; subject to security scanning |

## This repo

We use the **`external_dirs` pattern** — see
[dotfiles-integration.md](dotfiles-integration.md).
