#!/usr/bin/env python3
import argparse
import json
import re
import subprocess
import sys
import time
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path


REPO = "pingcap/tidb"
DEFAULT_QUERY = 'repo:pingcap/tidb is:issue label:"report/customer" label:"sig/planner" created:>=2024-01-01'
DEFAULT_OUT_DIR = Path("outputs/tidb-customer-planner-issues")
MAX_RETRIES = 3
SLEEP_SECS = 0.15


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate a local markdown corpus from GitHub issue and PR history."
    )
    parser.add_argument(
        "--repo",
        default=REPO,
        help="GitHub repository in owner/name form. Default: pingcap/tidb",
    )
    parser.add_argument(
        "--query",
        default=DEFAULT_QUERY,
        help="GitHub issue search query used by gh api search/issues.",
    )
    parser.add_argument(
        "--out-dir",
        default=str(DEFAULT_OUT_DIR),
        help="Directory where issue markdown files and README.md are written.",
    )
    return parser.parse_args()


def run(cmd):
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(
            f"command failed: {' '.join(cmd)}\nstdout:\n{proc.stdout}\nstderr:\n{proc.stderr}"
        )
    return proc.stdout


def gh_json(args):
    last_err = None
    for _ in range(MAX_RETRIES):
        try:
            out = run(["gh", "api", *args])
            return json.loads(out)
        except Exception as exc:
            last_err = exc
            time.sleep(0.5)
    raise last_err


def fetch_search_issues(query):
    issues = []
    page = 1
    while True:
        data = gh_json(
            [
                "search/issues",
                "-X",
                "GET",
                "-f",
                f"q={query}",
                "-f",
                "per_page=100",
                "-f",
                f"page={page}",
            ]
        )
        items = data.get("items", [])
        if not items:
            break
        issues.extend(items)
        if len(items) < 100:
            break
        page += 1
        time.sleep(SLEEP_SECS)
    return issues


def fetch_timeline(repo, issue_number):
    page = 1
    items = []
    while True:
        batch = gh_json(
            [
                f"repos/{repo}/issues/{issue_number}/timeline",
                "-X",
                "GET",
                "-H",
                "Accept: application/vnd.github+json",
                "-f",
                "per_page=100",
                "-f",
                f"page={page}",
            ]
        )
        if not batch:
            break
        items.extend(batch)
        if len(batch) < 100:
            break
        page += 1
        time.sleep(SLEEP_SECS)
    return items


def fetch_pr(repo, pr_number):
    return gh_json([f"repos/{repo}/pulls/{pr_number}"])


def fetch_pr_files(repo, pr_number):
    files = []
    page = 1
    while True:
        batch = gh_json(
            [
                f"repos/{repo}/pulls/{pr_number}/files",
                "-X",
                "GET",
                "-f",
                "per_page=100",
                "-f",
                f"page={page}",
            ]
        )
        if not batch:
            break
        files.extend(batch)
        if len(batch) < 100:
            break
        page += 1
        time.sleep(SLEEP_SECS)
    return files


