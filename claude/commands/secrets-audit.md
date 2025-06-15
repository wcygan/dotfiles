<!--
name: secrets:audit
purpose: Scan codebase for leaked credentials and sensitive information
tags: security, secrets, audit, compliance, modern-tools
-->

Scan the codebase for potentially leaked credentials, API keys, tokens, and other sensitive information using modern command-line tools. Provides comprehensive security audit with actionable remediation steps.

**Context**: $ARGUMENTS (optional - scan scope: all, staged, recent, or specific file patterns)

## Scanning Strategy

1. **Pattern-Based Detection**
   - API keys, tokens, and credentials
   - Database connection strings
   - Private keys and certificates
   - Environment variables with sensitive data

2. **File Type Analysis**
   - Configuration files (.env, config.json, etc.)
   - Source code across all languages
   - Documentation and README files
   - Git history and staged changes

3. **Contextual Analysis**
   - High-entropy strings
   - Base64 encoded secrets
   - URL-embedded credentials
   - Comments containing sensitive info

## Detection Patterns

### API Keys & Tokens

```bash
# Generic API key patterns
rg -i "api[-_]?key\s*[:=]\s*['\"]?[a-zA-Z0-9]{20,}['\"]?" --type-add 'config:*.{env,json,yaml,yml,toml,ini,conf}' --type config --type js --type ts --type python --type go --type rust

# Cloud provider keys
rg -i "(aws_access_key|aws_secret|azure_client|gcp_service_account)" --context 2 --color always

# GitHub tokens
rg "ghp_[a-zA-Z0-9]{36}|github_pat_[a-zA-Z0-9_]{82}" --context 1

# JWT tokens
rg "eyJ[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*" --context 1 --color always
```

### Database Credentials

```bash
# Connection strings
rg -i "(postgres|mysql|mongodb|redis)://.*:[^@]*@" --context 2 --color always

# Database passwords
rg -i "(db_pass|database_password|mysql_pass|postgres_pass)\s*[:=]\s*['\"]?[^\s'\"]{8,}['\"]?" --context 1

# Connection parameters
rg -i "(password|pwd)\s*[:=]\s*['\"]?[a-zA-Z0-9!@#$%^&*]{8,}['\"]?" --type-add 'config:*.{env,properties,conf}' --type config
```

### Private Keys & Certificates

```bash
# Private key headers
rg "-----BEGIN (RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----" --context 5 --color always

# Certificate files
fd "\.(pem|key|p12|pfx|crt|cer)$" --type file --hidden

# SSH keys in unusual locations
rg "ssh-(rsa|ed25519|ecdsa)" --exclude-dir .ssh --context 2
```

### High-Entropy Strings

```bash
# Base64 encoded secrets (longer than 40 chars)
rg "[a-zA-Z0-9+/]{40,}={0,2}" --context 1 --color always

# Hex encoded secrets (longer than 32 chars)
rg "[a-fA-F0-9]{32,}" --context 1 --color always

# URL with embedded credentials
rg "https?://[^/\s:]+:[^/\s@]+@[^/\s]+" --context 1 --color always
```

## Scanning Commands

### Full Codebase Scan

```bash
# Comprehensive scan excluding safe directories
rg -i "(password|secret|key|token|credential)" \
   --type-add 'text:*.{txt,md,rst,log}' \
   --type-add 'config:*.{env,json,yaml,yml,toml,ini,conf,properties}' \
   --type text --type config --type js --type ts --type python --type go --type rust \
   --context 2 --color always \
   --glob '!node_modules/*' --glob '!target/*' --glob '!dist/*' --glob '!.git/*'
```

### Git History Scan

```bash
# Recent commits
git log --since="30 days ago" --oneline --grep="password\|secret\|key\|token" --all

# Staged changes
git diff --staged | rg -i "(password|secret|key|token|credential)" --context 2 --color always

# All tracked files
git ls-files | xargs rg -i "(api_key|secret_key|password|token)" --context 1
```

### Environment Files

```bash
# Find all environment files
fd "\.(env|environment)$" --hidden --type file | xargs bat --language bash

# Check for unencrypted secrets in env files
fd "\.(env|environment)$" --hidden --type file | xargs rg -i "(password|secret|key|token)" --context 2 --color always
```

## Modern Tool Integration

### File Discovery with Context

```bash
# Find suspicious files with modern tools
fd "\.(env|config|properties|pem|key|p12)$" --hidden --type file | \
  xargs -I {} sh -c 'echo "=== {} ===" && bat --style=header,numbers --color=always {}'
```

### JSON Output for Processing

```bash
# Structured output for analysis
rg -i "(password|secret|key|token)" --json | \
  jq 'select(.type=="match") | {file: .data.path.text, line: .data.line_number, match: .data.lines.text}' | \
  jq -s 'group_by(.file) | map({file: .[0].file, matches: length, lines: map(.line)})'
```

### Interactive Review

```bash
# Use fzf for interactive secret review
rg -i "(password|secret|key|token)" --color=always --context 2 | \
  fzf --ansi --preview 'echo {} | cut -d: -f1 | xargs bat --color=always --highlight-line $(echo {} | cut -d: -f2)'
```

## Remediation Actions

### Immediate Actions

- Remove secrets from code and configuration files
- Add patterns to .gitignore to prevent future commits
- Rotate compromised credentials immediately
- Use environment variables or secret management systems

### Prevention Measures

```bash
# Create .gitignore patterns
echo "*.env
*.pem
*.key
config/secrets.yml
.env.local" >> .gitignore

# Setup pre-commit hook for secret detection
echo '#!/bin/bash
rg -i "(password|secret|key|token)" --quiet && echo "Potential secrets detected!" && exit 1' > .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

## Output Format

### Summary Report

```json
{
  "scan_timestamp": "2024-06-15T10:30:00Z",
  "scope": "full|staged|recent",
  "findings": [
    {
      "file": "src/config.ts",
      "line": 42,
      "type": "api_key",
      "severity": "high",
      "pattern": "API_KEY = 'sk-...'",
      "recommendation": "Move to environment variable"
    }
  ],
  "summary": {
    "total_files_scanned": 156,
    "files_with_findings": 3,
    "high_risk_findings": 2,
    "medium_risk_findings": 5
  },
  "recommendations": [
    "Rotate API key found in src/config.ts",
    "Add .env files to .gitignore",
    "Setup secret management system"
  ]
}
```

## Example Usage

```bash
# Full security audit
/secrets:audit

# Scan only staged changes
/secrets:audit staged

# Scan recent commits (last 30 days)  
/secrets:audit recent

# Scan specific file types
/secrets:audit "*.env *.json *.yaml"
```
