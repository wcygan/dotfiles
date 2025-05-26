# GitHub Actions for Dotfiles

This directory contains GitHub Actions workflows that provide comprehensive CI/CD for the dotfiles repository.

## Workflows

### 🔧 CI Workflow (`ci.yml`)
**Triggers:** Push to main/develop, Pull Requests, Weekly schedule

**What it does:**
- **Code Quality**: TypeScript type checking, linting, formatting validation
- **Integration Tests**: Runs comprehensive test suite across platforms
- **Smoke Tests**: Actual installation testing on clean VMs
- **Security Scanning**: Vulnerability and secret detection
- **Cross-Platform Testing**: macOS, Ubuntu, Windows
- **Multi-Shell Testing**: bash and zsh configurations

**Matrix Testing:**
- **Platforms**: `ubuntu-latest`, `macos-latest`, `windows-latest`
- **Shells**: `bash`, `zsh` (where available)
- **Test Types**: Integration tests, smoke tests, rollback tests

### 🔄 Maintenance Workflow (`maintenance.yml`)
**Triggers:** Daily at 2 AM UTC, Manual dispatch

**What it does:**
- **Dependency Monitoring**: Checks for Deno and dependency updates
- **Health Checks**: Validates repository structure and file integrity
- **Clean Environment Testing**: Daily smoke tests in fresh environments
- **Automated Issue Creation**: Creates GitHub issues when maintenance fails

### 📚 Documentation Workflow (`docs.yml`)
**Triggers:** Changes to markdown files or core scripts

**What it does:**
- **Markdown Validation**: Linting and link checking
- **README Structure Validation**: Ensures required sections exist
- **Code Example Validation**: Verifies README examples are current
- **Statistics Generation**: Updates repository metrics

## Benefits

### 🛡️ Reliability
- **Catch Breaking Changes**: Detect issues before they affect users
- **Cross-Platform Validation**: Ensure dotfiles work on all supported platforms
- **Dependency Drift Detection**: Weekly runs catch external dependency changes

### 🚀 Quality Assurance
- **Type Safety**: Full TypeScript checking with Deno
- **Code Standards**: Automated linting and formatting validation
- **Security**: Vulnerability scanning and secret detection
- **Documentation**: Keep README and docs current

### 🔍 Early Detection
- **Installation Issues**: Test actual installation process regularly
- **Shell Compatibility**: Verify bash and zsh configurations work
- **Rollback Functionality**: Ensure recovery mechanisms function

### 📊 Monitoring
- **Automated Health Checks**: Daily validation of repository health
- **Issue Creation**: Automatic GitHub issues for maintenance failures
- **Statistics Tracking**: Monitor repository metrics over time

## Inspired By

This setup builds on the concept from [mattorb.com's dotfiles CI article](https://mattorb.com/ci-your-dotfiles-with-github-actions/), but extends it significantly to leverage:

- **Existing Test Infrastructure**: Uses the comprehensive `integration-test.ts` suite
- **Deno TypeScript**: Type-safe automation with modern tooling
- **Multi-Platform Support**: Tests across macOS, Linux, and Windows
- **Advanced Features**: Security scanning, dependency monitoring, documentation validation

## Configuration Files

- **`markdown-link-check.json`**: Configuration for markdown link validation
- **`stats.json`**: Generated repository statistics (auto-updated)

## Workflow Status

You can view the status of all workflows in the [Actions tab](../../actions) of the repository.

### Status Badges

Add these to your main README.md to show workflow status:

```markdown
[![CI](https://github.com/YOUR_USERNAME/dotfiles/workflows/Dotfiles%20CI/badge.svg)](https://github.com/YOUR_USERNAME/dotfiles/actions/workflows/ci.yml)
[![Maintenance](https://github.com/YOUR_USERNAME/dotfiles/workflows/Maintenance/badge.svg)](https://github.com/YOUR_USERNAME/dotfiles/actions/workflows/maintenance.yml)
[![Documentation](https://github.com/YOUR_USERNAME/dotfiles/workflows/Documentation/badge.svg)](https://github.com/YOUR_USERNAME/dotfiles/actions/workflows/docs.yml)
```

## Local Testing

Before pushing changes, you can run the same checks locally:

```bash
# Type checking and linting
deno task check
deno lint
deno fmt --check

# Integration tests
deno task test

# Smoke test installation
deno task install:force
```

## Troubleshooting

### Common Issues

1. **Deno Version Mismatch**: Workflows use `v2.x` - ensure compatibility
2. **Permission Issues**: Scripts require `--allow-all` permissions
3. **Platform Differences**: Some features may not work on all platforms
4. **Shell Availability**: zsh may not be available on all systems

### Debugging Workflows

- Check the [Actions tab](../../actions) for detailed logs
- Look for specific job failures in the workflow runs
- Review the maintenance workflow for automated issue creation
- Use `workflow_dispatch` to manually trigger workflows for testing

## Security Considerations

- **Secrets Scanning**: TruffleHog checks for accidentally committed secrets
- **Vulnerability Scanning**: Trivy scans for security vulnerabilities
- **Permissions**: Workflows use minimal required permissions
- **Isolation**: Each test runs in a clean, isolated environment

This comprehensive CI/CD setup ensures your dotfiles remain reliable, secure, and functional across all supported platforms and configurations. 