# /context-load-java-spring

Load comprehensive documentation context for Java Spring Framework development.

## Instructions for Claude

When this command is executed, you MUST:

1. **Use the Context7 MCP server** (if available) to fetch and load context from the URLs below
2. **Use WebFetch tool** to gather information from these key sources:
   - **Spring Boot**: `https://spring.io/projects/spring-boot`
     - Focus on: auto-configuration, starters, actuator, testing
   - **Spring Framework Reference**: `https://docs.spring.io/spring-framework/reference/`
     - Focus on: dependency injection, AOP, transaction management
   - **Spring Security**: `https://spring.io/projects/spring-security`
     - Focus on: authentication, authorization, OAuth2, JWT
   - **Spring Data**: `https://spring.io/projects/spring-data`
     - Focus on: JPA, repositories, query methods, transactions
   - **Spring Guides**: `https://spring.io/guides`
     - Focus on: getting started guides, tutorials, best practices

3. **Key documentation sections to prioritize**:
   - Dependency injection and IoC container
   - Auto-configuration mechanisms
   - Web MVC framework
   - Data access and JPA integration
   - Security configuration
   - Testing strategies

4. **Focus areas for this stack**:
   - Spring Boot application setup
   - RESTful web services
   - Database integration with JPA
   - Security implementation
   - Configuration management
   - Aspect-oriented programming
   - Testing with Spring Boot
   - Actuator for monitoring

## Expected Outcome

After loading this context, you should be able to provide expert guidance on:

- Building Spring Boot applications
- Implementing REST APIs
- Database access with Spring Data JPA
- Security configuration and implementation
- Dependency injection patterns
- Testing Spring applications
- Configuration and profiles
- Monitoring and actuator endpoints

## Usage Example

```
/context-load-java-spring
```
