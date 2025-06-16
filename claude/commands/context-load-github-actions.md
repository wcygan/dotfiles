# /context-load-github-actions

Load comprehensive documentation context for GitHub Actions CI/CD workflows.

## Instructions for Claude

When this command is executed, you MUST:

1. **Use the Context7 MCP server** (if available) to fetch and load context from the URLs below
2. **Use WebFetch tool** to gather information from these key sources:
   - **GitHub Actions Documentation**: `https://docs.github.com/en/actions`
     - Focus on: workflow syntax, events, jobs, steps
   - **Workflow Syntax**: `https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions`
     - Focus on: YAML syntax, expressions, contexts
   - **Actions Marketplace**: `https://github.com/marketplace?type=actions`
     - Focus on: popular actions, usage patterns, best practices
   - **Security Guide**: `https://docs.github.com/en/actions/security-guides`
     - Focus on: secrets management, permissions, security hardening
   - **Advanced Features**: `https://docs.github.com/en/actions/using-workflows/reusing-workflows`
     - Focus on: reusable workflows, matrix builds, caching

3. **Key documentation sections to prioritize**:
   - Workflow triggers and events
   - Job configuration and strategy
   - Actions and marketplace usage
   - Secrets and environment management
   - Caching and optimization
   - Security best practices

4. **Focus areas for this stack**:
   - CI/CD pipeline design
   - Multi-environment deployments
   - Matrix build strategies
   - Dependency caching
   - Secret management
   - Security scanning integration
   - Performance optimization
   - Workflow reusability

## Expected Outcome

After loading this context, you should be able to provide expert guidance on:

- Designing efficient CI/CD pipelines
- Implementing matrix build strategies
- Optimizing workflow performance
- Managing secrets securely
- Integrating security scanning
- Creating reusable workflows
- Troubleshooting workflow issues
- Implementing deployment strategies

## Usage Example

```
/context-load-github-actions
```
