---
allowed-tools: Bash(kubectl:*), Bash(fd:*), Bash(rg:*), Bash(jq:*), Bash(gdate:*), Bash(echo:*), Bash(which:*), Bash(eza:*), Bash(yq:*)
description: Comprehensive Kubernetes cluster state inspection with health checks, resource usage, and failure detection
---

## Context

- Session ID: !`gdate +%s%N 2>/dev/null || date +%s%N 2>/dev/null || echo "$(date +%s)$(jot -r 1 100000 999999 2>/dev/null || shuf -i 100000-999999 -n 1 2>/dev/null || echo $RANDOM$RANDOM)"`
- Check mode: $ARGUMENTS (optional - quick or detailed, default: quick)
- Cluster context: !`kubectl config current-context 2>/dev/null || echo "No active context"`
- Cluster reachable: !`kubectl cluster-info --request-timeout=5s >/dev/null 2>&1 && echo "✅ Connected" || echo "❌ Unreachable"`
- Kubernetes version: !`kubectl version --short 2>&1 | rg "Server Version" || echo "Unable to get version"`
- Node count: !`kubectl get nodes --no-headers 2>/dev/null | wc -l | tr -d ' ' || echo "0"`
- Namespace count: !`kubectl get namespaces --no-headers 2>/dev/null | wc -l | tr -d ' ' || echo "0"`

## Your Task

STEP 1: Initialize Kubernetes cluster health check session

- CREATE session state file: `/tmp/k8s-status-$SESSION_ID.json`
- VALIDATE kubectl connectivity
- DETERMINE check mode from $ARGUMENTS (quick vs detailed)
- GATHER initial cluster metadata

```bash
# Initialize session state
echo '{
  "sessionId": "'$SESSION_ID'",
  "timestamp": "'$(gdate -Iseconds 2>/dev/null || date -Iseconds)'",
  "checkMode": "'${ARGUMENTS:-quick}'",
  "clusterContext": "'$(kubectl config current-context 2>/dev/null || echo "none")'",
  "healthStatus": {
    "nodes": "pending",
    "pods": "pending",
    "deployments": "pending",
    "services": "pending",
    "storage": "pending",
    "network": "pending"
  },
  "issues": []
}' > /tmp/k8s-status-$SESSION_ID.json
```

STEP 2: Node health and resource status

TRY:

```bash
echo "🖥️  NODE STATUS"
echo "═══════════════"

# Node health check
node_total=$(kubectl get nodes --no-headers 2>/dev/null | wc -l || echo "0")
node_ready=$(kubectl get nodes --no-headers 2>/dev/null | rg -c "Ready" || echo "0")
node_not_ready=$(kubectl get nodes --no-headers 2>/dev/null | rg -c "NotReady" || echo "0")

if [ "$node_total" -eq 0 ]; then
    echo "❌ No nodes found or cluster unreachable"
    jq '.healthStatus.nodes = "fail"' /tmp/k8s-status-$SESSION_ID.json > /tmp/k8s-status-$SESSION_ID.tmp && mv /tmp/k8s-status-$SESSION_ID.tmp /tmp/k8s-status-$SESSION_ID.json
elif [ "$node_not_ready" -gt 0 ]; then
    echo "⚠️  $node_not_ready/$node_total nodes NotReady"
    jq '.healthStatus.nodes = "warn"' /tmp/k8s-status-$SESSION_ID.json > /tmp/k8s-status-$SESSION_ID.tmp && mv /tmp/k8s-status-$SESSION_ID.tmp /tmp/k8s-status-$SESSION_ID.json
    kubectl get nodes --no-headers | rg "NotReady" | head -3
else
    echo "✅ All $node_total nodes Ready"
    jq '.healthStatus.nodes = "pass"' /tmp/k8s-status-$SESSION_ID.json > /tmp/k8s-status-$SESSION_ID.tmp && mv /tmp/k8s-status-$SESSION_ID.tmp /tmp/k8s-status-$SESSION_ID.json
fi

# Resource utilization
if kubectl top nodes >/dev/null 2>&1; then
    echo ""
    echo "📊 Resource utilization (top 3 nodes):"
    kubectl top nodes --sort-by=cpu | head -4
else
    echo "ℹ️  Metrics server not available"
fi

# Node conditions
if [ "${ARGUMENTS:-quick}" = "detailed" ]; then
    echo ""
    echo "🔍 Node conditions:"
    kubectl get nodes -o json | jq -r '.items[] | "\(.metadata.name): \([.status.conditions[] | select(.status != "False") | .type] | join(", "))"' 2>/dev/null | head -5
fi
```

