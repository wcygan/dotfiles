#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "click>=8.1,<9",
#   "httpx>=0.27,<1",
#   "platformdirs>=4,<5",
#   "pydantic>=2,<3",
#   "pydantic-settings>=2,<3",
#   "pyyaml>=6,<7",
#   "rich>=13,<15",
#   "tenacity>=8.2,<10",
# ]
# ///
"""Gold-standard long-running dev orchestration script.

Run:
    uv run --script orchestrate_dev.py --demo
    uv run --script orchestrate_dev.py --demo --duration 5 --plain
    uv run --script orchestrate_dev.py --config dev-services.yaml
"""

from __future__ import annotations

import os
import shlex
import signal
import socket
import subprocess
import sys
import threading
import time
from collections import deque
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Literal

import click
import httpx
import platformdirs
import yaml
from pydantic import BaseModel, Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from rich import box
from rich.console import Console, Group
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from tenacity import Retrying, retry_if_exception_type, stop_after_delay, wait_fixed

console = Console()
error_console = Console(stderr=True)
SERVICE_STYLE_PALETTE = [
    "cyan",
    "green",
    "yellow",
    "blue",
    "magenta",
    "bright_cyan",
    "bright_green",
    "bright_yellow",
    "bright_blue",
    "bright_magenta",
]


class HealthCheckPending(RuntimeError):
    pass


@dataclass(frozen=True)
class LogEntry:
    timestamp: str
    source: str
    message: str
    style: str


class OrchestratorSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="ORCH_", extra="ignore")

    app_name: str = "uv-scripts-orchestrator"
    refresh_interval: float = 0.25
    shutdown_timeout: float = 5.0
    default_readiness_timeout: float = 15.0


class ComposeSpec(BaseModel):
    project_name: str = "uv-scripts-dev"
    files: list[Path] = Field(default_factory=list)
    profiles: list[str] = Field(default_factory=list)
    services: list[str] = Field(default_factory=list)
    down_on_exit: bool = True


class ServiceSpec(BaseModel):
    name: str
    command: list[str]
    cwd: Path | None = None
    env: dict[str, str] = Field(default_factory=dict)
    depends_on: list[str] = Field(default_factory=list)
    health_url: str | None = None
    readiness_timeout: float | None = None
    optional: bool = False

    @model_validator(mode="after")
    def validate_command(self) -> ServiceSpec:
        if not self.command:
            raise ValueError(f"{self.name}: command must not be empty")
        return self


class DevConfig(BaseModel):
    app_name: str = "uv-scripts-orchestrator"
    docker_compose: ComposeSpec | None = None
    services: list[ServiceSpec]

    @model_validator(mode="after")
    def validate_names(self) -> DevConfig:
        names = [service.name for service in self.services]
        duplicates = sorted({name for name in names if names.count(name) > 1})
        if duplicates:
            raise ValueError(f"duplicate service names: {', '.join(duplicates)}")

        known = set(names)
        for service in self.services:
            missing = sorted(set(service.depends_on) - known)
            if missing:
                raise ValueError(
                    f"{service.name}: unknown dependencies: {', '.join(missing)}"
                )
        return self


class ManagedProcess:
    def __init__(self, spec: ServiceSpec, log_path: Path) -> None:
        self.spec = spec
        self.log_path = log_path
        self.process: subprocess.Popen[str] | None = None
        self.status: Literal[
            "pending", "starting", "online", "running", "failed", "stopped"
        ] = "pending"
        self.started_at: float | None = None
        self.returncode: int | None = None
        self.logs: deque[str] = deque(maxlen=80)
        self.reader: threading.Thread | None = None

    @property
    def pid(self) -> str:
        return str(self.process.pid) if self.process is not None else "-"

    @property
    def uptime(self) -> str:
        if self.started_at is None:
            return "-"
        seconds = max(0, int(time.monotonic() - self.started_at))
        return f"{seconds}s"

    def append_log(self, line: str) -> None:
        self.logs.append(line.rstrip())


