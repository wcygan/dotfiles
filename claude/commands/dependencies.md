# /dependencies

Analyze and visualize dependency relationships, impact analysis, and coupling patterns within codebases, systems, or project components.

## Usage

```
/dependencies [scope: component|service|project|system]
```

## Dependency Analysis Framework

### Phase 1: Dependency Discovery

**Code-Level Dependencies**

```bash
# Language-specific dependency files
fd "package.json|Cargo.toml|go.mod|pom.xml|requirements.txt|composer.json" --type f

# Import/require statements
rg "import|require|use|from|include" -n --type-add 'code:*.{rs,go,java,ts,js,py,cpp,h}'

# Internal module dependencies
rg "\.\/|\.\.\/|@\/" -n  # Relative imports
rg "src\/|lib\/|internal\/" -n  # Absolute internal imports
```

**Infrastructure Dependencies**

```bash
# Container and orchestration dependencies
fd "Dockerfile|docker-compose|k8s|kubernetes" --type f
rg "image:|FROM|depends_on|volumes_from" --type yaml --type dockerfile

# Service mesh and networking
rg "Service|Ingress|ConfigMap|Secret" --type yaml
rg "host:|port:|endpoint:|url:" --type yaml --type json
```

**Runtime Dependencies**

```bash
# Database and external service connections
rg "database|db|postgres|mysql|redis|mongo" -i -A 2 -B 1
rg "http:|https:|grpc:|tcp:|amqp:" -A 1 -B 1
rg "api\..*\.|client\.|service\." -A 1 -B 1
```

### Phase 2: Dependency Mapping

**Direct Dependencies**

- First-order dependencies explicitly declared or imported
- Version constraints and compatibility requirements
- Mandatory vs. optional dependencies
- Development vs. production dependencies

**Transitive Dependencies**

```bash
# Dependency tree analysis
npm ls --all  # Node.js full dependency tree
cargo tree  # Rust dependency tree
go mod graph  # Go module dependencies
mvn dependency:tree  # Maven dependency tree
```

**Circular Dependencies**

```bash
# Find potential circular imports
rg "import.*from ['\"]\.\./" -A 1 -B 1
# Look for module cycles in different languages
madge --circular src/  # JavaScript/TypeScript
cargo tree --duplicates  # Rust duplicates (potential cycles)
```

**Hidden Dependencies**

- Runtime service discovery dependencies
- Configuration-based dependencies
- Environment variable dependencies
- Network protocol dependencies

### Phase 3: Impact Analysis

**Dependency Hierarchy**

```markdown
## Dependency Layers

### Layer 1: Core/Foundation

- [Base libraries and frameworks]
- [System-level dependencies]
- [Critical infrastructure components]

### Layer 2: Business Logic

- [Domain-specific libraries]
- [Application frameworks]
- [Business service dependencies]

### Layer 3: Presentation/Interface

- [UI frameworks and components]
- [API client libraries]
- [Protocol implementations]

### Layer 4: Integration/External

- [Third-party services]
- [External APIs]
- [Vendor-specific tools]
```

**Change Impact Scoring**

```markdown
## Dependency Risk Matrix

| Component     | Dependents | Risk Level | Impact Scope  | Change Frequency |
| ------------- | ---------- | ---------- | ------------- | ---------------- |
| [Component A] | 15         | HIGH       | System-wide   | Weekly           |
| [Component B] | 3          | LOW        | Module-level  | Monthly          |
| [Component C] | 8          | MEDIUM     | Service-level | Quarterly        |

**Risk Levels:**

- HIGH: Changes affect >10 dependents or core functionality
- MEDIUM: Changes affect 3-10 dependents or important features
- LOW: Changes affect <3 dependents or isolated features
```

**Failure Mode Analysis**

- What happens if each dependency becomes unavailable?
- Which dependencies are single points of failure?
- What are the cascading failure scenarios?
- How can failures be contained or isolated?

### Phase 4: Dependency Visualization

**Dependency Graph Generation**

```bash
# Generate visual dependency graphs
madge --image deps.svg src/  # JavaScript/TypeScript
cargo depgraph | dot -Tsvg > deps.svg  # Rust
go mod graph | go-mod-graph-chart  # Go

# Custom dependency mapping
rg "import.*from|require\(" -o | sort | uniq -c | sort -nr
```

**Architecture Diagram**

```markdown
## System Dependency Map
```

┌─────────────────┐ ┌─────────────────┐
│ Frontend │───▶│ API Gateway │
│ (React/Deno) │ │ (Go/Connect) │
└─────────────────┘ └─────────────────┘
│
┌────────▼────────┐
│ Auth Service │
│ (Rust/Axum) │
└────────┬────────┘
│
┌────────▼────────┐
│ PostgreSQL │
│ (Database) │
└─────────────────┘

````
### Phase 5: Coupling Analysis

**Types of Coupling**
- **Content Coupling**: Direct access to internal data
- **Common Coupling**: Shared global data or state
- **Control Coupling**: Passing control flags or commands
- **Data Coupling**: Passing structured data between modules
- **Message Coupling**: Communication through messages/events

