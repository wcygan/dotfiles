# Cache And CI Troubleshooting

Use this reference when uv appears stale, too slow, inconsistent across machines, or confusing in CI.

## Cache Model

uv caches aggressively to avoid repeated downloads and builds. At a high level:

- registry and direct URL dependencies follow HTTP cache behavior;
- Git dependencies are keyed by resolved commit;
- local archives are keyed by last modification time;
- local directories are keyed by project metadata files and some structural changes.

The cache is designed for concurrent uv commands. Do not mutate cache directories directly.

## Escape Hatches

| Symptom | Prefer | Example |
| --- | --- | --- |
| Registry data may be stale | Refresh all dependency data | `uv run --refresh --script script.py` |
| One package may be stale | Refresh one package | `uv run --refresh-package ruff --script script.py` |
| Installed package should be rebuilt | Reinstall | `uv sync --reinstall` |
| One package cache is suspect | Clean that package cache | `uv cache clean ruff` |
| Whole cache is bad or huge | Clean everything | `uv cache clean` |
| Cache has old unused entries | Prune | `uv cache prune` |
| CI cache stores low-value artifacts | CI prune | `uv cache prune --ci` |

Prefer `--refresh` over `--no-cache` when the goal is to update cached data for future runs too.

## Cache Directory

uv chooses the cache directory in this order:

1. a temporary cache for `--no-cache`;
2. an explicit `--cache-dir`, `UV_CACHE_DIR`, or `tool.uv.cache-dir`;
3. the platform-appropriate default cache location.

Keep the cache on the same filesystem as the environment uv is operating on when performance matters. Otherwise uv may need slower copies instead of links.

## CI Pattern

For CI jobs that cache uv artifacts:

```sh
uv run --script scripts/check.py
uv cache prune --ci
```

Run `uv cache prune --ci` near the end of the job. It keeps source-built wheels while removing less valuable pre-built wheels and unzipped source distributions.

Set `UV_CACHE_DIR` only when the CI cache action or sandbox needs a predictable path. Do not hard-code a user-specific cache path in repo scripts.

## Dynamic Metadata

If a local package uses dynamic metadata, uv may need extra cache keys. Keep default files in the key list when replacing defaults:

```toml
[tool.uv]
cache-keys = [{ file = "pyproject.toml" }, { file = "requirements.txt" }]
```

For setuptools-scm or similar versioning from Git:

```toml
[tool.uv]
cache-keys = [{ file = "pyproject.toml" }, { git = { commit = true } }]
```

Use glob cache keys sparingly because they can force filesystem walks:

```toml
[tool.uv]
cache-keys = [{ file = "**/*.toml" }]
```

If cache keys cannot describe the dynamic behavior, force reinstall for the affected package:

```toml
[tool.uv]
reinstall-package = ["my-package"]
```

## Lock Contention

uv blocks cache-modifying operations while other uv processes are active. If a cache command waits unexpectedly, check for running uv processes before using force options. Use `--force` only when you know no other uv process is reading or writing the cache.

## Source

- https://docs.astral.sh/uv/concepts/cache/