CATCH (node_check_failed):

```bash
echo "⚠️  Node check failed - verifying cluster access:"
kubectl auth can-i get nodes >/dev/null 2>&1 && echo "✅ Node access permitted" || echo "❌ No node access"
```

STEP 3: Pod health and failure analysis

```bash
echo ""
echo "🐳 POD STATUS"
echo "═══════════════"

# Overall pod health
pod_total=$(kubectl get pods -A --no-headers 2>/dev/null | wc -l || echo "0")
pod_running=$(kubectl get pods -A --field-selector=status.phase=Running --no-headers 2>/dev/null | wc -l || echo "0")
pod_failed=$(kubectl get pods -A --no-headers 2>/dev/null | rg -c -E "(Error|CrashLoopBackOff|ImagePullBackOff|ErrImagePull|Evicted)" || echo "0")

if [ "$pod_total" -eq 0 ]; then
    echo "❌ No pods found"
    jq '.healthStatus.pods = "fail"' /tmp/k8s-status-$SESSION_ID.json > /tmp/k8s-status-$SESSION_ID.tmp && mv /tmp/k8s-status-$SESSION_ID.tmp /tmp/k8s-status-$SESSION_ID.json
elif [ "$pod_failed" -gt 0 ]; then
    echo "❌ $pod_failed/$pod_total pods in failed state"
    jq '.healthStatus.pods = "fail"' /tmp/k8s-status-$SESSION_ID.json > /tmp/k8s-status-$SESSION_ID.tmp && mv /tmp/k8s-status-$SESSION_ID.tmp /tmp/k8s-status-$SESSION_ID.json
    
    echo ""
    echo "Failed pods:"
    kubectl get pods -A --no-headers | rg -E "(Error|CrashLoopBackOff|ImagePullBackOff|ErrImagePull|Evicted)" | head -5 | awk '{print "  " $1 "/" $2 " - " $4}'
else
    echo "✅ $pod_running/$pod_total pods Running"
    jq '.healthStatus.pods = "pass"' /tmp/k8s-status-$SESSION_ID.json > /tmp/k8s-status-$SESSION_ID.tmp && mv /tmp/k8s-status-$SESSION_ID.tmp /tmp/k8s-status-$SESSION_ID.json
fi

# System-critical pods
echo ""
echo "🏗️  System pods (kube-system):"
system_healthy=$(kubectl get pods -n kube-system --no-headers 2>/dev/null | rg -c "Running" || echo "0")
system_total=$(kubectl get pods -n kube-system --no-headers 2>/dev/null | wc -l || echo "0")
if [ "$system_total" -gt 0 ]; then
    echo "   $system_healthy/$system_total healthy"
else
    echo "   ❌ Unable to check system pods"
fi

# Top resource consuming pods
if kubectl top pods -A >/dev/null 2>&1 && [ "${ARGUMENTS:-quick}" = "detailed" ]; then
    echo ""
    echo "💾 Top resource consumers:"
    kubectl top pods -A --sort-by=memory | head -6
fi
```

STEP 4: Deployment and replica health

