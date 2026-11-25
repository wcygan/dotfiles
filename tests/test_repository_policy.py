import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_root_agent_instructions_use_live_progressive_disclosure() -> None:
    agents = REPO_ROOT.joinpath("AGENTS.md").read_text()
    operations = REPO_ROOT.joinpath(
        ".agents/skills/dotfiles-operations/SKILL.md"
    ).read_text()
    migrations = REPO_ROOT.joinpath(
        ".agents/skills/dotfiles-operations/references/migrations.md"
    )

    assert "$dotfiles-operations" in agents
    assert "$agent-skills-integration" in agents
    assert "$config-change" in agents
    assert "$fish-shell-config" in agents
    assert "$nix-manager" in agents
    assert "fish-aliases-policy" not in agents
    assert "nix-direnv-perf" not in agents
    assert migrations.is_file()
    assert "references/migrations.md" in operations
    assert "## Migrations" not in agents


def test_agents_md_is_the_only_project_instruction_file() -> None:
    # Claude Code 2.1.277+ loads AGENTS.md itself, but only while no CLAUDE.md
    # exists anywhere in the project; one would also hide docs/AGENTS.md.
    tracked = [*REPO_ROOT.glob("CLAUDE.md"), *REPO_ROOT.glob("*/CLAUDE.md")]

    assert tracked == []
    assert REPO_ROOT.joinpath("AGENTS.md").is_file()
    assert not REPO_ROOT.joinpath("AGENTS.md").is_symlink()


def test_bootstrap_is_the_only_root_setup_shell_entrypoint() -> None:
    automation_scripts = sorted(
        [
            *REPO_ROOT.glob("*.sh"),
            *REPO_ROOT.glob("scripts/**/*.sh"),
            *REPO_ROOT.glob("tests/**/*.sh"),
        ]
    )

    assert automation_scripts == [REPO_ROOT / "bootstrap.sh"]


def test_shell_compatibility_config_remains_declarative() -> None:
    shell_config = REPO_ROOT / "config" / "shell-nix.sh"

    assert shell_config.is_file()
    assert "Shell configuration for Nix package manager" in shell_config.read_text()


def test_tracked_git_config_holds_no_machine_local_values() -> None:
    config = REPO_ROOT.joinpath("config/git/config").read_text()

    assert "path = config.local" in config
    assert "[user]" not in config
    assert "[credential" not in config
    assert "/Users/" not in config and "/home/" not in config


def test_zed_install_task_uses_bootstrap_entrypoint() -> None:
    tasks = json.loads(REPO_ROOT.joinpath(".zed", "tasks.json").read_text())

    install_task = next(task for task in tasks if task["label"] == "Install Dotfiles")
    assert install_task["command"] == "./bootstrap.sh install"


def test_operational_python_is_exactly_3_13() -> None:
    assert sys.version_info[:2] == (3, 13)

    flake = REPO_ROOT.joinpath("flake.nix").read_text()
    assert "python313" in flake
    assert "\n                python3\n" not in flake


def test_nix_consumers_do_not_write_the_committed_lock() -> None:
    bootstrap = REPO_ROOT.joinpath("bootstrap.sh").read_text()
    makefile = REPO_ROOT.joinpath("Makefile").read_text()
    profile = REPO_ROOT.joinpath("src/dotfiles_setup/nix_profile.py").read_text()

    assert 'develop --no-write-lock-file ".#$dev_shell"' in bootstrap
    assert "print-dev-env --no-write-lock-file" in bootstrap
    # Make enters the dev environment only through bootstrap.sh.
    assert 'NIX_DEV := DOTFILES_DEV_SHELL="$(DOTFILES_DEV_SHELL)" $(BOOTSTRAP) --run\n' in makefile
    assert "DOTFILES_DEV_SHELL ?= checks\n" in makefile
    assert " develop " not in makefile
    assert profile.count('"--no-write-lock-file"') == 2
    assert "flake update --refresh" in makefile
    update_recipe = makefile.split("update:", 1)[1].split("\n\n", 1)[0]
    assert "--no-write-lock-file" not in update_recipe

    for path in REPO_ROOT.joinpath(".github/workflows").glob("*.yml"):
        for line in path.read_text().splitlines():
            if "nix develop" in line:
                assert "--no-write-lock-file" in line, f"mutable Nix consumer in {path}"


