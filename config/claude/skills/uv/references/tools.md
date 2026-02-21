# UV — Tools (`uvx` / `uv tool`)

## Running Tools Ephemerally

`uvx` (alias for `uv tool run`) runs tools in temporary, isolated environments:

```bash
uvx ruff check .
uvx black --check .
uvx pycowsay hello
```

## Package vs Command Name

When they differ, use `--from`:

```bash
uvx --from httpie http https://example.com
uvx --from 'mypy[faster-cache]' mypy .
```

## Requesting Specific Versions

```bash
uvx ruff@0.3.0 check
uvx ruff@latest check
```

## Installing Tools Persistently

```bash
uv tool install ruff
uv tool install 'ruff>=0.3,<0.4'
```

Installed tools are isolated — their modules aren't importable, preventing conflicts.

## Managing Installed Tools

```bash
uv tool list                    # List installed tools
uv tool upgrade ruff            # Upgrade one tool
uv tool upgrade --all           # Upgrade all tools
uv tool uninstall ruff          # Remove tool
```

## Extra Dependencies

```bash
uvx --with mkdocs-material mkdocs serve
```

## From Git

```bash
uvx --from git+https://github.com/httpie/cli httpie
```

## With Specific Python

```bash
uvx --python 3.10 ruff check
```

---

Docs: https://docs.astral.sh/uv/guides/tools/#running-tools
