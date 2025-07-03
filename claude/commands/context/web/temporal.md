# /context-load-temporal

Load comprehensive documentation context for Temporal workflow orchestration platform.

## Instructions for Claude

When this command is executed, you MUST:

1. **Use the Context7 MCP server** (if available) to fetch and load context from the URLs below
2. **Use WebFetch tool** to gather information from these key sources:
   - **Temporal Documentation**: `https://docs.temporal.io/`
     - Focus on: core concepts, architecture, deployment
   - **Core Concepts**: `https://docs.temporal.io/concepts`
     - Focus on: workflows, activities, workers, task queues
   - **Development Guides**: `https://docs.temporal.io/dev-guide`
     - Focus on: language-specific implementations, best practices
   - **Best Practices**: `https://docs.temporal.io/dev-guide/worker-performance`
     - Focus on: performance, reliability, testing

3. **Key documentation sections to prioritize**:
   - Workflow execution model
   - Activity implementation patterns
   - Signal and query handling
   - Worker configuration
   - Versioning strategies
   - Testing methodologies

4. **Focus areas for this stack**:
   - Durable execution guarantees
   - Long-running business processes
   - Fault tolerance and recovery
   - Workflow versioning
   - Activity retries and timeouts
   - Event-driven architectures
   - Monitoring and observability
   - Multi-language support

## Expected Outcome

After loading this context, you should be able to provide expert guidance on:

- Designing resilient workflows
- Implementing activity patterns
- Handling workflow state management
- Testing distributed workflows
- Versioning workflow definitions
- Monitoring workflow execution
- Performance optimization
- Error handling strategies

## Usage Example

```
/context-load-temporal
```
