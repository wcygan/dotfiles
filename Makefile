# Nix Dotfiles Makefile
# Run 'make help' for available commands

.PHONY: help install test test-pre test-local test-docker link git-user clean update latest shell docs install-skills update-skills

# Default target
help:
	@echo "Nix Dotfiles Management"
	@echo "======================="
	@echo ""
	@echo "Installation:"
	@echo "  make install    - Full installation (Nix + packages + configs)"
	@echo "  make link       - Link configs only (fish, etc.)"
	@echo "  make link-dry   - Preview what link will do"
	@echo "  make git-user   - Set up git user name and email"
	@echo ""
	@echo "Testing:"
	@echo "  make test       - Run all tests (pre-flight + local + shell)"
	@echo "  make test-pre   - Pre-flight checks only"
	@echo "  make test-local - Local isolated test"
	@echo "  make test-shell - Shell handoff test (bash/zsh → fish)"
	@echo "  make setup-shell-handoff - Configure bash/zsh → fish handoff"
	@echo "  make test-docker- Docker isolated test"
	@echo "  make docker-fedora - Interactive Fedora container"
	@echo "  make docker-ubuntu - Interactive Ubuntu container"
	@echo ""
	@echo "Package Management:"
	@echo "  make latest     - Pull latest changes and reinstall"
	@echo "  make update     - Update flake and upgrade packages"
	@echo "  make install-packages - Install/upgrade packages from current flake"
	@echo "  make list       - List installed packages"
	@echo "  make clean      - Garbage collect old packages"
	@echo ""
	@echo "Agent Skills:"
	@echo "  make install-skills - Install curated vendor agent skills"
	@echo "  make update-skills  - Update all global agent skills"
	@echo ""
	@echo "Development:"
	@echo "  make shell      - Enter Nix development shell"
	@echo "  make fish       - Start fish shell"
	@echo "  make source     - Show command to source Nix environment"
	@echo "  make docs       - Start documentation dev server"
	@echo ""
	@echo "Troubleshooting:"
	@echo "  make verify     - Verify Nix installation"
	@echo "  make doctor     - Run diagnostic checks"

# Full installation
install:
	@echo "🚀 Running full installation..."
	@./install.sh
	@echo ""
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "✅ Installation complete!"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo ""
	@echo "🐠 To start using your new environment:"
	@echo "   exec fish -l"
	@echo ""
	@echo "Or use 'make fish' if exec doesn't work"

# Link configurations only
link:
	@echo "🔗 Linking configurations..."
	@./scripts/link-config.sh
	@echo "✅ Configs linked!"
	@echo ""
	@echo "💡 Run 'make git-user' to set up your git identity"

# Dry run for linking
link-dry:
	@echo "🔍 Preview of link changes..."
	@./scripts/link-config.sh --dry-run

# Set up git user configuration
git-user:
	@echo "👤 Setting up git user configuration..."
	@./scripts/setup-git-user.sh

# Run all non-docker tests
test: test-pre test-local test-shell
	@echo "✅ All tests completed!"

# Pre-flight checks
test-pre:
	@echo "🔍 Running pre-flight checks..."
	@cd tests && ./test-fish-setup.sh

# Local isolated test
test-local:
	@echo "🧪 Running local isolated test..."
	@cd tests && ./test-ephemeral.sh

# Shell handoff test
test-shell:
	@echo "🔄 Testing shell handoff (bash/zsh → fish)..."
	@cd tests && ./test-shell-handoff.sh

# Configure bash/zsh to hand off interactive sessions to fish
setup-shell-handoff:
	@echo "🛠️  Configuring shell handoff (bash/zsh → fish)..."
	@./scripts/setup-shell-handoff.sh
	@echo ""
	@echo "Run 'make test-shell' to verify."

# Docker isolated test
test-docker:
	@echo "🐳 Running Docker matrix…"
	@cd tests && ./test-matrix.sh

# Build and run Fedora test container
docker-fedora:
	@echo "🐳 Building Fedora test container..."
	@docker build -t dotfiles-fedora -f tests/Dockerfile.fedora .
	@echo "✅ Container built! Starting interactive session..."
	@echo ""
	@echo "To test the installation, run:"
	@echo "  ./install.sh"
	@echo "  make test"
	@echo ""
	@docker run --rm -it dotfiles-fedora

# Build and run Ubuntu test container
docker-ubuntu:
	@echo "🐳 Building Ubuntu test container..."
	@docker build -t dotfiles-ubuntu -f tests/Dockerfile.ubuntu .
	@echo "✅ Container built! Starting interactive session..."
	@echo ""
	@echo "To test the installation, run:"
	@echo "  ./install.sh"
	@echo "  make test"
	@echo ""
	@docker run --rm -it dotfiles-ubuntu

# Run both Docker containers for testing
docker-test: docker-fedora docker-ubuntu

# Pull latest changes and reinstall (for syncing remote machines)
latest:
	@echo "🔄 Pulling latest changes from git..."
	@git pull --rebase
	@echo ""
	@echo "📦 Installing latest configuration..."
	@$(MAKE) --no-print-directory install
	@echo ""
	@echo "✅ Successfully synced to latest version!"