class DevSupervisor:
    def __init__(
        self,
        config: DevConfig,
        settings: OrchestratorSettings,
        *,
        log_dir: Path,
        no_docker: bool,
    ) -> None:
        self.config = config
        self.settings = settings
        self.log_dir = log_dir
        self.no_docker = no_docker
        self.processes = {
            service.name: ManagedProcess(service, log_dir / f"{service.name}.log")
            for service in config.services
        }
        self.start_order: list[str] = []
        self.recent_logs: deque[LogEntry] = deque(maxlen=120)
        self.source_styles = {
            "orchestrator": "bright_magenta",
            **{
                service.name: SERVICE_STYLE_PALETTE[index % len(SERVICE_STYLE_PALETTE)]
                for index, service in enumerate(config.services)
            },
        }
        self.compose_started = False
        self.stopping = False
        self.refresh: Callable[[], None] = lambda: None

    def add_event(self, message: str) -> None:
        self.append_log("orchestrator", message)

    def append_log(self, source: str, message: str) -> None:
        self.recent_logs.append(
            LogEntry(
                timestamp=datetime.now().strftime("%H:%M:%S"),
                source=source,
                message=message,
                style=self.source_styles.get(source, "white"),
            )
        )

    def render(self) -> Layout:
        layout = Layout()
        layout.split_column(
            Layout(self.render_services(), name="services", ratio=2),
            Layout(self.render_logs(), name="logs", ratio=3),
            Layout(self.render_footer(), name="footer", size=3),
        )
        return layout

    def render_services(self) -> Panel:
        table = Table(expand=True)
        table.add_column("Service", style="cyan", no_wrap=True)
        table.add_column("Status", no_wrap=True)
        table.add_column("PID", justify="right", no_wrap=True)
        table.add_column("Uptime", justify="right", no_wrap=True)
        table.add_column("Health")
        table.add_column("Command")

        for managed in self.processes.values():
            spec = managed.spec
            command = shlex.join(spec.command)
            health = spec.health_url or "-"
            table.add_row(
                managed.spec.name,
                managed.status,
                managed.pid,
                managed.uptime,
                health,
                command,
            )

        return Panel(table, title="Services", border_style="blue")

    def render_logs(self) -> Panel:
        if not self.recent_logs:
            return Panel(
                Text("waiting for logs...", style="dim"),
                title="Recent Logs",
                border_style="green",
            )

        table = Table(
            box=box.SIMPLE_HEAVY,
            expand=True,
            show_edge=False,
            pad_edge=False,
        )
        table.add_column("Time", style="dim", no_wrap=True, width=8)
        table.add_column("Source", no_wrap=True, width=14)
        table.add_column("Message", overflow="fold")

        for entry in list(self.recent_logs)[-20:]:
            source = Text(f" {entry.source} ", style=f"bold {entry.style}")
            message = Text(entry.message)
            table.add_row(entry.timestamp, source, message)

        return Panel(table, title="Recent Logs", border_style="green")

    def render_footer(self) -> Panel:
        compose = "disabled"
        if self.config.docker_compose is not None:
            compose = "owned" if self.compose_started else "configured"
            if self.no_docker:
                compose = "skipped"
        body = f"logs: {self.log_dir}\ncompose: {compose} | Ctrl+C: graceful cleanup"
        return Panel(body, title="Dev Orchestrator", border_style="magenta")

    def compose_command(self, action: Literal["up", "down"]) -> list[str]:
        compose = self.config.docker_compose
        if compose is None:
            raise ValueError("docker compose is not configured")

        command = ["docker", "compose", "-p", compose.project_name]
        for file in compose.files:
            command.extend(["-f", str(file)])
        for profile in compose.profiles:
            command.extend(["--profile", profile])

        if action == "up":
            command.extend(["up", "-d"])
            command.extend(compose.services)
        else:
            command.extend(["down", "--remove-orphans"])
        return command

    def start_compose(self) -> None:
        if self.no_docker or self.config.docker_compose is None:
            return

        command = self.compose_command("up")
        self.add_event(f"starting docker compose: {shlex.join(command)}")
        subprocess.run(command, check=True)
        self.compose_started = True
        self.add_event("docker compose is online")

    def stop_compose(self) -> None:
        compose = self.config.docker_compose
        if (
            self.no_docker
            or compose is None
            or not self.compose_started
            or not compose.down_on_exit
        ):
            return

        command = self.compose_command("down")
        self.add_event(f"stopping docker compose: {shlex.join(command)}")
        subprocess.run(command, check=False)
        self.compose_started = False

    def dependencies_ready(self, spec: ServiceSpec) -> bool:
        for dependency in spec.depends_on:
            status = self.processes[dependency].status
            if status not in {"online", "running"}:
                return False
        return True

    def start_service(self, managed: ManagedProcess) -> None:
        spec = managed.spec
        env = os.environ.copy()
        env.update(spec.env)
        managed.log_path.parent.mkdir(parents=True, exist_ok=True)
        log_file = managed.log_path.open("w")

        self.add_event(f"starting {spec.name}: {shlex.join(spec.command)}")
        managed.process = subprocess.Popen(
            spec.command,
            cwd=spec.cwd,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            start_new_session=True,
        )
        managed.started_at = time.monotonic()
        managed.status = "starting"
        self.start_order.append(spec.name)

        def read_logs() -> None:
            assert managed.process is not None
            assert managed.process.stdout is not None
            with log_file:
                for line in managed.process.stdout:
                    clean = line.rstrip()
                    log_file.write(clean + "\n")
                    log_file.flush()
                    managed.append_log(clean)
                    self.append_log(spec.name, clean)

        managed.reader = threading.Thread(
            target=read_logs, name=f"{spec.name}-logs", daemon=True
        )
        managed.reader.start()
        self.refresh()

        if spec.health_url is None:
            managed.status = "running"
            self.add_event(f"{spec.name} is running")
            return

        try:
            self.wait_for_health(spec)
        except HealthCheckPending as exc:
            managed.status = "failed"
            raise RuntimeError(f"{spec.name} did not become healthy: {exc}") from exc
        managed.status = "online"
        self.add_event(f"{spec.name} is online")

    def wait_for_health(self, spec: ServiceSpec) -> None:
        timeout = spec.readiness_timeout or self.settings.default_readiness_timeout

        for attempt in Retrying(
            retry=retry_if_exception_type(HealthCheckPending),
            stop=stop_after_delay(timeout),
            wait=wait_fixed(0.5),
            reraise=True,
        ):
            with attempt:
                self.refresh()
                try:
                    response = httpx.get(
                        spec.health_url, timeout=1.0, follow_redirects=True
                    )
                except httpx.HTTPError as exc:
                    raise HealthCheckPending(str(exc)) from exc
                if response.status_code >= 400:
                    raise HealthCheckPending(
                        f"{spec.health_url} returned {response.status_code}"
                    )

    def start_ready_services(self) -> None:
        pending = set(self.processes)
        while pending:
            made_progress = False
            for name in sorted(pending):
                managed = self.processes[name]
                if not self.dependencies_ready(managed.spec):
                    continue
                self.start_service(managed)
                pending.remove(name)
                made_progress = True

            self.update_process_states()
            if not made_progress and pending:
                waiting = ", ".join(sorted(pending))
                self.add_event(f"waiting on dependencies for: {waiting}")
                self.refresh()
                time.sleep(self.settings.refresh_interval)

    def update_process_states(self) -> None:
        for managed in self.processes.values():
            process = managed.process
            if process is None:
                continue
            returncode = process.poll()
            if returncode is None:
                continue
            managed.returncode = returncode
            if self.stopping:
                managed.status = "stopped"
            elif returncode == 0 and managed.spec.optional:
                managed.status = "stopped"
            else:
                managed.status = "failed"

    def failed_processes(self) -> list[ManagedProcess]:
        return [
            managed for managed in self.processes.values() if managed.status == "failed"
        ]

    def run_forever(self, duration: float | None) -> int:
        started = time.monotonic()
        while True:
            self.update_process_states()
            failures = self.failed_processes()
            if failures:
                for failure in failures:
                    self.add_event(
                        f"{failure.spec.name} failed with exit={failure.returncode}"
                    )
                return 1
            if duration is not None and time.monotonic() - started >= duration:
                self.add_event(f"duration reached: {duration}s")
                return 0
            self.refresh()
            time.sleep(self.settings.refresh_interval)

    def stop_all(self) -> None:
        self.stopping = True
        self.add_event("stopping services")
        for name in reversed(self.start_order):
            self.stop_process(self.processes[name])
        self.stop_compose()
        self.refresh()

    def stop_process(self, managed: ManagedProcess) -> None:
        process = managed.process
        if process is None or process.poll() is not None:
            managed.status = "stopped"
            return

        self.add_event(f"stopping {managed.spec.name}")
        terminate_process_group(process)
        try:
            process.wait(timeout=self.settings.shutdown_timeout)
        except subprocess.TimeoutExpired:
            self.add_event(f"killing {managed.spec.name}")
            kill_process_group(process)
            process.wait(timeout=2)
        managed.returncode = process.returncode
        managed.status = "stopped"


