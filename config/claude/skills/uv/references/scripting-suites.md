# UV — Creating Scripting Suites

Guide for creating `scripts/` directories with UV-powered Python automation scripts.

## Script Template

```python
#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "click",
#     "rich",
# ]
# ///

"""Script description — what it does and why."""

import click
from rich.console import Console

console = Console()

@click.command()
@click.option("--verbose", "-v", is_flag=True, help="Verbose output")
def main(verbose: bool):
    """One-line summary for --help."""
    console.print("[green]Done.[/green]")

if __name__ == "__main__":
    main()
```

## Checklist for Each Script

1. Shebang: `#!/usr/bin/env -S uv run --quiet --script`
2. PEP 723 metadata with `requires-python` and `dependencies`
3. Module docstring explaining purpose
4. `main()` function with CLI parsing (click or typer)
5. `if __name__ == "__main__":` guard
6. Proper error handling and exit codes
7. `--help` support via click/typer

## After Creating Scripts

```bash
chmod +x scripts/*.py
```

## Common Dependency Combos

| Category | Packages |
|----------|----------|
| CLI/Output | `click`, `rich` |
| HTTP | `httpx` |
| Data | `polars`, `pandas`, `pydantic` |
| Testing | `pytest` |
| Lint/Format | `ruff` |
| AWS | `boto3` |
| Docker | `docker` |
| K8s | `kubernetes` |
| YAML/TOML | `pyyaml`, `tomli` |

## Running

```bash
./scripts/my-script.py --help       # Direct (after chmod +x)
uv run scripts/my-script.py         # Via uv
```

No virtual environment needed — UV resolves everything from inline metadata.

---

Docs: https://docs.astral.sh/uv/guides/scripts/
