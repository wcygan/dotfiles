---
allowed-tools: Write, Bash(deno:*), Bash(cargo:*), Bash(go:*), Bash(npm:*), Bash(mvn:*), Bash(mkdir:*)
description: Create project scaffolding for any technology stack
---

## Context

- Technology: $ARGUMENTS (e.g., "deno fresh", "go http", "rust axum", "java quarkus")
- Current directory: !`pwd`
- Existing files: !`ls -la | head -5`

## Your task

Generate project scaffolding for the specified technology:

1. **Parse Technology** - Understand the requested stack and framework
2. **Create Project Structure** - Set up directories and base files
3. **Generate Configuration** - Create necessary config files (package.json, Cargo.toml, etc.)
4. **Add Boilerplate** - Include basic code templates and examples
5. **Setup Instructions** - Provide next steps for development

**Supported Stacks:**

- **Deno**: Fresh web apps, CLI scripts, libraries
- **Go**: HTTP servers, CLI tools, ConnectRPC services
- **Rust**: Axum web services, CLI applications, libraries
- **Java**: Quarkus services, Spring Boot apps
- **Node.js**: Express servers, TypeScript projects
- **Documentation**: Docusaurus sites, README templates

**Generated Files:**

- Project configuration (package.json, Cargo.toml, go.mod, pom.xml)
- Basic source code structure
- Test file templates
- Development task configuration
- README with getting started guide

Example: `/scaffold deno fresh my-app` or `/scaffold rust axum api-server`
