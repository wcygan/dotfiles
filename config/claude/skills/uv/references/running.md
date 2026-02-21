# UV — Running Commands (`uv run`)

## Basic Usage

```bash
uv run python -c "import my_pkg"    # Python command
uv run my-cli-tool --flag            # Installed entry point
uv run bash scripts/setup.sh         # Shell script
uv run python main.py                # Python script
```

UV automatically ensures the environment is synced before running.

## Temporary Dependencies (`--with`)

```bash
# Add package for this invocation only (not saved to pyproject.toml)
uv run --with httpx==0.26.0 python -c "import httpx; print(httpx.__version__)"
```

The requested version is respected even if it conflicts with project dependencies.

## Running Scripts with Inline Metadata

Scripts with PEP 723 metadata run in their own isolated environment:

```bash
uv run example.py    # Detects inline metadata, resolves deps separately
```

## Specifying Python Version

```bash
uv run --python 3.10 script.py
```

## Environment Variables

`uv run` loads `.env` files automatically (via dotenvy):

```bash
uv run --env-file .env.production -- python app.py
```

Multiple env files can be specified; later files override earlier ones.

## Skipping Sync

```bash
uv run --no-sync script.py    # Don't check/update environment
uv run --frozen script.py     # Don't update lockfile
```

## Signal Handling

- Unix: UV forwards most signals to the child process
- SIGINT requires duplicate sends or cross-process handling
- Windows: UV ignores Ctrl-C, letting the child handle it

## Running Modules

```bash
uv run -m pytest              # python -m pytest
uv run -m http.server 8000    # python -m http.server
```

---

Docs: https://docs.astral.sh/uv/concepts/projects/run/
