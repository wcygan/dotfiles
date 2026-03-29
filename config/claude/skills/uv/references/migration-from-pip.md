---
title: Migration from pip/Poetry/Pipenv
description: Concise migration guide mapping pip, poetry, and pipenv commands to UV equivalents — automated migration tool, workflow changes, command mapping
tags: [uv, migration, pip, poetry, pipenv, pip-tools, migrate-to-uv]
---

# UV — Migration from pip/Poetry/Pipenv

## Automated Migration

The `migrate-to-uv` tool auto-detects your current setup and converts:

```bash
# Run in your project directory — handles pip, poetry, pipenv, pip-tools
uvx migrate-to-uv
```

It converts version specs to PEP 440, generates `uv.lock`, and preserves locked versions.

## Command Mapping

| pip / pip-tools | UV equivalent |
|-----------------|---------------|
| `pip install pkg` | `uv add pkg` |
| `pip install -r requirements.txt` | `uv add -r requirements.txt` |
| `pip install -e .` | `uv sync` (auto-editable) |
| `pip freeze` | `uv pip freeze` or `uv export` |
| `pip-compile requirements.in` | `uv lock` |
| `pip-sync requirements.txt` | `uv sync --locked` |
| `python -m venv .venv` | `uv venv` (automatic with `uv sync`) |

| Poetry | UV equivalent |
|--------|---------------|
| `poetry init` | `uv init` |
| `poetry add pkg` | `uv add pkg` |
| `poetry add --group dev pkg` | `uv add --dev pkg` |
| `poetry install` | `uv sync` |
| `poetry lock` | `uv lock` |
| `poetry run cmd` | `uv run cmd` |
| `poetry build` | `uv build` |
| `poetry publish` | `uv publish` |
| `poetry shell` | Not needed — `uv run` handles it |

| Pipenv | UV equivalent |
|--------|---------------|
| `pipenv install pkg` | `uv add pkg` |
| `pipenv install --dev pkg` | `uv add --dev pkg` |
| `pipenv lock` | `uv lock` |
| `pipenv sync` | `uv sync --locked` |
| `pipenv run cmd` | `uv run cmd` |
| `pipenv shell` | Not needed — `uv run` handles it |

## From requirements.txt

```bash
uv init
uv add -r requirements.txt
uv add --dev -r requirements-dev.txt

# If you have a constraints file, use -c to preserve locked versions
uv add -r requirements.in -c requirements.txt
```

## Key Workflow Changes

| Before | After |
|--------|-------|
| `requirements.txt` per platform | Single universal `uv.lock` |
| Manual venv activation | Automatic — `uv run` handles it |
| Multiple requirements files | `[dependency-groups]` in pyproject.toml |
| `pip install && python script.py` | `uv run script.py` |
| `pip install -e .` for dev | `uv sync` (editable by default) |

## What to Delete After Migration

Once `pyproject.toml` and `uv.lock` are working:

- `requirements.txt` / `requirements-dev.txt` / `requirements.in`
- `Pipfile` / `Pipfile.lock`
- `poetry.lock` / `poetry.toml`
- `setup.py` / `setup.cfg` (if fully migrated to pyproject.toml)

Keep `pyproject.toml` and commit `uv.lock`.

---

Docs: https://docs.astral.sh/uv/guides/migration/
