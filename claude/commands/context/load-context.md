---
allowed-tools: WebFetch, Read, Bash(fd:*), Bash(rg:*)
description: Load documentation context for any technology or framework
---

## Context

- Technology: $ARGUMENTS (e.g., "go web", "rust async", "kubernetes", "postgres", "deno fresh")
- Current directory: !`pwd`
- Project files: !`fd "(go.mod|Cargo.toml|package.json|deno.json|pom.xml)" . | head -3 | xargs basename 2>/dev/null || echo "no project files"`
- Current tech stack: !`fd "(go.mod|Cargo.toml|package.json|deno.json)" . | wc -l | tr -d ' ' || echo "0"` project files detected

## Your task

Load relevant documentation and context for the specified technology:

1. **Identify Technology** - Parse the target technology from arguments
2. **Load Documentation** - Fetch official docs, best practices, and examples
3. **Project Integration** - Show how it applies to the current project if applicable
4. **Provide Context** - Key concepts, patterns, and gotchas to remember

**Supported Technologies:**

- **Languages**: go, rust, java, python, typescript, deno
- **Web Frameworks**: gin, axum, spring, quarkus, fresh, express
- **Databases**: postgres, mysql, redis, dragonfly, scylla
- **Infrastructure**: kubernetes, docker, talos, cilium
- **Observability**: prometheus, grafana, jaeger, otel
- **Testing**: frameworks and patterns for any language

**Context Sources:**

- Official documentation websites
- GitHub repositories and examples
- Best practice guides
- Common patterns and anti-patterns

Example usage: `/load-context go web` or `/load-context kubernetes networking`
