# CLAUDE.md

IMPORTANT: These are my development preferences and guidelines. YOU MUST follow them when working on my projects.

## Code Style & Workflow

### Testing
- **ALWAYS** write clear, descriptive test names for better readability
- **ALWAYS** prefer running single tests over the whole test suite for performance
- Use `deno test --filter="test name"` or framework-specific single test runners

### Language & Framework Preferences

#### Backend Programming
IMPORTANT: I am primarily a backend developer and prefer these languages and frameworks:
- **Go**: Use [ConnectRPC](https://github.com/connectrpc/connect-go) for RPC services
- **Rust**: Use [axum](https://github.com/tokio-rs/axum) for web services  
- **Java**: Use [Spring Boot](https://spring.io/projects/spring-boot) with [Quarkus](https://quarkus.io/)

#### Scripting & Automation
**YOU MUST** use Deno for all scripting tasks instead of Bash or Python:
- Create `deno.json` in project root with tasks for common operations
- Use JSR imports: `import { walk } from "@std/fs";` NOT `https://deno.land/...`
- Use [Dax](https://github.com/dsherret/dax) for cross-platform shell operations
- Example deno.json imports: `"@std/fs": "jsr:@std/fs@^1.0.17"`

#### Web Development
Use [Deno Fresh](https://fresh.deno.dev/) with these practices:
- Built-in test runner: `Deno.test()`
- Organize tests: `/tests/unit/`, `/tests/component/`, `/tests/e2e/`
- Mock external dependencies for fast, reliable tests
- Use fresh-testing-library for component/handler testing

## Infrastructure Choices

IMPORTANT: I run a Talos Linux Kubernetes Cluster. Use these modern alternatives:
- **Database**: Postgres (NOT MySQL)
- **Cache**: DragonflyDB (NOT Redis)
- **Streaming**: RedPanda (NOT Kafka)
- **NoSQL**: ScyllaDB (NOT Cassandra)

## Common Commands

```bash
# Deno development
deno task dev          # Start development server
deno task test         # Run all tests
deno test --filter="specific test"  # Run single test
deno task build        # Build project
deno check            # Type check
deno fmt              # Format code
deno lint             # Lint code

# Project setup
deno task init        # Initialize / configure the project for a new environment
deno task deps        # Update dependencies
```

## Development Workflow

1. **ALWAYS** run type checking/linting after code changes (e.g., `deno check`, `go vet`, `cargo check`)
2. **ALWAYS** format code before committing using project's formatter
3. **ALWAYS** run relevant tests before pushing changes
4. **NEVER** commit without running pre-commit checks
5. **ALWAYS** use semantic commit messages (feat:, fix:, docs:, refactor:, test:, chore:)

## File Organization

- `/src/` - Source code
- `/tests/` - Test files organized by type
- `/scripts/` - Deno automation scripts
- `deno.json` - Project configuration and tasks
- `import_map.json` - Import mappings (if needed)

## IMPORTANT Notes

- **YOU MUST** follow these guidelines exactly as written
- **ALWAYS** ask for clarification if requirements conflict
- **NEVER** use deprecated patterns or old import styles
- **ALWAYS** prioritize performance and type safety