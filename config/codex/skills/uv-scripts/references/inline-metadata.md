# Inline Metadata

Use this reference when a script should carry its own Python version and dependency contract.

## When To Use Metadata

Use PEP 723 inline script metadata when:

- the script has third-party dependencies;
- the script should run for another developer without a setup section;
- the script depends on a Python version newer than the system default;
- the script will be called from `just`, `make`, CI, hooks, or another automation surface;
- future agents should not need to infer imports from failures.

Skip metadata for tiny stdlib-only throwaway scripts, unless a `requires-python` constraint would prevent version confusion.

## Core Shape

```python
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "httpx<1",
#   "rich",
# ]
# ///
```

The metadata block is TOML embedded in Python comments. Include `dependencies = []` even when the list is empty.

## Create Or Update Metadata

```sh
uv init --script script.py --python 3.12
uv add --script script.py 'httpx<1' rich
uv run --script script.py
```

Use `uv add --script` instead of manually editing dependency arrays when possible. It updates the inline metadata and avoids easy TOML mistakes.

## Project Boundary Behavior

When `uv run` executes a script with inline metadata, the surrounding project's dependencies are ignored. That makes metadata-bearing scripts a good fit for repo-adjacent utilities that need their own small dependency set.

For scripts without inline metadata inside a project directory, add `--no-project` before the script name when the script should not install or use the current project.

## Shebang Executables

Use a uv shebang for scripts that should run as commands:

```python
#!/usr/bin/env -S uv run --script
#
# /// script
# requires-python = ">=3.12"
# dependencies = ["httpx"]
# ///
```

Then make the file executable:

```sh
chmod +x script-name
./script-name
```

Keep the shebang as the first line. If the file must stay portable to environments that do not support `env -S`, document the fallback command: `uv run --script script-name`.

## Python Versions

Use `requires-python` when:

- the code uses syntax added in a specific version;
- a dependency has a meaningful Python support floor;
- the script should not silently run under an older system Python;
- CI and local machines must agree on interpreter behavior.

For ad hoc runs, a Python version can also be requested at invocation time:

```sh
uv run --python 3.12 --no-project script.py
```

Prefer metadata for durable scripts and command flags for experiments.

## Dependencies

Keep dependencies exact enough to avoid known breakage, but not so pinned that routine patch releases are blocked. Useful patterns:

```toml
dependencies = [
  "httpx>=0.27,<1",
  "rich>=13,<15",
]
```

Use extras only when the script actually imports or needs them:

```toml
dependencies = [
  "httpx[http2]>=0.27,<1",
]
```

## Alternative Indexes

For private or alternate indexes, prefer uv-supported index metadata and keep credentials outside the script:

```sh
uv add --index "https://example.com/simple" --script script.py package-name
```

Do not commit tokens in index URLs. Use the repo's established environment-variable, keyring, or auth flow.

## Source

- https://docs.astral.sh/uv/guides/scripts/
