---
allowed-tools: Bash(deno:*), Bash(cargo:*), Bash(go:*), Bash(mvn:*), Bash(kubectl:*), Bash(jq:*), Bash(yq:*)
description: Run comprehensive validation with automatic project type detection and live results
---

# /validate

Run comprehensive validation across @[project-files] with automatic project type detection and real-time validation results.

## Live Validation Context

- **JSON Validation**: !`fd "\.json$" . | xargs -I {} sh -c 'jq empty {} 2>&1 || echo "Invalid JSON: {}"' | grep -c "Invalid" || echo "0"`
- **YAML Validation**: !`fd "\.ya?ml$" . | xargs -I {} sh -c 'yq eval . {} > /dev/null 2>&1 || echo "Invalid YAML: {}"' | head -5`
- **TypeScript Check**: !`if [ -f "deno.json" ]; then deno check $(fd "\.ts$" . | head -5); fi`
- **Rust Check**: !`if [ -f "Cargo.toml" ]; then cargo check --quiet 2>&1 | head -3; fi`
- **Go Validation**: !`if [ -f "go.mod" ]; then go vet ./... 2>&1 | head -3; fi`

## Project Analysis

Analyze project configuration for targeted validation:

- **Project Detection**: @package.json @deno.json @Cargo.toml @go.mod @pom.xml
- **Configuration Files**: @tsconfig.json @docker-compose.yml @k8s/*.yaml
- **Build Configuration**: @Dockerfile @Makefile @gradle.build @webpack.config.js
- **Testing Setup**: @**/_.test._ @jest.config.* @vitest.config.*
- **Linting Config**: @.eslintrc.* @clippy.toml @golangci.yml

1. **Language-Specific Validation:**

   **Java:**
   - `mvn clean compile` or `gradle build`
   - `mvn verify` for full validation
   - SpotBugs/PMD static analysis
   - Checkstyle for code conventions

   **Go:**
   - `go build ./...` for compilation
   - `go vet ./...` for suspicious constructs
   - `golangci-lint run` for comprehensive linting
   - `go mod verify` for dependencies

   **Rust:**
   - `cargo check` for fast validation
   - `cargo clippy` for linting
   - `cargo fmt --check` for formatting
   - `cargo audit` for security vulnerabilities

   **TypeScript/JavaScript:**
   - `deno check **/*.ts` or `tsc --noEmit`
   - ESLint/Prettier validation
   - Import resolution checks

2. **Infrastructure Validation:**
   - Kubernetes manifests: `kubectl --dry-run=client`
   - Helm charts: `helm lint`
   - Docker: `docker build --check`
   - Terraform: `terraform validate`

3. **Configuration Files:**
   - JSON/YAML syntax validation
   - Schema validation where applicable
   - Environment-specific config checks
   - Secret/credential scanning

4. **Build System Validation:**
   - Maven: `mvn validate`
   - Gradle: `gradle check`
   - Make: `make -n` for dry run
   - Bazel: `bazel build --nobuild`

5. **Testing Validation:**
   - Unit test compilation
   - Test coverage thresholds
   - Integration test setup
   - Mock/stub availability

6. **Security Validation:**
   - Dependency vulnerability scanning
   - SAST (Static Application Security Testing)
   - License compliance
   - Exposed secrets scan

7. **Documentation Validation:**
   - API documentation generation
   - README completeness
   - Code comment coverage
   - Changelog updates

8. **Generate Validation Report:**
   ```markdown
   # Validation Report

   Generated: [timestamp]
   Project Type: [Java/Go/Rust/K8s/Mixed]

   ## Build Status

   - Compilation: ✓/✗
   - Tests: ✓/✗
   - Linting: ✓/✗

   ## Issues by Severity

   ### Critical (Must Fix)

   - [Issue with file:line]

   ### Warnings (Should Fix)

   - [Issue with file:line]

   ### Info (Consider Fixing)

   - [Issue with file:line]

   ## Recommendations

   - [Specific actions to take]
   ```

Save report to: `/tmp/validation-report-[timestamp].md`

Run appropriate validations based on project type before commits, PRs, or deployments.
