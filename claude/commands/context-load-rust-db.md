# /context-load-rust-db

Load comprehensive documentation context for Rust database access patterns and ORMs.

## Instructions for Claude

When this command is executed, you MUST:

1. **Use the Context7 MCP server** (if available) to fetch and load context from the URLs below
2. **Use WebFetch tool** to gather information from these key sources:
   - **SQLx**: `https://docs.rs/sqlx/latest/sqlx/`
     - Focus on: compile-time checked queries, connection pools, migrations, transactions
   - **Diesel**: `https://docs.rs/diesel/latest/diesel/`
     - Focus on: schema definition, query builder, associations, migrations
   - **SeaORM**: `https://docs.rs/sea-orm/latest/sea_orm/`
     - Focus on: entity definition, active record pattern, relations, migrations
   - **SQLx Guide**: `https://github.com/launchbadge/sqlx/blob/main/README.md`
     - Focus on: getting started, best practices, examples

3. **Key documentation sections to prioritize**:
   - Database connection management
   - Query building and execution
   - Type safety and compile-time checking
   - Transaction handling
   - Migration systems
   - Performance considerations

4. **Focus areas for this stack**:
   - Connection pooling strategies
   - Compile-time SQL verification
   - Async database operations
   - Transaction management
   - Migration workflows
   - Error handling patterns
   - Type mapping between Rust and SQL
   - Testing database code

## Expected Outcome

After loading this context, you should be able to provide expert guidance on:

- Setting up database connections
- Writing type-safe database queries
- Managing database schemas and migrations
- Handling transactions properly
- Optimizing database performance
- Testing database interactions
- Choosing between different ORM approaches
- Error handling for database operations

## Usage Example

```
/context-load-rust-db
```
