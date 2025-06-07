# Dotfiles CI Documentation

## Overview

The dotfiles project uses GitHub Actions for continuous integration to ensure code quality and functionality across different platforms.

## CI Workflow

The CI runs on:

- **Push events** to `main` and `develop` branches
- **Pull requests** targeting `main` branch
- **Manual triggers** via workflow dispatch

## Test Matrix

Tests run on multiple operating systems:

- `ubuntu-latest`
- `macos-latest`

## CI Steps

### 1. Setup

- Checkout code
- Install Deno v2.x
- Cache Deno dependencies

### 2. Code Quality Checks

- **Type Check**: `deno task check` - Validates TypeScript types
- **Lint**: `deno lint` - Enforces code style rules
- **Format**: `deno fmt --check` - Ensures consistent code formatting

### 3. Testing

- **Integration Tests**: `deno task test` - Runs full installation/rollback tests
- **Installation Test**: Verifies the install script help works

### 4. Verification

- Checks that all scripts in `scripts/` directory maintain proper permissions

## Running CI Locally

Test the CI workflow locally using Act:

```bash
# Run all CI tests locally
deno task test:actions
```

This uses [Act](https://github.com/nektos/act) to simulate GitHub Actions environment locally.

## Key Commands

```bash
# Run type checking
deno task check

# Run linter
deno lint

# Check formatting
deno fmt --check

# Run tests
deno task test

# Run CI locally
deno task test:actions
```

## Troubleshooting

- **Format failures**: Run `deno fmt` to auto-fix formatting
- **Type check failures**: Check for TypeScript errors in modified files
- **Test failures**: Review test output for specific error messages

The CI ensures all code changes maintain quality standards before merging.
