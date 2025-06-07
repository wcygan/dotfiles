Organize and tidy up the programming environment in $ARGUMENTS according to language-specific best practices and conventions.

Steps:

1. **Project Structure Analysis:**
   - Identify project type(s) by scanning for configuration files
   - Detect languages and frameworks in use
   - Map current directory structure vs. conventions

2. **Configuration File Placement:**

   **Rust Projects:**
   - Move `Cargo.toml`, `Cargo.lock` to project root
   - Organize `src/`, `tests/`, `benches/`, `examples/` directories
   - Place `.cargo/config.toml` in appropriate location

   **Go Projects:**
   - Move `go.mod`, `go.sum` to module root
   - Organize packages in logical directory hierarchy
   - Place `cmd/`, `internal/`, `pkg/`, `api/` directories appropriately

   **Java Projects:**
   - Move `pom.xml` (Maven) or `build.gradle` (Gradle) to project root
   - Organize `src/main/java/`, `src/test/java/`, `src/main/resources/`
   - Check `application.properties` placement in `resources/`

   **Deno Projects:**
   - Move `deno.json`, `deno.lock` to project root
   - Organize task definitions and import maps
   - Structure `src/`, `tests/`, `scripts/` directories

   **Node.js Projects:**
   - Move `package.json`, `package-lock.json` to project root
   - Organize `src/`, `dist/`, `tests/`, `scripts/` directories
   - Check `tsconfig.json`, `.eslintrc` placement

3. **Directory Structure Standardization:**

   **Source Code:**
   - Create missing standard directories (`src/`, `lib/`, `tests/`)
   - Move source files to appropriate locations
   - Separate application code from library code

   **Documentation:**
   - Move `README.md` to project root
   - Organize docs in `docs/` directory
   - Place API documentation appropriately

   **Configuration:**
   - Group editor configs (`.vscode/`, `.claude/`, etc.)
   - Organize CI/CD configs (`.github/`, `.gitlab/`, etc.)
   - Place environment configs (`.env.example`, `config/`)

   **Build Artifacts:**
   - Ensure `target/` (Rust), `build/` (others) are gitignored
   - Check `node_modules/`, `dist/` in gitignore
   - Verify temporary files are excluded

4. **File Organization Within Directories:**

   **Source Organization:**
   - Group related modules/packages together
   - Separate interfaces/traits from implementations
   - Organize by feature or layer (domain-driven design)

   **Test Organization:**
   - Match test directory structure to source structure
   - Separate unit, integration, and e2e tests
   - Place test utilities in appropriate shared locations

   **Script Organization:**
   - Move build/deployment scripts to `scripts/`
   - Create task runners in `deno.json`, `package.json`, or `Makefile`
   - Group automation scripts by purpose

5. **Import and Dependency Organization:**

   **Import Statements:**
   - Sort imports by type (standard library, third-party, local)
   - Remove unused imports
   - Use absolute paths where conventional

   **Dependency Management:**
   - Remove unused dependencies from manifests
   - Group dependencies by purpose (dev, test, runtime)
   - Update to compatible versions where safe

6. **Language-Specific Best Practices:**

   **Rust:**
   - Organize modules with `mod.rs` or single-file modules
   - Check `lib.rs` vs `main.rs` usage
   - Verify feature flags in `Cargo.toml`

   **Go:**
   - Follow Go module structure conventions
   - Check package naming conventions
   - Verify internal package usage

   **Java:**
   - Ensure proper package directory structure
   - Check Maven/Gradle multi-module setup
   - Verify resource file locations

   **Deno/TypeScript:**
   - Use JSR imports for standard library
   - Organize type definitions appropriately
   - Check `import_map.json` usage

7. **Cleanup Operations:**
   - Remove empty directories
   - Delete orphaned configuration files
   - Clean up duplicate or conflicting configs
   - Remove build artifacts from version control
   - Fix file permissions where needed

8. **Validation:**
   - Verify builds still work after reorganization
   - Check that tests can still find their targets
   - Ensure CI/CD configs reference correct paths
   - Validate import statements resolve correctly

Safety measures:

- Create git commit before major reorganization
- Preserve file history during moves (use `git mv`)
- Run project-specific tests after each major change
- Check that development workflows still function
- Backup any configuration that might be lost

Output:

- Summary of files moved and directories created
- List of configuration files relocated
- Report on dependency cleanup
- Suggestions for further improvements
- Updated project documentation if needed
