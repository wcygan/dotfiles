Create a new Rust CLI program named $ARGUMENTS with modern best practices and essential dependencies.

Set up a Rust CLI project with the following:

1. **Project Structure**:
   - Create a new Cargo project with the given name
   - Set up a proper directory structure with `src/cli.rs`, `src/commands/mod.rs`, and tests

2. **Dependencies to add**:
   - `clap` (v4+) with derive feature for argument parsing
   - `env_logger` for logging configuration from environment
   - `anyhow` for ergonomic error handling
   - `colored` for terminal output styling
   - `dialoguer` for interactive prompts
   - `indicatif` for progress bars and spinners
   - `ctrlc` for graceful shutdown handling
   - `signal-hook` for Unix signal handling
   - Dev dependencies: `assert_cmd` for integration testing
   - `atty` for terminal detection
   - `human-panic` for user-friendly panic messages

3. **CLI Structure** using modern Clap patterns:
   - Use derive macros with `#[derive(Parser)]`
   - Set up a main `Args` struct with author, version, and about metadata
   - Create an enum for subcommands using `#[derive(Subcommand)]`
   - Include at least 2 example subcommands with different argument patterns
   - Add global flags for verbosity and config file path

4. **Error Handling**:
   - Use `anyhow::Result<()>` as main return type
   - Implement context-aware error messages using `.context()`
   - Set up human-panic for production builds

5. **Logging Setup**:
   - Initialize env_logger in main()
   - Support RUST_LOG environment variable
   - Add -v/-vv/-vvv flags for verbosity levels

6. **Signal Handling**:
   - Implement graceful shutdown with ctrlc
   - Clean up resources on SIGTERM/SIGINT

7. **Testing Structure**:
   - Create unit tests for core logic
   - Set up integration tests using assert_cmd
   - Include example test for CLI invocation

8. **Documentation**:
   - Add comprehensive README.md with usage examples
   - Document all public functions and modules
   - Include examples of common CLI patterns

9. **Additional Features**:
   - Progress indicator example using indicatif
   - Interactive prompt example using dialoguer
   - Colored output example
   - Configuration file support skeleton

Make the CLI extensible and follow Rust idioms. Use small, focused functions and leverage the type system for robustness.
