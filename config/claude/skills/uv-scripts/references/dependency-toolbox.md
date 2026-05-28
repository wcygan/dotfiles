# Dependency Toolbox

Use this reference when the standard library is possible but a small dependency would make a script dramatically easier to use, safer, or clearer.

## Selection Rules

- Add a dependency only when it removes meaningful complexity or prevents likely errors.
- Prefer widely used, boring packages with stable APIs for automation scripts.
- Keep dependency groups small; a script with two excellent dependencies is often better than a mini-framework.
- Pin with bounded ranges for shared scripts and lock for CI or critical automation.
- Verify current package docs before relying on exact APIs, security behavior, or optional extras.
- Prefer opinionated defaults for script ergonomics: `click` over `typer`, `duckdb` over dataframe-first tools, `httpx` over `requests`, and `rich` for human-facing output.

## Strong Defaults

- CLI: use `argparse` for one-command stdlib scripts; use `click` when the CLI should feel polished.
- Output: use `rich` for human-readable tables, progress, status, and errors.
- HTTP: use `httpx` with explicit timeouts; add `tenacity` only for retryable remote operations.
- Data: use `duckdb` first for CSV, JSON, Parquet, ad hoc SQL, joins, aggregation, and report queries.
- Config: use `pydantic-settings` for structured environment config; use `platformdirs` for portable config/cache paths.
- Secrets: use `keyring` for local credential storage; do not put secrets in script metadata or `.env` examples.
- Validation: use `pydantic` at untrusted boundaries; use dataclasses for internal-only shapes.
- Files: use focused libraries for real formats instead of partial parsers: `openpyxl` for Excel, `pypdf` for PDFs, `pillow` for images.

## Ten High-Value Additions

These are the extra libraries to reach for when a script crosses from "small Python file" into real automation:

| Library | Why It Is High Value | Use When |
| --- | --- | --- |
| `tenacity` | Declarative retries, stop conditions, waits, jitter, and async support. | API calls, flaky subprocesses, polling, or remote services need bounded retry behavior. |
| `keyring` | Uses OS or configured credential stores instead of plaintext local files. | A script needs tokens, passwords, or local credentials across runs. |
| `diskcache` | Persistent, process-safe local cache with a simple mapping-like API. | Expensive API calls, crawls, derived artifacts, or resumable work need durable cache state. |
| `jinja2` | Mature templating for text, Markdown, HTML, SQL, config, prompts, or codegen. | String assembly starts growing conditionals, loops, includes, or escaping concerns. |
| `python-dateutil` | Practical datetime parsing, relative deltas, recurrence rules, and timezone helpers. | Inputs contain human or external date strings, recurring windows, or calendar math. |
| `openpyxl` | Native Excel workbook read/write for `.xlsx` and related OOXML formats. | Users provide or expect Excel files instead of CSV/Parquet. |
| `pypdf` | Pure-Python PDF split, merge, crop, transform, text, metadata, attachments, forms, and encryption/decryption workflows. | A script needs to inspect or manipulate existing PDFs. |
| `pillow` | Standard image toolkit for opening, resizing, converting, drawing, metadata, and format work. | A script touches PNG/JPEG/WebP/TIFF or generated visual assets. |
| `watchfiles` | Fast cross-platform file watching and reload loops backed by native filesystem notifications. | A local automation script should rerun when files change. |
| `defusedxml` | Safer XML parsing wrappers for hostile or unknown XML inputs. | XML comes from users, vendors, network calls, Office files, SVG, or any untrusted source. |

## Defaults By Need

| Need | Start With | Use When |
| --- | --- | --- |
| Basic CLI flags | `argparse` | The CLI is one command with simple flags. |
| Friendly terminal output | `rich` | Progress bars, tables, tracebacks, colors, status, or readable logs matter. |
| Multi-command CLI | `click` | The script has subcommands, prompts, nested commands, completion, or polished help output. |
| HTTP APIs | `httpx` | You need timeouts, sync or async clients, headers, auth, retries around calls, or HTTP/2. |
| Retry/backoff | `tenacity` | Remote calls, polling, locks, or transient failures need bounded retries with jitter. |
| Data validation | `pydantic` | Input comes from JSON, APIs, env, config, or users and needs typed validation. |
| Settings/env config | `pydantic-settings`, `python-dotenv` | Environment-driven config needs structure or local `.env` support. |
| Local credentials | `keyring` | Tokens or passwords must persist locally without plaintext config files. |
| YAML | `PyYAML` or `ruamel.yaml` | Read simple YAML with PyYAML; preserve comments/round-trip with ruamel.yaml. |
| TOML writes | `tomli-w` | Python can read TOML in modern versions, but writing TOML still benefits from a library. |
| Fast JSON or schemas | `orjson` or `msgspec` | Large JSON, strict structs, speed, or binary-friendly formats matter. |
| HTML parsing | `beautifulsoup4` plus `lxml` | Scraping or extracting from imperfect HTML. |
| XML parsing | `defusedxml` | XML is untrusted or comes from vendors, users, Office files, SVG, or network sources. |
| Tabular data | `duckdb` | CSV/JSON/Parquet/SQL-style analysis, joins, aggregation, and report queries. |
| Dataframe transforms | `polars` | In-memory columnar transformations are clearer than SQL for this specific script. |
| Existing pandas ecosystem | `pandas` | The repo already uses pandas or the task needs pandas-specific integrations. |
| Excel | `openpyxl` | Need to read or write `.xlsx`, `.xlsm`, `.xltx`, or `.xltm` workbooks. |
| PDF manipulation | `pypdf` | Need to split, merge, crop, transform, inspect, or extract text/metadata from PDFs. |
| Image processing | `pillow` | Need to resize, convert, inspect, draw, or write image files. |
| Text/template generation | `jinja2` | Output has loops, conditionals, includes, escaping, or repeated structured text. |
| Date parsing/calendar math | `python-dateutil` | Need robust date parsing, relative deltas, recurrence rules, or timezone helpers. |
| Persistent local cache | `diskcache` | Results should survive process restarts and be safe across processes. |
| File watching | `watchfiles` | Need to rerun local automation when files change. |
| Dev orchestration | `click`, `rich`, `pydantic`, `pydantic-settings`, `platformdirs`, `httpx`, `tenacity`, `PyYAML` | Need to supervise multiple local services, validate config, poll health, show logs, and clean up on Ctrl+C. |
| Paths by app/user dirs | `platformdirs` | Cache/config/data paths should be cross-platform and conventional. |
| Globs/gitignore matching | `pathspec` | Need `.gitignore`-style file matching. |
| Testing | `pytest` | Script logic is non-trivial and should be unit-tested outside process execution. |
| Lint/format | `ruff` | Fast formatting and linting for scripts, especially before committing. |

