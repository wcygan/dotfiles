# /docs-update

Updates and maintains existing Docusaurus documentation by analyzing codebase changes and refreshing content automatically.

## Usage

```bash
/docs-update [$ARGUMENTS]
```

## Context-Aware Behavior

The command intelligently analyzes the current project state and updates documentation accordingly:

- **No arguments**: Updates all documentation sources (codebase, OpenAPI, git history)
- **No `/docs` folder**: Suggests running `/docs-init` first
- **Detects OpenAPI files**: Automatically includes API documentation updates
- **Finds JSDoc comments**: Updates code reference documentation
- **Discovers new files**: Regenerates sidebar and navigation
- **Argument parsing**: Uses `$ARGUMENTS` for specific sources ("codebase", "api", "validate", "sidebar")

## Description

Automatically updates existing Docusaurus documentation by analyzing various sources of truth in your project. This command ensures your documentation stays synchronized with code changes, API updates, and project evolution.

### Update Sources

#### 1. Codebase Analysis

**Mermaid Diagram Detection:**

- Automatically detects existing Mermaid diagrams in documentation
- Updates diagram content based on code architecture changes
- Ensures diagram syntax is valid and properly formatted
- Integrates with Docusaurus Mermaid theme configuration

#### 2. Code Documentation Extraction

**Language-Aware Analysis:**

- Scans TypeScript/JavaScript files for JSDoc comments
- Extracts function signatures and type definitions
- Generates API reference documentation from exports
- Updates configuration documentation from config files

**Example Code Analysis:**

````typescript
/**
 * Creates a new user account with email verification
 * @param userData - User information including email and password
 * @param options - Optional settings for account creation
 * @returns Promise resolving to created user with verification status
 * @example
 * ```typescript
 * const user = await createUser(
 *   { email: 'user@example.com', password: 'secure123' },
 *   { sendVerificationEmail: true }
 * );
 * ```
 */
export async function createUser(userData: UserData, options?: CreateUserOptions): Promise<User> {
  // Implementation...
}
````

**Generated Documentation:**

````markdown
## createUser

Creates a new user account with email verification.

### Parameters

- `userData` (UserData) - User information including email and password
- `options` (CreateUserOptions, optional) - Optional settings for account creation

### Returns

Promise resolving to created user with verification status

### Example

```typescript
const user = await createUser(
  { email: "user@example.com", password: "secure123" },
  { sendVerificationEmail: true },
);
```
````

````
#### 3. OpenAPI/Swagger Integration

**API Documentation Generation:**
- Parses `openapi.yaml`, `swagger.json`, or API definition files
- Generates endpoint documentation with examples
- Creates request/response schemas
- Updates authentication documentation

**Supported Formats:**
- OpenAPI 3.x specifications
- Swagger 2.0 specifications
- Postman collections (via conversion)
- GraphQL schemas (via introspection)

**Generated Content:**
```markdown
## POST /api/users

Creates a new user account.

### Request Body

```json
{
  "email": "user@example.com",
  "password": "secure123",
  "firstName": "John",
  "lastName": "Doe"
}
````

### Responses

#### 201 Created

```json
{
  "id": "user_123",
  "email": "user@example.com",
  "firstName": "John",
  "lastName": "Doe",
  "createdAt": "2024-06-18T10:30:00Z"
}
```

#### 400 Bad Request

```json
{
  "error": "VALIDATION_ERROR",
  "message": "Invalid email format",
  "field": "email"
}
```

```
#### 4. Git History Analysis

**Changelog Generation:**
- Analyzes commit messages using conventional commit format
- Groups changes by type (feat, fix, docs, refactor, etc.)
- Extracts breaking changes and migration notes
- Updates version history and release notes

**Migration Documentation:**
- Detects API breaking changes from code diffs
- Generates migration guides for major version updates
- Documents deprecated features and replacement APIs
- Creates upgrade instructions with examples

#### 5. Project Configuration Updates

**Environment Variables:**
- Scans code for environment variable usage
- Updates configuration documentation automatically
- Generates example `.env` files with descriptions
- Documents required vs. optional configuration

**Dependencies:**
- Tracks dependency updates and security advisories
- Updates installation and setup documentation
- Documents breaking changes in major dependency updates
- Generates compatibility matrices for supported versions

### Content Validation

**Link Checking:**
- Validates all internal and external links
- Checks code examples for syntax errors
- Verifies image and asset references
- Reports broken cross-references

**Content Quality:**
- Checks for outdated examples and code snippets
- Validates API endpoint documentation against actual APIs
- Ensures consistent formatting and style
- Detects missing documentation for public APIs
- Validates Mermaid diagram syntax and renders correctly

**Example Validation Report:**
```

