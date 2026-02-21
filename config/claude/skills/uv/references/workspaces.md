# UV — Workspaces

Workspaces manage multiple interconnected packages in a single repository with a shared lockfile.

## Setup

Add to root `pyproject.toml`:

```toml
[tool.uv.workspace]
members = ["packages/*"]
exclude = ["packages/seeds"]
```

Every member directory must contain a `pyproject.toml`.

## Structure

```
my-workspace/
  pyproject.toml          # Root (also a workspace member)
  uv.lock                 # Shared lockfile
  src/
  packages/
    lib-a/
      pyproject.toml
      src/
    lib-b/
      pyproject.toml
      src/
```

## Inter-Member Dependencies

```toml
# In a member's pyproject.toml
[project]
dependencies = ["lib-a", "tqdm>=4"]

[tool.uv.sources]
lib-a = { workspace = true }
```

Workspace member dependencies are automatically editable.

## Root Sources Apply Globally

Any `tool.uv.sources` in the root `pyproject.toml` apply to all members unless overridden.

## Commands

```bash
uv lock                         # Lock entire workspace
uv run --package lib-a test     # Run in specific member
uv sync --package lib-a         # Sync specific member
```

## When to Use

- Multiple interconnected packages with shared dependency resolution
- Extension modules (Rust, C++) alongside Python packages
- Plugin systems

## When NOT to Use

- Members have conflicting requirements
- Members need separate virtual environments
- Use path dependencies instead

---

Docs: https://docs.astral.sh/uv/concepts/projects/workspaces/#getting-started
