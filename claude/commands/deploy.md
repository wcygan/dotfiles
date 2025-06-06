# /deploy

Automates Kubernetes deployment of containerized applications.

## Usage
```
/deploy <service> --to <environment>
```

## Description
This command automates the entire deployment process for containerized applications to your Kubernetes cluster. It acts as the crucial next step after `/containerize`, bridging the gap between code and a running application.

### What it does:
1. **Environment Analysis**: Locates `k8s/`, `infra/`, or `deploy/` directories and identifies existing deployment patterns (Kustomize, Helm)
2. **Manifest Generation/Update**: Creates or updates Kubernetes manifests (Deployment, Service, Ingress, HPA)
3. **Image Tag Management**: Updates image tags to latest version (from `git rev-parse --short HEAD`)
4. **Secret Handling**: Creates templates for Kubernetes secrets with secure population commands
5. **CI/CD Integration**: Generates GitHub Actions workflow steps for continuous deployment

### Supported Patterns:
- **Kustomize**: Uses `kustomization.yaml` files with environment overlays
- **Helm**: Detects `Chart.yaml` and uses Helm templating
- **Raw Manifests**: Creates standard Kubernetes YAML files

### Directory Structure Created:
```
k8s/
├── base/
│   ├── deployment.yaml
│   ├── service.yaml
│   └── kustomization.yaml
├── overlays/
│   ├── staging/
│   │   ├── kustomization.yaml
│   │   └── env-patch.yaml
│   └── production/
│       ├── kustomization.yaml
│       └── env-patch.yaml
└── secrets/
    └── secret-template.yaml
```

### Generated Deployment Features:
- **Health Checks**: Readiness and liveness probes
- **Resource Management**: CPU/memory requests and limits
- **Security**: Non-root user, read-only filesystem, dropped capabilities
- **Observability**: Prometheus metrics annotations
- **Scaling**: Horizontal Pod Autoscaler configuration

### Secret Management:
Creates secure secret templates with commands like:
```bash
kubectl create secret generic app-secrets \
  --from-literal=DATABASE_URL='postgres://...' \
  --from-literal=API_KEY='your-api-key' \
  --dry-run=client -o yaml | kubectl apply -f -
```

### CI/CD Integration:
Generates `.github/workflows/cd.yml` with:
- Automated builds on push to main
- Image building and pushing to registry
- Deployment to staging/production environments
- Rollback capabilities

## Examples

### Deploy to staging:
```
/deploy auth-service --to staging
```

### Deploy with custom image tag:
```
/deploy api-gateway --to production --tag v1.2.3
```

### Deploy with Helm:
```
/deploy web-app --to staging --helm
```

## Prerequisites
- Docker images available in registry
- kubectl configured for target cluster
- Appropriate RBAC permissions for deployment

## Environment Configuration
Supports these standard environments:
- `staging`: Lower resource limits, debug logging
- `production`: Production-ready configuration, monitoring enabled
- `development`: Local cluster, minimal resources

## Integration with Other Commands
- Use after `/containerize` to deploy the containerized application
- Combine with `/observe` for production monitoring
- Use with `/harden` for security-enhanced deployments