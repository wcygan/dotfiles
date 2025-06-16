# /context-load-java-temporal

Load comprehensive documentation context for Java Temporal workflow development.

## Instructions for Claude

When this command is executed, you MUST:

1. **Use the Context7 MCP server** (if available) to fetch and load context from the URLs below
2. **Use WebFetch tool** to gather information from these key sources:
   - **Temporal Documentation**: `https://docs.temporal.io/`
     - Focus on: core concepts, workflows, activities, workers
   - **Java SDK Guide**: `https://docs.temporal.io/dev-guide/java`
     - Focus on: workflow implementation, activity definition, testing
   - **Java Samples**: `https://github.com/temporalio/samples-java`
     - Focus on: practical examples, patterns, best practices
   - **Temporal Concepts**: `https://docs.temporal.io/concepts`
     - Focus on: workflow execution, task queues, signals, queries
   - **Testing Guide**: `https://docs.temporal.io/dev-guide/java/testing`
     - Focus on: unit testing, integration testing, time skipping

3. **Key documentation sections to prioritize**:
   - Workflow definition and execution
   - Activity implementation patterns
   - Signal and query handling
   - Worker configuration
   - Versioning strategies
   - Testing methodologies

4. **Focus areas for this stack**:
   - Durable workflow execution
   - Long-running business processes
   - Fault tolerance and retries
   - Workflow versioning
   - Activity timeouts and retries
   - Signal and query patterns
   - Testing with TestWorkflowEnvironment
   - Monitoring and observability

## Expected Outcome

After loading this context, you should be able to provide expert guidance on:

- Designing durable workflows
- Implementing activities properly
- Handling workflow signals and queries
- Testing workflow logic
- Versioning workflow definitions
- Error handling and retry policies
- Monitoring workflow execution
- Performance optimization

## Usage Example

```
/context-load-java-temporal
```