# Update packages
update:
	@echo "📦 Updating flake and packages..."
	@nix flake update --refresh
	@nix profile upgrade '.*'
	@echo "✅ Packages updated!"

# Install/upgrade packages from flake
install-packages:
	@echo "📦 Installing packages from flake..."
	@nix profile install . --priority 5
	@echo "✅ Packages installed!"

# Install curated vendor agent skills (Stripe, Resend, etc.)
install-skills:
	@echo "🧠 Installing vendor agent skills..."
	@./scripts/install-skills.sh
	@echo "✅ Skills installed!"

# Update all global agent skills
update-skills:
	@echo "🔄 Updating global agent skills..."
	@./scripts/install-skills.sh --update

# List installed packages
list:
	@echo "📋 Installed packages:"
	@nix profile list

# Clean old packages
clean:
	@echo "🧹 Cleaning old package versions..."
	@nix-collect-garbage -d
	@echo "✅ Cleanup complete!"

# Enter development shell
shell:
	@echo "🐚 Entering Nix development shell..."
	@nix develop

# Start fish shell
fish:
	@echo "🐠 Starting fish shell..."
	@bash -c 'source /nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh 2>/dev/null || true; \
		if command -v fish >/dev/null 2>&1; then \
			if [ -f .envrc ] && command -v direnv >/dev/null 2>&1; then \
				echo "🔓 Allowing direnv for this directory..."; \
				direnv allow; \
			fi; \
			exec fish -l; \
		else \
			echo "❌ Fish not found in PATH."; \
			echo ""; \
			echo "Try running:"; \
			echo "  source /nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh"; \
			echo "  fish"; \
			echo ""; \
			echo "Or run '\''make install'\'' if you haven'\''t already."; \
			exit 1; \
		fi'

# Start documentation dev server
docs:
	@echo "📚 Starting documentation server..."
	@npm --prefix docs start

# Source Nix environment (useful in containers)
source:
	@echo "📦 To source Nix environment, run:"
	@echo ""
	@echo "  source /nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh"
	@echo ""
	@echo "Then you can use 'fish' or any Nix-installed tools."

# Verify Nix installation
verify:
	@echo "🔍 Verifying Nix installation..."
	@command -v nix >/dev/null 2>&1 && echo "✅ Nix is installed: $$(nix --version)" || echo "❌ Nix not found"
	@test -d /nix && echo "✅ /nix directory exists" || echo "❌ /nix directory not found"
	@test -d ~/.nix-profile && echo "✅ Nix profile exists" || echo "⚠️  No user profile (might be multi-user)"
	@command -v fish >/dev/null 2>&1 && echo "✅ Fish is available: $$(fish --version)" || echo "⚠️  Fish not installed yet"

# Diagnostic checks
doctor: verify
	@echo ""
	@echo "🏥 Running diagnostics..."
	@echo ""
	@echo "System: $$(uname -s) $$(uname -m)"
	@echo "Shell: $$SHELL"
	@test -f ~/.config/fish/config.fish && echo "✅ Fish config exists" || echo "⚠️  Fish config not linked"
	@test -L ~/.config/fish && echo "✅ Fish config is symlinked" || echo "⚠️  Fish config is not a symlink"
	@test -f .envrc && echo "✅ .envrc exists" || echo "⚠️  No .envrc file"
	@command -v direnv >/dev/null 2>&1 && echo "✅ direnv available" || echo "⚠️  direnv not installed"
	@command -v starship >/dev/null 2>&1 && echo "✅ starship available" || echo "⚠️  starship not installed"
	@echo ""
	@echo "Run 'make test' to perform full testing"

# Quick setup for new users
.PHONY: quickstart
quickstart:
	@echo "⚡ Quick Start Setup"
	@echo "==================="
	@echo ""
	@echo "1. Installing Nix and packages..."
	@$(MAKE) --no-print-directory install
	@echo ""
	@echo "2. Running tests..."
	@$(MAKE) --no-print-directory test-pre
	@echo ""
	@echo "3. Linking configurations..."
	@$(MAKE) --no-print-directory link
	@echo ""
	@echo "4. Setting up git user..."
	@$(MAKE) --no-print-directory git-user
	@echo ""
	@echo "🎉 Setup complete! Start fish with: make fish"

# Clean everything (use with caution!)
.PHONY: uninstall
uninstall:
	@echo "⚠️  This will remove all symlinks created by the installer"
	@echo "Press Ctrl+C to cancel, or Enter to continue..."
	@read dummy
	@./scripts/cleanup-symlinks.sh
	@echo ""
	@echo "To remove Nix completely, run the official Nix uninstaller"

# Dry-run cleanup to preview what will be removed
.PHONY: uninstall-dry
uninstall-dry:
	@echo "🔍 Preview of what 'make uninstall' will remove:"
	@./scripts/cleanup-symlinks.sh --dry-run
