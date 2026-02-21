# UV — Configuration Files

## Configuration Locations

| Level | File | Scope |
|-------|------|-------|
| Project | `pyproject.toml` or `uv.toml` | Current project |
| User | `~/.config/uv/uv.toml` | All projects |
| System | `/etc/uv/uv.toml` | Machine-wide |

Precedence: CLI args > env vars > project > user > system

`uv.toml` takes precedence over `pyproject.toml` in the same directory.

## pyproject.toml Format

```toml
[tool.uv]
default-groups = ["dev"]

[[tool.uv.index]]
url = "https://test.pypi.org/simple"
default = true
```

## uv.toml Format

Same structure without the `[tool.uv]` prefix:

```toml
default-groups = ["dev"]

[[index]]
url = "https://test.pypi.org/simple"
default = true
```

## .env Files

`uv run` loads dotenv files automatically:

```bash
uv run --env-file .env.production -- python app.py
```

Multiple files supported; later files override earlier.

Disable: `UV_NO_ENV_FILE=1` or `--no-env-file`

## pip-Specific Config

Only applies to `uv pip` subcommands, not other UV operations:

```toml
[tool.uv.pip]
index-url = "https://test.pypi.org/simple"
```

## Useful Flags

```bash
--no-config           # Disable all config discovery
--config-file path    # Use specific config file
```

---

Docs: https://docs.astral.sh/uv/concepts/configuration-files/
