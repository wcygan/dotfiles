#!/usr/bin/env python3
"""Exercise migrated tools from a Nix profile using disposable fixtures."""

from __future__ import annotations

import argparse
import functools
import hashlib
import http.server
import io
import json
import os
import platform
import shlex
import socket
import subprocess
import tarfile
import tempfile
import threading
import time
import xml.etree.ElementTree as ET
from pathlib import Path

FIRST = (
    "age",
    "age-keygen",
    "sops",
    "act",
    "crane",
    "kubectl",
    "kubent",
    "skaffold",
    "temporal",
    "pnpm",
    "jj",
)
NEXT = (
    "hyperfine",
    "typst",
    "exiftool",
    "pdftotext",
    "pdftoppm",
    "ocrmypdf",
    "ffmpeg",
    "ffprobe",
    "yt-dlp",
    "dot",
)


def run(
    command: list[str],
    *,
    env: dict[str, str],
    cwd: Path,
    timeout: int = 60,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        command,
        cwd=cwd,
        env=env,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )
    if result.returncode:
        raise RuntimeError(
            f"{command[0]} exited {result.returncode}:\n{result.stdout}\n{result.stderr}"
        )
    return result


def first(profile: Path, work: Path, env: dict[str, str]) -> None:
    def cli(name: str, *args: str, timeout: int = 60) -> str:
        return run([str(profile / "bin" / name), *args], env=env, cwd=work, timeout=timeout).stdout

    key = work / "age.key"
    cli("age-keygen", "-o", str(key))
    recipient = cli("age-keygen", "-y", str(key)).strip()
    plain = work / "plain.txt"
    plain.write_text("Nix migration check\n")
    encrypted = work / "encrypted.age"
    cli("age", "-r", recipient, "-o", str(encrypted), str(plain))
    assert cli("age", "-d", "-i", str(key), str(encrypted)) == plain.read_text()
    print("PASS age: encrypt/decrypt round trip", flush=True)

    secret = work / "secret.json"
    secret.write_text('{"message":"Nix migration check"}')
    env["SOPS_AGE_KEY_FILE"] = str(key)
    sealed = work / "sealed.json"
    sealed.write_text(cli("sops", "--encrypt", "--age", recipient, str(secret)))
    assert json.loads(cli("sops", "--decrypt", str(sealed))) == {"message": "Nix migration check"}
    print("PASS sops: encrypt/decrypt JSON with age", flush=True)

    manifest = json.loads(
        cli(
            "kubectl",
            "--kubeconfig=/dev/null",
            "create",
            "configmap",
            "migration-check",
            "--from-literal=message=verified",
            "--dry-run=client",
            "-o",
            "json",
        )
    )
    assert manifest["metadata"]["name"] == "migration-check"
    assert manifest["data"] == {"message": "verified"}
    print("PASS kubectl: generate ConfigMap without contacting a cluster", flush=True)

    deprecated = work / "deployment.yaml"
    deprecated.write_text(
        "apiVersion: extensions/v1beta1\nkind: Deployment\n"
        "metadata:\n  name: migration-check\nspec: {}\n"
    )
    findings = json.loads(
        cli(
            "kubent",
            "--cluster=false",
            "--helm3=false",
            "--filename",
            str(deprecated),
            "--target-version=1.29.0",
            "--output=json",
        )
    )
    assert any(
        item["Name"] == "migration-check" and item["ReplaceWith"] == "apps/v1" for item in findings
    )
    print("PASS kubent: detect a removed Deployment API from a file", flush=True)

    skaffold = work / "skaffold.yaml"
    skaffold.write_text(
        "apiVersion: skaffold/v4beta13\nkind: Config\n"
        "metadata:\n  name: migration-check\nmanifests:\n"
        "  rawYaml:\n    - deployment.yaml\ndeploy:\n  kubectl: {}\n"
    )
    diagnosed = cli("skaffold", "diagnose", "--yaml-only", "-f", str(skaffold))
    assert "migration-check" in diagnosed and "deployment.yaml" in diagnosed
    print("PASS skaffold: resolve a local deployment configuration", flush=True)

    layer = work / "layer.tar"
    with tarfile.open(layer, "w") as archive:
        contents = b"Nix migration check\n"
        entry = tarfile.TarInfo("migration.txt")
        entry.size = len(contents)
        archive.addfile(entry, io.BytesIO(contents))
    image = work / "image.tar"
    cli(
        "crane",
        "append",
        "--new_layer",
        str(layer),
        "--new_tag",
        "migration-check:local",
        "--output",
        str(image),
    )
    cli("crane", "validate", "--tarball", str(image))
    with tarfile.open(image) as archive:
        metadata_file = archive.extractfile("manifest.json")
        assert metadata_file is not None
        metadata = json.load(metadata_file)[0]
        assert metadata["RepoTags"] == ["migration-check:local"]
        layer_file = archive.extractfile(metadata["Layers"][0])
        assert layer_file is not None
        with tarfile.open(fileobj=layer_file) as contents_archive:
            fixture = contents_archive.extractfile("migration.txt")
            assert fixture is not None and fixture.read() == b"Nix migration check\n"
    print("PASS crane: build and validate a local container image", flush=True)

    package = work / "package.json"
    package.write_text(
        json.dumps(
            {
                "name": "nix-migration-check",
                "private": True,
                "scripts": {
                    "verify": (
                        "node -e \"require('fs').writeFileSync('pnpm-result.txt','verified')\""
                    )
                },
            }
        )
    )
    cli("pnpm", "run", "verify")
    assert (work / "pnpm-result.txt").read_text() == "verified"
    print("PASS pnpm: run a package script through Nix Node", flush=True)

    repository = work / "jj-workspace"
    cli("jj", "git", "init", str(repository))
    (repository / "fixture.txt").write_text("verified\n")
    cli("jj", "-R", str(repository), "describe", "-m", "Nix migration")
    assert (
        cli(
            "jj", "-R", str(repository), "log", "-r", "@", "--no-graph", "-T", "description"
        ).strip()
        == "Nix migration"
    )
    assert "fixture.txt" in cli("jj", "-R", str(repository), "file", "list")
    print("PASS jj: track a file and update a disposable repository", flush=True)

    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        port = listener.getsockname()[1]
    address = f"127.0.0.1:{port}"
    with (work / "temporal.log").open("w") as log:
        server = subprocess.Popen(
            [
                str(profile / "bin/temporal"),
                "server",
                "start-dev",
                "--headless",
                "--ip",
                "127.0.0.1",
                "--port",
                str(port),
            ],
            env=env,
            cwd=work,
            stdout=log,
            stderr=subprocess.STDOUT,
        )
        try:
            deadline = time.monotonic() + 45
            while True:
                if server.poll() is not None:
                    raise RuntimeError((work / "temporal.log").read_text())
                result = subprocess.run(
                    [
                        str(profile / "bin/temporal"),
                        "operator",
                        "namespace",
                        "describe",
                        "--namespace",
                        "default",
                        "--address",
                        address,
                    ],
                    env=env,
                    cwd=work,
                    capture_output=True,
                    text=True,
                    timeout=5,
                    check=False,
                )
                if result.returncode == 0:
                    assert "default" in result.stdout
                    break
                if time.monotonic() >= deadline:
                    raise RuntimeError("Temporal dev server did not become ready")
                time.sleep(0.2)
        finally:
            server.terminate()
            try:
                server.wait(timeout=10)
            except subprocess.TimeoutExpired:
                server.kill()
                server.wait()
    print("PASS temporal: start a localhost server and describe its namespace", flush=True)

    workflow_home = work / "act-workspace"
    workflow_home.mkdir()
    run([str(profile / "bin/git"), "init", str(workflow_home)], env=env, cwd=work)
    workflow = workflow_home / "workflow.yaml"
    workflow.write_text(
        "name: migration\non: push\njobs:\n  verify:\n"
        "    runs-on: ubuntu-latest\n    steps:\n"
        "      - run: printf 'NIX_ACT_VERIFIED\\n'\n"
    )
    architecture = "arm64" if platform.machine() in ("arm64", "aarch64") else "amd64"
    result = run(
        [
            str(profile / "bin/act"),
            "-W",
            str(workflow),
            "-j",
            "verify",
            "-P",
            (
                "ubuntu-latest=node:24-bookworm-slim@"
                "sha256:c86ecead9e55a5210ac1727de38a4ca840bf03dcaf34dc9749addbf383b1920c"
            ),
            "--container-architecture",
            f"linux/{architecture}",
            "--pull=false",
        ],
        env=env,
        cwd=workflow_home,
        timeout=180,
    )
    assert "NIX_ACT_VERIFIED" in result.stdout + result.stderr
    print("PASS act: execute a local workflow in Docker", flush=True)