def terminate_process_group(process: subprocess.Popen[str]) -> None:
    if hasattr(os, "killpg"):
        os.killpg(process.pid, signal.SIGTERM)
    else:
        process.terminate()


def kill_process_group(process: subprocess.Popen[str]) -> None:
    if hasattr(os, "killpg"):
        os.killpg(process.pid, signal.SIGKILL)
    else:
        process.kill()


def find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def demo_config() -> DevConfig:
    port = find_free_port()
    return DevConfig(
        app_name="uv-scripts-orchestrator-demo",
        services=[
            ServiceSpec(
                name="web",
                command=[
                    sys.executable,
                    "-u",
                    "-m",
                    "http.server",
                    str(port),
                    "--bind",
                    "127.0.0.1",
                ],
                health_url=f"http://127.0.0.1:{port}",
                readiness_timeout=10.0,
            ),
            ServiceSpec(
                name="worker",
                command=[
                    "sh",
                    "-c",
                    "i=0; while true; do i=$((i + 1)); echo worker tick $i; sleep 1; done",
                ],
                depends_on=["web"],
            ),
            ServiceSpec(
                name="scheduler",
                command=[
                    "sh",
                    "-c",
                    "while true; do echo scheduler heartbeat $(date +%H:%M:%S); sleep 2; done",
                ],
            ),
        ],
    )


