# /context-load-cilium

Load comprehensive documentation context for Cilium eBPF-based networking and security.

## Instructions for Claude

When this command is executed, you MUST:

1. **Use the Context7 MCP server** (if available) to fetch and load context from the URLs below
2. **Use WebFetch tool** to gather information from these key sources:
   - **Cilium Documentation**: `https://docs.cilium.io/`
     - Focus on: installation, concepts, configuration
   - **Network Policies**: `https://docs.cilium.io/en/stable/security/policy/`
     - Focus on: L3/L4 policies, L7 policies, DNS policies
   - **Service Mesh**: `https://docs.cilium.io/en/stable/network/servicemesh/`
     - Focus on: Envoy integration, traffic management, observability
   - **Observability**: `https://docs.cilium.io/en/stable/gettingstarted/hubble/`
     - Focus on: Hubble, metrics, tracing, monitoring
   - **Performance Guide**: `https://docs.cilium.io/en/stable/operations/performance/`
     - Focus on: tuning, benchmarking, optimization

3. **Key documentation sections to prioritize**:
   - eBPF networking concepts
   - Network policy implementation
   - Service mesh capabilities
   - Load balancing strategies
   - Security enforcement
   - Observability features

4. **Focus areas for this stack**:
   - CNI configuration and management
   - Network security policies
   - Service mesh integration
   - Load balancing and traffic management
   - Network observability
   - Performance optimization
   - Troubleshooting network issues
   - Integration with Kubernetes

## Expected Outcome

After loading this context, you should be able to provide expert guidance on:

- Configuring Cilium as CNI
- Implementing network security policies
- Setting up service mesh features
- Optimizing network performance
- Monitoring network traffic
- Troubleshooting connectivity issues
- Integrating with observability tools
- Designing secure network architectures

## Usage Example

```
/context-load-cilium
```
