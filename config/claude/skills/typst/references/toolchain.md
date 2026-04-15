# Toolchain

CLI, LSP, fonts, package namespaces, CI.

## Contents

- [CLI](#cli)
- [tinymist LSP](#tinymist-lsp)
- [Fonts](#fonts)
- [Package namespaces](#package-namespaces)
- [Local-package dev workflow](#local-package-dev-workflow)
- [Publishing a package](#publishing-a-package)
- [CI rendering](#ci-rendering)
- [Troubleshooting](#troubleshooting)

## CLI

```bash
# Compile once to PDF (default)
typst compile main.typ                    # → main.pdf
typst compile main.typ output.pdf         # explicit output
typst compile --format svg main.typ       # → main.svg (one per page)
typst compile --format png main.typ       # → main.png (one per page, or {n}.png)

# Watch for live rebuild
typst watch main.typ                      # re-renders on file changes

# Import-root discipline
typst compile --root . main.typ           # set root for /absolute imports
typst compile --root ../ subdir/main.typ  # roots can be above CWD

# Fonts
typst compile --font-path ./fonts main.typ
typst fonts                               # list discovered fonts
typst fonts --variants                    # with styles/weights
typst fonts --font-path ./fonts

# Package cache
typst compile --package-cache-path ./.cache/typst main.typ

# Queries (pull data out of the compiled doc)
typst query main.typ "<fig:diagram>"      # query by label
typst query main.typ "heading.where(level: 1)" --field body --one
```

### Useful flags

| Flag | Effect |
|---|---|
| `--input key=value` | Pass data into the doc via `sys.inputs.key` |
| `--format {pdf,svg,png}` | Output format |
| `--ppi 300` | PNG resolution (default 144) |
| `--pages 1,3,5-7` | Compile specific pages only |
| `--jobs N` | Parallel compilation workers |
| `--diagnostic-format {human,short}` | Error format (short is machine-parseable) |

### Sys inputs pattern

```bash
typst compile --input draft=true --input author="Ada" main.typ
```

```typ
#let is-draft = sys.inputs.at("draft", default: "false") == "true"
#if is-draft [#text(fill: red)[DRAFT]]
```

Great for CI (inject git commit, build date, etc.).

## tinymist LSP

**tinymist** is the current, actively-maintained Typst language server. It replaced `typst-lsp` (archived).

- Ships with: formatter (`typstyle`), preview, hover docs, completion, diagnostics, symbol outline.
- Editor integrations: VS Code (`Tinymist Typst` extension), Neovim (via `nvim-lspconfig` or `lazy.nvim`), Helix (native), Zed (native).
- CLI: `tinymist compile`, `tinymist preview`, `typstyle` (formatter — also standalone).

```bash
# Format a file
typstyle -i main.typ                      # in-place
typstyle main.typ                         # print to stdout

# Format with line width
typstyle --column 100 main.typ
```

## Fonts

Typst discovers fonts from:

1. System font directories
2. `--font-path <dir>` (can be repeated)
3. `TYPST_FONT_PATHS` env var (colon-separated)
4. Fonts bundled in the binary (subset of common defaults: New Computer Modern, DejaVu Sans Mono, Linux Libertine, etc.)

```bash
typst fonts                               # what's available
typst fonts "New Computer Modern"         # search

# Set per-project
export TYPST_FONT_PATHS="$HOME/.fonts:./project-fonts"
```

In documents:

```typ
#set text(font: "New Computer Modern")
#set text(font: ("Inter", "Helvetica", "sans-serif"))  // fallback list
```

**Gotcha:** font name must match exactly as reported by `typst fonts`. Case-sensitive. `"Inter"` != `"Inter Regular"`.

## Package namespaces

| Namespace | Source | Use |
|---|---|---|
| `@preview/<name>:<ver>` | https://typst.app/universe (git: `typst/packages`) | Published community packages |
| `@local/<name>:<ver>` | `~/.local/share/typst/packages/local/` (Linux/macOS) or `%APPDATA%\typst\packages\local` (Windows) | Your unpublished packages |
| relative import `"./x.typ"` | filesystem | Project-local modules |

**Versions are immutable.** Once `@preview/foo:1.2.3` is published, it never changes. Bumps require a new version.

## Local-package dev workflow

```bash
mkdir -p ~/.local/share/typst/packages/local/mypkg/0.1.0
cd ~/.local/share/typst/packages/local/mypkg/0.1.0

# Create typst.toml
cat > typst.toml <<'EOF'
[package]
name = "mypkg"
version = "0.1.0"
entrypoint = "lib.typ"
authors = ["Your Name"]
license = "MIT"
description = "What it does"
EOF

# Create the entrypoint
cat > lib.typ <<'EOF'
#let greet(name) = [Hello, #name!]
EOF
```

```typ
// In any project:
#import "@local/mypkg:0.1.0": greet
#greet("world")
```

For active dev, symlink a working directory into the local namespace:

```bash
ln -s ~/src/mypkg-dev ~/.local/share/typst/packages/local/mypkg/0.1.0
```

## Publishing a package

1. Fork https://github.com/typst/packages.
2. Copy your package to `packages/preview/<name>/<version>/` (lowercase-kebab name, semver version).
3. Required files: `typst.toml`, `README.md`, entrypoint (usually `lib.typ`), `thumbnail.png` (recommended).
4. `typst.toml` must declare `[package]` with `name`, `version`, `entrypoint`, `authors`, `license`, `description`, `categories`, `repository`, and `compiler = "0.13.0"` (min Typst version).
5. Open a PR. Maintainers review; merged versions are immutable and propagate to `@preview`.

**Immutability means:** if you ship a bug, publish a new patch version. Do not rewrite history or force-push.

## CI rendering

Dockerfile snippet:

```dockerfile
FROM ghcr.io/typst/typst:v0.13.1

WORKDIR /work
COPY . .

RUN typst compile main.typ
```

GitHub Actions:

```yaml
- uses: typst-community/setup-typst@v4
  with:
    typst-version: '0.13.1'
- run: typst compile main.typ
- uses: actions/upload-artifact@v4
  with:
    name: pdf
    path: main.pdf
```

For packages, pre-warm the cache to avoid per-run downloads:

```yaml
- uses: actions/cache@v4
  with:
    path: ~/.cache/typst
    key: typst-${{ hashFiles('**/*.typ') }}
```

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `error: file not found (searched at ...)` on `#image(...)` | `--root` not set or path outside root | `typst compile --root . main.typ` |
| `error: package not found: @preview/foo:1.2.3` | Hallucinated version or offline cache miss | Check universe page; `ls ~/.cache/typst/packages/preview/foo/` |
| `warning: unknown font family "Foo"` | Name mismatch | `typst fonts | grep -i foo` to find the exact name |
| Layout drifts between runs | Non-deterministic input (random, time) in the doc | Make inputs deterministic; use `--input` for controlled variation |
| `locate(loc => ...)` compile error | Pre-0.11 idiom | Replace with `#context` block (see [version-drift](version-drift.md)) |
| Compile is slow on large doc | Cold cache + many `@preview` packages | Pre-compile once to warm `~/.cache/typst`; use `typst watch` for dev |
| Emoji / CJK missing glyphs | Font doesn't cover those codepoints | Add fallback in `font: (...)` tuple, e.g., `("Inter", "Noto Sans CJK JP")` |
