Manage dependencies intelligently for the current project.

Steps:

1. Detect package manager and read dependencies:
   - **Java**: pom.xml (Maven), build.gradle (Gradle)
   - **Go**: go.mod, go.sum
   - **Rust**: Cargo.toml, Cargo.lock
   - **Node.js**: package.json (npm/yarn/pnpm)
   - **Python**: requirements.txt, Pipfile, pyproject.toml
   - **Deno**: deno.json, import_map.json
   - **Kubernetes**: Chart.yaml (Helm), kustomization.yaml

2. Security audit:
   - **Java**: `mvn dependency-check:check` or `gradle dependencyCheckAnalyze`
   - **Go**: `go list -m all | nancy sleuth` or `gosec ./...`
   - **Rust**: `cargo audit`
   - **Node.js**: `npm audit`, `yarn audit`
   - **Kubernetes**: `trivy image` for container scanning
   - Check CVE databases and security advisories
   - Prioritize by severity (Critical > High > Medium > Low)
   - Generate SBOM (Software Bill of Materials)

3. Outdated packages analysis:
   - **Java**: `mvn versions:display-dependency-updates`
   - **Go**: `go list -u -m all`
   - **Rust**: `cargo outdated`
   - **Node.js**: `npm outdated`, `yarn outdated`
   - Categorize by update type (patch/minor/major)
   - Check breaking changes in changelogs/release notes
   - Identify packages that haven't been updated in >1 year
   - Flag unmaintained or archived packages

4. Unused dependencies:
   - Scan codebase for actual usage
   - Identify dependencies never imported
   - Find dev dependencies in production
   - Check for duplicate functionality packages
   - Calculate size impact of unused packages

5. Dependency optimization:
   - Suggest lighter alternatives (e.g., date-fns vs moment)
   - Identify packages that can be replaced with native code
   - Find opportunities to reduce bundle size
   - Recommend tree-shakeable alternatives
   - Check for polyfills no longer needed

6. Update strategy:
   - Create staged update plan (security > patch > minor > major)
   - Generate update commands:
     - **Java**: `mvn versions:set -DnewVersion=X.Y.Z`
     - **Go**: `go get -u package@version`
     - **Rust**: `cargo update -p package --precise version`
   - Include rollback commands and git tags
   - Document testing requirements for each update
   - Create PR-ready update batches
   - Consider using Dependabot or Renovate for automation

7. License compliance:
   - Check all dependency licenses
   - Flag incompatible licenses
   - Identify copyleft licenses requiring attention

Output format:

- Executive summary with risk score
- Categorized list of issues
- Specific remediation commands
- Testing checklist
- Estimated effort and risk for updates
