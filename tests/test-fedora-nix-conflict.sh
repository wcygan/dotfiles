#!/usr/bin/env bash

# Test script to reproduce the Fedora Nix installation conflict scenario
# This simulates when Nix is installed but not in PATH

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Testing Fedora Nix Conflict Scenario ===${NC}"
echo "This test simulates the case where:"
echo "1. Nix receipt exists at /nix/receipt.json"
echo "2. But 'nix' command is not in PATH"
echo ""

# Build and run Fedora container
echo -e "${BLUE}Building Fedora test container...${NC}"

cat > /tmp/Dockerfile.fedora-nix-test << 'EOF'
FROM fedora:40

# Install dependencies
RUN dnf update -y && \
    dnf install -y \
    curl \
    git \
    sudo \
    which \
    xz \
    tar \
    procps-ng \
    && dnf clean all

# Create test user with sudo
RUN useradd -m -s /bin/bash testuser && \
    echo "testuser ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Simulate partial Nix installation (receipt exists but command not in PATH)
# First, actually install Nix to get a valid receipt
USER testuser
WORKDIR /home/testuser

# Install Nix as testuser
RUN curl --proto '=https' --tlsv1.2 -sSf -L https://install.determinate.systems/nix | sh -s -- install --no-confirm || true

# Now simulate the broken state: receipt exists but nix not in PATH
USER root
RUN if [ -f /nix/receipt.json ]; then \
        echo "Receipt exists, simulating PATH issue..."; \
        # Remove nix from default profile to simulate PATH issue \
        rm -f /etc/profile.d/nix.sh || true; \
    fi

# Copy dotfiles repo
COPY --chown=testuser:testuser . /home/testuser/dotfiles

USER testuser
WORKDIR /home/testuser/dotfiles

# Test the install script
CMD ["bash", "-c", "echo '=== Testing install.sh ==='; ./install.sh 2>&1"]
EOF

# Build the container
docker build -t fedora-nix-test -f /tmp/Dockerfile.fedora-nix-test . 2>&1 | tail -20

echo ""
echo -e "${BLUE}Running test container...${NC}"
docker run --rm fedora-nix-test

echo ""
echo -e "${GREEN}Test complete!${NC}"
echo ""
echo "To debug interactively, run:"
echo "  docker run --rm -it fedora-nix-test bash"
