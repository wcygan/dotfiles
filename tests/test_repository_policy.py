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

    assert "develop --no-write-lock-file .#default" in bootstrap
    assert "develop --no-write-lock-file .\\#default" in makefile
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
        uses = [line.strip() for line in path.read_text().splitlines() if "uses:" in line]
        assert uses, f"workflow has no actions: {path}"
        assert all(action.search(line) for line in uses), (
            f"mutable or undocumented action in {path}"
        )


def test_reproducible_dockerfiles_pin_manifest_digests() -> None:
    pinned = re.compile(r"^FROM\s+\S+:\S+@sha256:[0-9a-f]{64}(?:\s+AS\s+\S+)?$")

    for path in sorted(REPO_ROOT.glob("Dockerfile.*")):
        from_lines = [line for line in path.read_text().splitlines() if line.startswith("FROM ")]
        assert from_lines
        assert all(pinned.fullmatch(line) for line in from_lines), f"unpinned image in {path}"


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
    assert "needs: [quality, flake-eval, docs, docker-matrix]" in ci
    for job in ("quality", "flake-eval", "docs", "docker-matrix"):
        assert f'test "${{{{ needs.{job}.result }}}}" = success' in ci
    assert "make docs-build" in ci
    assert ci.count("git diff --exit-code") == 4


def test_docs_build_on_pull_requests_and_deploy_only_from_main_push() -> None:
    workflow = REPO_ROOT.joinpath(".github/workflows/deploy-docs.yml").read_text()

    assert "pull_request:" in workflow
    for path in ("docs/**", "README.md", "AGENTS.md", "Makefile"):
        assert path in workflow
    assert "make docs-build" in workflow
    deploy_guard = "github.event_name == 'push' && github.ref == 'refs/heads/main'"
    assert workflow.count(deploy_guard) == 2
    assert "pages: write" in workflow
    assert "id-token: write" in workflow


def test_all_system_evaluation_and_macos_acceptance_are_explicit() -> None:
    flake = REPO_ROOT.joinpath("flake.nix").read_text()
    makefile = REPO_ROOT.joinpath("Makefile").read_text()
    macos = REPO_ROOT.joinpath(".github/workflows/macos.yml").read_text()

    for system in ("x86_64-linux", "aarch64-linux", "x86_64-darwin", "aarch64-darwin"):
        assert flake.count(f'"{system}"') == 1
    assert "flake check --all-systems --no-build --no-write-lock-file" in makefile
    assert "runs-on: macos-15" in macos
    assert "runs-on: macos-15-intel" in macos
    assert "schedule:" in macos and "workflow_dispatch:" in macos
    assert "./bootstrap.sh verify" in macos
    assert "git diff --exit-code" in macos


def test_reproducible_docker_acceptance_is_cached_and_runtime_checked() -> None:
    driver = REPO_ROOT.joinpath("tests/docker_matrix.py").read_text()
    makefile = REPO_ROOT.joinpath("Makefile").read_text()
    dockerignore = REPO_ROOT.joinpath(".dockerignore").read_text()

    acceptance_sources = [
        *REPO_ROOT.glob("Dockerfile.*"),
        REPO_ROOT / "Makefile",
        REPO_ROOT / "tests/docker_matrix.py",
        *REPO_ROOT.joinpath(".github/workflows").glob("*.yml"),
    ]
    assert all("docker-test-commands.fish" not in path.read_text() for path in acceptance_sources)
    assert "buildx" in driver and '"--load"' in driver
    assert "type=gha,scope={scope}" in driver
    assert "type=gha,mode=max,scope={scope}" in driver
    assert (
        "crazy-max/ghaction-github-runtime@"
        in REPO_ROOT.joinpath(".github/workflows/ci.yml").read_text()
    )
    assert "./bootstrap.sh verify" in driver
    assert "__direnv_export_eval" in driver
    assert "python3 tests/docker_matrix.py" in makefile
    assert dockerignore.startswith("**\n")
    for path in sorted(REPO_ROOT.glob("Dockerfile.*")):
        contents = path.read_text()
        assert "COPY --chown=${USER}:${USER} . ." not in contents
        assert "hostname" in contents
        for locked_input in ("flake.lock", "uv.lock", "rust-toolchain.toml"):
            assert locked_input in contents