def test_github_actions_are_pinned_to_full_release_shas() -> None:
    action = re.compile(r"uses:\s+[^@\s]+@([0-9a-f]{40})\s+#\s+v\S+$")

    for path in REPO_ROOT.joinpath(".github/workflows").glob("*.yml"):
        uses = [
            line.strip()
            for line in path.read_text().splitlines()
            # An action in this repository is fixed by the commit that runs it.
            if "uses:" in line and "uses: ./.github/actions/" not in line
        ]
        assert uses, f"workflow has no actions: {path}"
        assert all(action.search(line) for line in uses), (
            f"mutable or undocumented action in {path}"
        )


def test_reproducible_dockerfiles_pin_manifest_digests() -> None:
    pinned = re.compile(r"^FROM\s+\S+:\S+@sha256:[0-9a-f]{64}(?:\s+AS\s+\S+)?$")
    # A stage may also start from an earlier stage of the same file.
    stage = re.compile(r"^FROM\s+(base|acceptance|\$\{INSTALL_BASE\})\s+AS\s+\S+$")

    for path in sorted(REPO_ROOT.glob("Dockerfile.*")):
        from_lines = [line for line in path.read_text().splitlines() if line.startswith("FROM ")]
        assert sum(1 for line in from_lines if pinned.fullmatch(line)) == 2
        assert all(pinned.fullmatch(line) or stage.fullmatch(line) for line in from_lines), (
            f"unpinned image in {path}"
        )


def test_floating_images_are_confined_to_freshness_workflow() -> None:
    ci = REPO_ROOT.joinpath(".github/workflows/ci.yml").read_text()
    makefile = REPO_ROOT.joinpath("Makefile").read_text()
    driver = REPO_ROOT.joinpath("tests/docker_matrix.py").read_text()
    freshness = REPO_ROOT.joinpath(".github/workflows/freshness.yml").read_text()

    assert "--pull" not in ci
    assert "docker build --pull" not in makefile
    assert "--pull" not in driver
    assert "schedule:" in freshness
    assert "workflow_dispatch:" in freshness
    assert "docker build --pull" in freshness
    # The scheduled build also installs with nothing fetched ahead.
    assert "--build-arg INSTALL_BASE=base --target acceptance" in freshness
    assert "s/@sha256:[0-9a-f]{64}//g" in freshness
    assert "docker run --rm" in freshness
    assert "git diff --exit-code" in freshness


def test_dependency_automation_requires_human_review() -> None:
    dependabot = REPO_ROOT.joinpath(".github/dependabot.yml").read_text()

    assert "package-ecosystem: github-actions" in dependabot
    assert "package-ecosystem: docker" in dependabot
    assert "interval: weekly" in dependabot
    workflows = "\n".join(
        path.read_text() for path in REPO_ROOT.joinpath(".github/workflows").glob("*.yml")
    )
    assert "auto-merge" not in workflows.lower()
    assert "automerge" not in workflows.lower()


def test_workflows_use_explicit_runners_least_privilege_and_timeouts() -> None:
    workflows = sorted(REPO_ROOT.joinpath(".github/workflows").glob("*.yml"))

    for path in workflows:
        contents = path.read_text()
        assert "permissions:\n  contents: read" in contents
        assert "ubuntu-latest" not in contents
        assert "macos-latest" not in contents
        job_count = len(re.findall(r"^    runs-on:", contents, re.MULTILINE))
        timeout_count = len(re.findall(r"^    timeout-minutes:", contents, re.MULTILINE))
        assert timeout_count == job_count, f"every job needs a timeout in {path}"


def test_ci_uses_canonical_commands_reports_and_strict_summary() -> None:
    ci = REPO_ROOT.joinpath(".github/workflows/ci.yml").read_text()

    for command in ("make test-pre", "make test-syntax", "make test-eval", "make test-docker"):
        assert command in ci
    assert "--junitxml=reports/pytest.xml" in ci
    assert "actions/upload-artifact@043fb46d1a93c77aae656e7c1c64a875d1fc6a0a" in ci
    assert "if: always()" in ci
    for step in ("doctor", "install", "install", "verify"):
        assert f"          ./bootstrap.sh {step}\n" in ci
    # The summary requires every job, so a job cannot be added and forgotten.
    jobs = re.findall(r"^  ([a-z-]+):$", ci.split("\njobs:\n", 1)[1], re.MULTILINE)
    assert jobs == ["quality", "bootstrap", "docker-matrix", "summary"]
    assert f"needs: [{', '.join(jobs[:-1])}]" in ci
    for job in jobs[:-1]:
        assert f'test "${{{{ needs.{job}.result }}}}" = success' in ci
    assert "make docs-build" in ci
    assert ci.count("git diff --exit-code") == len(jobs) - 1
    # CI enters the dev environment only through make and bootstrap.sh.
    assert "nix develop" not in ci


