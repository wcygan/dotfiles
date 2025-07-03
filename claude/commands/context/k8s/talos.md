# /context-load-talos

Load comprehensive documentation context for Talos Linux Kubernetes OS.

## Instructions for Claude

When this command is executed, you MUST:

1. **Use the Context7 MCP server** (if available) to fetch and load context from the URLs below
2. **Use WebFetch tool** to gather information from these key sources:
   - **Talos Documentation**: `https://www.talos.dev/latest/`
     - Focus on: installation, configuration, cluster management
   - **Machine Configuration**: `https://www.talos.dev/latest/reference/configuration/`
     - Focus on: config schema, networking, storage, security
   - **API Reference**: `https://www.talos.dev/latest/reference/api/`
     - Focus on: machine API, cluster API, service management
   - **Guides and Tutorials**: `https://www.talos.dev/latest/talos-guides/`
     - Focus on: deployment scenarios, troubleshooting
   - **Upgrade Guide**: `https://www.talos.dev/latest/talos-guides/upgrading-talos/`
     - Focus on: upgrade procedures, rollback strategies

3. **Key documentation sections to prioritize**:
   - Machine configuration schema
   - Cluster bootstrap process
   - Networking configuration
   - Storage management
   - Security and certificates
   - Upgrade procedures

4. **Focus areas for this stack**:
   - Immutable infrastructure
   - Secure by default configuration
   - API-driven management
   - Cluster lifecycle management
   - Network policy enforcement
   - Certificate management
   - Troubleshooting and debugging
   - Integration with GitOps

## Expected Outcome

After loading this context, you should be able to provide expert guidance on:

- Configuring Talos machines
- Bootstrapping Kubernetes clusters
- Managing cluster networking
- Implementing security policies
- Performing cluster upgrades
- Troubleshooting Talos issues
- Integrating with automation tools
- Optimizing cluster performance

## Usage Example

```
/context-load-talos
```
