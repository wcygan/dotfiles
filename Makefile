# Nix Dotfiles Makefile
# Run 'make help' for available commands

.PHONY: help install test test-pre test-local test-docker link clean update shell

# Default target
help:
	@echo "Nix Dotfiles Management"
	@echo "======================="
	@echo ""
	@echo "Installation:"
	@echo "  make install    - Full installation (Nix + packages + configs)"
	@echo "  make link       - Link configs only (fish, etc.)"
	@echo "  make link-dry   - Preview what link will do"
	@echo ""
	@echo "Testing:"
	@echo "  make test       - Run all tests (pre-flight + local)"
	@echo "  make test-pre   - Pre-flight checks only"
	@echo "  make test-local - Local isolated test"
	@echo "  make test-docker- Docker isolated test"
	@echo "  make docker-fedora - Interactive Fedora container"
	@echo "  make docker-ubuntu - Interactive Ubuntu container"
	@echo ""
	@echo "Package Management:"
	@echo "  make update     - Update flake and upgrade packages"
	@echo "  make list       - List installed packages"
	@echo "  make clean      - Garbage collect old packages"
	@echo ""
	@echo "Development:"
	@echo "  make shell      - Enter Nix development shell"
	@echo "  make fish       - Start fish shell"
	@echo "  make source     - Show command to source Nix environment"
	@echo ""
	@echo "Troubleshooting:"
	@echo "  make verify     - Verify Nix installation"
	@echo "  make doctor     - Run diagnostic checks"

# Full installation
install:
	@echo "🚀 Running full installation..."
	@./install.sh
	@echo "✅ Installation complete!"
	@echo "Run 'make fish' to start fish shell"

# Link configurations only
link:
	@echo "🔗 Linking configurations..."
	@./scripts/link-config.sh
	@echo "✅ Configs linked!"

# Dry run for linking
link-dry:
	@echo "🔍 Preview of link changes..."
	@./scripts/link-config.sh --dry-run

# Run all non-docker tests
test: test-pre test-local
	@echo "✅ All tests completed!"

# Pre-flight checks
test-pre:
	@echo "🔍 Running pre-flight checks..."
	@cd tests && ./test-fish-setup.sh

# Local isolated test
test-local:
	@echo "🧪 Running local isolated test..."
	@cd tests && ./test-ephemeral.sh

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

# Update packages
update:
	@echo "📦 Updating flake and packages..."
	@nix flake update
	@nix profile upgrade '.*'
	@echo "✅ Packages updated!"

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
