# /context-load-postgres

Load comprehensive documentation context for PostgreSQL database development.

## Instructions for Claude

When this command is executed, you MUST:

1. **Use the Context7 MCP server** (if available) to fetch and load context from the URLs below
2. **Use WebFetch tool** to gather information from these key sources:
   - **PostgreSQL Documentation**: `https://www.postgresql.org/docs/current/`
     - Focus on: SQL reference, administration, performance tuning
   - **PostgreSQL Tutorial**: `https://www.postgresql.org/docs/current/tutorial.html`
     - Focus on: getting started, basic concepts, advanced features
   - **Performance Optimization**: `https://wiki.postgresql.org/wiki/Performance_Optimization`
     - Focus on: indexing, query optimization, configuration tuning
   - **PostgreSQL Extensions**: `https://www.postgresql.org/docs/current/external-extensions.html`
     - Focus on: popular extensions, PostGIS, full-text search
   - **Best Practices**: `https://wiki.postgresql.org/wiki/Don%27t_Do_This`
     - Focus on: common pitfalls, anti-patterns, recommendations

3. **Key documentation sections to prioritize**:
   - Advanced SQL features
   - Indexing strategies
   - Query optimization
   - Transaction management
   - Backup and recovery
   - Monitoring and maintenance

4. **Focus areas for this stack**:
   - Complex query design
   - Index optimization
   - Partitioning strategies
   - Replication setup
   - Extension usage
   - Performance monitoring
   - Security configuration
   - Migration strategies

## Expected Outcome

After loading this context, you should be able to provide expert guidance on:

- Writing efficient PostgreSQL queries
- Designing optimal database schemas
- Implementing indexing strategies
- Performance tuning and optimization
- Setting up replication
- Using PostgreSQL extensions
- Database security best practices
- Backup and recovery procedures

## Usage Example

```
/context-load-postgres
```
