---
name: uv
description: UV Python package manager and project tool expert. Auto-loads when working with uv, pyproject.toml, Python project setup, inline script metadata (PEP 723), uv run, uv init, uv add, uv lock, uv sync, uvx, uv tool, Python dependency management, virtual environments, workspaces, or UV-based scripting suites. Keywords: uv, python, pyproject, pip, venv, dependencies, scripts, packaging.
allowed-tools: Read, Grep, Glob, Bash, Write, Edit
---

# UV — Python Package & Project Manager

UV is an extremely fast Python package and project manager written in Rust. It replaces pip, pip-tools, pipx, poetry, pyenv, twine, and virtualenv.

## Quick Reference

| Command | Purpose |
|---------|---------|
| `uv init` | Create new project (app by default) |
| `uv init --lib` | Create library project (src layout) |
| `uv init --script foo.py` | Create script with inline metadata |
| `uv add <pkg>` | Add dependency to project |
| `uv add --dev <pkg>` | Add dev dependency |
| `uv add --script foo.py <pkg>` | Add dependency to inline script |
| `uv remove <pkg>` | Remove dependency |
| `uv run <cmd>` | Run command in project environment |
| `uv run foo.py` | Run script (handles inline metadata) |
| `uv lock` | Create/update lockfile |
| `uv sync` | Sync environment to lockfile |
| `uv build` | Build source dist + wheel |
| `uvx <tool>` | Run tool in ephemeral environment |
| `uv tool install <tool>` | Install tool persistently |
| `uv auth login <service>` | Authenticate to package index |

## Inline Script Metadata (PEP 723)

Zero-config scripts with embedded dependencies:

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "httpx",
#     "rich",
# ]
# ///

"""Script description."""

def main():
    ...

if __name__ == "__main__":
    main()
```

Run directly: `chmod +x script.py && ./script.py` or `uv run script.py`

## Project Structure (Application)

```
my-project/
  pyproject.toml       # Metadata + dependencies
  .python-version      # Python version pin
  uv.lock              # Cross-platform lockfile (commit this)
  .venv/               # Virtual environment (gitignored)
  main.py              # Entry point
```

## Project Structure (Library)

```
my-lib/
  pyproject.toml
  uv.lock
  .python-version
  src/
    my_lib/
      __init__.py
      py.typed
```

## pyproject.toml Essentials

```toml
[project]
name = "my-project"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = ["httpx>=0.27", "rich"]

[dependency-groups]
dev = ["pytest", "ruff"]
lint = ["ruff"]
test = ["pytest", "pytest-cov"]

[tool.uv]
default-groups = ["dev"]

[tool.uv.sources]
my-lib = { workspace = true }
```

## References

- [Scripts](references/scripts.md) — inline metadata, shebang, locking, creating scripts
- [Projects](references/projects.md) — init, layout, structure, build
- [Dependencies](references/dependencies.md) — add/remove, groups, sources, platform-specific
- [Running](references/running.md) — uv run options, --with, signals, .env files
- [Tools](references/tools.md) — uvx, uv tool install, versions, extras
- [Workspaces](references/workspaces.md) — monorepo, members, shared lockfile
- [Configuration](references/configuration.md) — pyproject.toml, uv.toml, precedence
- [Authentication](references/authentication.md) — uv auth login, keyring, private indexes
- [Scripting Suites](references/scripting-suites.md) — creating project automation scripts with UV
