Perform a security and best practices audit:

1. Security scanning:
   - Search for hardcoded credentials:
     - API keys, tokens, passwords
     - AWS/GCP/Azure credentials
     - Database connection strings
     - Kubernetes secrets
   - Check for exposed secrets in:
     - Environment files (.env, .properties)
     - Configuration files (application.yml, config.toml)
     - Docker/container images
     - Git history

2. Code-level security:
   **Java:**
   - SQL injection (PreparedStatement usage)
   - XXE attacks in XML parsing
   - Deserialization vulnerabilities
   - Spring Security misconfigurations

   **Go:**
   - SQL injection (parameterized queries)
   - Command injection in os/exec
   - Path traversal vulnerabilities
   - Improper error handling exposing internals

   **Rust:**
   - Unsafe block usage review
   - Memory safety violations
   - Panic handling in production

   **Shell scripts:**
   - Proper quoting and escaping
   - Command injection vulnerabilities
   - Input validation

3. File permissions audit:
   - Check executable scripts have proper permissions
   - Verify no world-writable files
   - Ensure backup directories have restricted access
   - Validate .ssh and sensitive config permissions

4. Portability checks:
   - Verify no hard-coded paths (should use ~ or variables)
   - Check for platform-specific commands
   - Validate shell compatibility (bash vs zsh)
   - Ensure Windows compatibility where needed

5. Backup safety:
   - Verify backups don't include sensitive data
   - Check backup paths are secure
   - Validate restore process doesn't expose secrets
   - Ensure atomic operations for critical files

6. Best practices review:
   - Check for proper error handling
   - Verify cleanup on script failure
   - Validate logging doesn't expose sensitive data
   - Ensure idempotent operations

7. Language/Framework specific:
   **Java:**
   - Dependency vulnerabilities (OWASP Dependency Check)
   - Outdated Spring Boot version
   - Insecure defaults
   - JVM security flags

   **Go:**
   - Module vulnerabilities (nancy, gosec)
   - Goroutine leaks
   - Race conditions
   - Proper context cancellation

   **Rust:**
   - Cargo audit results
   - Unsafe code justification
   - Proper error handling

   **Kubernetes:**
   - Pod security policies
   - RBAC misconfigurations
   - Network policies
   - Secret management

8. Infrastructure security:
   - Container image scanning (Trivy, Grype)
   - Kubernetes manifest validation
   - Helm chart security
   - Infrastructure as Code scanning (Terraform, CloudFormation)
   - CI/CD pipeline security

9. Generate audit report:
   ```markdown
   # Security Audit Report

   Generated: [timestamp]
   Project Type: [Java/Go/Rust/K8s/Mixed]

   ## Critical Issues (Immediate Action Required)

   - [CVE-2023-XXXXX] Vulnerable dependency: package@version
   - [SEC001] Hardcoded database password in config.properties:45

   ## High Priority (Fix Soon)

   - [SEC002] SQL injection risk in UserRepository.java:78
   - [SEC003] Missing RBAC for admin endpoints

   ## Medium Priority (Plan to Fix)

   - [SEC004] Outdated TLS version in use
   - [SEC005] Missing rate limiting on API

   ## Low Priority (Best Practice)

   - [BP001] Consider using structured logging
   - [BP002] Add security headers

   ## Compliance Status

   - OWASP Top 10: [Status]
   - CIS Benchmarks: [Status]
   - PCI DSS: [Status if applicable]

   ## Summary

   - Total issues found: X
   - Critical: X, High: X, Medium: X, Low: X
   - Estimated remediation time: X hours
   - Recommended actions: [prioritized list]
   ```

Save report to: `/tmp/security-audit-[timestamp].md`

Include specific remediation commands and code examples for each finding.