def next_group(profile: Path, work: Path, env: dict[str, str]) -> None:
    def cli(name: str, *args: str, timeout: int = 60) -> str:
        return run([str(profile / "bin" / name), *args], env=env, cwd=work, timeout=timeout).stdout

    benchmark = shlex.join(
        [
            str(profile / "bin/python3"),
            "-c",
            "from pathlib import Path; Path('benchmark-result.txt').write_text('verified')",
        ]
    )
    cli("hyperfine", "--shell=none", "--runs=2", "--export-json", "timings.json", benchmark)
    timings = json.loads((work / "timings.json").read_text())["results"][0]
    if "measurements" in timings:
        assert [item["exit_code"] for item in timings["measurements"]] == [0, 0]
    else:
        assert timings["exit_codes"] == [0, 0]
    assert (work / "benchmark-result.txt").read_text() == "verified"
    print("PASS hyperfine: benchmark a command and export two successful runs", flush=True)

    graph = work / "graph.dot"
    graph.write_text("digraph { nix -> verified; }\n")
    cli("dot", "-Tsvg", str(graph), "-o", "graph.svg")
    document = ET.parse(work / "graph.svg")
    titles = {element.text for element in document.findall(".//{http://www.w3.org/2000/svg}title")}
    assert {"nix", "verified", "nix->verified"} <= titles
    cli("dot", "-Tpng", str(graph), "-o", "graph.png")
    assert (work / "graph.png").read_bytes().startswith(b"\x89PNG\r\n\x1a\n")
    print("PASS graphviz: render two connected nodes to SVG and PNG", flush=True)

    source = work / "page.typ"
    source.write_text(
        "#set page(width: 160mm, height: 90mm, margin: 12mm)\n"
        "#set text(size: 24pt)\nNix migration check\n\nVerified with Nix.\n"
    )
    cli("typst", "compile", str(source), "page.pdf")
    assert (work / "page.pdf").read_bytes().startswith(b"%PDF-")
    print("PASS typst: compile a document to PDF", flush=True)
    assert "Nix migration check" in cli("pdftotext", "page.pdf", "-")
    cli("pdftoppm", "-png", "-r", "160", "-singlefile", "page.pdf", "page")
    assert (work / "page.png").read_bytes().startswith(b"\x89PNG\r\n\x1a\n")
    print("PASS poppler: extract PDF text and rasterize its page", flush=True)

    cli("exiftool", "-overwrite_original", "-Title=Nix migration check", "page.png")
    metadata = json.loads(cli("exiftool", "-json", "-Title", "page.png"))
    assert metadata[0]["Title"] == "Nix migration check"
    print("PASS exiftool: write and read PNG metadata", flush=True)

    scanned = work / "scan.typ"
    scanned.write_text(
        '#set page(width: 160mm, height: 90mm, margin: 0pt)\n#image("page.png", width: 100%)\n'
    )
    cli("typst", "compile", "--no-pdf-tags", str(scanned), "scan.pdf")
    assert "Nix migration check" not in cli("pdftotext", "scan.pdf", "-")
    cli(
        "ocrmypdf",
        "--jobs=1",
        "--language=eng",
        "--output-type=pdf",
        "--optimize=0",
        "--sidecar=ocr.txt",
        "scan.pdf",
        "ocr.pdf",
        timeout=120,
    )
    assert "Nix migration check" in (work / "ocr.txt").read_text()
    assert "Nix migration check" in cli("pdftotext", "ocr.pdf", "-")
    print("PASS ocrmypdf: recover searchable text from a scanned PDF", flush=True)

    cli(
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "error",
        "-f",
        "lavfi",
        "-i",
        "testsrc=size=64x64:rate=1",
        "-f",
        "lavfi",
        "-i",
        "sine=frequency=440:sample_rate=44100:duration=1",
        "-t",
        "1",
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "aac",
        "clip.mp4",
    )
    streams = json.loads(
        cli("ffprobe", "-v", "error", "-count_frames", "-show_streams", "-of", "json", "clip.mp4")
    )["streams"]
    video = next(stream for stream in streams if stream["codec_type"] == "video")
    audio = next(stream for stream in streams if stream["codec_type"] == "audio")
    assert (video["codec_name"], video["width"], video["height"], video["nb_read_frames"]) == (
        "h264",
        64,
        64,
        "1",
    )
    assert (audio["codec_name"], audio["sample_rate"], audio["channels"]) == ("aac", "44100", 1)
    print("PASS ffmpeg: encode and probe an H.264/AAC MP4", flush=True)

    class QuietHandler(http.server.SimpleHTTPRequestHandler):
        def log_message(self, format: str, *args: object) -> None:
            pass

    server = http.server.ThreadingHTTPServer(
        ("127.0.0.1", 0),
        functools.partial(QuietHandler, directory=str(work)),
    )
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        url = f"http://127.0.0.1:{server.server_port}/clip.mp4"
        diagnostics = run(
            [
                str(profile / "bin/yt-dlp"),
                "--ignore-config",
                "--verbose",
                "--no-progress",
                "-o",
                "downloaded.mp4",
                url,
            ],
            env=env,
            cwd=work,
        )
        assert "deno-" in diagnostics.stderr
        assert hashlib.sha256((work / "downloaded.mp4").read_bytes()).digest() == (
            hashlib.sha256((work / "clip.mp4").read_bytes()).digest()
        )
    finally:
        server.shutdown()
        server.server_close()
        thread.join()
    print("PASS yt-dlp: discover packaged Deno and download a localhost video intact", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--group", choices=("first", "next"), required=True)
    parser.add_argument("--profile", type=Path, default=Path.home() / ".nix-profile")
    args = parser.parse_args()
    profile = args.profile.expanduser().resolve()
    for executable in FIRST if args.group == "first" else NEXT:
        path = profile / "bin" / executable
        if not path.is_file() or not os.access(path, os.X_OK):
            raise RuntimeError(f"missing profile executable: {path}")
        if not path.resolve().is_relative_to(Path("/nix/store")):
            raise RuntimeError(f"not a Nix store executable: {path}")

    docker_host = (
        subprocess.check_output(
            [
                str(profile / "bin/docker"),
                "context",
                "inspect",
                "--format",
                "{{.Endpoints.docker.Host}}",
            ],
            text=True,
        ).strip()
        if args.group == "first"
        else ""
    )
    with tempfile.TemporaryDirectory(prefix="dotfiles-cli-check-") as temporary:
        work = Path(temporary)
        home = work / "home"
        home.mkdir()
        env = {
            **os.environ,
            "HOME": str(home),
            "XDG_CONFIG_HOME": str(home / ".config"),
            "XDG_CACHE_HOME": str(home / ".cache"),
            "XDG_DATA_HOME": str(home / ".local/share"),
            "XDG_STATE_HOME": str(home / ".local/state"),
            "PATH": f"{profile}/bin:/usr/bin:/bin:/usr/sbin:/sbin",
            "DOCKER_CONFIG": str(home / ".docker"),
            "DOCKER_HOST": docker_host,
            "KUBECONFIG": str(home / "unused-kubeconfig"),
            "GIT_CONFIG_GLOBAL": str(home / ".gitconfig"),
            "GIT_CONFIG_NOSYSTEM": "1",
            "JJ_CONFIG": "",
            "TEMPORAL_ADDRESS": "",
            "CI": "1",
        }
        env.pop("DOCKER_CONTEXT", None)
        check = first if args.group == "first" else next_group
        check(profile, work, env)


if __name__ == "__main__":
    main()