```bash
echo ""
echo "🚀 DEPLOYMENT STATUS"
echo "═══════════════════"

# Deployment health
deploy_total=$(kubectl get deployments -A --no-headers 2>/dev/null | wc -l || echo "0")
deploy_ready=$(kubectl get deployments -A --no-headers 2>/dev/null | awk '$3 == $4 {print}' | wc -l || echo "0")
deploy_issues=$(kubectl get deployments -A --no-headers 2>/dev/null | awk '$3 != $4 {print}' | wc -l || echo "0")

if [ "$deploy_total" -eq 0 ]; then
    echo "ℹ️  No deployments found"
    jq '.healthStatus.deployments = "pass"' /tmp/k8s-status-$SESSION_ID.json > /tmp/k8s-status-$SESSION_ID.tmp && mv /tmp/k8s-status-$SESSION_ID.tmp /tmp/k8s-status-$SESSION_ID.json
elif [ "$deploy_issues" -gt 0 ]; then
    echo "⚠️  $deploy_issues/$deploy_total deployments degraded"
    jq '.healthStatus.deployments = "warn"' /tmp/k8s-status-$SESSION_ID.json > /tmp/k8s-status-$SESSION_ID.tmp && mv /tmp/k8s-status-$SESSION_ID.tmp /tmp/k8s-status-$SESSION_ID.json
    
    echo ""
    echo "Degraded deployments:"
    kubectl get deployments -A --no-headers 2>/dev/null | awk '$3 != $4 {print "  " $1 "/" $2 " - " $3 "/" $4 " replicas ready"}' | head -5
else
    echo "✅ All $deploy_total deployments healthy"
    jq '.healthStatus.deployments = "pass"' /tmp/k8s-status-$SESSION_ID.json > /tmp/k8s-status-$SESSION_ID.tmp && mv /tmp/k8s-status-$SESSION_ID.tmp /tmp/k8s-status-$SESSION_ID.json
fi

# StatefulSets
sts_total=$(kubectl get statefulsets -A --no-headers 2>/dev/null | wc -l || echo "0")
if [ "$sts_total" -gt 0 ]; then
    sts_ready=$(kubectl get statefulsets -A --no-headers 2>/dev/null | awk '$2 == $3 {print}' | wc -l || echo "0")
    echo ""
    echo "📦 StatefulSets: $sts_ready/$sts_total ready"
fi

# DaemonSets
ds_total=$(kubectl get daemonsets -A --no-headers 2>/dev/null | wc -l || echo "0")
if [ "$ds_total" -gt 0 ]; then
    echo "🔄 DaemonSets: $ds_total deployed"
fi
```

STEP 5: Service and networking health

```bash
echo ""
echo "🌐 SERVICE & NETWORK STATUS"
echo "══════════════════════════"

# Service check
svc_total=$(kubectl get services -A --no-headers 2>/dev/null | wc -l || echo "0")
svc_lb=$(kubectl get services -A --field-selector=spec.type=LoadBalancer --no-headers 2>/dev/null | wc -l || echo "0")
svc_nodeport=$(kubectl get services -A --field-selector=spec.type=NodePort --no-headers 2>/dev/null | wc -l || echo "0")

echo "✅ Services: $svc_total total"
[ "$svc_lb" -gt 0 ] && echo "   LoadBalancer: $svc_lb"
[ "$svc_nodeport" -gt 0 ] && echo "   NodePort: $svc_nodeport"
jq '.healthStatus.services = "pass"' /tmp/k8s-status-$SESSION_ID.json > /tmp/k8s-status-$SESSION_ID.tmp && mv /tmp/k8s-status-$SESSION_ID.tmp /tmp/k8s-status-$SESSION_ID.json

# Ingress resources
ingress_total=$(kubectl get ingress -A --no-headers 2>/dev/null | wc -l || echo "0")
if [ "$ingress_total" -gt 0 ]; then
    echo "🔀 Ingress resources: $ingress_total"
    if [ "${ARGUMENTS:-quick}" = "detailed" ]; then
        kubectl get ingress -A --no-headers 2>/dev/null | head -3 | awk '{print "   " $1 "/" $2 " - " $3}'
    fi
fi

# Network policies
netpol_total=$(kubectl get networkpolicies -A --no-headers 2>/dev/null | wc -l || echo "0")
[ "$netpol_total" -gt 0 ] && echo "🛡️  Network policies: $netpol_total active"

# Endpoints check
if [ "${ARGUMENTS:-quick}" = "detailed" ]; then
    echo ""
    echo "🔍 Checking service endpoints..."
    endpoints_missing=$(kubectl get endpoints -A -o json 2>/dev/null | jq -r '.items[] | select(.subsets == null or (.subsets | length) == 0) | "\(.metadata.namespace)/\(.metadata.name)"' | wc -l || echo "0")
    if [ "$endpoints_missing" -gt 0 ]; then
        echo "⚠️  $endpoints_missing services without endpoints"
        jq '.healthStatus.network = "warn"' /tmp/k8s-status-$SESSION_ID.json > /tmp/k8s-status-$SESSION_ID.tmp && mv /tmp/k8s-status-$SESSION_ID.tmp /tmp/k8s-status-$SESSION_ID.json
    else
        echo "✅ All services have endpoints"
        jq '.healthStatus.network = "pass"' /tmp/k8s-status-$SESSION_ID.json > /tmp/k8s-status-$SESSION_ID.tmp && mv /tmp/k8s-status-$SESSION_ID.tmp /tmp/k8s-status-$SESSION_ID.json
    fi
else
    jq '.healthStatus.network = "pass"' /tmp/k8s-status-$SESSION_ID.json > /tmp/k8s-status-$SESSION_ID.tmp && mv /tmp/k8s-status-$SESSION_ID.tmp /tmp/k8s-status-$SESSION_ID.json
fi
```

