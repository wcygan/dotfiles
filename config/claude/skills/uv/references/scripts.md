# UV — Scripts (PEP 723 Inline Metadata)

## Creating a Script

```bash
uv init --script example.py --python 3.12
```

## Inline Metadata Format

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "requests<3",
#     "rich",
# ]
# ///
```

The `dependencies` field must be provided even if empty.

## Adding Dependencies to a Script

```bash
uv add --script example.py 'requests<3' 'rich'
```

This updates the metadata block automatically.

## Running Scripts

```bash
# Basic
uv run example.py

# With arguments
uv run example.py arg1 arg2

# From stdin
echo 'print("hello")' | uv run -

# Temporary extra dependency
uv run --with rich example.py

# Specific Python version
uv run --python 3.10 example.py
```

## Shebang for Direct Execution

```python
#!/usr/bin/env -S uv run --script
```

Then: `chmod +x script.py && ./script.py`

Use `--quiet` in shebang to suppress UV output: `#!/usr/bin/env -S uv run --quiet --script`

## Locking Script Dependencies

```bash
uv lock --script example.py
```

Generates `example.py.lock` for reproducible runs.

## Alternative Package Indexes

```bash
uv add --index "https://example.com/simple" --script example.py 'package'
```

## Reproducibility

Add `exclude-newer` to metadata to pin resolution to a point in time:

```python
# /// script
# requires-python = ">=3.12"
# dependencies = ["httpx"]
# exclude-newer = "2024-01-01T00:00:00Z"
# ///
```

---

Docs: https://docs.astral.sh/uv/guides/scripts/
