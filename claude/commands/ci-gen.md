# /ci-gen

Generates or updates GitHub Actions CI workflow files based on project needs.

## Usage
```
/ci-gen
/ci-gen --platform <github|gitlab|circleci>
/ci-gen --template <basic|advanced|security>
/ci-gen --update
```

## Description
This command automatically creates comprehensive CI/CD pipelines tailored to your specific technology stack and project requirements. It follows industry best practices for testing, security, and deployment automation.

### What it generates:

#### 1. Technology Stack Detection
Analyzes your project to determine the appropriate CI configuration:

**Project Analysis:**
- **Go**: Detects `go.mod`, analyzes Go version and build tags
- **Rust**: Identifies `Cargo.toml`, Rust edition, and feature flags
- **Java**: Finds `pom.xml`/`build.gradle`, determines Java version and build tool
- **Node/Deno**: Locates `package.json`/`deno.json`, package manager detection
- **Python**: Discovers `requirements.txt`/`pyproject.toml`, virtual environment setup
- **Docker**: Detects `Dockerfile` and `docker-compose.yml`
- **Kubernetes**: Identifies `k8s/` directory and manifest files

#### 2. Comprehensive Workflow Generation

**Go Project Example:**
```yaml
name: Go CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

env:
  GO_VERSION: '1.21'

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: testdb
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
          
      redis:
        image: redis:7-alpine
        options: >-
          --health-cmd \"redis-cli ping\"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 6379:6379

    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Go
      uses: actions/setup-go@v4
      with:\n        go-version: ${{ env.GO_VERSION }}\n        cache: true\n        cache-dependency-path: go.sum\n    \n    - name: Download dependencies\n      run: go mod download\n    \n    - name: Verify dependencies\n      run: go mod verify\n    \n    - name: Run go vet\n      run: go vet ./...\n    \n    - name: Install staticcheck\n      run: go install honnef.co/go/tools/cmd/staticcheck@latest\n    \n    - name: Run staticcheck\n      run: staticcheck ./...\n    \n    - name: Install golangci-lint\n      uses: golangci/golangci-lint-action@v3\n      with:\n        version: latest\n        args: --timeout=5m\n    \n    - name: Run tests\n      run: |\n        go test -v -race -coverprofile=coverage.out ./...\n        go tool cover -html=coverage.out -o coverage.html\n    \n    - name: Upload coverage reports\n      uses: codecov/codecov-action@v3\n      with:\n        file: ./coverage.out\n        flags: unittests\n        name: codecov-go\n\n  security-scan:\n    runs-on: ubuntu-latest\n    steps:\n    - uses: actions/checkout@v4\n    \n    - name: Run Gosec Security Scanner\n      uses: securecodewarrior/github-action-gosec@master\n      with:\n        args: './...'\n    \n    - name: Run govulncheck\n      run: |\n        go install golang.org/x/vuln/cmd/govulncheck@latest\n        govulncheck ./...\n\n  build:\n    needs: [test, security-scan]\n    runs-on: ubuntu-latest\n    \n    steps:\n    - uses: actions/checkout@v4\n    \n    - name: Set up Go\n      uses: actions/setup-go@v4\n      with:\n        go-version: ${{ env.GO_VERSION }}\n    \n    - name: Build\n      run: |\n        CGO_ENABLED=0 GOOS=linux go build -ldflags=\"-s -w\" -o bin/app ./cmd/...\n    \n    - name: Build Docker image\n      if: github.event_name == 'push'\n      run: |\n        docker build -t ${{ github.repository }}:${{ github.sha }} .\n        docker tag ${{ github.repository }}:${{ github.sha }} ${{ github.repository }}:latest\n```\n\n**Rust Project Example:**\n```yaml\nname: Rust CI/CD Pipeline\n\non:\n  push:\n    branches: [ main ]\n  pull_request:\n    branches: [ main ]\n\nenv:\n  CARGO_TERM_COLOR: always\n  RUST_BACKTRACE: 1\n\njobs:\n  check:\n    runs-on: ubuntu-latest\n    \n    steps:\n    - uses: actions/checkout@v4\n    \n    - name: Install Rust toolchain\n      uses: dtolnay/rust-toolchain@stable\n      with:\n        components: clippy, rustfmt\n    \n    - name: Cache Cargo registry\n      uses: actions/cache@v3\n      with:\n        path: |\n          ~/.cargo/registry\n          ~/.cargo/git\n          target\n        key: ${{ runner.os }}-cargo-${{ hashFiles('**/Cargo.lock') }}\n    \n    - name: Format check\n      run: cargo fmt -- --check\n    \n    - name: Clippy lint\n      run: cargo clippy --all-targets --all-features -- -D warnings\n    \n    - name: Security audit\n      run: |\n        cargo install cargo-audit\n        cargo audit\n\n  test:\n    runs-on: ubuntu-latest\n    \n    strategy:\n      matrix:\n        rust-version: [stable, beta]\n    \n    steps:\n    - uses: actions/checkout@v4\n    \n    - name: Install Rust ${{ matrix.rust-version }}\n      uses: dtolnay/rust-toolchain@master\n      with:\n        toolchain: ${{ matrix.rust-version }}\n    \n    - name: Run tests\n      run: |\n        cargo test --verbose --all-features\n        cargo test --verbose --no-default-features\n    \n    - name: Run doctests\n      run: cargo test --doc\n    \n    - name: Generate code coverage\n      if: matrix.rust-version == 'stable'\n      run: |\n        cargo install cargo-tarpaulin\n        cargo tarpaulin --verbose --all-features --workspace --timeout 120 --out Xml\n    \n    - name: Upload coverage\n      if: matrix.rust-version == 'stable'\n      uses: codecov/codecov-action@v3\n      with:\n        file: cobertura.xml\n\n  build:\n    needs: [check, test]\n    runs-on: ubuntu-latest\n    \n    steps:\n    - uses: actions/checkout@v4\n    \n    - name: Install Rust\n      uses: dtolnay/rust-toolchain@stable\n    \n    - name: Build release\n      run: cargo build --release --verbose\n    \n    - name: Upload artifacts\n      uses: actions/upload-artifact@v3\n      with:\n        name: binary\n        path: target/release/\n```\n\n#### 3. Advanced Features\n\n**Matrix Testing:**\n```yaml\nstrategy:\n  matrix:\n    os: [ubuntu-latest, windows-latest, macos-latest]\n    rust-version: [stable, beta, nightly]\n    include:\n      - os: ubuntu-latest\n        rust-version: stable\n        features: \"--all-features\"\n    exclude:\n      - os: windows-latest\n        rust-version: nightly\n```\n\n**Dependency Caching:**\n```yaml\n- name: Cache dependencies\n  uses: actions/cache@v3\n  with:\n    path: |\n      ~/.cargo/registry\n      ~/.cargo/git\n      target\n      node_modules\n      ~/.deno\n    key: ${{ runner.os }}-deps-${{ hashFiles('**/Cargo.lock', '**/package-lock.json', '**/deno.lock') }}\n    restore-keys: |\n      ${{ runner.os }}-deps-\n```\n\n**Security Integration:**\n```yaml\nsecurity:\n  runs-on: ubuntu-latest\n  steps:\n  - uses: actions/checkout@v4\n  \n  - name: Run Trivy vulnerability scanner\n    uses: aquasecurity/trivy-action@master\n    with:\n      scan-type: 'fs'\n      scan-ref: '.'\n      format: 'sarif'\n      output: 'trivy-results.sarif'\n  \n  - name: Upload Trivy scan results\n    uses: github/codeql-action/upload-sarif@v2\n    with:\n      sarif_file: 'trivy-results.sarif'\n  \n  - name: SAST CodeQL Analysis\n    uses: github/codeql-action/analyze@v2\n    with:\n      languages: go, javascript\n```\n\n#### 4. Deployment Integration\n\n**Container Registry Push:**\n```yaml\ndeploy:\n  if: github.ref == 'refs/heads/main'\n  needs: [test, security]\n  runs-on: ubuntu-latest\n  \n  steps:\n  - uses: actions/checkout@v4\n  \n  - name: Set up Docker Buildx\n    uses: docker/setup-buildx-action@v3\n  \n  - name: Login to GitHub Container Registry\n    uses: docker/login-action@v3\n    with:\n      registry: ghcr.io\n      username: ${{ github.actor }}\n      password: ${{ secrets.GITHUB_TOKEN }}\n  \n  - name: Build and push Docker image\n    uses: docker/build-push-action@v5\n    with:\n      context: .\n      push: true\n      tags: |\n        ghcr.io/${{ github.repository }}:latest\n        ghcr.io/${{ github.repository }}:${{ github.sha }}\n      cache-from: type=gha\n      cache-to: type=gha,mode=max\n```\n\n**Kubernetes Deployment:**\n```yaml\n  - name: Deploy to Kubernetes\n    run: |\n      echo \"${{ secrets.KUBE_CONFIG }}\" | base64 -d > kubeconfig\n      export KUBECONFIG=kubeconfig\n      \n      # Update image tag in deployment\n      kubectl set image deployment/app app=ghcr.io/${{ github.repository }}:${{ github.sha }}\n      \n      # Wait for rollout\n      kubectl rollout status deployment/app --timeout=600s\n      \n      # Verify deployment\n      kubectl get pods -l app=myapp\n```\n\n### 5. Quality Gates and Notifications\n\n**Branch Protection Integration:**\n```yaml\n# Generates .github/branch-protection.yml\nbranch_protection:\n  main:\n    required_status_checks:\n      - \"test\"\n      - \"security-scan\"\n      - \"build\"\n    enforce_admins: false\n    required_pull_request_reviews:\n      required_approving_review_count: 2\n      dismiss_stale_reviews: true\n      require_code_owner_reviews: true\n```\n\n**Slack/Discord Notifications:**\n```yaml\n  - name: Notify deployment status\n    if: always()\n    uses: 8398a7/action-slack@v3\n    with:\n      status: ${{ job.status }}\n      channel: '#deployments'\n      webhook_url: ${{ secrets.SLACK_WEBHOOK }}\n      fields: repo,message,commit,author,action,eventName,ref,workflow\n```\n\n## Platform Support\n\n### GitHub Actions (Default)\n- Full workflow generation with advanced features\n- Integration with GitHub native features\n- Supports GitHub Container Registry\n- CodeQL security scanning integration\n\n### GitLab CI\n```yaml\n# .gitlab-ci.yml\nstages:\n  - test\n  - security\n  - build\n  - deploy\n\nvariables:\n  DOCKER_DRIVER: overlay2\n  DOCKER_TLS_CERTDIR: \"/certs\"\n\ntest:go:\n  stage: test\n  image: golang:1.21\n  services:\n    - postgres:15\n  script:\n    - go mod download\n    - go test -v -race -coverprofile=coverage.out ./...\n  coverage: '/coverage: \\d+\\.\\d+% of statements/'\n  artifacts:\n    reports:\n      coverage_report:\n        coverage_format: cobertura\n        path: coverage.xml\n```\n\n### CircleCI\n```yaml\n# .circleci/config.yml\nversion: 2.1\n\norbs:\n  go: circleci/go@1.7.0\n  docker: circleci/docker@2.2.0\n\nworkflows:\n  test-and-deploy:\n    jobs:\n      - go/test:\n          version: \"1.21\"\n      - docker/publish:\n          requires:\n            - go/test\n          filters:\n            branches:\n              only: main\n```\n\n## Examples\n\n### Generate basic CI for current project:\n```\n/ci-gen\n```\n\n### Create advanced CI with security scanning:\n```\n/ci-gen --template advanced\n```\n\n### Generate GitLab CI configuration:\n```\n/ci-gen --platform gitlab\n```\n\n### Update existing CI workflow:\n```\n/ci-gen --update\n```\n\n## Configuration Templates\n\n### Basic Template\n- Essential testing and building\n- Basic security scanning\n- Simple deployment to staging\n\n### Advanced Template\n- Matrix testing across platforms/versions\n- Comprehensive security scanning\n- Performance benchmarking\n- Multi-environment deployment\n\n### Security Template\n- SAST/DAST scanning\n- Dependency vulnerability checks\n- Container image scanning\n- Compliance reporting\n\n## Integration with Other Commands\n- Use with `/containerize` to add Docker build steps\n- Combine with `/deploy` for Kubernetes deployment automation\n- Use with `/harden` to include security scanning\n- Integrate with `/test` to include comprehensive testing strategies