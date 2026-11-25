import io
import json
import zipfile
from pathlib import Path

import pytest


@pytest.mark.parametrize(
    "invalid", [None, "expired", "fork", "pr", "branch", "workflow", "failed", "sha", "key"]
)
def test_receipt_requires_a_matching_successful_main_push(monkeypatch, invalid):
    monkeypatch.syspath_prepend(str(Path(__file__).resolve().parents[1] / "scripts"))
    import ci_evidence

    repo = "owner/repo"
    monkeypatch.setenv("GITHUB_REPOSITORY", repo)
    monkeypatch.setenv("DEFAULT_BRANCH", "main")
    artifact = {
        "id": 21,
        "workflow_run": {"id": 11},
        "name": "evidence-native-key",
        "expired": invalid == "expired",
    }
    run = {
        "head_repository": {"full_name": "other/repo" if invalid == "fork" else repo},
        "head_branch": "topic" if invalid == "branch" else "main",
        "event": "pull_request" if invalid == "pr" else "push",
        "path": "other.yml" if invalid == "workflow" else ".github/workflows/ci.yml",
        "conclusion": "failure" if invalid == "failed" else "success",
        "head_sha": "abc",
        "html_url": "trusted-run",
    }
    archive = io.BytesIO()
    with zipfile.ZipFile(archive, "w") as out:
        out.writestr(
            "receipt.json",
            json.dumps(
                {
                    "job": "native",
                    "fingerprint": "old" if invalid == "key" else "key",
                    "sha": "old" if invalid == "sha" else "abc",
                }
            ),
        )

    def api(endpoint):
        if endpoint.endswith("/zip"):
            return archive.getvalue()
        if "/actions/runs/" in endpoint:
            return json.dumps(run)
        return json.dumps({"artifacts": [artifact]})

    monkeypatch.setattr(ci_evidence, "api", api)
    assert ci_evidence.receipt("native", "key") == (None if invalid else "trusted-run")