📋 Documentation Validation Results

✅ Links: 45/45 valid
❌ Code Examples: 2 syntax errors found

- docs/api/users.md:23 - Invalid JSON syntax
- docs/guides/deployment.md:67 - Outdated CLI command

⚠️ Missing Documentation: 3 items

- src/utils/encryption.ts - No documentation for exportPublicKey()
- src/api/webhooks.ts - Missing webhook signature validation docs
- config/database.ts - No documentation for connection pooling options

📊 Coverage: 87% (174/200 public APIs documented)

````
### Sidebar Regeneration

**Automatic Organization:**
- Analyzes document structure and relationships
- Groups related content together
- Maintains logical information hierarchy
- Preserves custom ordering where specified

**Generated Sidebar Structure:**
```javascript
module.exports = {
  docsSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Getting Started',
      items: ['getting-started', 'installation', 'configuration'],
    },
    {
      type: 'category', 
      label: 'API Reference',
      items: [
        'api/overview',
        'api/authentication',
        {
          type: 'category',
          label: 'Endpoints',
          items: ['api/users', 'api/projects', 'api/webhooks'],
        },
      ],
    },
    {
      type: 'category',
      label: 'Guides',
      items: ['guides/deployment', 'guides/monitoring', 'guides/troubleshooting'],
    },
  ],
};
````

### Update Triggers

**File System Watching:**

- Monitors source code changes
- Tracks API specification updates
- Watches configuration file modifications
- Detects new documentation files

**Git Integration:**

- Triggers updates on commit hooks
- Runs validation in CI/CD pipelines
- Generates documentation diffs for pull requests
- Automates documentation releases with code releases

### Smart Content Merging

**Conflict Resolution:**

- Preserves manual edits while updating generated content
- Uses content markers to separate auto-generated sections
- Maintains custom examples and explanations
- Provides merge conflict resolution for documentation updates

**Content Markers:**

```markdown
<!-- AUTO-GENERATED:START - Do not edit manually -->

## API Reference

This section is automatically generated from code comments.

<!-- AUTO-GENERATED:END -->

## Additional Notes

You can add custom content here that won't be overwritten.
```

## Examples

### Update all documentation sources:

```bash
/docs-update
```

### Update only from code changes:

```bash
/docs-update codebase
```

### Validate and fix issues:

```bash
/docs-update validate
```

### Update API documentation:

```bash
/docs-update api
```

### Regenerate sidebar after adding new files:

```bash
/docs-update sidebar
```

## Integration with Development Workflow

**Pre-commit Hooks:**

```bash
#!/bin/sh
# .git/hooks/pre-commit
/docs-update --validate --dry-run
if [ $? -ne 0 ]; then
  echo "Documentation validation failed. Run '/docs-update --validate' to fix issues."
  exit 1
fi
```

**CI/CD Pipeline Integration:**

```yaml
name: Documentation Update
on:
  push:
    paths: ["src/**", "api/**", "openapi.yaml"]

jobs:
  update-docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Update documentation
        run: |
          /docs-update --source=codebase --source=openapi
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add docs/
          git diff --staged --quiet || git commit -m "docs: update auto-generated documentation"
          git push
```

## Prerequisites

- Existing `/docs` folder with Docusaurus installation
- Node.js 16+ for Docusaurus commands
- Git repository for history analysis
- Valid project structure with supported file types

## Integration with Other Commands

- Run after `/docs-init` to populate initial content
- Use before `/docs-add` to ensure existing content is current
- Combine with `/api-docs` for comprehensive API documentation
- Integrate with `/changelog` for release documentation updates

## Configuration

**Custom Update Rules (`.docsconfig.json`):**

```json
{
  "update": {
    "sources": ["codebase", "openapi", "git"],
    "exclude": ["docs/manual/**", "docs/legacy/**"],
    "codePatterns": ["src/**/*.ts", "lib/**/*.js"],
    "apiSpecs": ["openapi.yaml", "swagger.json"],
    "autoGenerateMarkers": true,
    "preserveCustomContent": true
  },
  "validation": {
    "checkLinks": true,
    "validateCodeExamples": true,
    "requireApiDocumentation": true,
    "minimumCoverage": 80
  }
}
```
