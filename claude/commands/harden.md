# /harden

Proactively applies security best practices to applications and infrastructure.

## Usage
```
/harden <target>
/harden <target> --level <basic|strict|paranoid>
/harden <target> --compliance <soc2|pci|hipaa>
```

## Description
This command systematically reduces your application's attack surface by implementing security hardening across multiple layers. Unlike audit-focused tools, `/harden` makes actual security improvements to your code and infrastructure.

### Security Layers

#### 1. Container Security (Dockerfile)
Transforms Docker images to follow security best practices:

**Before:**
```dockerfile
FROM node:18
COPY . /app
WORKDIR /app
RUN npm install
USER root
CMD ["npm", "start"]
```

**After:**
```dockerfile
# Multi-stage build with distroless final image
FROM node:18-alpine AS builder
WORKDIR /build
COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force

FROM gcr.io/distroless/nodejs18-debian11:nonroot
COPY --from=builder /build/node_modules /app/node_modules
COPY --from=builder --chown=nonroot:nonroot /build/src /app/src

# Security hardening
USER nonroot
WORKDIR /app

# Read-only root filesystem
COPY --chmod=444 package.json ./
ENV NODE_ENV=production

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node healthcheck.js

EXPOSE 3000
CMD ["node", "src/index.js"]
```

**Applied Hardening:**
- Distroless or minimal base images (Alpine, scratch)
- Non-root user execution with proper UID/GID
- Read-only root filesystem where possible
- Dropped unnecessary capabilities
- Multi-stage builds to reduce image size
- Dependency vulnerability scanning integration

#### 2. Kubernetes Security
Implements Pod Security Standards and network policies:

**Generated Pod Security Context:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: secure-app
spec:
  template:
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 10001
        runAsGroup: 10001
        fsGroup: 10001
        seccompProfile:
          type: RuntimeDefault
      containers:
      - name: app
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          capabilities:
            drop:
            - ALL
            add:
            - NET_BIND_SERVICE  # Only if needed for port 80/443
        resources:
          requests:
            memory: "64Mi"
            cpu: "250m"
          limits:
            memory: "128Mi"
            cpu: "500m"
        volumeMounts:
        - name: tmp
          mountPath: /tmp
        - name: var-cache
          mountPath: /var/cache
      volumes:
      - name: tmp
        emptyDir: {}
      - name: var-cache
        emptyDir: {}
```

**Network Policy Generation:**
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: secure-app-netpol
spec:
  podSelector:
    matchLabels:
      app: secure-app
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
    ports:
    - protocol: TCP
      port: 8080
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          name: database
    ports:
    - protocol: TCP
      port: 5432
  - to: []  # DNS resolution
    ports:
    - protocol: UDP
      port: 53
```

#### 3. Application-Level Security
Injects security controls directly into application code:

**Web Framework Hardening (Go with Gin):**
```go
func SecurityMiddleware() gin.HandlerFunc {
    return gin.HandlerFunc(func(c *gin.Context) {
        // Security headers
        c.Header("X-Frame-Options", "DENY")
        c.Header("X-Content-Type-Options", "nosniff")
        c.Header("X-XSS-Protection", "1; mode=block")
        c.Header("Strict-Transport-Security", "max-age=31536000; includeSubDomains")
        c.Header("Content-Security-Policy", "default-src 'self'")
        c.Header("Referrer-Policy", "strict-origin-when-cross-origin")
        
        // Remove server identification
        c.Header("Server", "")
        
        c.Next()
    })
}

func CORSMiddleware() gin.HandlerFunc {
    return cors.New(cors.Config{
        AllowOrigins:     []string{"https://yourdomain.com"},
        AllowMethods:     []string{"GET", "POST", "PUT", "DELETE"},
        AllowHeaders:     []string{"Content-Type", "Authorization"},
        ExposeHeaders:    []string{"Content-Length"},
        AllowCredentials: false,
        MaxAge:           12 * time.Hour,
    })
}
```

**Rust Axum Security Implementation:**
```rust
use axum::{
    http::{HeaderMap, HeaderName, HeaderValue, StatusCode},
    middleware::{self, Next},
    response::Response,
    Router,
};

async fn security_headers_middleware<B>(
    mut request: axum::extract::Request<B>,
    next: Next<B>,
) -> Response {
    let mut response = next.run(request).await;
    
    let headers = response.headers_mut();
    headers.insert("x-frame-options", HeaderValue::from_static("DENY"));
    headers.insert("x-content-type-options", HeaderValue::from_static("nosniff"));
    headers.insert("x-xss-protection", HeaderValue::from_static("1; mode=block"));
    headers.insert(
        "strict-transport-security",
        HeaderValue::from_static("max-age=31536000; includeSubDomains"),
    );
    headers.insert(
        "content-security-policy",
        HeaderValue::from_static("default-src 'self'"),
    );
    
    response
}

pub fn create_secure_router() -> Router {
    Router::new()
        .layer(middleware::from_fn(security_headers_middleware))
        .layer(middleware::from_fn(rate_limiting_middleware))
        .layer(middleware::from_fn(request_timeout_middleware))
}
```

