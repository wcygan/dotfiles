# UV — Projects

## Creating Projects

```bash
# Application (default) — no build system, simple main.py
uv init my-app

# Packaged application — src layout, build system, entry points
uv init --package my-app

# Library — src layout, py.typed, build system
uv init --lib my-lib

# Minimal — pyproject.toml only
uv init --bare my-project

# With specific Python version
uv init --python 3.12 my-app

# Extension module (Rust via maturin)
uv init --build-backend maturin my-ext
```

## Project Types

| Type | Flag | Layout | Build System | Use Case |
|------|------|--------|-------------|----------|
| Application | (default) | flat `main.py` | none | Scripts, servers, CLIs |
| Packaged App | `--package` | `src/` | yes | Distributable apps |
| Library | `--lib` | `src/` + `py.typed` | yes | PyPI packages |
| Script | `--script` | single `.py` file | none | One-off scripts |

## Application Layout

```
my-app/
  pyproject.toml
  .python-version
  README.md
  main.py
```

## Library Layout (src)

```
my-lib/
  pyproject.toml
  .python-version
  README.md
  src/
    my_lib/
      __init__.py
      py.typed
```

## Core Files

| File | Purpose |
|------|---------|
| `pyproject.toml` | Project metadata, dependencies, build config |
| `uv.lock` | Cross-platform lockfile (commit to VCS) |
| `.python-version` | Python version pin for the project |
| `.venv/` | Virtual environment (gitignore this) |

## Building

```bash
uv build                    # Build sdist + wheel → dist/
uv build --no-sources       # Verify build without custom sources
```

## Lockfile

- `uv.lock` is human-readable TOML managed by UV
- Do not edit manually
- Commit to version control
- `uv lock` to create/update
- `uv lock --upgrade` to upgrade all
- `uv lock --upgrade-package <name>` to upgrade one

---

Docs: https://docs.astral.sh/uv/guides/projects/ | https://docs.astral.sh/uv/concepts/projects/init/ | https://docs.astral.sh/uv/concepts/projects/layout/
