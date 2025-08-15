---
allowed-tools: Bash(deno:*), Bash(go:*), Bash(cargo:*), Bash(npm:*), Bash(pnpm:*), Bash(kubectl:*), Bash(fd:*), Bash(rg:*)
description: Project health check for any technology stack
---

## Context

- Target: $ARGUMENTS (optional - specify technology: deno|go|rust|java|k8s|pnpm)
- Current directory: !`pwd`
- Project type detected: !`fd "(deno.json|go.mod|Cargo.toml|pom.xml|package.json|kubernetes|kustomization)" . -d 1 | head -1 | xargs basename 2>/dev/null || echo "unknown"`

**Technology-Specific Context:**

_Deno:_ !`if [ -f deno.json ]; then deno --version 2>&1 | head -1 && echo "Tasks: $(jq -r '.tasks | keys | join(", ")' deno.json 2>/dev/null || echo "none")"; fi`

_Go:_ !`if [ -f go.mod ]; then go version 2>/dev/null && echo "Module: $(head -1 go.mod)"; fi`

_Rust:_ !`if [ -f Cargo.toml ]; then rustc --version 2>/dev/null && echo "Package: $(rg '^name = "' Cargo.toml | head -1)"; fi`

_Node/PNPM:_ !`if [ -f package.json ]; then node --version 2>/dev/null && pnpm --version 2>/dev/null && echo "Scripts: $(jq -r '.scripts | keys | join(", ")' package.json 2>/dev/null || echo "none")"; fi`

_Java:_ !`if [ -f pom.xml -o -f build.gradle ]; then java -version 2>&1 | head -1; fi`

_Kubernetes:_ !`if [ -f "*.yaml" ] && rg -q "apiVersion|kind" *.yaml 2>/dev/null; then kubectl version --client 2>/dev/null | head -1; fi`

## Your task

Perform a focused health check for the detected project type:

1. **Build/Compile Status** - Check if the project builds successfully
2. **Test Status** - Run tests and check coverage if available
3. **Code Quality** - Check formatting/linting standards
4. **Dependencies** - Verify dependency health and security
5. **Configuration** - Validate project configuration files

**Technology-Specific Checks:**

- **Deno**: `deno check`, `deno test`, `deno lint`, `deno fmt --check`
- **Go**: `go build`, `go test`, `go mod tidy`, `golangci-lint` if available
- **Rust**: `cargo check`, `cargo test`, `cargo clippy`, `cargo fmt --check`
- **Node**: `npm test`, lint scripts, dependency audit
- **Java**: Maven/Gradle build, test execution, static analysis
- **K8s**: YAML validation, resource checks, cluster connectivity

Provide a concise health summary with any issues found and recommended actions.
