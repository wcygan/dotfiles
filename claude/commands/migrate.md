Create a migration strategy for $ARGUMENTS:

1. **Identify Migration Type:**
   - Database schema migrations
   - API version migrations
   - Dependency updates
   - Code refactoring patterns
   - Infrastructure/K8s resource migrations
   - Configuration format changes

2. **Database Migrations:**

   **Java (Flyway/Liquibase):**
   ```java
   // Flyway: V1__Description.sql
   // Liquibase: changelog-1.0.xml
   ```

   **Go (golang-migrate):**
   ```bash
   migrate create -ext sql -dir migrations description
   migrate -path migrations -database "postgres://..." up
   ```

   **General SQL:**
   ```sql
   -- Forward migration
   ALTER TABLE ...
   -- Rollback migration
   ALTER TABLE ...
   ```

3. **API Version Migrations:**
   - Identify deprecated endpoints
   - Create compatibility layer
   - Plan deprecation timeline
   - Update client SDKs
   - Version documentation

4. **Code Pattern Migrations:**
   ```bash
   # Find candidates for migration
   grep -r "old_pattern" --include="*.java" .
   rg "deprecated_method" -t go

   # Batch processing with headless Claude
   for file in $(find . -name "*.go" -type f); do
     claude -p "Migrate $file from old_pattern to new_pattern" \
       --allowedTools Edit Read
   done
   ```

5. **Kubernetes Resource Migrations:**
   ```yaml
   # Migrate from apps/v1beta1 to apps/v1
   # Update apiVersion and any changed fields
   ```

   Tools:
   - `kubectl convert` for API version updates
   - Helm chart version migrations
   - Custom controller updates

6. **Dependency Migrations:**

   **Java:**
   ```xml
   <!-- Maven: Update versions in pom.xml -->
   <dependency>
     <groupId>...</groupId>
     <version>NEW_VERSION</version>
   </dependency>
   ```

   **Go:**
   ```bash
   go get -u package@version
   go mod tidy
   ```

   **Rust:**
   ```toml
   # Cargo.toml
   [dependencies]
   package = "new_version"
   ```

7. **Migration Plan Template:**
   ```markdown
   # Migration Plan: $DESCRIPTION

   ## Pre-Migration Checklist

   - [ ] Backup current state
   - [ ] Test rollback procedure
   - [ ] Notify stakeholders

   ## Migration Steps

   1. Step with specific commands
   2. Validation after each step

   ## Rollback Plan

   - Specific rollback commands

   ## Post-Migration Validation

   - [ ] Run test suite
   - [ ] Check application health
   - [ ] Verify data integrity
   ```

8. **Automation Script (Deno for scripting):**
   Create `scripts/migrate-$DESCRIPTION.ts` if automating:
   - Include dry-run mode
   - Progress tracking
   - Error handling and rollback
   - Validation steps

What type of migration do we need for $ARGUMENTS?
