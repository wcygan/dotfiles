# Networking

Authoritative deep links:

- <https://kubernetes.io/docs/concepts/services-networking/service/>
- <https://kubernetes.io/docs/concepts/services-networking/ingress/>
- <https://kubernetes.io/docs/concepts/services-networking/gateway/>
- <https://kubernetes.io/docs/concepts/services-networking/network-policies/>
- <https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/>

## Service Types

| Type | Exposes | Typical use |
|---|---|---|
| **ClusterIP** (default) | Virtual IP inside the cluster | In-cluster service-to-service |
| **NodePort** | Static port on every node | Bare-metal external access, dev |
| **LoadBalancer** | Cloud load balancer → NodePort → Pods | Production external traffic on cloud |
| **ExternalName** | DNS CNAME to external host | Alias external services into cluster DNS |
| **Headless** (`clusterIP: None`) | No VIP; DNS returns pod IPs | StatefulSet peer discovery, client-side LB |

```yaml
apiVersion: v1
kind: Service
metadata:
  name: app
spec:
  type: ClusterIP
  selector:
    app.kubernetes.io/name: app
  ports:
    - name: http
      port: 80          # service port
      targetPort: 8080  # container port (or name)
      protocol: TCP
```

## Cluster DNS

Standard form: `<service>.<namespace>.svc.cluster.local`

- Same namespace: `app`
- Cross-namespace: `app.other-ns`
- FQDN: `app.other-ns.svc.cluster.local`
- Headless StatefulSet pods: `<pod-name>.<service>.<ns>.svc.cluster.local`

Search path (typical): `<ns>.svc.cluster.local svc.cluster.local cluster.local`. This is why unqualified names resolve inside the same namespace.

## Ingress (Legacy Path, Still Valid)

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  ingressClassName: nginx
  tls:
    - hosts: [app.example.com]
      secretName: app-tls
  rules:
    - host: app.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: app
                port: { number: 80 }
```

`pathType` values: `Exact`, `Prefix`, `ImplementationSpecific`. Behavior depends on the Ingress controller (nginx, traefik, contour, ALB, etc.).

## Gateway API (Preferred for New Work)

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: app-gateway
spec:
  gatewayClassName: istio     # or contour, nginx, envoy-gateway, ...
  listeners:
    - name: https
      protocol: HTTPS
      port: 443
      tls:
        mode: Terminate
        certificateRefs:
          - { name: app-tls }
      allowedRoutes:
        namespaces: { from: All }
---
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: app
spec:
  parentRefs:
    - name: app-gateway
  hostnames: [app.example.com]
  rules:
    - matches:
        - path: { type: PathPrefix, value: / }
      backendRefs:
        - name: app
          port: 80
```

**Why Gateway API over Ingress**: first-class HTTP routing (method/header matching, traffic splits, mirroring), role separation (Gateway vs Route), no annotation soup, cross-namespace route attachment. Requires controller support — verify with `kubectl get gatewayclass`.

## NetworkPolicy — Default Deny

NetworkPolicy is additive: if no policy selects a pod, all traffic is allowed. Once any policy selects it, only explicitly-allowed traffic passes.

**Default deny all ingress in a namespace**:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-ingress
  namespace: app
spec:
  podSelector: {}
  policyTypes: [Ingress]
```

**Allow app ← frontend, same namespace**:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend-to-app
  namespace: app
spec:
  podSelector:
    matchLabels: { app.kubernetes.io/name: app }
  policyTypes: [Ingress]
  ingress:
    - from:
        - podSelector:
            matchLabels: { app.kubernetes.io/name: frontend }
      ports:
        - { protocol: TCP, port: 8080 }
```

**Critical**: NetworkPolicy requires a CNI that enforces it (Calico, Cilium, Antrea, Weave). Flannel alone does not enforce NetworkPolicy.

## Debugging Connectivity

```bash
# Is the Service backing any pods?
kubectl get endpoints <svc>
kubectl get endpointslices -l kubernetes.io/service-name=<svc>

# DNS resolution from inside the cluster
kubectl run -it --rm dnsutils --image=registry.k8s.io/e2e-test-images/jessie-dnsutils:1.3 -- nslookup <svc>

# Port-forward around the Service
kubectl port-forward pod/<pod> 8080

# Which NetworkPolicies apply to a pod?
kubectl get networkpolicy -n <ns>
```

Empty endpoints usually means: selector doesn't match pod labels, pods aren't Ready (readiness probe failing), or pods are in a different namespace than the Service.
