# GitHub Actions for Dotfiles

This directory contains a streamlined GitHub Actions workflow that provides comprehensive CI for the dotfiles repository.

## Workflow

### 🔧 CI Workflow (`ci.yml`)

**Triggers:** Push to main/develop, Pull Requests, Manual dispatch

**What it does:**

- **Code Quality**: TypeScript type checking, linting, formatting validation
- **Integration Tests**: Runs comprehensive test suite across platforms
- **Cross-Platform Testing**: Ubuntu, macOS, Windows
- **Multi-Shell Testing**: bash and zsh configurations (non-Windows)

**Matrix Testing:**

- **Platforms**: `ubuntu-latest`, `macos-latest`, `windows-latest`
- **Test Steps**: Type check, lint, format check, integration tests, bash enhancements

## Benefits

### 🛡️ Reliability

- **Catch Breaking Changes**: Detect issues before they affect users
- **Cross-Platform Validation**: Ensure dotfiles work on all supported platforms
- **Shell Compatibility**: Verify bash and zsh configurations work

### 🚀 Quality Assurance

- **Type Safety**: Full TypeScript checking with Deno
- **Code Standards**: Automated linting and formatting validation
- **Integration Testing**: Comprehensive test coverage

### 🔍 Early Detection

- **Installation Issues**: Test actual installation process
- **Shell Compatibility**: Verify bash and zsh configurations work
- **Rollback Functionality**: Ensure recovery mechanisms function

## Configuration

The workflow uses:
- **Deno v2.x** for TypeScript execution
- **Dependency caching** for faster builds
- **Cross-platform matrix** for comprehensive testing
- **Conditional bash testing** (skipped on Windows)

## Local Testing

Before pushing changes, you can run the same checks locally:

```bash
# Type checking and linting
deno task check
deno lint
deno fmt --check

# Integration tests
deno task test

# Bash enhancement tests (Unix-like systems only)
deno task test:bash

# Test GitHub Actions locally with act
deno task test:actions
deno task test:actions -d  # Dry run
deno task test:actions -l  # List jobs
```

## Workflow Status

You can view the status of the workflow in the [Actions tab](../../actions) of the repository.

### Status Badge

Add this to your main README.md to show workflow status:

```markdown
[![CI](https://github.com/YOUR_USERNAME/dotfiles/workflows/CI/badge.svg)](https://github.com/YOUR_USERNAME/dotfiles/actions/workflows/ci.yml)
```

## Troubleshooting

### Common Issues

1. **Deno Version Mismatch**: Workflow uses `v2.x` - ensure compatibility
2. **Permission Issues**: Scripts require `--allow-all` permissions
3. **Platform Differences**: Some features may not work on all platforms
4. **Shell Availability**: bash tests are skipped on Windows

### Debugging Workflows

- Check the [Actions tab](../../actions) for detailed logs
- Look for specific job failures in the workflow runs
- Use `workflow_dispatch` to manually trigger workflows for testing
- Use the local testing script with `deno task test:actions` for debugging

## Security Considerations

- **Permissions**: Workflows use minimal required permissions
- **Isolation**: Each test runs in a clean, isolated environment
- **Dependency Caching**: Secure caching of Deno dependencies

This streamlined CI setup ensures your dotfiles remain reliable and functional across all supported platforms and configurations while maintaining simplicity and fast feedback cycles.
