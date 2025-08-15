---
allowed-tools: Bash(fd:*), Bash(rg:*), Bash(npm:*), Bash(cargo:*), Bash(go:*), Bash(jq:*), Read
description: Analyze project dependencies and their relationships
---

## Context

- Current directory: !`pwd`
- Package managers: !`fd "(package.json|deno.json|Cargo.toml|go.mod|pom.xml|requirements.txt)" . | head -5 | xargs -I {} basename {} 2>/dev/null || echo "none detected"`
- Lock files: !`fd "(package-lock.json|yarn.lock|Cargo.lock|go.sum)" . | head -3 | xargs -I {} basename {} 2>/dev/null || echo "none found"`
- Dependency dirs: !`fd "(node_modules|target|vendor)" -t d | head -3 | xargs -I {} basename {} 2>/dev/null || echo "none found"`

## Your task

Analyze the project's dependency structure and health:

1. **Dependency Overview** - List direct and key transitive dependencies
2. **Security Analysis** - Check for known vulnerabilities or outdated packages
3. **Dependency Tree** - Show key dependency relationships and potential conflicts
4. **Recommendations** - Suggest updates, removals, or security fixes

**Analysis by Technology:**

- **Node.js**: Use `npm audit`, `npm ls`, check package.json vs package-lock.json
- **Deno**: Analyze JSR vs npm imports, check deno.lock consistency
- **Rust**: Use `cargo audit` if available, check Cargo.toml vs Cargo.lock
- **Go**: Use `go mod graph`, `go list -m all`, check for indirect dependencies
- **Java**: Analyze pom.xml or build.gradle, check for version conflicts

Focus on security vulnerabilities, outdated dependencies, and potential conflicts.
