# /context-load-flux

Load comprehensive documentation context for Flux GitOps continuous delivery.

## Instructions for Claude

When this command is executed, you MUST:

1. **Use the Context7 MCP server** (if available) to fetch and load context from the URLs below
2. **Use WebFetch tool** to gather information from these key sources:
   - **Flux Documentation**: `https://fluxcd.io/flux/`
     - Focus on: installation, concepts, getting started
   - **GitOps Toolkit**: `https://fluxcd.io/flux/components/`
     - Focus on: source controller, kustomize controller, helm controller
   - **Guides and Tutorials**: `https://fluxcd.io/flux/guides/`
     - Focus on: repository structure, security, monitoring
   - **API Reference**: `https://fluxcd.io/flux/components/source/`
     - Focus on: custom resources, field descriptions
   - **Best Practices**: `https://fluxcd.io/flux/guides/repository-structure/`
     - Focus on: repository organization, security, automation

3. **Key documentation sections to prioritize**:
   - GitOps principles and workflows
   - Source controller configuration
   - Kustomization and Helm releases
   - Multi-tenancy patterns
   - Security and access control
   - Monitoring and alerting

4. **Focus areas for this stack**:
   - Git repository management
   - Continuous delivery pipelines
   - Application deployment automation
   - Configuration drift detection
   - Secret management
   - Multi-cluster deployments
   - Monitoring and notifications
   - Disaster recovery

## Expected Outcome

After loading this context, you should be able to provide expert guidance on:

- Implementing GitOps workflows
- Configuring Flux controllers
- Managing application deployments
- Setting up multi-tenancy
- Implementing security best practices
- Monitoring deployment pipelines
- Troubleshooting Flux issues
- Designing repository structures

## Usage Example

```
/context-load-flux
```
