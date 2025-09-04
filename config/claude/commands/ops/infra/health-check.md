---
allowed-tools: Bash(kubectl:*), Bash(docker:*), Bash(curl:*), Bash(systemctl:*)
description: Quick infrastructure health assessment
---

## Context

- Target system: $ARGUMENTS
- Kubernetes context: !`kubectl config current-context 2>/dev/null || echo "No K8s context"`
- Docker daemon: !`docker info --format '{{.ServerVersion}}' 2>/dev/null || echo "Docker unavailable"`
- System load: !`uptime | awk '{print $10, $11, $12}' 2>/dev/null || echo "Load unavailable"`
- Failed services: !`systemctl --failed --no-legend 2>/dev/null | wc -l | tr -d ' ' || echo "0"` failed systemd services

**Resource Status:**

- Memory: !`free -h 2>/dev/null | awk 'NR==2{print $3 "/" $2}' || echo "unavailable"`
- Disk: !`df -h / 2>/dev/null | awk 'NR==2{print $3 "/" $2 " (" $5 " used)"}' || echo "unavailable"`

**Service Health:**

- Kubernetes nodes: !`kubectl get nodes --no-headers 2>/dev/null | wc -l | tr -d ' ' || echo "0"` nodes
- Running containers: !`docker ps -q 2>/dev/null | wc -l | tr -d ' ' || echo "0"` containers
- Health endpoint: !`curl -s --connect-timeout 3 http://localhost:8080/health 2>/dev/null | jq -r '.status // "unreachable"' || echo "unreachable"`

## Your task

Analyze the infrastructure health status from the context above and provide:

1. **Overall Health Assessment** - Critical, Warning, or Healthy
2. **Key Issues** - Any failing services, resource constraints, or connectivity problems
3. **Immediate Actions** - Specific commands to investigate or fix critical issues
4. **Monitoring Recommendations** - What to watch for ongoing health

Focus on actionable insights based on the live system data provided in the context.
