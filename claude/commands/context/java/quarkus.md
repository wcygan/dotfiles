# /context-load-java-quarkus

Load comprehensive documentation context for Java Quarkus framework development.

## Instructions for Claude

When this command is executed, you MUST:

1. **Use the Context7 MCP server** (if available) to fetch and load context from the URLs below
2. **Use WebFetch tool** to gather information from these key sources:
   - **Quarkus Guides**: `https://quarkus.io/guides/`
     - Focus on: getting started, native compilation, reactive programming
   - **GraalVM Documentation**: `https://www.graalvm.org/latest/docs/`
     - Focus on: native image, compilation, optimization
   - **MicroProfile Specifications**: `https://microprofile.io/`
     - Focus on: health checks, metrics, fault tolerance, JWT
   - **Quarkus Reference**: `https://quarkus.io/guides/getting-started`
     - Focus on: dependency injection, configuration, extensions
   - **Reactive Programming**: `https://quarkus.io/guides/getting-started-reactive`
     - Focus on: reactive streams, Mutiny, non-blocking I/O

3. **Key documentation sections to prioritize**:
   - Native compilation with GraalVM
   - Reactive programming patterns
   - Dependency injection with CDI
   - Configuration and profiles
   - Health checks and metrics
   - Testing strategies

4. **Focus areas for this stack**:
   - Supersonic startup times
   - Low memory footprint applications
   - Native image compilation
   - Reactive programming with Mutiny
   - MicroProfile compliance
   - Cloud-native development
   - Testing with Quarkus
   - Extension development

## Expected Outcome

After loading this context, you should be able to provide expert guidance on:

- Building cloud-native Java applications
- Native compilation strategies
- Reactive programming patterns
- MicroProfile implementations
- Performance optimization
- Testing Quarkus applications
- Extension usage and development
- Cloud deployment patterns

## Usage Example

```
/context-load-java-quarkus
```
