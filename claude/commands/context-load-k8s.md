# /context-load-k8s

Load comprehensive documentation context for Kubernetes container orchestration.

## Instructions for Claude

When this command is executed, you MUST:

1. **Use the Context7 MCP server** (if available) to fetch and load context from the URLs below
2. **Use WebFetch tool** to gather information from these key sources:
   - **Kubernetes Documentation**: `https://kubernetes.io/docs/`
     - Focus on: concepts, tutorials, reference documentation
   - **API Reference**: `https://kubernetes.io/docs/reference/kubernetes-api/`
     - Focus on: resource definitions, field descriptions
   - **Best Practices**: `https://kubernetes.io/docs/concepts/configuration/overview/`
     - Focus on: configuration management, security, networking
   - **Kubectl Reference**: `https://kubernetes.io/docs/reference/kubectl/`
     - Focus on: command usage, examples, cheat sheet
   - **Troubleshooting Guide**: `https://kubernetes.io/docs/tasks/debug/`
     - Focus on: debugging, monitoring, common issues

3. **Key documentation sections to prioritize**:
   - Core concepts (Pods, Services, Deployments)
   - Configuration management
   - Networking and ingress
   - Storage and volumes
   - Security and RBAC
   - Monitoring and logging

4. **Focus areas for this stack**:
   - Workload management
   - Service discovery and networking
   - Configuration and secrets
   - Storage orchestration
   - Security policies
   - Resource management
   - Monitoring and observability
   - Cluster administration

## Expected Outcome

After loading this context, you should be able to provide expert guidance on:

- Deploying applications to Kubernetes
- Managing Kubernetes resources
- Implementing networking solutions
- Configuring security policies
- Troubleshooting cluster issues
- Optimizing resource usage
- Setting up monitoring
- Managing cluster upgrades

## Usage Example

```
/context-load-k8s
```
