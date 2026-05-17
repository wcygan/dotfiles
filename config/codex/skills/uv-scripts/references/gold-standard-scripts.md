# Gold-Standard Scripts

Use this reference before writing a new non-trivial uv script. Copy the closest script under `scripts/`, then adapt it to the task.

## Minimum Bar

Every durable script should model:

- PEP 723 metadata with `requires-python` and explicit `dependencies`.
- `#!/usr/bin/env -S uv run --script` when the script is meant to be executable.
- `main(argv: list[str] | None = None) -> int` plus `raise SystemExit(main())`.
- No import-time side effects beyond definitions and constants.
- Clear `--help`, useful errors, predictable exit codes, and `KeyboardInterrupt` handling.
- `Path` inputs, no hard-coded machine-specific paths, and no secrets in code or metadata.
- `--demo` or sample mode when possible so the script can be validated without credentials.
- Explicit network timeouts and bounded retries only for transient operations.
- Atomic writes when partial files would be harmful.
- Human-readable output through `rich`; machine output through `--json` when useful.

## Exemplar Map

| Script | Copy When | Main Libraries |
| --- | --- | --- |
| `scripts/cli_click_rich.py` | Building a polished CLI with commands, options, status, tables, and optional JSON. | `click`, `rich` |
| `scripts/fetch_http.py` | Fetching API or web data with timeouts, retries, caching, output files, and content-type handling. | `httpx`, `tenacity`, `diskcache`, `rich` |
| `scripts/inspect_files.py` | Ingesting mixed local files and summarizing formats before transformation. | `duckdb`, `openpyxl`, `defusedxml`, `pypdf`, `pillow`, `pyyaml`, `rich` |
| `scripts/analyze_duckdb.py` | Doing local CSV, JSON, or Parquet analysis with SQL and exports. | `duckdb`, `rich` |
| `scripts/render_template.py` | Rendering repeatable Markdown, config, SQL, prompt, report, or code templates from validated data. | `jinja2`, `pydantic`, `pyyaml`, `rich` |
| `scripts/script_quality_gate.py` | Checking uv scripts against the minimum bar before committing them. | stdlib, optional Ruff via `uv run --with` |
| `scripts/config_and_secrets.py` | Reading structured env config, selecting portable app paths, or storing local credentials. | `pydantic-settings`, `platformdirs`, `keyring`, `rich` |
| `scripts/orchestrate_dev.py` | Supervising multiple long-running dev processes, optional Docker Compose infra, logs, health checks, and Ctrl+C cleanup. | `click`, `rich`, `pydantic`, `pydantic-settings`, `platformdirs`, `httpx`, `tenacity`, `pyyaml` |
| `scripts/watch_and_run.py` | Creating a local loop that reruns a command when files change. | `watchfiles`, `rich` |
| `scripts/document_assets.py` | Inspecting or transforming PDFs and images in Python. | `pypdf`, `pillow`, `rich` |

## Dev Orchestration Config Shape

Use this shape with `scripts/orchestrate_dev.py --config dev-services.yaml`:

```yaml
app_name: my-app-dev
docker_compose:
  project_name: my-app-dev
  files: [compose.yaml]
  profiles: [dev]
  services: [postgres, redis]
  down_on_exit: true
services:
  - name: api
    command: ["uv", "run", "python", "-m", "my_app.api"]
    health_url: "http://127.0.0.1:8000/health"
    readiness_timeout: 30
  - name: web
    command: ["npm", "run", "dev"]
    depends_on: [api]
    health_url: "http://127.0.0.1:5173"
  - name: worker
    command: ["uv", "run", "python", "-m", "my_app.worker"]
    depends_on: [api]
```

The script treats Docker Compose as owned only when it starts it. Owned Compose resources are stopped with `docker compose down --remove-orphans` during cleanup.

The Recent Logs panel should stay structured: render time, service source, and message as separate columns, and use stable per-service colors so interleaved logs remain scannable.

## Validation Commands

From `config/codex/skills/uv-scripts`, run the examples directly:

```sh
uv run --script scripts/cli_click_rich.py demo
uv run --script scripts/fetch_http.py --demo
uv run --script scripts/inspect_files.py --demo
uv run --script scripts/analyze_duckdb.py --demo
uv run --script scripts/render_template.py --demo
uv run --script scripts/config_and_secrets.py --demo
uv run --script scripts/orchestrate_dev.py --demo --duration 5
uv run --script scripts/watch_and_run.py --demo
uv run --script scripts/document_assets.py --demo
```

Check the whole directory:

```sh
uv run --script scripts/script_quality_gate.py scripts --run-help
uv run --script scripts/script_quality_gate.py scripts --ruff
```

From the dotfiles repo root, run the preflight wrapper:

```sh
tests/test-uv-scripts.sh
```