STEP 6: Storage and persistent volume status

```bash
echo ""
echo "💾 STORAGE STATUS"
echo "═════════════════"

# PersistentVolumes
pv_total=$(kubectl get pv --no-headers 2>/dev/null | wc -l || echo "0")
pv_bound=$(kubectl get pv --no-headers 2>/dev/null | rg -c "Bound" || echo "0")
pv_available=$(kubectl get pv --no-headers 2>/dev/null | rg -c "Available" || echo "0")
pv_failed=$(kubectl get pv --no-headers 2>/dev/null | rg -c "Failed" || echo "0")

if [ "$pv_total" -gt 0 ]; then
    echo "📀 PersistentVolumes: $pv_total total"
    echo "   Bound: $pv_bound"
    [ "$pv_available" -gt 0 ] && echo "   Available: $pv_available"
    [ "$pv_failed" -gt 0 ] && echo "   ❌ Failed: $pv_failed"
    
    if [ "$pv_failed" -gt 0 ]; then
        jq '.healthStatus.storage = "fail"' /tmp/k8s-status-$SESSION_ID.json > /tmp/k8s-status-$SESSION_ID.tmp && mv /tmp/k8s-status-$SESSION_ID.tmp /tmp/k8s-status-$SESSION_ID.json
    else
        jq '.healthStatus.storage = "pass"' /tmp/k8s-status-$SESSION_ID.json > /tmp/k8s-status-$SESSION_ID.tmp && mv /tmp/k8s-status-$SESSION_ID.tmp /tmp/k8s-status-$SESSION_ID.json
    fi
else
    echo "ℹ️  No PersistentVolumes found"
    jq '.healthStatus.storage = "pass"' /tmp/k8s-status-$SESSION_ID.json > /tmp/k8s-status-$SESSION_ID.tmp && mv /tmp/k8s-status-$SESSION_ID.tmp /tmp/k8s-status-$SESSION_ID.json
fi

# PersistentVolumeClaims
pvc_total=$(kubectl get pvc -A --no-headers 2>/dev/null | wc -l || echo "0")
pvc_pending=$(kubectl get pvc -A --field-selector=status.phase=Pending --no-headers 2>/dev/null | wc -l || echo "0")

if [ "$pvc_total" -gt 0 ]; then
    echo ""
    echo "📋 PersistentVolumeClaims: $pvc_total total"
    if [ "$pvc_pending" -gt 0 ]; then
        echo "   ⚠️  Pending: $pvc_pending"
        kubectl get pvc -A --field-selector=status.phase=Pending --no-headers 2>/dev/null | head -3 | awk '{print "      " $1 "/" $2}'
    else
        echo "   ✅ All claims bound"
    fi
fi

# Storage classes
sc_total=$(kubectl get storageclass --no-headers 2>/dev/null | wc -l || echo "0")
sc_default=$(kubectl get storageclass --no-headers 2>/dev/null | rg -c "default" || echo "0")
[ "$sc_total" -gt 0 ] && echo ""
[ "$sc_total" -gt 0 ] && echo "🗄️  StorageClasses: $sc_total (default: $sc_default)"
```