def slugify(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = text.strip("-")
    return text[:80] or "issue"


def issue_type(labels):
    for label in labels:
        name = label["name"]
        if name.startswith("type/"):
            return name
    return "type/unknown"


def label_names(labels):
    return sorted(label["name"] for label in labels)


def sanitize_text(text):
    text = text.replace("\r\n", "\n")
    text = re.sub(r"<![\s\S]*?-->", "", text)
    text = re.sub(r"https://github\.com/[^\s)]+", "", text)
    text = re.sub(r"https?://[^\s)]+", "", text)
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", text)
    text = re.sub(r"<img[^>]*>", "", text)
    text = re.sub(r"`{3}[\s\S]*?`{3}", "", text)
    text = re.sub(r"`[^`]*`", "", text)
    text = re.sub(r"^#+\s*", "", text, flags=re.M)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def parse_iso8601(ts):
    if not ts:
        return None
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


def extract_section(body, heading):
    pattern = re.compile(rf"{re.escape(heading)}\s*(.*?)(?=\n### |\n## |\Z)", re.S)
    match = pattern.search(body)
    if match:
        return sanitize_text(match.group(1))
    return ""


def extract_phenomenon(body):
    body = body or ""
    for heading in [
        "### 3. What did you see instead (Required)",
        "### 1. Minimal reproduce step (Required)",
        "### What did you see instead (Required)",
        "### Problem Summary",
        "## Problem Summary",
    ]:
        section = extract_section(body, heading)
        if section:
            lines = [ln.strip("- ").strip() for ln in section.splitlines() if ln.strip()]
            lines = [ln for ln in lines if not ln.startswith("<!--")]
            lines = [
                ln
                for ln in lines
                if "What is your TiDB version" not in ln
                and "Paste the output" not in ln
                and "Please answer these questions" not in ln
                and "tidb version is" not in ln.lower()
                and "release version" not in ln.lower()
                and ln.lower() != "master"
                and not re.fullmatch(r"v?\d+(\.\d+)+", ln.lower())
            ]
            if lines:
                candidate = " ".join(lines[:4]).strip()
                if len(candidate) >= 20:
                    return candidate[:1200]
    fallback = sanitize_text(body)
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", fallback) if p.strip()]
    bad_prefixes = (
        "Bug Report",
        "Enhancement",
        "Feature Request",
        "Please answer these questions",
        "Minimal reproduce step",
        "What did you expect to see",
        "What did you see instead",
        "What is your TiDB version",
        "Compatibility Conclusion",
    )
    for para in paragraphs:
        if para.startswith(bad_prefixes):
            continue
        if len(para) < 20:
            continue
        if para.lower() == "master":
            continue
        if "tidb version is" in para.lower() or "release version" in para.lower():
            continue
        if re.fullmatch(r"v?\d+(\.\d+)+", para.lower()):
            continue
        return " ".join(para.split())[:1200]
    lines = [ln.strip("- ").strip() for ln in fallback.splitlines() if ln.strip()]
    lines = [ln for ln in lines if not ln.startswith("Please answer these questions")]
    return " ".join(lines[:4])[:1200]


def parse_pr_numbers_from_timeline(timeline):
    explicit = []
    refs = []
    seen_explicit = set()
    seen_refs = set()
    for item in timeline:
        if item.get("event") == "cross-referenced":
            src = item.get("source", {}).get("issue", {})
            if src.get("pull_request") and src.get("number"):
                num = src["number"]
                if num not in seen_refs:
                    seen_refs.add(num)
                    refs.append(num)
        if item.get("event") == "commented":
            body = item.get("body", "") or ""
            target = explicit if re.search(r"(fix|fixed|close|closed|resolve|resolved)\s+by", body, re.I) else refs
            seen = seen_explicit if target is explicit else seen_refs
            for num in re.findall(r"/pull/(\d+)", body):
                number = int(num)
                if number not in seen:
                    seen.add(number)
                    target.append(number)
    ordered = explicit + [number for number in refs if number not in seen_explicit]
    return ordered, set(explicit)


def module_bucket(path):
    if path.startswith("pkg/planner/core"):
        return "pkg/planner/core"
    if path.startswith("pkg/planner/"):
        return "pkg/planner"
    if path.startswith("pkg/statistics"):
        return "pkg/statistics"
    if path.startswith("pkg/executor"):
        return "pkg/executor"
    if path.startswith("pkg/parser"):
        return "pkg/parser"
    if path.startswith("pkg/session"):
        return "pkg/session"
    if path.startswith("pkg/infoschema"):
        return "pkg/infoschema"
    parts = path.split("/")
    if len(parts) >= 2:
        return "/".join(parts[:2])
    return parts[0]


def summarize_files(files):
    names = [f["filename"] for f in files]
    buckets = Counter(module_bucket(name) for name in names)
    top_buckets = [name for name, _ in buckets.most_common(6)]
    return top_buckets, names[:20]


def summarize_pr_body(body):
    if not body:
        return ""
    body = sanitize_text(body)
    lines = [ln.strip("- ").strip() for ln in body.splitlines() if ln.strip()]
    useful = []
    for ln in lines:
        if ln.startswith("Issue Number:"):
            continue
        if ln.startswith("Thank you for contributing"):
            continue
        if ln.startswith("PR Title Format:"):
            continue
        if ln.startswith("<!"):
            continue
        if ln.startswith("Check List"):
            break
        if ln.startswith("Release note"):
            break
        useful.append(ln)
    return " ".join(useful[:5])[:800]


def render_issue(issue, pr_details):
    labels = label_names(issue["labels"])
    phenomenon = extract_phenomenon(issue.get("body", ""))
    status = issue["state"]
    issue_num = issue["number"]
    lines = []
    lines.append(f"# Issue #{issue_num}: {issue['title']}")
    lines.append("")
    lines.append("## Metadata")
    lines.append(f"- Issue: {issue.get('html_url', '')}")
    lines.append(f"- Status: {status}")
    lines.append(f"- Type: {issue_type(issue['labels'])}")
    lines.append(f"- Created At: {issue.get('created_at', '')}")
    if issue.get("closed_at"):
        lines.append(f"- Closed At: {issue.get('closed_at', '')}")
    lines.append(f"- Labels: {', '.join(labels)}")
    lines.append("")
    lines.append("## Customer-Facing Phenomenon")
    lines.append(f"- {phenomenon or 'No concise phenomenon text could be extracted automatically.'}")
    lines.append("")
    lines.append("## Linked PRs")
    if not pr_details:
        lines.append("- No linked PR was found from the issue timeline.")
    else:
        for pr in pr_details:
            prefix = "Fix PR" if pr.get("relation") == "explicit_fix" else "Related PR"
            lines.append(f"- {prefix} #{pr['number']}: {pr['title']}")
            lines.append(f"  URL: {pr['html_url']}")
            lines.append(f"  State: {pr['state']}")
            if pr.get("merged_at"):
                lines.append(f"  Merged At: {pr['merged_at']}")
            else:
                lines.append("  Merged At: not merged")
            lines.append(f"  Changed Files Count: {len(pr['files'])}")
            if pr["top_buckets"]:
                lines.append(f"  Main Modules: {', '.join(pr['top_buckets'])}")
            if pr["sample_files"]:
                lines.append("  Sample Changed Files:")
                for path in pr["sample_files"]:
                    lines.append(f"  - {path}")
            if pr.get("body_summary"):
                lines.append(f"  PR Summary: {pr['body_summary']}")
    lines.append("")
    lines.append("## Notes")
    if status == "open":
        lines.append(
            "- This issue is still open. Use this file as a reminder list for customer-driven gaps that still need a fix or a completed rollout."
        )
    elif not any(pr.get("merged_at") for pr in pr_details):
        lines.append(
            "- The issue is closed, but no merged PR was resolved automatically from the timeline. It may have been fixed by an internal branch, a batch PR, or manual closure."
        )
    else:
        lines.append(
            "- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch."
        )
    return "\n".join(lines) + "\n"


def main():
    args = parse_args()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    issues = fetch_search_issues(args.query)
    issues.sort(key=lambda item: item["number"], reverse=True)

    index_lines = [
        "# TiDB Customer Issue Experiences",
        "",
        f"- Repository: `{args.repo}`",
        f"- Source Query: `{args.query}`",
        f"- Total Issues: {len(issues)}",
        "",
        "| Issue | Status | Type | Linked PR Count | File |",
        "| --- | --- | --- | ---: | --- |",
    ]

    for idx, issue in enumerate(issues, start=1):
        issue_number = issue["number"]
        timeline = fetch_timeline(args.repo, issue_number)
        pr_numbers, explicit_prs = parse_pr_numbers_from_timeline(timeline)
        issue_created_at = parse_iso8601(issue.get("created_at"))
        prs = []

        for pr_number in pr_numbers:
            try:
                pr = fetch_pr(args.repo, pr_number)
                body = pr.get("body", "") or ""
                pr_created_at = parse_iso8601(pr.get("created_at"))
                relation = "timeline_ref"

                if pr_number in explicit_prs:
                    relation = "explicit_fix"
                elif re.search(rf"\b(?:fix|fixed|close|closed|resolve|resolved)\s+#?{issue_number}\b", body, re.I):
                    relation = "explicit_fix"
                elif re.search(rf"\bIssue Number:\s*(?:fix|fixed|close|closed|ref)\s+#?{issue_number}\b", body, re.I):
                    relation = "explicit_fix"

                if relation != "explicit_fix" and issue_created_at and pr_created_at:
                    if pr_created_at < issue_created_at - timedelta(days=14):
                        continue

                files = fetch_pr_files(args.repo, pr_number)
                top_buckets, sample_files = summarize_files(files)
                prs.append(
                    {
                        "number": pr["number"],
                        "title": pr["title"],
                        "html_url": pr["html_url"],
                        "state": pr["state"],
                        "merged_at": pr.get("merged_at"),
                        "files": files,
                        "top_buckets": top_buckets,
                        "sample_files": sample_files,
                        "body_summary": summarize_pr_body(body),
                        "relation": relation,
                    }
                )
            except Exception as exc:
                prs.append(
                    {
                        "number": pr_number,
                        "title": f"Failed to fetch PR details: {exc}",
                        "html_url": f"https://github.com/{args.repo}/pull/{pr_number}",
                        "state": "unknown",
                        "merged_at": None,
                        "files": [],
                        "top_buckets": [],
                        "sample_files": [],
                        "body_summary": "",
                        "relation": "timeline_ref",
                    }
                )
            time.sleep(SLEEP_SECS)

        filename = f"issue-{issue_number}-{slugify(issue['title'])}.md"
        path = out_dir / filename
        path.write_text(render_issue(issue, prs), encoding="utf-8")

        index_lines.append(
            f"| #{issue_number} | {issue['state']} | {issue_type(issue['labels'])} | {len(prs)} | [{filename}](./{filename}) |"
        )

        if idx % 10 == 0:
            (out_dir / "README.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")
            print(f"[progress] generated {idx}/{len(issues)} issues", flush=True)

    (out_dir / "README.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")
    print(f"[done] generated {len(issues)} issues into {out_dir}", flush=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)
