<!--
name: analyze:deps
purpose: Analyze project dependencies using modern tools and provide insights
tags: dependencies, analysis, security, performance, modern-tools
-->

Analyze project dependencies across multiple languages and package managers using modern command-line tools. Provides security, performance, and maintenance insights for dependency management.

**Context**: $ARGUMENTS (optional - specific analysis type: security, outdated, size, licenses, graph, or all)

## Analysis Types

1. **Security Analysis**
   - Vulnerable dependency detection
   - CVE database checks
   - Security advisory reports

2. **Performance Analysis**
   - Bundle size impact
   - Load time analysis
   - Dependency tree depth

3. **Maintenance Analysis**
   - Outdated packages
   - Maintenance status
   - Update recommendations

## Language-Specific Commands

### Deno Projects

```bash
# Dependency graph with modern tools
deno info --json | jq '.modules[] | {specifier, dependencies: .dependencies[].specifier}' | bat --language json

# Security audit
deno task audit || echo "No audit task defined"

# Outdated dependencies (check deno.json)
fd "deno.json" | xargs bat --language json | jq '.imports'

# Size analysis
deno bundle main.ts | wc -c | numfmt --to=iec
```

### Rust Projects

```bash
# Cargo dependency analysis
cargo tree --format "{p} {f}" | rg -v "build-dependencies|dev-dependencies" | head -20

# Security audit
cargo audit --json | jq '.vulnerabilities[] | {package: .package.name, version: .package.version, id: .advisory.id, severity: .advisory.severity}'

# Outdated dependencies
cargo outdated --root-deps-only --format json | jq '.dependencies[] | select(.status != "up-to-date") | {name, project, latest, status}'

# Build time analysis
cargo build --timings --release 2>&1 | rg "time:" | head -10
```

### Go Projects

```bash
# Module dependency graph
go mod graph | head -20 | bat

# Vulnerability check
go list -json -m all | jq -r '.Path + " " + .Version' | head -20

# Module size analysis
go list -m -json all | jq -r '.Path' | xargs -I {} sh -c 'echo -n "{}: "; go list -f "{{.ImportPath}} {{.Module.Path}}" {} 2>/dev/null | wc -c'

# Unused dependencies
go mod tidy && git diff go.mod go.sum
```

### Node.js/TypeScript Projects

```bash
# Security audit with JSON output
npm audit --json | jq '.vulnerabilities | keys[] as $k | {package: $k, severity: .[$k].severity, via: .[$k].via}'

# Outdated packages
npm outdated --json | jq 'to_entries[] | {package: .key, current: .value.current, wanted: .value.wanted, latest: .value.latest}'

# Bundle size analysis
fd "package.json" | xargs jq '.dependencies, .devDependencies' | jq -s 'add | keys[]' | wc -l

# License analysis
fd "package.json" | xargs jq -r '.dependencies, .devDependencies | keys[]' | head -10
```

## Modern Tool Integration

### Dependency Visualization

```bash
# Create dependency graph with modern tools
case $PROJECT_TYPE in
  "rust")
    cargo tree --format "{p}" | rg -v "├─|└─" | sort | uniq | head -20 | bat
    ;;
  "go") 
    go mod graph | cut -d' ' -f1 | sort | uniq | head -20 | bat
    ;;
  "deno")
    deno info --json | jq -r '.modules[].specifier' | head -20 | bat
    ;;
esac
```

### Security Scanning

```bash
# Universal security check
rg -i "(vulnerable|cve-|security|advisory)" package-lock.json Cargo.lock go.sum deno.lock --context 2 --type json

# Check for known problematic packages
rg -i "(left-pad|event-stream|flatmap-stream)" package*.json Cargo.toml go.mod deno.json --context 1
```

### Performance Impact

```bash
# Large dependency detection
case $PROJECT_TYPE in
  "rust")
    cargo tree --format "{c}" | rg "([0-9]+\.[0-9]+\s*(MB|KB))" --only-matching | sort -hr | head -10
    ;;
  "node")
    fd node_modules | head -20 | xargs du -sh | sort -hr | head -10 | bat
    ;;
esac
```

## Analysis Outputs

### Summary Report

```json
{
  "project_type": "rust|go|deno|node",
  "total_dependencies": 42,
  "security_issues": [
    {
      "package": "package-name",
      "severity": "high|medium|low",
      "advisory": "CVE-2024-1234",
      "fixed_version": "1.2.3"
    }
  ],
  "outdated_packages": [
    {
      "package": "package-name",
      "current": "1.0.0",
      "latest": "2.0.0",
      "breaking_changes": true
    }
  ],
  "recommendations": [
    "Update package-name to fix security vulnerability",
    "Consider removing unused dependency xyz"
  ]
}
```

### Maintenance Dashboard

- Dependency freshness score
- Security risk assessment
- Bundle size impact
- Update priority ranking

## Example Usage

```bash
# Full dependency analysis
/analyze:deps

# Security-focused analysis
/analyze:deps security

# Check for outdated packages
/analyze:deps outdated

# Bundle size analysis
/analyze:deps size

# License compliance check
/analyze:deps licenses
```
