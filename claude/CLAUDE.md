Guidlines:

Your preferences are described below as `{ <Theme> } <Preference>`. This format allows you to understand what themes our preferences are related to.

- { Workflow } Follow best practices for the frameworks and languages you use.
  - { Testing } Write clear, descriptive test names for better readability.
  - { Testing } Prefer running single tests, and not the whole test suite, for performance
- { Backend Programming } Prefer Java, Go, and Rust as languages for building servers. Use the best tool for the job.
  - { Go } When using Go, prefer [ConnectRPC](https://github.com/connectrpc/connect-go)
  - { Rust } When using Rust, prefer [axum](https://github.com/tokio-rs/axum)
  - { Java } When using Java, prefer [Spring Boot](https://spring.io/projects/spring-boot) with [Quarkus](https://quarkus.io/)
- { Data Infrastructure} Use modern choices for data infrastructure. I run a Talos Linux Kuberneter Cluster.
  - Prefer Postgres over MySQL
  - Prefer DragonflyDB over Redis
  - Prefer RedPanda over Kafka
  - Prefer ScyllaDB over Cassandra
- { Scripting } Prefer using [Deno](https://github.com/denoland/deno/) for scripting over Bash and Python. Frequently Leverage Deno Scripting for automation and task management.
  - { Deno } In the project's root, create a `deno.json` file. It should contain tasks for common operations for the project
  - { Deno } Prefer JSR imports like `import { walk } from "@std/fs";` instead of `import { walk } from "https://deno.land/std@0.224.0/fs/walk.ts";`. In `deno.json`, this will appear as a JSR Import like `"@std/fs": "jsr:@std/fs@^1.0.17",`.
  - { Deno } Use [Dax](https://github.com/dsherret/dax) to provide Cross-platform shell tools for Deno
- { Web Framework } Prefer [Deno Fresh](https://fresh.deno.dev/) for web development
  - { Deno Fresh} Use Deno’s built-in test runner (Deno.test) for unit tests (either in Deno Scripts or in Deno Fresh).
  - { Deno Fresh}  Organize tests by type: unit, component, and E2E.
  - { Deno Fresh}  Mock external dependencies to keep tests fast and reliable.
  - { Deno Fresh}  Use fresh-testing-library for component and handler testing.

