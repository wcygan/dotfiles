---
description: Create a justfile with project-appropriate recipes and conventions
---

Set up a `just` task runner (https://just.systems/) for the current project.

**Analysis steps:**
1. Detect project type by examining files (package.json, Cargo.toml, go.mod, deno.json, pom.xml, etc.)
2. Check for existing justfile (offer to enhance or replace)
3. Identify common tasks already defined (scripts, Makefile, etc.)
4. Generate appropriate recipes based on project conventions

**Justfile conventions to follow:**
- Use lowercase recipe names with hyphens (e.g., `build-release`, `test-unit`)
- Group related recipes with comments
- Set sensible defaults (`set shell := ["bash", "-uc"]` or fish equivalent)
- Include a `default` recipe that lists available commands
- Add `[private]` attribute for helper recipes
- Use `@` prefix for quiet commands where appropriate
- Document recipes with comments above them

**Standard recipe categories:**

1. **Development**
   - `dev` - Start development server/watcher
   - `build` - Build the project
   - `test` - Run tests
   - `lint` - Run linters
   - `fmt` - Format code
   - `check` - Run all quality checks (fmt + lint + test)

2. **Lifecycle**
   - `install` - Install dependencies
   - `clean` - Remove build artifacts
   - `update` - Update dependencies

3. **Utilities**
   - `default` - Show available recipes (use `just --list`)

**Project-specific adaptations:**

- **Node.js**: Wrap npm/pnpm/yarn scripts
- **Rust**: Wrap cargo commands, include `clippy`, `build-release`
- **Go**: Wrap go commands, include `tidy`, `vet`
- **Deno**: Wrap deno tasks
- **Python**: Include venv activation, pip/poetry commands
- **Java/Kotlin**: Wrap gradle/maven commands

**Output:**
1. Create `justfile` in project root
2. Brief explanation of key recipes
3. Suggest adding `just` to project prerequisites in README

**Example justfile structure:**
```just
# Project task runner
set shell := ["bash", "-uc"]

# List available recipes
default:
    @just --list

# Development
dev:
    # ... project-specific dev command

# Build the project
build:
    # ... project-specific build

# Run tests
test *args:
    # ... project-specific test with optional args

# Format code
fmt:
    # ... project-specific formatter

# Lint code
lint:
    # ... project-specific linter

# Run all checks (CI-equivalent)
check: fmt lint test
    @echo "All checks passed"
```

**Do not:**
- Add recipes for commands that don't exist in the project
- Over-engineer with complex shell logic (keep recipes simple)
- Duplicate existing Makefile if user wants to keep it
