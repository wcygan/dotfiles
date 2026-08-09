# Nix Dotfiles Makefile
# Run `make help` for available commands.

BOOTSTRAP := ./bootstrap.sh
NIX_DEV := nix --extra-experimental-features "nix-command flakes" develop --no-write-lock-file .\#default --command
UV_RUN := $(NIX_DEV) uv run --locked

.PHONY: \
	help install profile install-packages link link-dry git-user rustup setup-rustup-components \
	setup-shell-handoff shell-handoff uninstall uninstall-dry verify doctor \
	test test-pre test-local test-shell test-docker docker-test docker-fedora docker-ubuntu \
	test-syntax test-eval docs-build latest update clean docs quickstart

help:
	@echo "Nix Dotfiles Management"
	@echo ""
	@echo "Setup:"
	@echo "  make install                 - Install profile, links, Rust tools, and verify"
	@echo "  make profile                 - Install or upgrade the Nix package profile"
	@echo "  make link                    - Link managed configuration"
	@echo "  make link-dry                - Preview managed configuration links"
	@echo "  make git-user                - Configure the local Git identity"
	@echo "  make setup-rustup-components - Configure rust-analyzer"
	@echo "  make setup-shell-handoff     - Configure Bash/zsh to launch Fish"
	@echo "  make uninstall               - Remove managed links (asks for confirmation)"
	@echo "  make doctor                  - Run setup diagnostics"
	@echo "  make verify                  - Run strict post-installation acceptance"
	@echo ""
	@echo "Validation:"
	@echo "  make test                    - Run the locked Python test suite in the Nix dev shell"
	@echo "  make test-syntax             - Parse shell and workflow-owned source files"
	@echo "  make test-eval               - Evaluate all four flake systems without building"
	@echo "  make test-docker             - Build Ubuntu and Fedora validation images"
	@echo "  make docs-build              - Install and build documentation reproducibly"

install:
	@$(BOOTSTRAP) install

profile:
	@$(BOOTSTRAP) profile

install-packages: profile

link:
	@$(BOOTSTRAP) link

link-dry:
	@$(BOOTSTRAP) link --dry-run

git-user:
	@$(BOOTSTRAP) git-user

rustup setup-rustup-components:
	@$(BOOTSTRAP) rustup

shell-handoff setup-shell-handoff:
	@$(BOOTSTRAP) shell-handoff

uninstall:
	@$(BOOTSTRAP) uninstall

uninstall-dry:
	@$(BOOTSTRAP) uninstall --dry-run

verify:
	@$(BOOTSTRAP) verify

doctor:
	@$(BOOTSTRAP) doctor

# Python tests supersede the retired shell test harnesses.  Keep the legacy
# target names as aliases so existing local automation remains usable.
test: test-pre

test-pre:
	@$(NIX_DEV) uv lock --check
	@$(UV_RUN) ruff check .
	@$(UV_RUN) pytest

test-local:
	@$(UV_RUN) pytest tests/test_ephemeral.py tests/test_links.py tests/test_cleanup.py

test-shell:
	@$(UV_RUN) pytest tests/test_shell_handoff.py tests/test_fish_config.py

test-syntax:
	@bash -n bootstrap.sh config/shell-nix.sh
	@$(NIX_DEV) bash -c 'for file in config/fish/config.fish config/fish/conf.d/*.fish config/fish/functions/*.fish; do fish --no-execute "$$file" || exit; done'
	@make --dry-run help >/dev/null

test-eval:
	@nix --extra-experimental-features "nix-command flakes" flake check --all-systems --no-build --no-write-lock-file

test-docker:
	@python3 tests/docker_matrix.py $(if $(DOCKER_CASE),--case $(DOCKER_CASE),)

docker-test: test-docker

docker-ubuntu:
	@docker build -f Dockerfile.ubuntu -t nixdotfiles:test-ubuntu .
	@docker run --rm -it nixdotfiles:test-ubuntu /bin/bash

docker-fedora:
	@docker build -f Dockerfile.fedora -t nixdotfiles:test-fedora .
	@docker run --rm -it nixdotfiles:test-fedora /bin/bash

latest:
	@git pull --rebase
	@$(BOOTSTRAP) install

update:
	@nix --extra-experimental-features "nix-command flakes" flake update --refresh
	@$(BOOTSTRAP) profile

clean:
	@nix-collect-garbage -d

docs:
	@npm --prefix docs start

docs-build:
	@npm --prefix docs ci
	@npm --prefix docs run build

quickstart: install test-pre
