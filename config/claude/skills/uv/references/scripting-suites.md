---
title: Scripting Suites
description: Creating project automation scripts with UV — script template, checklist, common dependency combos, click/typer CLI patterns
tags: [uv, scripts, automation, click, typer, scripting-suite, template, cli]
---

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

## Error Handling Patterns

Use `sys.exit(1)` for errors and let click handle CLI validation:

```python
#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["click", "rich"]
# ///

import sys
import click
from rich.console import Console

console = Console(stderr=True)

@click.command()
@click.argument("config_path", type=click.Path(exists=True))
def main(config_path: str):
    """Deploy from CONFIG_PATH."""
    try:
        deploy(config_path)
    except PermissionError:
        console.print("[red]Error:[/red] insufficient permissions")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

Key patterns:
- `Console(stderr=True)` — errors go to stderr, stdout stays clean for piping
- `click.Path(exists=True)` — click validates before your code runs
- `sys.exit(1)` — callers (CI, Makefiles) can detect failure
- Catch specific exceptions first, generic `Exception` as fallback

## Common Mistakes

Error output — separate errors from data output:

```python
# CORRECT: errors to stderr, data to stdout
console = Console(stderr=True)  # errors
output = Console()              # data
console.print("[red]Error:[/red] not found")
output.print_json(data=result)

# WRONG: everything to stdout — breaks piping
console = Console()
console.print("[red]Error:[/red] not found")
console.print_json(data=result)
```

Exit codes — always signal failure to callers:

```python
# CORRECT: non-zero exit for errors
except ValueError as e:
    console.print(f"[red]{e}[/red]")
    sys.exit(1)

# WRONG: prints error but exits 0 — CI thinks it succeeded
except ValueError as e:
    print(f"Error: {e}")
    return
```

Click vs argparse — prefer click for consistency across a suite:

```python
# CORRECT: click gives --help, validation, and consistent UX for free
@click.command()
@click.option("--dry-run", is_flag=True)
def main(dry_run: bool): ...

# WRONG: argparse works but lacks --help formatting and type safety
parser = argparse.ArgumentParser()
parser.add_argument("--dry-run", action="store_true")
```

## Running

```bash
./scripts/my-script.py --help       # Direct (after chmod +x)
uv run scripts/my-script.py         # Via uv
```

No virtual environment needed — UV resolves everything from inline metadata.

---

Docs: https://docs.astral.sh/uv/guides/scripts/
