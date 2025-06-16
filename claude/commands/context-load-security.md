# /context-load-security

Load comprehensive documentation context for Kubernetes security and secrets management.

## Instructions for Claude

When this command is executed, you MUST:

1. **Use the Context7 MCP server** (if available) to fetch and load context from the URLs below
2. **Use WebFetch tool** to gather information from these key sources:
   - **External Secrets Operator**: `https://external-secrets.io/latest/`
     - Focus on: provider integration, secret stores, automation
   - **1Password Kubernetes Integration**: `https://developer.1password.com/docs/k8s/operator/`
     - Focus on: operator setup, secret injection, best practices
   - **Kubernetes Security**: `https://kubernetes.io/docs/concepts/security/`
     - Focus on: RBAC, network policies, pod security, admission controllers
   - **Security Best Practices**: `https://kubernetes.io/docs/concepts/security/security-checklist/`
     - Focus on: cluster hardening, workload security, supply chain
   - **NIST Guidelines**: `https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-190.pdf`
     - Focus on: container security, vulnerability management

3. **Key documentation sections to prioritize**:
   - Secret management strategies
   - RBAC implementation
   - Network security policies
   - Pod security standards
   - Supply chain security
   - Vulnerability scanning

4. **Focus areas for this stack**:
   - External secret integration
   - Zero-trust security model
   - Identity and access management
   - Network segmentation
   - Container security scanning
   - Compliance frameworks
   - Incident response
   - Security monitoring

## Expected Outcome

After loading this context, you should be able to provide expert guidance on:

- Implementing secure secret management
- Configuring RBAC policies
- Setting up network security
- Hardening Kubernetes clusters
- Integrating security scanning
- Designing zero-trust architectures
- Implementing compliance controls
- Responding to security incidents

## Usage Example

```
/context-load-security
```