**Java Spring Security Configuration:**
```java
@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .headers(headers -> headers
                .frameOptions().deny()
                .contentTypeOptions().and()
                .httpStrictTransportSecurity(hstsConfig -> hstsConfig
                    .maxAgeInSeconds(31536000)
                    .includeSubdomains(true))
                .contentSecurityPolicy("default-src 'self'"))
            .cors(cors -> cors.configurationSource(corsConfigurationSource()))
            .csrf(csrf -> csrf
                .csrfTokenRepository(CookieCsrfTokenRepository.withHttpOnlyFalse())
                .ignoringRequestMatchers("/api/public/**"))
            .sessionManagement(session -> session
                .sessionCreationPolicy(SessionCreationPolicy.STATELESS)
                .maximumSessions(1)
                .maxSessionsPreventsLogin(false));
                
        return http.build();
    }
}
```

#### 4. Dependency Security
Automatically secures dependencies and supply chain:

**Go Module Security:**
```go
// go.mod - Pin dependencies to specific secure versions
module secure-app

go 1.21

require (
    github.com/gin-gonic/gin v1.9.1
    github.com/golang-jwt/jwt/v5 v5.0.0  // Updated from vulnerable v4
    golang.org/x/crypto v0.14.0          // Latest security patches
)

// Remove indirect dependencies with known vulnerabilities
replace github.com/old-vulnerable-dep => github.com/secure-alternative v1.0.0
```

**Rust Cargo.toml Hardening:**
```toml
[dependencies]
# Pin to exact versions for reproducible builds
serde = "=1.0.190"
tokio = { version = "=1.33.0", features = ["macros", "rt-multi-thread"] }

# Security-focused alternatives
ring = "0.17.5"  # Instead of older crypto libraries
rustls = "0.21.8"  # Instead of OpenSSL bindings

[dependencies.sqlx]
version = "0.7.2"
features = ["runtime-tokio-rustls", "postgres", "chrono", "uuid"]
# Use rustls instead of native-tls for better security

# Audit configuration
[profile.release]
panic = "abort"  # Prevent stack unwinding attacks
lto = true       # Link-time optimization
codegen-units = 1
```

#### 5. Secrets and Configuration Security
Implements secure secret management patterns:

**Environment Variable Security:**
```bash
#!/bin/bash
# secure-env.sh - Generated secure environment setup

# Validate required secrets are present
required_vars=("DATABASE_URL" "JWT_SECRET" "API_KEY")
for var in "${required_vars[@]}"; do
    if [[ -z "${!var}" ]]; then
        echo "ERROR: Required environment variable $var is not set"
        exit 1
    fi
done

# Validate secret formats
if [[ ! $DATABASE_URL =~ ^postgresql://.*$ ]]; then
    echo "ERROR: DATABASE_URL must be a valid PostgreSQL connection string"
    exit 1
fi

if [[ ${#JWT_SECRET} -lt 32 ]]; then
    echo "ERROR: JWT_SECRET must be at least 32 characters"
    exit 1
fi

export NODE_ENV=production
export LOG_LEVEL=info
export SECURE_COOKIES=true
export SESSION_TIMEOUT=3600
```

**Kubernetes Secret Management:**
```yaml
# External Secrets Operator configuration
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: vault-backend
spec:
  provider:
    vault:
      server: "https://vault.company.com"
      path: "secret"
      version: "v2"
      auth:
        kubernetes:
          mountPath: "kubernetes"
          role: "secure-app"

---
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: app-secrets
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: vault-backend
    kind: SecretStore
  target:
    name: app-secrets
    creationPolicy: Owner
  data:
  - secretKey: database-url
    remoteRef:
      key: secure-app/config
      property: database_url
```

### Security Levels

#### Basic Level
- Essential security headers
- Non-root container execution
- Basic input validation
- HTTPS enforcement

#### Strict Level
- Comprehensive security headers with CSP
- Read-only filesystems
- Network segmentation policies
- Secrets rotation policies
- Security scanning in CI/CD

#### Paranoid Level
- Zero-trust network architecture
- Mandatory access controls (SELinux/AppArmor)
- Runtime security monitoring
- Comprehensive audit logging
- Multi-factor authentication requirements

### Compliance Templates

#### SOC 2 Compliance
- Audit logging for all data access
- Encryption at rest and in transit
- Access control documentation
- Incident response procedures

#### PCI DSS Compliance
- Payment data isolation
- Strong cryptography implementation
- Regular security testing
- Network segmentation

#### HIPAA Compliance
- PHI data encryption
- Access controls and audit trails
- Risk assessment documentation
- Breach notification procedures

## Examples

### Harden a Dockerfile:
```
/harden ./Dockerfile
```

### Apply strict security to Kubernetes manifests:
```
/harden ./k8s --level strict
```

### SOC 2 compliance hardening:
```
/harden ./src --compliance soc2
```

### Harden entire application:
```
/harden . --level paranoid
```

## Generated Security Documentation
Creates comprehensive security documentation:

```
security/
├── SECURITY.md           # Security policy and procedures
├── threat-model.md       # Application threat model
├── compliance/
│   ├── soc2-controls.md
│   └── security-checklist.md
└── incident-response/
    └── runbook.md
```

## Integration with Other Commands
- Use with `/containerize` to create secure container images
- Combine with `/deploy` for secure Kubernetes deployments
- Use with `/observe` for security monitoring and alerting
- Integrate with `/ci-gen` to add security scanning to CI pipelines