---
description: Create a UV-based Python scripting suite for project automation
---

Create a UV-based scripting suite for the current project. UV uses inline script metadata (PEP 723) for zero-config dependency management.

**User's requirements:** $ARGUMENTS

## Task

Analyze the user's requirements and create a `scripts/` directory with UV-powered Python scripts.

## UV Script Structure (PEP 723)

Each script MUST use inline metadata at the top:

```python
#!/usr/bin/env -S uv run --quiet
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "package-name>=1.0",
# ]
# ///

"""Script description."""

def main():
    ...

if __name__ == "__main__":
    main()
```

## Implementation Steps

1. **Analyze requirements**: Understand what scripts the user needs
2. **Create `scripts/` directory** if it doesn't exist
3. **Create each script** with:
   - Proper shebang: `#!/usr/bin/env -S uv run --quiet`
   - PEP 723 metadata block with dependencies
   - `requires-python = ">=3.12"` (or higher if needed)
   - Clear docstring explaining purpose
   - `main()` function with CLI argument parsing if needed
   - `if __name__ == "__main__":` guard
4. **Make scripts executable**: `chmod +x scripts/*.py`
5. **Create `scripts/README.md`** documenting each script

## Script Categories & Common Dependencies

**CLI/Automation:**
- `click` or `typer` - CLI frameworks
- `rich` - Terminal formatting
- `httpx` - HTTP client (async-friendly)

**Data Processing:**
- `pandas` - Data manipulation
- `polars` - Fast dataframes
- `pydantic` - Data validation

**Development:**
- `pytest` - Testing
- `ruff` - Linting/formatting

**Infrastructure:**
- `boto3` - AWS
- `kubernetes` - K8s client
- `docker` - Docker SDK

## Example Scripts

### Build/Deploy Script
```python
#!/usr/bin/env -S uv run --quiet
# /// script
# requires-python = ">=3.12"
# dependencies = ["click", "rich"]
# ///
"""Build and deploy automation."""

import click
from rich.console import Console

console = Console()

@click.command()
@click.option("--env", default="dev", help="Target environment")
def main(env: str):
    console.print(f"[green]Deploying to {env}...[/green]")
    # Implementation here

if __name__ == "__main__":
    main()
```

### Data Processing Script
```python
#!/usr/bin/env -S uv run --quiet
# /// script
# requires-python = ">=3.12"
# dependencies = ["polars", "rich"]
# ///
"""Process data files."""

import polars as pl
from pathlib import Path

def main():
    # Implementation here
    pass

if __name__ == "__main__":
    main()
```

## Output Requirements

1. Create all requested scripts in `scripts/`
2. Each script must be self-contained with UV metadata
3. Include proper error handling and logging
4. Add `--help` support via click/typer for CLI scripts
5. Create `scripts/README.md` with usage examples

## Running Scripts

After creation, scripts run directly:
```bash
# UV handles dependencies automatically
./scripts/my-script.py --help
./scripts/my-script.py --env prod

# Or explicitly via uv
uv run scripts/my-script.py
```

No virtual environment setup needed - UV manages everything inline.