STEP 7: Cluster events and recent issues (detailed mode)

IF check_mode is "detailed":

```bash
echo ""
echo "📅 RECENT CLUSTER EVENTS"
echo "═══════════════════════"

# Warning events in last hour
warning_events=$(kubectl get events -A --field-selector=type=Warning -o json 2>/dev/null | jq -r '[.items[] | select(.lastTimestamp | fromdateiso8601 > (now - 3600))] | length' || echo "0")

if [ "$warning_events" -gt 0 ]; then
    echo "⚠️  $warning_events warning events in last hour"
    echo ""
    echo "Recent warnings:"
    kubectl get events -A --field-selector=type=Warning --sort-by='.lastTimestamp' 2>/dev/null | tail -5 | awk '{print "  " $1 "/" $4 " - " substr($0, index($0,$6))}'
else
    echo "✅ No warning events in last hour"
fi

# Failed pods analysis
echo ""
echo "🔍 FAILURE ANALYSIS"
failed_pods=$(kubectl get pods -A --no-headers 2>/dev/null | rg -E "(Error|CrashLoopBackOff|ImagePullBackOff)" | wc -l || echo "0")

if [ "$failed_pods" -gt 0 ]; then
    echo "Analyzing $failed_pods failed pods..."
    
    # Common failure reasons
    image_pull_errors=$(kubectl get pods -A -o json 2>/dev/null | jq -r '[.items[] | select(.status.containerStatuses[]?.state.waiting.reason == "ImagePullBackOff" or .status.containerStatuses[]?.state.waiting.reason == "ErrImagePull")] | length' || echo "0")
    crash_loops=$(kubectl get pods -A -o json 2>/dev/null | jq -r '[.items[] | select(.status.containerStatuses[]?.state.waiting.reason == "CrashLoopBackOff")] | length' || echo "0")
    
    [ "$image_pull_errors" -gt 0 ] && echo "   🖼️  Image pull errors: $image_pull_errors"
    [ "$crash_loops" -gt 0 ] && echo "   🔄 Crash loops: $crash_loops"
fi

# Resource pressure
echo ""
echo "⚡ RESOURCE PRESSURE"
memory_pressure=$(kubectl get nodes -o json 2>/dev/null | jq -r '[.items[] | select(.status.conditions[] | select(.type == "MemoryPressure" and .status == "True"))] | length' || echo "0")
disk_pressure=$(kubectl get nodes -o json 2>/dev/null | jq -r '[.items[] | select(.status.conditions[] | select(.type == "DiskPressure" and .status == "True"))] | length' || echo "0")
pid_pressure=$(kubectl get nodes -o json 2>/dev/null | jq -r '[.items[] | select(.status.conditions[] | select(.type == "PIDPressure" and .status == "True"))] | length' || echo "0")

if [ "$memory_pressure" -eq 0 ] && [ "$disk_pressure" -eq 0 ] && [ "$pid_pressure" -eq 0 ]; then
    echo "✅ No resource pressure detected"
else
    [ "$memory_pressure" -gt 0 ] && echo "❌ Memory pressure on $memory_pressure nodes"
    [ "$disk_pressure" -gt 0 ] && echo "❌ Disk pressure on $disk_pressure nodes"
    [ "$pid_pressure" -gt 0 ] && echo "❌ PID pressure on $pid_pressure nodes"
fi
```

FINALLY: Generate executive summary and recommendations

