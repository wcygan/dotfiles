# /document

Generates high-quality, user-facing documentation automatically.

## Usage

```
/document [options]
```

## Options

```
/document --readme-only          # Generate only README.md
/document --changelog-only       # Generate only CHANGELOG.md  
/document --api-docs            # Generate API documentation
/document --all                 # Generate all documentation (default)
```

## Description

This command automatically generates and maintains project documentation by analyzing your codebase, configuration files, and git history. It complements the internal-facing `/knowledge-extract` command by focusing on user-facing documentation.

### What it generates:

#### 1. README.md (Root Directory)

Creates comprehensive project documentation in the project root including:

**Project Overview Section:**

- Auto-detected project name and description from `package.json`, `Cargo.toml`, `go.mod`, `deno.json`
- Technology stack detection and badges
- Build status and version badges

**Installation Section:**

- Package manager detection (npm, cargo, go mod, deno)
- Platform-specific installation commands
- Dependency requirements and version constraints

**Usage Section:**

- CLI commands from `deno.json` tasks, `package.json` scripts, or Makefile
- API endpoints from OpenAPI specs or code analysis
- Configuration examples from config files

**Development Section:**

- Setup instructions for new contributors
- Testing commands and coverage information
- Code style and contribution guidelines

#### 2. CHANGELOG.md (Root Directory)

Analyzes git history to create structured changelog in the project root:

**Conventional Commits Analysis:**

- Groups commits by type: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`
- Extracts breaking changes from commit footers
- Links to issues and pull requests

**Version Detection:**

- Uses git tags to determine release versions
- Calculates semantic version bumps based on commit types
- Includes release dates and contributor information

**Example Output:**

```markdown
# Changelog

## [1.2.0] - 2024-06-06

### Features

- Add user authentication system (#42)
- Implement real-time notifications (#45)

### Bug Fixes

- Fix database connection pooling issue (#48)
- Resolve memory leak in websocket handler (#50)

### Breaking Changes

- Remove deprecated `/v1/auth` endpoint
```

#### 3. API Documentation (`/docs` Directory)

Converts technical specs to human-readable docs in the `/docs` folder:

**OpenAPI/Swagger:**

- Generates markdown from `openapi.yaml` or `swagger.json`
- Includes endpoint descriptions, parameters, and examples
- Creates authentication and error handling sections

**gRPC/Protocol Buffers:**

- Parses `.proto` files to create service documentation
- Documents message types and field descriptions
- Generates client code examples

**GraphQL:**

- Analyzes schema files to document queries, mutations, and types
- Creates interactive examples and usage patterns

#### 4. Configuration Documentation (`/docs` Directory)

Documents environment variables and config options in the `/docs` folder:

**Environment Variables:**

```markdown
## Configuration

| Variable       | Description                  | Default | Required |
| -------------- | ---------------------------- | ------- | -------- |
| `DATABASE_URL` | PostgreSQL connection string | -       | Yes      |
| `JWT_SECRET`   | Secret key for JWT tokens    | -       | Yes      |
| `LOG_LEVEL`    | Logging level                | `info`  | No       |
```

**Config File Examples:**

```yaml
# config.example.yaml
database:
  host: localhost
  port: 5432
  name: myapp_development

server:
  port: 8080
  host: 0.0.0.0
```

### Technology Detection

**Project Types Recognized:**

- **Web APIs**: REST, GraphQL, gRPC services
- **CLI Tools**: Command-line applications with help text
- **Libraries**: Packages for distribution (npm, crates.io, etc.)
- **Web Apps**: Frontend applications with build processes
- **Microservices**: Containerized services with health endpoints

**Framework Detection:**

- **Go**: Gin, Echo, Fiber, Connect-Go, Cobra CLI
- **Rust**: Axum, Actix-web, Warp, Rocket, Clap CLI
- **Java**: Spring Boot, Quarkus, Micronaut
- **Deno**: Fresh, Oak, Hono
- **Node**: Express, Fastify, Next.js

### Documentation Maintenance

**Automatic Updates:**

- Detects when documentation is stale compared to code
- Updates version numbers and dependency information
- Refreshes API documentation when schemas change

**Quality Checks:**

- Validates markdown syntax and links
- Checks for broken references to code or files
- Ensures all public APIs are documented

## Examples

### Generate all documentation:

```
/document
```

### Update only README:

```
/document --readme-only
```

### Generate API docs from OpenAPI spec:

```
/document --api-docs
```

### Create changelog since last release:

```
/document --changelog-only
```

## File Structure Created

```
project-root/
├── README.md                    # Main project documentation
├── CHANGELOG.md                 # Release history and changes
└── docs/                        # Detailed documentation
    ├── api.md                   # API reference documentation
    ├── configuration.md         # Environment variables and config
    ├── installation.md          # Detailed installation guide
    ├── usage.md                 # Usage examples and tutorials
    └── templates/               # Custom documentation templates
        ├── README.template.md
        ├── CHANGELOG.template.md
        └── API.template.md
```

## Template Customization

Supports custom templates in `docs/templates/`:

- `README.template.md` - Custom README structure
- `CHANGELOG.template.md` - Custom changelog format
- `API.template.md` - Custom API documentation layout

## Integration Features

**GitHub Integration:**

- Creates `.github/ISSUE_TEMPLATE/` and `.github/PULL_REQUEST_TEMPLATE.md`
- Generates GitHub Pages configuration for documentation sites
- Sets up automated documentation updates via GitHub Actions

**Badge Generation:**

- Build status from CI providers
- Code coverage from testing tools
- Version badges from package registries
- License and language statistics

## Best Practices Applied

**SEO and Discoverability:**

- Proper heading hierarchy for table of contents
- Keywords and descriptions for search engines
- Social media preview metadata

**Accessibility:**

- Alt text for images and diagrams
- Proper semantic HTML in generated content
- Screen reader friendly formatting

**Internationalization:**

- Template support for multiple languages
- RTL language considerations in generated layouts

## Integration with Other Commands

- Use after `/refactor` to update documentation for code changes
- Combine with `/ci-gen` to automate documentation updates in CI
- Use with `/release` to generate release notes and update changelogs
