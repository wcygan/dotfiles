Set up a complete development environment for new team members working on $ARGUMENTS.

Steps:

1. **Environment Detection & Requirements:**
   - Detect project language(s) and frameworks
   - Identify required tools and dependencies
   - Check for existing setup documentation (README, docs/)
   - Scan for configuration files (.env.example, .tool-versions, etc.)

2. **System Prerequisites:**

   **Modern CLI Tools (per CLAUDE.md preferences):**
   ```bash
   # Check and install modern alternatives
   which rg || echo "Install ripgrep for fast code search"
   which fd || echo "Install fd for fast file finding" 
   which bat || echo "Install bat for syntax-highlighted viewing"
   which eza || echo "Install eza for better file listings"
   which fzf || echo "Install fzf for fuzzy finding"
   which delta || echo "Install delta for better git diffs"
   which zoxide || echo "Install zoxide for smart directory navigation"
   which jq || echo "Install jq for JSON processing"
   which yq || echo "Install yq for YAML processing"
   ```

   **Language-Specific Tools:**
   ```bash
   # Rust
   if [ -f "Cargo.toml" ]; then
     curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
     rustup component add clippy rustfmt
   fi

   # Go  
   if [ -f "go.mod" ]; then
     # Install Go via official installer or package manager
     go install golang.org/x/tools/gopls@latest
   fi

   # Deno (preferred for scripting)
   if [ -f "deno.json" ] || [ -f "deno.lock" ]; then
     curl -fsSL https://deno.land/install.sh | sh
   fi

   # Java
   if [ -f "pom.xml" ] || [ -f "build.gradle" ]; then
     # Install SDKMAN for Java management
     curl -s "https://get.sdkman.io" | bash
     sdk install java 21-tem
   fi
   ```

3. **Project Dependencies:**

   **Package Management:**
   ```bash
   # Rust
   if [ -f "Cargo.toml" ]; then
     cargo fetch
     cargo build
   fi

   # Go
   if [ -f "go.mod" ]; then
     go mod download
     go mod tidy
   fi

   # Deno
   if [ -f "deno.json" ]; then
     deno cache deps.ts || deno cache **/*.ts
     deno task install || echo "No install task defined"
   fi

   # Java Maven
   if [ -f "pom.xml" ]; then
     ./mvnw dependency:go-offline || mvn dependency:go-offline
   fi

   # Java Gradle
   if [ -f "build.gradle" ]; then
     ./gradlew build --dry-run
   fi
   ```

4. **Infrastructure Setup:**

   **Database Setup (using modern alternatives):**
   ```bash
   # PostgreSQL (preferred over MySQL)
   createdb development_db || echo "Create PostgreSQL database manually"

   # DragonflyDB (preferred over Redis)
   # Start with: dragonflydb --bind 127.0.0.1 --port 6379

   # Run migrations if available
   find . -name "*migrate*" -type f
   find . -name "migrations" -type d
   ```

   **Container Environment:**
   ```bash
   # Check for Docker setup
   if [ -f "Dockerfile" ] || [ -f "docker-compose.yml" ]; then
     docker-compose up -d || docker compose up -d
   fi

   # Check for Kubernetes configs
   if [ -d "k8s" ] || [ -d "kubernetes" ]; then
     echo "Kubernetes configs found - see deployment docs"
   fi
   ```

5. **Development Tools Configuration:**

   **Editor Setup:**
   ```bash
   # VSCode settings
   if [ -d ".vscode" ]; then
     echo "VSCode workspace configuration found"
     code . # Open in VSCode if available
   fi

   # Zed settings  
   if [ -d ".zed" ]; then
     echo "Zed workspace configuration found"
   fi

   # Claude Code setup
   if [ -d ".claude" ]; then
     echo "Claude Code configuration found"
     echo "Available commands:"
     ls .claude/commands/ | sed 's/.md$//' | sed 's/^/  \/project:/'
   fi
   ```

   **Git Configuration:**
   ```bash
   # Set up git hooks if available
   if [ -d ".git/hooks" ] && [ -f "scripts/pre-commit-check.ts" ]; then
     ln -sf ../../scripts/pre-commit-check.ts .git/hooks/pre-commit
   fi

   # Configure git user if not set
   git config user.name >/dev/null || echo "Set git user.name"
   git config user.email >/dev/null || echo "Set git user.email"
   ```

6. **Environment Variables & Secrets:**
   ```bash
   # Copy environment templates
   if [ -f ".env.example" ]; then
     cp .env.example .env
     echo "Created .env from template - update with actual values"
   fi

   # Check for other config templates
   find . -name "*.example" -o -name "*.template" | head -10
   ```

7. **Validation & Health Checks:**

   **Build Verification:**
   ```bash
   # Run project-specific build
   if [ -f "deno.json" ]; then
     deno task build || echo "No build task defined"
   elif [ -f "Cargo.toml" ]; then
     cargo check
   elif [ -f "go.mod" ]; then
     go build ./...
   elif [ -f "pom.xml" ]; then
     ./mvnw compile test-compile
   fi
   ```

   **Test Suite:**
   ```bash
   # Run a subset of tests to verify setup
   if [ -f "deno.json" ]; then
     deno test --allow-all || echo "Tests may require additional setup"
   elif [ -f "Cargo.toml" ]; then
     cargo test --no-run # Just compile tests
   elif [ -f "go.mod" ]; then
     go test -short ./...
   fi
   ```

8. **Documentation & Knowledge Transfer:**
   - Generate list of key files to read first
   - Identify main entry points (main.rs, main.go, mod.ts)
   - Find API documentation or OpenAPI specs
   - Locate architectural decision records (ADRs)
   - List available npm/deno/cargo scripts and tasks

9. **Team Integration:**
   - Set up communication channels (Slack, Discord, etc.)
   - Add to relevant GitHub teams/repositories
   - Share development workflow documentation
   - Schedule knowledge transfer sessions with team members

10. **Troubleshooting Setup:**
    ```bash
    # Common fix commands
    echo "If issues persist, try these:"
    echo "- Clear dependency cache and reinstall"
    echo "- Check tool versions match .tool-versions or docs"
    echo "- Verify network access to package registries"
    echo "- Check disk space and permissions"
    ```

**Output Checklist:**

- [ ] All required tools installed and accessible
- [ ] Project dependencies resolved and cached
- [ ] Development database/services running
- [ ] Environment variables configured
- [ ] Editor/IDE workspace opened and configured
- [ ] Git hooks and configuration set up
- [ ] Initial build successful
- [ ] Sample tests pass
- [ ] Development server starts successfully
- [ ] Access to team resources and documentation

**Next Steps:**

- Review project README and contributing guidelines
- Explore codebase starting with main entry points
- Run `/project:knowledge-extract` to understand domain concepts
- Set up preferred development workflow and shortcuts
- Join team standups and introduce yourself
