---
description: Set up Python project with Astral toolchain (uv, ruff, ty) and pytest
---

Set up a modern Python project using the Astral toolchain: **uv** (package manager), **Ruff** (linter/formatter), **ty** (type checker), and **pytest** (testing).

**Step 1: Gather Project Information**

Ask the user (or infer from context):
1. **Project name**: snake_case preferred (e.g., `my_project`)
2. **Python version**: Default to 3.12+ if not specified
3. **Project type**: Library, CLI app, web service, or script collection
4. **Source layout**: `src/` layout (recommended) or flat layout

If in an existing directory with Python files, adapt to existing structure.

**Step 2: Initialize with UV**

```bash
# New project
uv init <project-name>
cd <project-name>

# Or in existing directory
uv init
```

**Step 3: Create Project Structure**

For `src/` layout (recommended):
```
project-name/
├── .zed/
│   └── settings.json     # Project-local Zed settings
├── src/
│   └── project_name/
│       ├── __init__.py
│       └── main.py
├── tests/
│   ├── __init__.py
│   └── test_main.py
├── justfile
├── pyproject.toml
├── .python-version
├── uv.lock
└── README.md
```

**Step 4: Configure pyproject.toml**

```toml
[project]
name = "project-name"
version = "0.1.0"
description = "Project description"
requires-python = ">=3.12"
dependencies = []


[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

# ─── UV ───────────────────────────────────────────────────────────────────────
[tool.uv]
dev-dependencies = [
    "pytest>=8.0",
    "pytest-cov",
    "ruff",
    "ty",
]

# ─── RUFF ─────────────────────────────────────────────────────────────────────
[tool.ruff]
line-length = 88
target-version = "py312"
src = ["src", "tests"]

[tool.ruff.lint]
select = [
    "E",      # pycodestyle errors
    "W",      # pycodestyle warnings
    "F",      # pyflakes
    "I",      # isort (import sorting)
    "B",      # flake8-bugbear
    "C4",     # flake8-comprehensions
    "UP",     # pyupgrade
    "ARG",    # unused arguments
    "SIM",    # simplify
    "PTH",    # use pathlib
    "RUF",    # ruff-specific
]
ignore = [
    "E501",   # line too long (formatter handles)
]

[tool.ruff.lint.isort]
known-first-party = ["project_name"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
docstring-code-format = true

# ─── TY ───────────────────────────────────────────────────────────────────────
[tool.ty.environment]
python-version = "3.12"
python = ".venv"

# ─── PYTEST ───────────────────────────────────────────────────────────────────
[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
addopts = [
    "-ra",
    "-q",
    "--strict-markers",
]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
]
```

**Step 5: Create justfile**

```just
# Python project with uv + ruff + ty + pytest

set shell := ["bash", "-cu"]

# List available recipes
default:
    @just --list

# ─── ENVIRONMENT ──────────────────────────────────────────────────────────────

# Install/sync dependencies
install:
    uv sync

# Update dependencies to latest versions
update:
    uv lock --upgrade
    uv sync

# ─── CODE QUALITY ─────────────────────────────────────────────────────────────

# Run linter
lint:
    uv run ruff check .

# Fix auto-fixable lint issues
lint-fix:
    uv run ruff check --fix .

# Format code
fmt:
    uv run ruff format .

# Check formatting without changes
fmt-check:
    uv run ruff format --check .

# Type check
typecheck:
    uv run ty check

# Run all checks
check: lint fmt-check typecheck

# ─── TESTING ──────────────────────────────────────────────────────────────────

# Run tests
test *ARGS:
    uv run pytest {{ ARGS }}

# Run tests with verbose output
test-v:
    uv run pytest -v

# Run tests with coverage
test-cov:
    uv run pytest --cov=src --cov-report=term-missing

# Run fast tests only
test-fast:
    uv run pytest -m "not slow"

# ─── DEVELOPMENT ──────────────────────────────────────────────────────────────

# Run main module
run *ARGS:
    uv run python -m project_name.main {{ ARGS }}

# Start Python REPL
repl:
    uv run python

# ─── MAINTENANCE ──────────────────────────────────────────────────────────────

# Clean build artifacts
clean:
    rm -rf .pytest_cache .ruff_cache .coverage htmlcov dist build
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true

# Build distribution
build: clean
    uv build

# ─── CI ───────────────────────────────────────────────────────────────────────

# Run full CI checks
ci: install check test
```

