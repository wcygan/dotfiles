---
name: security-review
description: Run a targeted security audit on specified files or modules. Uses OWASP-informed checks, dependency vulnerability scanning, and auth/input validation review. Use for security audits, vulnerability checks, or before deploying sensitive code. Keywords: security, audit, vulnerability, OWASP, CVE, secrets, injection, XSS, auth, authentication, authorization
disable-model-invocation: true
context: fork
argument-hint: "[path-or-module]"
---

# Security Review

Run a targeted security audit using two specialized agents: security-auditor for offensive analysis and reliability-engineer for defensive gaps.

## Workflow

### 1. Determine Scope

Parse the target from `$ARGUMENTS`. If no argument provided, default to the current directory.

```bash
TARGET="${ARGUMENTS:-$(pwd)}"
```

Identify the tech stack to tailor the review:

```bash
# Detect language/framework
ls package.json Cargo.toml go.mod pyproject.toml setup.py requirements.txt pom.xml build.gradle Gemfile 2>/dev/null
```

### 2. Spawn Security Auditor

Use the Task tool to spawn a sub-agent with the security-auditor role.

**Prompt:**

```
You are a security auditor. Perform a thorough security review of: $TARGET

Check for OWASP Top 10 vulnerabilities appropriate to this codebase:

**Injection (A03:2021)**
- SQL injection: raw queries, string concatenation in queries
- Command injection: shell exec with user input, unsanitized args
- LDAP/XPath/NoSQL injection patterns
- Template injection (SSTI)

**Broken Authentication (A07:2021)**
- Hardcoded credentials or API keys
- Weak password policies or missing rate limiting
- Session management issues (fixation, missing expiry)
- Missing MFA enforcement on sensitive operations
- JWT issues (none algorithm, weak secrets, missing expiry)

**Sensitive Data Exposure (A02:2021)**
- Secrets in source code (grep for API keys, tokens, passwords)
- Missing encryption for data at rest or in transit
- Overly verbose error messages exposing internals
- PII in logs or debug output

**Broken Access Control (A01:2021)**
- Missing authorization checks on endpoints
- IDOR (insecure direct object references)
- Path traversal vulnerabilities
- Missing CORS configuration or overly permissive CORS
- Privilege escalation paths

**Security Misconfiguration (A05:2021)**
- Debug mode enabled in production configs
- Default credentials in config files
- Unnecessary features or endpoints exposed
- Missing security headers

**XSS (A03:2021)**
- Unescaped user input in HTML output
- DOM-based XSS via innerHTML or similar unsafe DOM APIs
- Missing Content-Security-Policy

**Dependency Vulnerabilities**
- Check for known CVEs in dependencies if lockfile exists
- Outdated dependencies with known vulnerabilities

For each finding report:
- Severity: Critical / High / Medium / Low
- File and line number
- Description of the vulnerability
- Attack scenario (how it could be exploited)
- Remediation (specific code fix suggestion)
```

### 3. Spawn Reliability Engineer

Use the Task tool to spawn a sub-agent with the reliability-engineer role.

**Prompt:**

```
You are a reliability engineer focusing on defensive security gaps. Review: $TARGET

**Error Handling and Information Leakage**
- Stack traces or internal paths exposed to users
- Error messages that reveal database schema, file paths, or versions
- Different error responses for valid vs invalid users (user enumeration)
- Missing error handling that could crash the service

**Unsafe Deserialization**
- Deserializing untrusted data (unsafe yaml.load, unvalidated JSON parsing, insecure object deserialization)
- Missing schema validation on API inputs
- Prototype pollution in JavaScript

**Logging Security**
- Sensitive data in logs (passwords, tokens, PII)
- Missing audit logging for security-relevant operations
- Log injection vulnerabilities

**Rate Limiting and Resource Exhaustion**
- Missing rate limiting on authentication endpoints
- Unbounded queries or pagination
- File upload without size limits
- Regular expressions vulnerable to ReDoS
- Missing timeouts on external calls

**Cryptographic Issues**
- Weak hashing algorithms (MD5, SHA1 for passwords)
- Missing salt on password hashes
- Predictable random values for security tokens
- Hardcoded initialization vectors or keys

For each finding report:
- Severity: Critical / High / Medium / Low
- File and line number
- Description
- Impact (what could go wrong)
- Remediation
```

### 4. Consolidate Findings

Merge findings from both agents, deduplicate overlapping issues, and sort by severity.

### 5. Output Format

```markdown
## Security Review: [target]

**Scope:** [files/modules reviewed]
**Stack:** [detected language/framework]
**Date:** [current date]

### Critical
- **[VULN-TYPE]** [FILE:LINE] - Description
  Attack: How it could be exploited
  Fix: Specific remediation steps

### High
- **[VULN-TYPE]** [FILE:LINE] - Description
  Impact: What could go wrong
  Fix: Specific remediation steps

### Medium
- ...

### Low
- ...

### Dependency Status
- [PASS/WARN] Known vulnerabilities in dependencies

### Summary
X critical, Y high, Z medium, W low findings.
Top priority: [most important thing to fix first and why]
```

## Notes

- Adapt checks to the detected tech stack (e.g., skip XSS checks for a CLI tool).
- For dependency scanning, check lockfiles: package-lock.json, Cargo.lock, go.sum, poetry.lock, etc.
- If npm audit, cargo audit, or similar tools are available, run them.
- Focus on actionable findings with specific file:line references.
- Do not report theoretical issues without evidence in the code.
