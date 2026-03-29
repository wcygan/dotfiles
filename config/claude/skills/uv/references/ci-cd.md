---
title: CI/CD Integration
description: UV in GitHub Actions and Docker — setup-uv action, caching, matrix testing, Docker layer optimization, multi-stage builds, trusted publishing
tags: [uv, ci-cd, github-actions, docker, setup-uv, caching, multi-stage, publishing]
---

# UV — CI/CD Integration

## GitHub Actions

## Setup

```yaml
steps:
  - uses: actions/checkout@v4
  - uses: astral-sh/setup-uv@v7
    with:
      version: "0.11.2"       # Pin for reproducibility
      enable-cache: true       # Caches ~/.cache/uv between runs
```

## Python Version Matrix

```yaml
strategy:
  matrix:
    python-version: ["3.11", "3.12", "3.13"]
steps:
  - uses: astral-sh/setup-uv@v7
    with:
      python-version: ${{ matrix.python-version }}
  - run: uv sync --locked --all-extras --dev
  - run: uv run pytest tests
```

## Full CI Workflow

```yaml
name: CI
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12", "3.13"]
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v7
        with:
          version: "0.11.2"
          python-version: ${{ matrix.python-version }}
          enable-cache: true
      - run: uv sync --locked --all-extras --dev
      - run: uv run pytest tests
      - run: uv run ruff check .
      - run: uv run ruff format --check .
```

## Trusted Publishing (PyPI)

```yaml
permissions:
  id-token: write
  contents: read
steps:
  - run: uv build
  - run: uv publish    # Uses OIDC token, no API key needed
```

## Docker

## Install UV (Multi-Stage Copy)

```dockerfile
FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:0.11.2 /uv /uvx /bin/
```

Pin to a specific version tag, not `latest`, for reproducible builds.

## Required Environment Variables

```dockerfile
ENV UV_COMPILE_BYTECODE=1       # Pre-compile .pyc for faster startup
ENV UV_LINK_MODE=copy           # Required — Docker doesn't support hardlinks across layers
ENV UV_PYTHON_DOWNLOADS=never   # Use base image Python, don't download
```

## Layer-Optimized Install

Install dependencies first (changes less often), then the project:

```dockerfile
WORKDIR /app

# Dependencies only — cached unless pyproject.toml/uv.lock change
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-editable

# Project code — rebuilt on every code change
COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-editable
```

## Multi-Stage Production Build

UV is only needed at build time — exclude it from the final image:

```dockerfile
FROM python:3.12-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:0.11.2 /uv /uvx /bin/
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=never
WORKDIR /app
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-editable
COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-editable

FROM python:3.12-slim
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"
CMD ["my_app"]
```

## Common Mistakes

Lockfile flags — use `--locked` in CI/CD, not `--frozen`:

```bash
# CORRECT: verifies lockfile matches pyproject.toml, fails if stale
uv sync --locked

# WRONG in CI: --frozen skips lockfile validation — can deploy stale deps
uv sync --frozen
```

Docker .dockerignore — exclude the local venv:

```
# CORRECT: add to .dockerignore
.venv/
__pycache__/

# WRONG: copying host .venv into container causes platform mismatches
```

Image pinning — pin uv version for reproducible builds:

```dockerfile
# CORRECT: pinned version
COPY --from=ghcr.io/astral-sh/uv:0.11.2 /uv /uvx /bin/

# RISKY: latest can change between builds
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
```

---

Docs:
- https://docs.astral.sh/uv/guides/integration/github/
- https://docs.astral.sh/uv/guides/integration/docker/