**Coupling Metrics**
```bash
# Analyze import/usage patterns
rg "import.*{.*}" -c  # Count of imported symbols
rg "export.*{.*}" -c  # Count of exported symbols
rg "\w+\.\w+" -c     # Method/property access count

# Interface surface area analysis
rg "public|export|pub " -c  # Public interface size
rg "private|internal" -c    # Internal implementation size
````

**Refactoring Opportunities**

- Overly coupled components that should be decoupled
- Missing abstractions that could reduce coupling
- Opportunities for dependency inversion
- Candidates for interface segregation

### Phase 6: Dependency Health Assessment

**Version Management**

```bash
# Find version conflicts and outdated dependencies
npm outdated  # Node.js outdated packages
cargo audit   # Rust security audit
go list -u -m all  # Go module updates available
```

**Security Analysis**

```bash
# Security vulnerability scanning
npm audit  # Node.js security audit
cargo audit  # Rust security vulnerabilities
go list -json -m all | nancy sleuth  # Go security scanning
```

**License Compliance**

```bash
# License compatibility analysis
license-checker  # Node.js license checker
cargo license    # Rust license information
go-licenses check  # Go license verification
```

**Maintenance Burden**

- Frequency of dependency updates required
- Breaking changes and migration effort
- Community support and maintenance status
- Alternative options and migration paths

### Phase 7: Optimization Strategies

**Dependency Reduction**

- Eliminate unused dependencies
- Replace heavy dependencies with lighter alternatives
- Bundle common functionality to reduce dependency count
- Use standard library features instead of external dependencies

**Dependency Injection**

````markdown
## Dependency Injection Opportunities

### Current Direct Dependencies

```rust
// Tightly coupled
fn process_data() {
    let db = PostgresDb::new();
    let cache = RedisCache::new();
    // ...
}
```
````

### Improved with DI

```rust
// Loosely coupled
fn process_data(db: impl Database, cache: impl Cache) {
    // ...
}
```

**Abstraction Layers**

- Create interfaces for external dependencies
- Implement adapter patterns for third-party services
- Use repository patterns for data access
- Apply facade patterns for complex subsystems

**Circuit Breaker Patterns**

```rust
// Example circuit breaker for external service
struct ExternalServiceClient {
    circuit_breaker: CircuitBreaker,
    client: HttpClient,
}

impl ExternalServiceClient {
    async fn call_service(&self) -> Result<Response> {
        self.circuit_breaker.call(|| {
            self.client.get("/api/data").await
        }).await
    }
}
```

## Output Structure

```markdown
# Dependency Analysis: [Scope]

## Executive Summary

- **Total Dependencies**: [Count by type]
- **Highest Risk Dependencies**: [Top 3-5 critical dependencies]
- **Optimization Opportunities**: [Key areas for improvement]

## Dependency Inventory

### External Dependencies

| Name      | Version   | Type          | Risk Level     | Last Updated |
| --------- | --------- | ------------- | -------------- | ------------ |
| [Package] | [Version] | [Runtime/Dev] | [High/Med/Low] | [Date]       |

### Internal Dependencies

| Component  | Dependents | Dependees | Coupling Level |
| ---------- | ---------- | --------- | -------------- |
| [Module A] | 5          | 3         | Medium         |

## Impact Analysis

### Critical Path Dependencies

- [Dependencies that would halt system if unavailable]

### Change Impact Map

- [Which changes would affect which components]

### Failure Scenarios

- [What happens when key dependencies fail]

## Coupling Assessment

### High Coupling Areas

- [Components with excessive interdependencies]

### Decoupling Opportunities

- [Where abstractions could reduce coupling]

### Interface Quality

- [Assessment of dependency interfaces]

## Security & Compliance

### Vulnerability Report

- [Known security issues in dependencies]

### License Compatibility

- [License conflicts or compliance issues]

### Update Status

- [Dependencies requiring updates]

## Optimization Recommendations

### Short-term (1-4 weeks)

1. [Remove unused dependencies]
2. [Update vulnerable packages]
3. [Fix circular dependencies]

### Medium-term (1-3 months)

1. [Introduce abstraction layers]
2. [Implement dependency injection]
3. [Reduce coupling in high-risk areas]

### Long-term (3-12 months)

1. [Architectural refactoring]
2. [Dependency consolidation]
3. [Service boundary optimization]

## Monitoring & Maintenance

### Dependency Health Metrics

- [Key metrics to track over time]

### Automation Opportunities

- [Automated dependency management tools]

### Review Process

- [Regular dependency review cadence]
```

## Integration with Other Commands

- Use with `/deep-dive` for detailed analysis of critical dependencies
- Combine with `/investigate` to research dependency alternatives
- Follow with `/plan` to organize dependency optimization work
- Use with `/monitor` to track dependency health over time
- Apply `/refactor` to implement decoupling strategies

The goal is to maintain healthy, secure, and manageable dependency relationships that support system evolution without creating excessive technical debt or operational risk.