def load_config(path: Path) -> DevConfig:
    raw = yaml.safe_load(path.read_text())
    if not isinstance(raw, dict):
        raise ValueError(f"{path} must contain a YAML object")
    return DevConfig.model_validate(raw)


def default_log_dir(app_name: str) -> Path:
    return Path(platformdirs.user_log_dir(app_name)) / datetime.now().strftime(
        "%Y%m%d-%H%M%S"
    )


def run_orchestrator(
    config: DevConfig,
    settings: OrchestratorSettings,
    *,
    log_dir: Path,
    no_docker: bool,
    duration: float | None,
    plain: bool,
) -> int:
    supervisor = DevSupervisor(config, settings, log_dir=log_dir, no_docker=no_docker)

    try:
        if plain:
            supervisor.start_compose()
            supervisor.start_ready_services()
            return supervisor.run_forever(duration)

        with Live(supervisor.render(), refresh_per_second=4, screen=False) as live:
            supervisor.refresh = lambda: live.update(supervisor.render(), refresh=True)
            supervisor.start_compose()
            supervisor.start_ready_services()
            return supervisor.run_forever(duration)
    except KeyboardInterrupt:
        error_console.print("[red]interrupted[/red]")
        return 130
    finally:
        supervisor.stop_all()
        console.print(Group(supervisor.render_services(), supervisor.render_footer()))


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.option(
    "--config",
    "config_path",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
)
@click.option(
    "--demo", is_flag=True, help="Run with built-in Linux-friendly example processes."
)
@click.option(
    "--duration", type=float, help="Stop after N seconds. Demo defaults to 8 seconds."
)
@click.option(
    "--log-dir",
    type=click.Path(file_okay=False, path_type=Path),
    help="Directory for service logs.",
)
@click.option(
    "--no-docker", is_flag=True, help="Skip configured Docker Compose startup."
)
@click.option(
    "--plain", is_flag=True, help="Disable the live dashboard; useful for tests and CI."
)
def cli(
    config_path: Path | None,
    demo: bool,
    duration: float | None,
    log_dir: Path | None,
    no_docker: bool,
    plain: bool,
) -> None:
    """Run a local dev process supervisor with logs, health checks, and cleanup."""
    if demo and config_path is not None:
        raise click.UsageError("choose either --demo or --config, not both")
    if not demo and config_path is None:
        raise click.UsageError("provide --config or use --demo")

    settings = OrchestratorSettings()
    config = demo_config() if demo else load_config(config_path)
    if demo and duration is None:
        duration = 8.0

    resolved_log_dir = log_dir or default_log_dir(config.app_name or settings.app_name)
    exit_code = run_orchestrator(
        config,
        settings,
        log_dir=resolved_log_dir,
        no_docker=no_docker,
        duration=duration,
        plain=plain,
    )
    raise click.exceptions.Exit(exit_code)


def main(argv: list[str] | None = None) -> int:
    try:
        cli.main(args=argv, prog_name="orchestrate_dev", standalone_mode=False)
    except click.ClickException as exc:
        exc.show(file=error_console.file)
        return exc.exit_code
    except subprocess.CalledProcessError as exc:
        error_console.print(
            f"[red]command failed[/red] {shlex.join(exc.cmd)} exit={exc.returncode}"
        )
        return exc.returncode or 1
    except FileNotFoundError as exc:
        error_console.print(f"[red]command not found[/red] {exc.filename}")
        return 127
    except (OSError, RuntimeError, ValueError, yaml.YAMLError) as exc:
        error_console.print(f"[red]orchestration failed[/red] {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
