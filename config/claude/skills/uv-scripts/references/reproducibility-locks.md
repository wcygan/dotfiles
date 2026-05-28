# Reproducibility And Locks

Use this reference when a script should still work the same way next week, in CI, or on another machine.

## Reproducibility Levels

| Level | Use When | Technique |
| --- | --- | --- |
| 0: Throwaway | Local exploration only | `uv run --with ... --no-project script.py` |
| 1: Re-runnable | Script is kept or shared | Inline metadata with version ranges |
| 2: Stable automation | CI, releases, migrations, data exports | `uv lock --script script.py` and commit the adjacent lockfile |
| 3: Time-bounded resolution | Future package releases could change behavior | Add `[tool.uv] exclude-newer` |
| 4: Auditable output | Results affect users, billing, data, or production | Lock, test, record command, inputs, outputs, and timestamps |

## Script Lockfiles

Create a lockfile next to a PEP 723 script:

```sh
uv lock --script script.py
```

The lockfile is named after the script, such as `script.py.lock`. Commit it when the script is part of repeatable automation. Do not commit it for disposable experiments unless the result must be exactly reproducible.

Related commands can reuse script metadata:

```sh
uv run --script script.py
uv export --script script.py
uv tree --script script.py
```

## Version Constraints

Prefer a Python requirement plus bounded dependency ranges before reaching for exact pins:

```python
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "httpx>=0.27,<1",
#   "rich>=13,<15",
# ]
# ///
```

Use exact pins or a lockfile when failures would be costly or hard to diagnose. The lockfile is usually a better durable artifact than hand-pinning every package in the metadata.

## Exclude Newer

Use `exclude-newer` when future releases should not affect a script resolution:

```python
# /// script
# dependencies = ["httpx"]
# [tool.uv]
# exclude-newer = "2026-05-17T00:00:00Z"
# ///
```

Pick an RFC 3339 timestamp tied to the validation date, release date, migration window, or incident investigation. Record why the date exists if it is not obvious.

## Python Version Requests

For durable scripts, prefer `requires-python` in metadata. For one-off validation, request the interpreter at runtime:

```sh
uv run --python 3.12 --script script.py
```

If uv needs a Python version that is not installed, it can fetch one according to uv's Python management behavior. Be explicit when that matters for CI or air-gapped environments.

## What To Commit

Commit:

- the script;
- the adjacent `.lock` file for stable automation;
- a `Justfile`, `Makefile`, README snippet, or CI step with the one blessed run command;
- tests or sample input/output when the script performs non-trivial transformation.

Avoid committing:

- secrets, tokens, or private index credentials;
- local cache paths;
- generated outputs unless they are expected artifacts;
- lockfiles for scratch scripts that should keep floating.

## Validation Loop

For a reusable script:

```sh
uv run --script script.py --help
uv run --script script.py <sample-input>
uv lock --script script.py
```

For a script with formatting or lint expectations:

```sh
uv run --with ruff --no-project ruff format script.py
uv run --with ruff --no-project ruff check script.py
```

## Source

- https://docs.astral.sh/uv/guides/scripts/
