# Navigating Pi documentation and source

Do not assume a checkout path. Locate a likely clone from the current workspace,
repository metadata, or a path supplied by the user.

## Establish version alignment

```bash
command -v pi
pi --version
git -C <pi-checkout> status --short --branch
jq -r '.name + " " + .version' \
  <pi-checkout>/packages/coding-agent/package.json
```

If installed and source versions differ, use installed help for CLI behavior and
label source-derived explanations with the source version.

## Documentation map

Under `packages/coding-agent/docs/`, common topics include:

| Topic | Typical file |
| --- | --- |
| install, auth, first run | `quickstart.md` |
| interactive mode and CLI usage | `usage.md` |
| providers and credentials | `providers.md` |
| global settings | `settings.md` |
| keybindings | `keybindings.md` |
| sessions and on-disk format | `sessions.md`, `session-format.md` |
| compaction | `compaction.md` |
| custom/local models | `models.md` |
| custom providers | `custom-provider.md` |
| extensions | `extensions.md` |
| skills | `skills.md` |
| packages and resources | `packages.md` |
| JSON, RPC, and SDK integration | `json.md`, `rpc.md`, `sdk.md` |
| development | `development.md` |

Confirm filenames with `rg --files packages/coding-agent/docs`; the catalog can
change between versions.

## Source map

The monorepo commonly separates:

- `packages/coding-agent`: CLI, tools, sessions, resource loading, modes, and
  extension host;
- `packages/agent`: core agent/tool loop;
- `packages/ai`: provider integrations and model registry; and
- `packages/tui`: terminal UI.

Useful searches:

```bash
rg -n "<flag-or-command>" packages/coding-agent/src
rg -n "<event-or-method>" packages/coding-agent/src/core/extensions
rg -n "<compat-field>" packages/ai/src/providers
rg --files packages/coding-agent/examples
```

Read the repository's `AGENTS.md` and `CONTRIBUTING.md` before changing Pi source.

## Trace recipes

- CLI flag: argument parsing, then the consuming call site.
- Tool behavior: built-in tool implementation and its tests.
- Extension behavior: public types, runner/loader, then closest example.
- Model compatibility: config schema, model resolver, provider transform.
- Session behavior: session manager, session format docs, mode-specific adapter.
- TUI behavior: keybinding map and relevant component.

Prefer `rg` over broad recursive grep. Cite exact relative paths and distinguish
observed behavior from inference.
