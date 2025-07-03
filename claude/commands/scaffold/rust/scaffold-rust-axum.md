# /scaffold-rust-axum

Creates a new Rust web server project for $ARGUMENT using Axum framework with modern async/await patterns and essential endpoints.

## What it does

1. Creates a new directory with the specified project name
2. Initializes a Cargo.toml with latest version of Axum and Tokio dependencies
3. Sets up a basic main.rs with health check and root endpoints
4. Adds appropriate .gitignore for Rust projects
5. Runs `cargo build` to verify the setup

## Example

```
/scaffold-rust-axum my-api-server
```

This creates a production-ready Axum web server with:

- Async/await request handlers
- Health check endpoint at `/health`
- Root endpoint at `/`
- Listening on 127.0.0.1:3000
- All dependencies properly configured
