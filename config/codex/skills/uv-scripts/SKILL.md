---
name: uv-scripts
description: Use when Codex needs to write, run, debug, package, or make reproducible standalone Python scripts using uv, including uv run, uv init --script, uv add --script, PEP 723 inline metadata, shebang executables, script lockfiles, cache refresh or cleanup, CI cache behavior, or lightweight dependency choices for script ergonomics.
---

# uv Scripts

Use this skill to create Python scripts that are easy to run once, easy to rerun later, and honest about their dependencies.

## Workflow

1. Inspect the local context first: existing script, `pyproject.toml`, `uv.lock`, `Justfile`, `Makefile`, CI workflow, Python version, and nearby script style.
2. Choose the execution shape:
   - No third-party imports: `uv run --no-project script.py`.
   - Temporary one-off dependency: `uv run --with package --no-project script.py`.
   - Reusable standalone script: PEP 723 inline metadata plus `uv run --script script.py`.
   - Executable command: uv shebang plus inline metadata.
   - Repo application code: use the project's existing uv workflow instead of turning it into a standalone script.
3. Load the smallest relevant reference file from the map below.
4. When writing a non-trivial script, inspect the closest exemplar under `scripts/` before inventing structure.
5. Author scripts with linear control flow, explicit CLI arguments, predictable exit codes, `pathlib`, timeouts for network calls, and no hidden machine-specific paths.
6. Run the exact script command after editing. Add dependencies with `uv add --script` when the script should be reusable.
7. For shared, CI, or release-critical scripts, add a lockfile or reproducibility guard and document the one command users should run.

## Reference Map

- `references/authoring-workflow.md`: choose the right script shape, command form, and maintainable Python structure.
- `references/inline-metadata.md`: use PEP 723 metadata, `uv add --script`, shebangs, Python requirements, indexes, and dependency declarations.
- `references/reproducibility-locks.md`: decide when to lock, pin, use `exclude-newer`, request Python versions, and commit script artifacts.
- `references/cache-ci-troubleshooting.md`: handle uv cache behavior, refresh/reinstall escape hatches, CI pruning, cache directories, and dynamic metadata.
- `references/dependency-toolbox.md`: pick high-value third-party libraries for CLI UX, HTTP, config, validation, serialization, data work, scraping, testing, and formatting.
- `references/gold-standard-scripts.md`: choose which permanent exemplar script to copy before creating a new script.

## Script Exemplars

- `scripts/cli_click_rich.py`: polished Click command surface with Rich output and JSON mode.
- `scripts/fetch_http.py`: HTTP fetching with `httpx`, bounded retries, durable cache, content handling, and no-network demo mode.
- `scripts/inspect_files.py`: safe file intake for JSON, YAML, TOML, CSV, Excel, XML, PDF, and image files.
- `scripts/analyze_duckdb.py`: local CSV/JSON/Parquet analysis with DuckDB, schemas, samples, SQL, and exports.
- `scripts/render_template.py`: validated YAML data plus Jinja rendering with atomic writes.
- `scripts/script_quality_gate.py`: minimum-bar checker for uv standalone scripts, with optional help and Ruff checks.
- `scripts/config_and_secrets.py`: structured settings, portable app paths, and local keyring usage without plaintext secrets.
- `scripts/orchestrate_dev.py`: long-running dev process supervisor with startup order, health checks, logs, Docker Compose hooks, and cleanup.
- `scripts/watch_and_run.py`: file-watch loop for local development commands.
- `scripts/document_assets.py`: practical PDF and image inspection/transformation.

## Quality Rules

- Prefer the standard library until a dependency clearly reduces complexity, failures, or user friction.
- Use inline script metadata for scripts that another person or future agent should run without reconstructing setup.
- Include `requires-python` when syntax, stdlib APIs, or dependency support require a specific Python range.
- Include `dependencies = []` for metadata-bearing scripts even when no third-party packages are needed.
- Use `--no-project` for repo-adjacent scripts that should not install or import the current project.
- Prefer `--refresh` or `--refresh-package` over deleting caches when dependency data may be stale.
- Never edit uv cache directories manually; use `uv cache` commands.
- Keep secrets out of script metadata, lockfiles, command examples, and committed configs.
- If exact uv CLI behavior matters, verify against the current Astral docs before making a precise claim.

## Fast Commands

```sh
uv run --no-project script.py
uv run --with rich --no-project script.py
uv init --script script.py --python 3.12
uv add --script script.py 'httpx<1' rich
uv run --script script.py
uv lock --script script.py
uv cache prune --ci
```

## Sources

- https://docs.astral.sh/uv/guides/scripts/
- https://docs.astral.sh/uv/concepts/cache/
