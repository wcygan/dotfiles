# hermes skills CLI Reference

Subcommands under `hermes skills` for managing and exploring skills.

Source: Hermes docs at `/docs/user-guide/features/skills/`. Verify with
`hermes skills --help` on the installed version if a command below behaves
unexpectedly.

## Local management

| Command | Purpose |
|---|---|
| `hermes skills list` | Show all skills visible in the current environment (respects conditional activation). |
| `hermes skills inspect <name>` | Parse and display a single skill's metadata and body. Use to validate frontmatter. |
| `hermes skills audit` | Run security/validation checks across installed skills. |

## Hub interaction

| Command | Purpose |
|---|---|
| `hermes skills browse` | Interactive browser over configured hub sources (skills.sh, GitHub taps, etc.). |
| `hermes skills search <query>` | Keyword search across hub sources. |
| `hermes skills install <source/path>` | Install a skill from a hub. Example: `hermes skills install openai/skills/k8s`. |
| `hermes skills uninstall <name>` | Remove an installed skill. |
| `hermes skills check` | Check for updates from the original hub source. |
| `hermes skills update [<name>]` | Pull the latest version from the hub. |
| `hermes skills tap <source>` | Add a new hub source (e.g., a GitHub repo). |

## Publishing

| Command | Purpose |
|---|---|
| `hermes skills snapshot` | Create a portable snapshot of a skill. |
| `hermes skills publish` | Publish to a hub source. |

## Authoring workflow

When iterating on a skill under `config/hermes/skills/<category>/<name>/`:

```bash
# 1. Edit SKILL.md in your editor

# 2. Confirm Hermes picks it up (external_dirs must include the dotfiles path)
hermes skills list | rg <name>

# 3. Validate frontmatter parses cleanly
hermes skills inspect <name>

# 4. Try it in a session
hermes
> /<name>
```

If `inspect` errors:
- YAML indentation is off (tabs vs spaces)
- A required field is missing or has the wrong type
- `metadata.hermes.category` doesn't match the parent directory

If `list` doesn't show it at all:
- External dir isn't registered in `~/.hermes/config.yaml`
- A conditional activation field is excluding it (check toolsets/platform)
- The file isn't named exactly `SKILL.md`
