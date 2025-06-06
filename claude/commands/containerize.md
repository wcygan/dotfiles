Create production-ready containerization for $ARGUMENTS with multi-stage builds, security hardening, and Kubernetes optimization.

Steps:

1. **Project Analysis:**
   - Detect project type(s) and build requirements
   - Identify runtime dependencies and external services
   - Analyze current deployment patterns
   - Check for existing container configurations

2. **Multi-Stage Dockerfile Creation:**
   
   **Rust Projects:**
   ```dockerfile
   # Build stage
   FROM rust:1.80-alpine AS builder
   WORKDIR /app
   
   # Install build dependencies
   RUN apk add --no-cache musl-dev pkgconfig openssl-dev
   
   # Cache dependencies
   COPY Cargo.toml Cargo.lock ./
   RUN mkdir src && echo "fn main() {}" > src/main.rs
   RUN cargo build --release && rm -rf src/
   
   # Build application
   COPY src/ src/
   RUN touch src/main.rs && cargo build --release
   
   # Runtime stage
   FROM alpine:3.19
   RUN apk add --no-cache ca-certificates tzdata
   RUN addgroup -g 1001 -S appgroup && adduser -u 1001 -S appuser -G appgroup
   
   WORKDIR /app
   COPY --from=builder /app/target/release/app /app/
   RUN chown -R appuser:appgroup /app
   
   USER appuser
   EXPOSE 8080
   CMD ["./app"]
   ```

   **Go Projects:**
   ```dockerfile
   # Build stage
   FROM golang:1.22-alpine AS builder
   WORKDIR /app
   
   # Install build dependencies
   RUN apk add --no-cache git ca-certificates tzdata
   
   # Cache dependencies
   COPY go.mod go.sum ./
   RUN go mod download && go mod verify
   
   # Build application
   COPY . .
   RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o app ./cmd/server
   
   # Runtime stage
   FROM scratch
   COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
   COPY --from=builder /usr/share/zoneinfo /usr/share/zoneinfo
   COPY --from=builder /app/app /app
   
   EXPOSE 8080
   CMD ["/app"]
   ```

   **Java Projects (Spring Boot/Quarkus):**
   ```dockerfile
   # Build stage
   FROM eclipse-temurin:21-jdk-alpine AS builder
   WORKDIR /app
   
   # Cache dependencies
   COPY pom.xml ./
   COPY mvnw ./
   COPY .mvn .mvn
   RUN ./mvnw dependency:go-offline -B
   
   # Build application
   COPY src src
   RUN ./mvnw clean package -DskipTests -B
   
   # Runtime stage
   FROM eclipse-temurin:21-jre-alpine
   RUN addgroup -g 1001 -S appgroup && adduser -u 1001 -S appuser -G appgroup
   
   WORKDIR /app
   COPY --from=builder /app/target/*.jar app.jar
   RUN chown appuser:appgroup app.jar
   
   USER appuser
   EXPOSE 8080
   ENTRYPOINT ["java", "-jar", "app.jar"]
   ```

   **Deno Projects:**
   ```dockerfile
   # Build stage (if compilation needed)
   FROM denoland/deno:1.46.0 AS builder
   WORKDIR /app
   
   # Cache dependencies
   COPY deno.json deno.lock* ./
   RUN deno cache deps.ts
   
   # Copy source and compile if needed
   COPY . .
   RUN deno task build || echo "No build step required"
   
   # Runtime stage
   FROM denoland/deno:1.46.0
   RUN groupadd -g 1001 appgroup && useradd -u 1001 -g appgroup appuser
   
   WORKDIR /app
   COPY --from=builder /app .
   RUN chown -R appuser:appgroup /app
   
   USER appuser
   EXPOSE 8080
   CMD ["deno", "task", "start"]
   ```

3. **Security Hardening:**
   
   **Base Image Security:**
   ```dockerfile
   # Use minimal, security-focused base images
   # Alpine for small attack surface
   # Distroless for zero-package images
   # scratch for static binaries
   
   # Regular security updates
   RUN apk update && apk upgrade && apk add --no-cache ca-certificates
   
   # Remove package managers in final stage
   # Use multi-stage to avoid build tools in production
   ```

   **User Security:**
   ```dockerfile
   # Never run as root
   RUN addgroup -g 1001 -S appgroup && adduser -u 1001 -S appuser -G appgroup
   USER appuser
   
   # Read-only filesystem when possible
   # Use tmpfs for writable areas
   VOLUME ["/tmp"]
   ```

   **Secret Management:**
   ```dockerfile
   # Use build secrets for sensitive data
   # --mount=type=secret,id=api_key
   
   # Environment variables for non-sensitive config
   ENV APP_ENV=production
   ENV LOG_LEVEL=info
   
   # Use external secret management (K8s secrets, Vault)
   ```

4. **Performance Optimization:**
   
   **Layer Optimization:**
   ```dockerfile
   # Order layers by change frequency (least to most)
   # 1. System packages
   # 2. Application dependencies  
   # 3. Application code
   
   # Combine RUN commands to reduce layers
   RUN apk update && apk add --no-cache \
       ca-certificates \
       tzdata \
       && rm -rf /var/cache/apk/*
   
   # Use .dockerignore to exclude unnecessary files
   ```

   **Build Caching:**
   ```dockerfile
   # Cache dependencies separately from source code
   COPY package.json package-lock.json ./
   RUN npm ci --only=production
   
   # Copy source after dependencies
   COPY src/ src/
   ```

