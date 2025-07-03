<!--
name: infra:status
purpose: Check Talos Kubernetes cluster and infrastructure health status
tags: infrastructure, kubernetes, monitoring, health-check
-->

Check the health status of Talos Linux Kubernetes cluster and modern infrastructure components. Provides comprehensive overview of cluster nodes, workloads, and preferred infrastructure services.

**Context**: $ARGUMENTS (optional - specific component to check: nodes, pods, services, storage, network, or all)

## Health Check Process

1. **Cluster Status**
   - Node readiness and resource utilization
   - Control plane health and etcd status
   - Network connectivity and CNI status

2. **Infrastructure Services**
   - **Postgres**: Database connectivity and replication status
   - **DragonflyDB**: Cache performance and memory usage
   - **RedPanda**: Streaming service health and partition status
   - **ScyllaDB**: NoSQL cluster status and consistency

3. **System Resources**
   - CPU, memory, and storage utilization across nodes
   - Network bandwidth and latency metrics
   - Pod resource consumption and limits

## Commands Executed

```bash
# Cluster overview with JSON output for parsing
kubectl get nodes -o json | jq '.items[] | {name: .metadata.name, status: .status.conditions[-1].type, ready: (.status.conditions[] | select(.type=="Ready").status)}'

# Resource utilization
kubectl top nodes --use-protocol-buffers=false
kubectl top pods --all-namespaces --use-protocol-buffers=false

# Infrastructure service checks
kubectl get pods -n postgres-system -o json | jq '.items[] | {name: .metadata.name, status: .status.phase, ready: (.status.conditions[] | select(.type=="Ready").status)}'
kubectl get pods -n dragonfly-system -o json | jq '.items[] | {name: .metadata.name, status: .status.phase, ready: (.status.conditions[] | select(.type=="Ready").status)}'
kubectl get pods -n redpanda-system -o json | jq '.items[] | {name: .metadata.name, status: .status.phase, ready: (.status.conditions[] | select(.type=="Ready").status)}'
kubectl get pods -n scylla-system -o json | jq '.items[] | {name: .metadata.name, status: .status.phase, ready: (.status.conditions[] | select(.type=="Ready").status)}'

# Storage and networking
kubectl get pv -o json | jq '.items[] | {name: .metadata.name, status: .status.phase, capacity: .spec.capacity.storage}'
kubectl get svc -A -o json | jq '.items[] | select(.spec.type=="LoadBalancer") | {name: .metadata.name, namespace: .metadata.namespace, external_ip: .status.loadBalancer.ingress[0].ip}'
```

## Output Format

Returns structured JSON with:

- Cluster health summary (nodes, pods, services)
- Infrastructure service status
- Resource utilization warnings
- Recommended actions for issues found

## Example Usage

```bash
# Full infrastructure health check
/infra:status

# Check specific component
/infra:status nodes
/infra:status postgres

# Check all infrastructure services
/infra:status services
```
