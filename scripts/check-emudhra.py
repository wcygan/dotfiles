#!/usr/bin/env python3
"""Check real TLS rejection and a healthy control without changing trust stores."""

from __future__ import annotations

import argparse
import concurrent.futures
import shutil
import subprocess
import sys

HOSTS = (
    "dv-g3b-emudhra.we-have-a-problem.com",
    "dv-g3b-aaa-emudhra.we-have-a-problem.com",
    "example.com",
)
NODE_CHECK = """
require('https').get(process.argv[1], response => {
  response.resume();
  console.log('TLS_ACCEPTED');
}).on('error', error => {
  console.error(error.code);
  process.exitCode = 1;
});
"""
FETCH_CHECK = """
fetch(process.argv[1]).then(response => {
  response.body?.cancel();
  console.log('TLS_ACCEPTED');
}).catch(error => {
  console.error(error.code || error.message);
  process.exitCode = 1;
});
"""
PYTHON_CHECK = """
import ssl, sys, urllib.error, urllib.request
try:
    with urllib.request.urlopen(sys.argv[1], timeout=15):
        print('TLS_ACCEPTED')
except urllib.error.URLError as error:
    if isinstance(error.reason, ssl.SSLCertVerificationError):
        print('CERTIFICATE_REJECTED', file=sys.stderr)
    else:
        print(str(error), file=sys.stderr)
    sys.exit(1)
"""
CERT_ERRORS = {
    "CERT_REVOKED",
    "CERT_UNTRUSTED",
    "UNABLE_TO_GET_ISSUER_CERT_LOCALLY",
    "UNABLE_TO_VERIFY_LEAF_SIGNATURE",
    "CERT_SIGNATURE_FAILURE",
    "INVALID_PURPOSE",
    "UNABLE_TO_GET_ISSUER_CERT",
    "CERTIFICATE_REJECTED",
}


def check(task: tuple[str, str, str]) -> tuple[str, bool]:
    kind, executable, host = task
    url = f"https://{host}/"
    command = {
        "curl": [
            executable,
            "-q",
            "--connect-timeout",
            "8",
            "--max-time",
            "15",
            "--silent",
            "--show-error",
            "--output",
            "/dev/null",
            url,
        ],
        "wget": [executable, "--spider", "--timeout=15", "--tries=1", url],
        "python": [executable, "-c", PYTHON_CHECK, url],
        "bun": [executable, "-e", FETCH_CHECK, url],
        "node": [executable, "-e", NODE_CHECK, url],
    }[kind]
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=20)
    except (OSError, subprocess.TimeoutExpired) as error:
        return f"INCONCLUSIVE {executable} {host}: {error}", False
    accepted = result.returncode == 0
    if kind in ("curl", "wget"):
        rejected = result.returncode == {"curl": 60, "wget": 5}[kind]
    else:
        rejected = result.returncode != 0 and result.stderr.strip() in CERT_ERRORS
    healthy = host == "example.com"
    passed = accepted if healthy else rejected
    observation = "accepted" if accepted else "certificate rejected" if rejected else "inconclusive"
    detail = "" if accepted or rejected else f": {result.stderr.strip()}"
    return f"{'PASS' if passed else 'FAIL'} {executable} {host}: {observation}{detail}", passed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--curl", action="append", help="curl executable; repeat to test several")
    parser.add_argument("--node", default=shutil.which("node"), help="Node executable")
    parser.add_argument("--bun", default=shutil.which("bun"), help="Bun executable")
    parser.add_argument("--python", default=sys.executable, help="Python executable")
    parser.add_argument("--wget", default=shutil.which("wget"), help="wget executable")
    args = parser.parse_args()
    curls = args.curl or [shutil.which("curl") or "curl"]
    if not args.curl and sys.platform == "darwin":
        curls.append("/usr/bin/curl")
    clients = [("curl", path) for path in dict.fromkeys(curls)]
    for kind in ("node", "bun", "python", "wget"):
        if executable := getattr(args, kind):
            clients.append((kind, executable))
    tasks = [(kind, path, host) for kind, path in clients for host in HOSTS]
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        results = list(executor.map(check, tasks))
    for message, _ in results:
        print(message)
    return 0 if all(passed for _, passed in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
