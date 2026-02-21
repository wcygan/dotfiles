# UV — Dependencies

## Adding Dependencies

```bash
uv add httpx                      # Latest
uv add 'httpx>=0.27'              # With constraint
uv add 'httpx==0.27.0'            # Exact
uv add --dev pytest               # Dev dependency
uv add --group lint ruff          # Named group
uv add --optional plot matplotlib # Optional extra
uv add -r requirements.txt        # From requirements file
```

## Removing Dependencies

```bash
uv remove httpx
uv remove --dev pytest
uv remove --group lint ruff
```

## Dependency Groups

```toml
[dependency-groups]
dev = ["pytest", "ruff"]
lint = ["ruff>=0.8"]
test = ["pytest", "pytest-cov"]

# Nested groups
dev = [
  {include-group = "lint"},
  {include-group = "test"},
]
```

Control defaults:

```toml
[tool.uv]
default-groups = ["dev"]        # Only install dev by default
default-groups = "all"          # Install all groups
```

```bash
uv run --no-default-groups ...           # Skip default groups
uv run --group lint -- ruff check        # Include specific group
```

## Dependency Sources (`tool.uv.sources`)

Development-only alternative sources:

```toml
[tool.uv.sources]

# Git
httpx = { git = "https://github.com/encode/httpx", tag = "0.27.0" }
httpx = { git = "https://github.com/encode/httpx", branch = "main" }

# Local path
my-lib = { path = "../my-lib" }
my-lib = { path = "../my-lib", editable = true }

# Workspace member
my-lib = { workspace = true }

# Private index
torch = { index = "pytorch" }

# URL
httpx = { url = "https://files.example.com/httpx-0.27.0.tar.gz" }
```

## Platform-Specific Dependencies

```bash
uv add "jax; sys_platform == 'linux'"
uv add "numpy; python_version >= '3.11'"
```

Multiple sources per platform:

```toml
[tool.uv.sources]
httpx = [
  { git = "...", tag = "0.27.2", marker = "sys_platform == 'darwin'" },
  { git = "...", tag = "0.24.1", marker = "sys_platform == 'linux'" },
]
```

## Optional Dependencies (Extras)

```toml
[project.optional-dependencies]
plot = ["matplotlib>=3.6"]
excel = ["openpyxl>=3.1"]
```

```bash
uv add matplotlib --optional plot
```

## Private Indexes

```toml
[[tool.uv.index]]
name = "pytorch"
url = "https://download.pytorch.org/whl/cpu"

[[tool.uv.index]]
name = "private"
url = "https://private.example.com/simple"
```

## Version Specifiers (PEP 508)

| Syntax | Meaning |
|--------|---------|
| `foo>=1.2` | 1.2 or higher |
| `foo>=1.2,<2` | Range |
| `foo~=1.2` | Compatible release (>=1.2,<2) |
| `foo==2.1.*` | Wildcard |
| `foo!=1.4.0` | Exclude version |
| `foo[extra1,extra2]` | With extras |

---

Docs: https://docs.astral.sh/uv/concepts/projects/dependencies/