## Good Starter Packs

Human-facing CLI:

```sh
uv add --script script.py click rich
```

Resilient HTTP JSON utility:

```sh
uv add --script script.py 'httpx<1' pydantic tenacity rich
```

Config and secrets automation:

```sh
uv add --script script.py pydantic pydantic-settings platformdirs keyring
```

YAML/TOML repo maintenance:

```sh
uv add --script script.py pyyaml tomli-w rich
```

Template or report generator:

```sh
uv add --script script.py jinja2 rich
```

HTML extraction:

```sh
uv add --script script.py 'httpx<1' beautifulsoup4 lxml
```

Local data query and reporting:

```sh
uv add --script script.py duckdb rich
```

Excel report pipeline:

```sh
uv add --script script.py duckdb openpyxl rich
```

PDF/image artifact utility:

```sh
uv add --script script.py pypdf pillow rich
```

File-watching local automation:

```sh
uv add --script script.py watchfiles rich
```

Long-running dev orchestration:

```sh
uv add --script script.py click rich pydantic pydantic-settings platformdirs 'httpx<1' tenacity pyyaml
```

Script quality check without making the checker a script dependency:

```sh
uv run --with ruff --no-project ruff format script.py
uv run --with ruff --no-project ruff check script.py
```

## Dependency Tradeoffs

- `argparse` vs `click`: stay with `argparse` for small scripts; choose `click` when help text, subcommands, prompts, completion, testing helpers, or user experience are worth the dependency.
- `click` vs `typer`: prefer `click` by default. Reach for `typer` only when the script is intentionally type-hint-first and the team already likes Typer's conventions.
- `requests` vs `httpx`: prefer `httpx` for new scripts because it covers sync and async clients with modern timeout handling. Use `requests` when the surrounding repo already standardizes on it.
- Manual retry loops vs `tenacity`: write a manual loop for one obvious retry; use `tenacity` when stop conditions, backoff, jitter, retry predicates, or async retry matter.
- `pydantic` vs dataclasses: use dataclasses for internal shapes; use pydantic for untrusted boundaries and clear validation errors.
- `.env` vs `keyring`: use `.env` for non-secret local config and examples; use `keyring` for credentials that should persist outside plaintext files.
- `PyYAML` vs `ruamel.yaml`: use PyYAML for simple load/dump; use ruamel.yaml when preserving comments, quoting, or ordering matters.
- `duckdb` vs `polars`: prefer DuckDB for file-backed data, SQL-shaped questions, joins, aggregation, CSV/JSON/Parquet queries, and reporting. Use Polars when dataframe expressions make the transform clearer.
- `polars` vs `pandas`: use Polars for fast, focused dataframe scripts; use pandas when compatibility with existing notebooks, Excel workflows, or pandas-only libraries matters.
- `duckdb` vs SQLite: use DuckDB for analytical queries over files; use SQLite for small persistent local state.
- `diskcache` vs `shelve` or raw SQLite: use DiskCache when you want a durable cache with eviction, cross-process safety, memoization, or resumable work without designing a schema.
- `openpyxl` vs CSV: prefer CSV/Parquet when you control the interface; use openpyxl when the human or vendor interface is Excel.
- `pypdf` vs OCR tools: use pypdf for existing PDF structure, pages, metadata, forms, and extractable text; use OCR-specific tooling only when the PDF is scanned images.
- `pillow` vs image command-line tools: use Pillow when image logic belongs inside the Python script; use dedicated CLI tools when the operation is already a single reliable shell command.
- `defusedxml` vs stdlib XML: use defusedxml for untrusted XML. Treat stdlib XML as acceptable only for trusted, local, controlled inputs.

## Source

- https://docs.astral.sh/uv/guides/scripts/
- https://click.palletsprojects.com/
- https://duckdb.org/docs/stable/clients/python/overview
- https://tenacity.readthedocs.io/
- https://keyring.readthedocs.io/
- https://grantjenks.com/docs/diskcache/
- https://jinja.palletsprojects.com/
- https://dateutil.readthedocs.io/
- https://openpyxl.readthedocs.io/
- https://pypdf.readthedocs.io/
- https://pillow.readthedocs.io/
- https://watchfiles.helpmanual.io/
- https://pypi.org/project/defusedxml/
