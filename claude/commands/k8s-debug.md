# /k8s-debug

Systematically diagnose and troubleshoot Kubernetes issues with intelligent pod, service, and cluster-level debugging workflows.

## Usage

```
/k8s-debug [pod-name]
/k8s-debug [service-name]
/k8s-debug [deployment-name]
/k8s-debug
```

## Context Detection

**When no argument provided:**

- Lists failing pods across all namespaces
- Shows recent events and warnings
- Provides interactive selection for detailed investigation

**When argument provided:**

- Auto-detects resource type (pod, service, deployment, etc.)
- Focuses debugging on specified resource
- Includes related resources in analysis

## Diagnostic Workflow

### Phase 1: Quick Health Assessment

**Cluster Overview**

- Node status and resource availability
- Critical system pod health (kube-system namespace)
- Recent cluster events and warnings
- Resource quotas and limits

**Namespace Analysis**

- Pod status summary across namespaces
- Service connectivity overview
- ConfigMap and Secret integrity
- Recent deployment activity

### Phase 2: Resource-Specific Investigation

**Pod Debugging**

```bash
# Pod status and events
kubectl describe pod [pod-name] -n [namespace]
kubectl get events --field-selector involvedObject.name=[pod-name]

# Container logs and status
kubectl logs [pod-name] --previous --tail=100
kubectl logs [pod-name] -c [container] --follow

# Resource usage and limits
kubectl top pod [pod-name] -n [namespace]
kubectl get pod [pod-name] -o yaml | grep -A 10 resources
```

**Service Debugging**

```bash
# Service endpoints and connectivity
kubectl describe service [service-name] -n [namespace]
kubectl get endpoints [service-name] -n [namespace]

# Network policy analysis
kubectl get networkpolicies -n [namespace]
kubectl describe networkpolicy -n [namespace]

# Ingress and load balancer status
kubectl get ingress -n [namespace]
kubectl describe ingress [ingress-name] -n [namespace]
```

**Deployment Analysis**

```bash
# Deployment status and history
kubectl describe deployment [deployment-name] -n [namespace]
kubectl rollout status deployment/[deployment-name] -n [namespace]
kubectl rollout history deployment/[deployment-name] -n [namespace]

# ReplicaSet investigation
kubectl get rs -n [namespace] --selector=app=[app-label]
kubectl describe rs [replicaset-name] -n [namespace]
```

### Phase 3: Deep Diagnostic Analysis

**Container Runtime Issues**

1. **Image Pull Problems**
   - Verify image exists and is accessible
   - Check imagePullSecrets configuration
   - Validate registry authentication
   - Review image pull policy settings

2. **Resource Constraints**
   - CPU and memory limit analysis
   - Node resource availability
   - Quality of Service (QoS) class impact
   - Pod eviction scenarios

3. **Configuration Errors**
   - Environment variable validation
   - ConfigMap and Secret mounting
   - Volume mount permissions
   - Security context conflicts

**Network Connectivity Issues**

1. **DNS Resolution**
   ```bash
   # Test DNS from within cluster
   kubectl run debug-pod --image=busybox --rm -it -- nslookup [service-name]
   kubectl exec -it [pod-name] -- nslookup kubernetes.default
   ```

2. **Service Discovery**
   - Service selector label matching
   - Endpoint availability and health
   - Port configuration verification
   - Load balancer status

3. **Network Policies**
   - Ingress and egress rule analysis
   - Pod-to-pod communication testing
   - External connectivity validation

**Storage and Persistence**

1. **Volume Mount Issues**
   - PersistentVolume and PersistentVolumeClaim status
   - Storage class configuration
   - Mount path permissions and ownership
   - Disk space and inode availability

2. **ConfigMap and Secret Problems**
   - Key existence and format validation
   - Mount path conflicts
   - Update propagation delays
   - Base64 encoding issues

### Phase 4: Performance Analysis

**Resource Utilization**

```bash
# Current resource usage
kubectl top pods -n [namespace] --sort-by=cpu
kubectl top pods -n [namespace] --sort-by=memory

# Node resource availability
kubectl top nodes
kubectl describe nodes | grep -A 5 "Allocated resources"
```

**Application Metrics**

1. **Pod Performance**
   - CPU throttling detection
   - Memory pressure indicators
   - Container restart patterns
   - Readiness and liveness probe failures

2. **Cluster Performance**
   - Node resource contention
   - Scheduler performance
   - etcd health and latency
   - API server response times

### Phase 5: Actionable Recommendations

**Immediate Actions**

- Critical issues requiring immediate attention
- Resource constraint resolutions
- Configuration fixes with specific commands
- Network connectivity repairs

**Short-term Improvements**

- Resource limit optimization
- Health check configuration
- Monitoring and alerting setup
- Documentation of debugging steps

**Long-term Optimizations**

- Cluster architecture improvements
- Automation of common debugging tasks
- Preventive monitoring implementation
- Disaster recovery procedures

## Common Debugging Scenarios

### CrashLoopBackOff

1. **Check container logs**:
   ```bash
   kubectl logs [pod-name] --previous
   ```

2. **Verify resource limits**:
   ```bash
   kubectl describe pod [pod-name] | grep -A 10 Limits
   ```

3. **Test container locally**:
   ```bash
   docker run --rm -it [image] [command]
   ```

### ImagePullBackOff

1. **Verify image exists**:
   ```bash
   docker pull [image-name]
   ```

2. **Check registry authentication**:
   ```bash
   kubectl get secrets -n [namespace] | grep docker
   kubectl describe secret [secret-name] -n [namespace]
   ```

### Pending Pods

1. **Check node resources**:
   ```bash
   kubectl describe nodes | grep -A 10 "Non-terminated Pods"
   ```

2. **Verify node selectors and affinity**:
   ```bash
   kubectl describe pod [pod-name] | grep -A 5 "Node-Selectors"
   ```

### Service Not Accessible

1. **Check service endpoints**:
   ```bash
   kubectl get endpoints [service-name] -n [namespace]
   ```

2. **Test service connectivity**:
   ```bash
   kubectl run debug --image=busybox --rm -it -- wget -qO- [service-name]:[port]
   ```

## Integration with Existing Commands

- Use `/monitor` for ongoing cluster health tracking
- Follow with `/health-check` for systematic validation
- Apply `/harden` for security improvements discovered
- Use `/document` to record debugging procedures

## Output Format

**Summary Dashboard**

- Health status overview with color coding
- Critical issues requiring immediate attention
- Resource utilization highlights
- Connectivity status summary

**Detailed Analysis**

- Step-by-step diagnostic results
- Specific kubectl commands used
- Configuration recommendations
- Performance optimization suggestions

**Action Plan**

- Prioritized list of issues to address
- Specific commands to run for fixes
- Monitoring recommendations
- Follow-up investigation areas

The debugging process adapts based on detected issues, focusing efforts on the most likely root causes while providing comprehensive coverage of potential problems.