```bash
echo ""
echo "═══════════════════════════════════════════"
echo "📊 KUBERNETES CLUSTER HEALTH SUMMARY"
echo "═══════════════════════════════════════════"
echo "Session: $SESSION_ID"
echo "Context: $(kubectl config current-context 2>/dev/null || echo "none")"
echo "Cluster: $(kubectl cluster-info 2>/dev/null | head -1 | rg -o "https://[^ ]+" || echo "unknown")"
echo ""

# Overall health score
health_data=$(cat /tmp/k8s-status-$SESSION_ID.json)
pass_count=$(echo "$health_data" | jq -r '[.healthStatus[] | select(. == "pass")] | length')
total_checks=$(echo "$health_data" | jq -r '[.healthStatus[] | select(. != "pending")] | length')
health_percentage=$((pass_count * 100 / total_checks))

echo "🏆 Overall Health Score: $health_percentage%"
echo ""

# Quick status overview
echo "Status Overview:"
echo "$health_data" | jq -r '.healthStatus | to_entries[] | select(.value != "pending") | "  \(.key): \(.value)"' | sed 's/pass/✅/g; s/fail/❌/g; s/warn/⚠️/g'

# Key metrics
echo ""
echo "📈 KEY METRICS"
echo "═════════════"
echo "Nodes: $node_ready/$node_total ready"
echo "Pods: $pod_running/$pod_total running"
echo "Deployments: $deploy_ready/$deploy_total healthy"
echo "Services: $svc_total active"
[ "$pv_total" -gt 0 ] && echo "Storage: $pv_bound/$pv_total volumes bound"

# Recommendations
echo ""
echo "📋 RECOMMENDATIONS"
echo "═════════════════"

if [ "$health_percentage" -eq 100 ]; then
    echo "✨ Excellent! Your Kubernetes cluster is healthy."
else
    # Node issues
    [ "$node_not_ready" -gt 0 ] && echo "🖥️  Investigate NotReady nodes: kubectl describe node <node-name>"
    
    # Pod issues
    [ "$pod_failed" -gt 0 ] && echo "🐳 Debug failed pods: kubectl describe pod <pod-name> -n <namespace>"
    [ "$image_pull_errors" -gt 0 ] && echo "🖼️  Fix image pull errors: check image names and registry access"
    [ "$crash_loops" -gt 0 ] && echo "🔄 Debug crash loops: kubectl logs <pod-name> -n <namespace> --previous"
    
    # Deployment issues
    [ "$deploy_issues" -gt 0 ] && echo "🚀 Fix deployment issues: kubectl rollout status deployment/<name> -n <namespace>"
    
    # Storage issues
    [ "$pvc_pending" -gt 0 ] && echo "💾 Resolve pending PVCs: check StorageClass and available PVs"
    [ "$pv_failed" -gt 0 ] && echo "📀 Fix failed PVs: kubectl describe pv <pv-name>"
    
    # Resource issues
    [ "$memory_pressure" -gt 0 ] && echo "💾 Address memory pressure: scale cluster or optimize workloads"
    [ "$disk_pressure" -gt 0 ] && echo "💿 Address disk pressure: clean up unused resources"
fi

# Additional checks
echo ""
echo "🔧 ADDITIONAL CHECKS"
echo "══════════════════"
echo "• Certificate expiry: kubectl get certificates -A"
echo "• Resource quotas: kubectl describe resourcequotas -A"
echo "• Pod security: kubectl get podsecuritypolicies"
echo "• RBAC audit: kubectl auth can-i --list"

echo ""
echo "💾 Full report saved to: /tmp/k8s-status-$SESSION_ID.json"
```

## Quick Reference

### Usage Examples

```bash
# Quick cluster health check (default)
/project-status-k8s

# Detailed analysis with events and pressure checks
/project-status-k8s detailed

# Check specific cluster context
kubectl config use-context my-cluster && /project-status-k8s
```

### Health Checks Performed

1. **Node Health**: Ready state, resource utilization, conditions
2. **Pod Health**: Running/failed states, system pods, resource usage
3. **Deployment Health**: Replica readiness, StatefulSets, DaemonSets
4. **Service & Network**: Service endpoints, Ingress, NetworkPolicies
5. **Storage Health**: PV/PVC status, StorageClasses
6. **Cluster Events**: Recent warnings and failures (detailed mode)
7. **Resource Pressure**: Memory, disk, and PID pressure analysis (detailed mode)

This command provides comprehensive Kubernetes cluster health monitoring instead of build/test checks.