def test_docs_build_on_pull_requests_and_deploy_only_from_main_push() -> None:
    workflow = REPO_ROOT.joinpath(".github/workflows/deploy-docs.yml").read_text()

    ci = REPO_ROOT.joinpath(".github/workflows/ci.yml").read_text()
    assert "pull_request:" in ci and "make docs-build" in ci
    assert "pull_request:" not in workflow
    for path in ("docs/**", "README.md", "AGENTS.md", "Makefile"):
        assert path in workflow
    assert "make docs-build" in workflow
    deploy_guard = "github.event_name == 'push' && github.ref == 'refs/heads/main'"
    assert workflow.count(deploy_guard) == 2
    assert "pages: write" in workflow
    assert "id-token: write" in workflow


def test_shadow_includes_documentation_only_changes() -> None:
    ci = REPO_ROOT.joinpath(".github/workflows/ci.yml").read_text()

    assert "paths-ignore:" not in ci


def test_all_system_evaluation_and_macos_acceptance_are_explicit() -> None:
    flake = REPO_ROOT.joinpath("flake.nix").read_text()
    makefile = REPO_ROOT.joinpath("Makefile").read_text()
    macos = REPO_ROOT.joinpath(".github/workflows/macos.yml").read_text()

    systems = re.search(r"allSystems = \[(.*?)\];", flake, re.DOTALL)
    assert systems is not None
    assert sorted(re.findall(r'"([^"]+)"', systems[1])) == sorted(
        ("x86_64-linux", "aarch64-linux", "x86_64-darwin", "aarch64-darwin")
    )
    assert "flake check --all-systems --no-build --no-write-lock-file" in makefile
    assert "runs-on: macos-15" in macos
    assert "runs-on: macos-15-intel" in macos
    assert "schedule:" in macos and "workflow_dispatch:" in macos
    assert macos.count("make test-macos") == 2
    assert '["./bootstrap.sh", "verify"]' in REPO_ROOT.joinpath("tests/macos_e2e.py").read_text()
    assert "git diff --exit-code" in macos


def test_reproducible_docker_acceptance_shares_only_the_ubuntu_archive() -> None:
    driver = REPO_ROOT.joinpath("tests/docker_matrix.py").read_text()
    makefile = REPO_ROOT.joinpath("Makefile").read_text()
    dockerignore = REPO_ROOT.joinpath(".dockerignore").read_text()
    ci = REPO_ROOT.joinpath(".github/workflows/ci.yml").read_text()

    acceptance_sources = [
        *REPO_ROOT.glob("Dockerfile.*"),
        REPO_ROOT / "Makefile",
        REPO_ROOT / "tests/docker_matrix.py",
        *REPO_ROOT.joinpath(".github/workflows").glob("*.yml"),
    ]
    assert all("docker-test-commands.fish" not in path.read_text() for path in acceptance_sources)
    assert '"type=cacheonly"' in driver
    assert "type=gha" not in driver
    assert (
        "SEED_DOCKER_CACHE: ${{ matrix.distro == 'ubuntu' && "
        "github.ref == format('refs/heads/{0}', github.event.repository.default_branch) }}"
    ) in ci
    restore = ci.split("Restore Ubuntu's locked-input layers", 1)[1].split("- name:", 1)[0]
    assert "if: steps.inputs.outputs.skip != 'true' && matrix.distro == 'ubuntu'" in restore
    assert "actions/cache/restore@" in restore
    assert (
        "DOCKER_LAYER_CACHE: ${{ (steps.layers.outputs.cache-hit == 'true' "
        "|| env.SEED_DOCKER_CACHE == 'true') && format('{0}/docker-layers', runner.temp) || '' }}"
    ) in ci
    assert 'if [[ -z "$DOCKER_LAYER_CACHE" ]]; then\n            export DOCKER_SKIP_PREWARM=1' in ci
    save = ci.split("Save Ubuntu's locked-input layers", 1)[1].split("\n  summary:", 1)[0]
    assert (
        "if: steps.inputs.outputs.skip != 'true' && env.SEED_DOCKER_CACHE == 'true' "
        "&& steps.layers.outputs.cache-hit != 'true'"
    ) in save
    assert "actions/cache/save@" in save
    assert "key: ${{ steps.layers.outputs.cache-primary-key }}" in save
    assert "python3 tests/docker_matrix.py" in makefile
    assert "python3 tests/docker_matrix.py --target tests" in makefile
    assert dockerignore.startswith("**\n")
    for path in sorted(REPO_ROOT.glob("Dockerfile.*")):
        contents = path.read_text()
        assert "hostname" in contents
        for locked_input in ("flake.lock", "uv.lock", "rust-toolchain.toml"):
            assert locked_input in contents