**Step 6: Create Project-Local Zed Settings**

Create `.zed/settings.json` for project-specific editor configuration:

```json
{
  "languages": {
    "Python": {
      "language_servers": [
        "ruff",
        "ty",
        "!basedpyright",
        "!pyright",
        "..."
      ],
      "format_on_save": "on",
      "formatter": {
        "language_server": {
          "name": "ruff"
        }
      },
      "code_actions_on_format": {
        "source.organizeImports.ruff": true,
        "source.fixAll.ruff": true
      }
    }
  },
  "lsp": {
    "ruff": {
      "initialization_options": {
        "settings": {
          "lineLength": 88,
          "lint": {
            "extendSelect": ["I", "B", "UP", "SIM"]
          }
        }
      }
    },
    "ty": {
      "binary": {
        "path": "ty",
        "arguments": ["server"]
      }
    }
  }
}
```

**Step 7: Create Starter Files**

`src/project_name/__init__.py`:
```python
"""Project name package."""

__version__ = "0.1.0"
```

`src/project_name/main.py`:
```python
"""Main entry point."""


def main() -> None:
    """Run the application."""
    print("Hello from project_name!")


if __name__ == "__main__":
    main()
```

`tests/__init__.py`:
```python
"""Test package."""
```

`tests/test_main.py`:
```python
"""Tests for main module."""

from project_name.main import main


def test_main(capsys: object) -> None:
    """Test main function output."""
    main()
    # Add assertions here
```

**Step 8: Update .gitignore**

Append Python-specific ignores:
```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
.venv/
venv/
ENV/

# UV
uv.lock

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/
.nox/

# Ruff
.ruff_cache/

# Build
dist/
build/
*.egg-info/

# IDE
.idea/
.vscode/
*.swp
*.swo

# Zed local settings are project-specific, commit them
# !.zed/
```

**Step 9: Initialize and Verify**

Run these commands to complete setup:
```bash
# Install dependencies
just install

# Verify all checks pass
just check

# Run tests
just test

# Open in Zed
zed .
```

**Available Commands Summary**

| Command | Description |
|---------|-------------|
| `just` | List all recipes |
| `just install` | Sync dependencies |
| `just update` | Update all dependencies |
| `just lint` | Run Ruff linter |
| `just lint-fix` | Auto-fix lint issues |
| `just fmt` | Format with Ruff |
| `just typecheck` | Run ty type checker |
| `just check` | All quality checks |
| `just test` | Run pytest |
| `just test-cov` | Tests with coverage |
| `just run` | Run main module |
| `just ci` | Full CI pipeline |

**Key Design Decisions**

1. **src/ layout**: Prevents accidental imports of uninstalled package
2. **Project-local Zed settings**: Keeps editor config with project, team-shareable
3. **ty over pyright**: Faster, same team as ruff/uv (Astral)
4. **justfile**: Cross-platform task runner, better than Makefile for non-build tasks
5. **uv.lock committed**: Reproducible installs across team/CI

**After Setup**

1. Update `project-name` and `project_name` throughout files
2. Edit project description in pyproject.toml
3. Add runtime dependencies: `uv add <package>`
4. Add dev dependencies: `uv add --dev <package>`
5. Commit the initial structure

**Optional Enhancements**

- Add `nix flake` for Nix users (use `/nix-project` command)
- Add `.envrc` for direnv integration
- Add pre-commit hooks
- Add GitHub Actions CI workflow