5. **Health Checks and Monitoring:**
   ```dockerfile
   # Application health check
   HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
     CMD curl -f http://localhost:8080/health || exit 1
   
   # Or for non-HTTP services
   HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
     CMD ./health-check.sh || exit 1
   
   # Expose metrics port for monitoring
   EXPOSE 8080 9090
   ```

6. **Docker Compose for Development:**
   ```yaml
   version: '3.8'
   services:
     app:
       build:
         context: .
         target: builder  # Use builder stage for development
       volumes:
         - .:/app
         - /app/target  # Exclude build artifacts
       ports:
         - "8080:8080"
       environment:
         - DATABASE_URL=postgres://user:pass@db:5432/appdb
         - DRAGONFLY_URL=redis://cache:6379
       depends_on:
         - db
         - cache
   
     db:
       image: postgres:16-alpine
       environment:
         POSTGRES_DB: appdb
         POSTGRES_USER: user
         POSTGRES_PASSWORD: pass
       volumes:
         - postgres_data:/var/lib/postgresql/data
       ports:
         - "5432:5432"
   
     cache:
       image: docker.dragonflydb.io/dragonflydb/dragonfly:v1.17.1
       ports:
         - "6379:6379"
       command: dragonfly --bind 0.0.0.0 --port 6379
   
   volumes:
     postgres_data:
   ```

7. **Kubernetes Manifests:**
   
   **Deployment:**
   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: app
     labels:
       app: app
   spec:
     replicas: 3
     selector:
       matchLabels:
         app: app
     template:
       metadata:
         labels:
           app: app
       spec:
         containers:
         - name: app
           image: your-registry/app:latest
           ports:
           - containerPort: 8080
             name: http
           - containerPort: 9090
             name: metrics
           env:
           - name: DATABASE_URL
             valueFrom:
               secretKeyRef:
                 name: app-secrets
                 key: database-url
           resources:
             requests:
               memory: "128Mi"
               cpu: "100m"
             limits:
               memory: "512Mi"
               cpu: "500m"
           livenessProbe:
             httpGet:
               path: /health
               port: 8080
             initialDelaySeconds: 30
             periodSeconds: 10
           readinessProbe:
             httpGet:
               path: /ready
               port: 8080
             initialDelaySeconds: 5
             periodSeconds: 5
           securityContext:
             runAsNonRoot: true
             runAsUser: 1001
             runAsGroup: 1001
             readOnlyRootFilesystem: true
             allowPrivilegeEscalation: false
             capabilities:
               drop:
               - ALL
   ```

   **Service:**
   ```yaml
   apiVersion: v1
   kind: Service
   metadata:
     name: app-service
   spec:
     selector:
       app: app
     ports:
     - name: http
       port: 80
       targetPort: 8080
     - name: metrics
       port: 9090
       targetPort: 9090
     type: ClusterIP
   ```

   **Ingress:**
   ```yaml
   apiVersion: networking.k8s.io/v1
   kind: Ingress
   metadata:
     name: app-ingress
     annotations:
       kubernetes.io/ingress.class: nginx
       cert-manager.io/cluster-issuer: letsencrypt-prod
   spec:
     tls:
     - hosts:
       - app.example.com
       secretName: app-tls
     rules:
     - host: app.example.com
       http:
         paths:
         - path: /
           pathType: Prefix
           backend:
             service:
               name: app-service
               port:
                 number: 80
   ```

8. **CI/CD Integration:**
   ```yaml
   # .github/workflows/docker.yml
   name: Build and Push Docker Image
   
   on:
     push:
       branches: [main]
       tags: [v*]
   
   jobs:
     build:
       runs-on: ubuntu-latest
       steps:
       - uses: actions/checkout@v4
       
       - name: Set up Docker Buildx
         uses: docker/setup-buildx-action@v3
       
       - name: Login to Container Registry
         uses: docker/login-action@v3
         with:
           registry: ghcr.io
           username: ${{ github.actor }}
           password: ${{ secrets.GITHUB_TOKEN }}
       
       - name: Build and push
         uses: docker/build-push-action@v5
         with:
           context: .
           push: true
           tags: |
             ghcr.io/${{ github.repository }}:latest
             ghcr.io/${{ github.repository }}:${{ github.sha }}
           cache-from: type=gha
           cache-to: type=gha,mode=max
   ```

9. **Security Scanning:**
   ```bash
   # Dockerfile linting
   docker run --rm -i hadolint/hadolint < Dockerfile
   
   # Image vulnerability scanning
   docker scout cves your-image:latest
   trivy image your-image:latest
   
   # Container runtime security
   docker bench for-security
   ```

10. **Documentation:**
    ```markdown
    # Container Documentation
    
    ## Building
    ```bash
    docker build -t app:latest .
    ```
    
    ## Running
    ```bash
    docker run -p 8080:8080 app:latest
    ```
    
    ## Development
    ```bash
    docker-compose up -d
    ```
    
    ## Deployment
    ```bash
    kubectl apply -f k8s/
    ```
    ```

**Output Deliverables:**
- Optimized multi-stage Dockerfile
- Docker Compose for local development
- Kubernetes manifests (Deployment, Service, Ingress)
- CI/CD pipeline configuration
- Security scanning setup
- Health check implementation
- Documentation and deployment guides

**Best Practices Applied:**
- Minimal attack surface with distroless/Alpine images
- Non-root user execution
- Layer caching optimization
- Security scanning integration
- Health checks and observability
- Resource limits and requests
- Secrets management
- Container registry integration