def _dockerfile_stages(path: Path) -> dict[str, str]:
    stages: dict[str, str] = {}
    name = ""
    for line in path.read_text().splitlines():
        if line.startswith("FROM "):
            name = line.rsplit(" AS ", 1)[1]
        stages[name] = stages.get(name, "") + line + "\n"
    return stages


def test_docker_heavy_layers_depend_only_on_locked_inputs() -> None:
    for path in sorted(REPO_ROOT.glob("Dockerfile.*")):
        stages = _dockerfile_stages(path)
        assert list(stages) == ["", "nix-fixture", "base", "prewarm", "acceptance", "tests"]

        # Nothing from the checkout reaches the image before the prewarm stage.
        assert "COPY --chown" not in stages["base"]
        copies = [line for line in stages["prewarm"].splitlines() if line.startswith("COPY ")]
        assert copies == ["COPY --chown=tester:tester flake.nix flake.lock rust-toolchain.toml ./"]
        assert "bootstrap.sh" not in stages["prewarm"]
        assert stages["prewarm"].count("--no-write-lock-file") == 2
        assert "rustup toolchain install" in stages["prewarm"]


def test_docker_acceptance_proves_install_reinstall_and_the_installed_result() -> None:
    for path in sorted(REPO_ROOT.glob("Dockerfile.*")):
        stages = _dockerfile_stages(path)
        acceptance = stages["acceptance"]

        assert stages[""].count("ARG INSTALL_BASE=prewarm") == 1
        assert acceptance.startswith("FROM ${INSTALL_BASE} AS acceptance\n")
        runs = [line for line in acceptance.splitlines() if line.startswith("RUN ")]
        assert runs[:2] == [
            'RUN NIX_CONFIG="${ACCEPTANCE_NIX_CONFIG:-${NIX_CONFIG:-}}" ./bootstrap.sh install',
            "RUN ./bootstrap.sh install && ./bootstrap.sh profile"
            " && ./bootstrap.sh doctor && ./bootstrap.sh verify",
        ]
        smoke = acceptance.split("RUN <<'SMOKE'\n", 1)[1].split("\nSMOKE\n", 1)[0]
        assert smoke.startswith("#!/bin/bash -l\nset -eu\n")
        for check in (
            'test "$(id -un)" = tester',
            "bash -n bootstrap.sh",
            "./bootstrap.sh verify",
            "command -v fish",
            "command -v rg",
            "command -v nvim",
            "__direnv_export_eval",
        ):
            assert check in smoke
        for installer in ("install.determinate.systems", "curl --proto", "| sh"):
            assert installer not in path.read_text()
        assert "COPY --chown=tester:tester . ." not in acceptance
        assert stages["tests"].rstrip().endswith("RUN make test-syntax test-pre")


def test_distro_dockerfiles_differ_only_in_the_base_packages() -> None:
    marker = "# Shared with the other distro's Dockerfile from here on.\n"
    ubuntu = REPO_ROOT.joinpath("Dockerfile.ubuntu").read_text()
    fedora = REPO_ROOT.joinpath("Dockerfile.fedora").read_text()

    assert ubuntu.count(marker) == fedora.count(marker) == 1
    assert ubuntu.split(marker)[1] == fedora.split(marker)[1]
    assert ubuntu.split("FROM ubuntu:")[0] == fedora.split("FROM fedora:")[0]


def test_manual_runs_force_reference_checks_and_reused_results_cannot_seed_receipts() -> None:
    workflow = REPO_ROOT.joinpath(".github/workflows/ci.yml").read_text()
    assert "github.event_name == 'workflow_dispatch' || vars.CI_FORCE_FULL == 'true'" in workflow
    assert workflow.count("Compare install evidence") == 3
    assert workflow.count("if: success() && steps.inputs.outputs.skip != 'true'") == 3
    assert workflow.count("uses: ./.github/actions/prepare-shadow") == 3
    # A historical checkout may remove local actions before GitHub runs their post hooks.
    assert workflow.count("uses: DeterminateSystems/nix-installer-action@") == 2
    for title in ("Run canonical syntax and quality checks", "Prove native bootstrap idempotency",
                  "Build and run canonical distro acceptance"):
        assert f"- name: {title}\n        if: steps.inputs.outputs.skip != 'true'" in workflow
