"""
agents/run_tests_and_publish_inside_notion.py
=============================================
Runs the Playwright test suite and publishes a structured report to Notion.

Usage:
    python3 agents/run_tests_and_publish_inside_notion.py
"""

import json
import os
import platform
import subprocess
from collections import defaultdict
from datetime import datetime

import requests
from dotenv import load_dotenv

load_dotenv()

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_PAGE_ID = os.getenv("NOTION_PAGE_ID")
NOTION_API_URL = "https://api.notion.com/v1/pages"

HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

REPORT_FILE = "/tmp/pytest_report.json"


# ─────────────────────────────────────────────
# STEP 1 — Run tests
# ─────────────────────────────────────────────

def run_tests():
    """Run pytest and save results to a JSON report file."""
    print("Running tests...")
    result = subprocess.run(
        ["pytest", "tests/", "--json-report", f"--json-report-file={REPORT_FILE}", "-v"],
        capture_output=True,
        text=True,
        cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    )
    print(result.stdout)
    return result


# ─────────────────────────────────────────────
# STEP 2 — Parse the JSON report
# ─────────────────────────────────────────────

def parse_report():
    """Parse the JSON report into a structured summary."""
    with open(REPORT_FILE, "r") as f:
        data = json.load(f)

    summary = data.get("summary", {})
    total    = summary.get("total", 0)
    passed   = summary.get("passed", 0)
    failed   = summary.get("failed", 0) + summary.get("error", 0)
    duration = round(data.get("duration", 0), 2)

    pass_rate = f"{round(passed / total * 100)}%" if total > 0 else "0%"

    # Group tests by file
    files = defaultdict(list)
    for test in data.get("tests", []):
        nodeid = test.get("nodeid", "")
        # nodeid format: tests/ui/test_foo.py::ClassName::test_name
        parts = nodeid.split("::")
        file_path = parts[0]                          # e.g. tests/ui/test_foo.py
        file_name = os.path.basename(file_path)       # e.g. test_foo.py
        class_name = parts[1] if len(parts) > 1 else ""
        test_name  = parts[2] if len(parts) > 2 else parts[-1]
        category   = "API" if "/api/" in file_path else "UI"
        outcome    = test.get("outcome", "unknown")
        result_str = "✅ PASS" if outcome == "passed" else "❌ FAIL"

        files[file_name].append({
            "file_path": file_path,
            "class": class_name,
            "test_name": test_name,
            "category": category,
            "outcome": outcome,
            "result": result_str,
        })

    # Count API vs UI
    api_count = sum(1 for tests in files.values() for t in tests if t["category"] == "API")
    ui_count  = sum(1 for tests in files.values() for t in tests if t["category"] == "UI")

    # Collect failed test names
    failed_tests = [
        t for tests in files.values() for t in tests
        if t["outcome"] in ("failed", "error")
    ]

    return {
        "total": total,
        "passed": passed,
        "failed": failed,
        "duration": duration,
        "pass_rate": pass_rate,
        "api_count": api_count,
        "ui_count": ui_count,
        "files": dict(files),
        "failed_tests": failed_tests,
    }


# ─────────────────────────────────────────────
# STEP 3 — Notion block helpers
# ─────────────────────────────────────────────

def cell(text):
    """Build a single Notion table cell with plain text."""
    return [{"type": "text", "text": {"content": str(text)}}]


def table_row(values):
    """Build a Notion table_row block from a list of string values."""
    return {
        "object": "block",
        "type": "table_row",
        "table_row": {"cells": [cell(v) for v in values]},
    }


def table(rows, width, has_header=True):
    """Build a Notion table block. rows[0] is the header if has_header=True."""
    return {
        "object": "block",
        "type": "table",
        "table": {
            "table_width": width,
            "has_column_header": has_header,
            "has_row_header": False,
            "children": [table_row(r) for r in rows],
        },
    }


def h1(text):
    return {"object": "block", "type": "heading_1",
            "heading_1": {"rich_text": [{"type": "text", "text": {"content": text}}]}}


def h2(text):
    return {"object": "block", "type": "heading_2",
            "heading_2": {"rich_text": [{"type": "text", "text": {"content": text}}]}}


def paragraph(text=""):
    return {"object": "block", "type": "paragraph",
            "paragraph": {"rich_text": [{"type": "text", "text": {"content": text}}] if text else []}}


def divider():
    return {"object": "block", "type": "divider", "divider": {}}


def callout(text, emoji):
    return {
        "object": "block",
        "type": "callout",
        "callout": {
            "rich_text": [{"type": "text", "text": {"content": text}}],
            "icon": {"type": "emoji", "emoji": emoji},
            "color": "default",
        },
    }


# ─────────────────────────────────────────────
# STEP 4 — Build the Notion page
# ─────────────────────────────────────────────

def build_notion_page(summary):
    """Assemble the full Notion page matching the established report template."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    status_emoji = "✅" if summary["failed"] == 0 else "❌"
    title = f"Test Run Report — {now} {status_emoji}"

    # ── Top callout ──
    top_callout_text = (
        f"Run Date: {now}  |  "
        f"Total: {summary['total']}  |  "
        f"Passed: {summary['passed']}  |  "
        f"Failed: {summary['failed']}  |  "
        f"Duration: {summary['duration']}s"
    )

    # ── Run Summary table ──
    pass_icon = "✅" if summary["failed"] == 0 else "❌"
    summary_table = table(
        rows=[
            ["Metric",         "Value"],
            ["Run Date",       now],
            ["Total Tests",    str(summary["total"])],
            ["Passed",         f"✅ {summary['passed']}"],
            ["Failed",         f"{pass_icon} {summary['failed']}"],
            ["Pass Rate",      summary["pass_rate"]],
            ["Total Duration", f"{summary['duration']}s"],
            ["API Tests",      f"{summary['api_count']} passed" if summary["failed"] == 0
                               else f"{summary['api_count']} total"],
            ["UI Tests",       f"{summary['ui_count']} passed" if summary["failed"] == 0
                               else f"{summary['ui_count']} total"],
        ],
        width=2,
    )

    # ── Results by File sections ──
    file_sections = []
    for file_name, tests in summary["files"].items():
        file_passed = sum(1 for t in tests if t["outcome"] == "passed")
        file_failed = len(tests) - file_passed
        category    = tests[0]["category"]
        file_emoji  = "✅" if file_failed == 0 else "❌"
        heading_text = f"{file_emoji} {file_name}  [{category}]  —  {file_passed} passed / {file_failed} failed"

        file_table = table(
            rows=[["Class", "Test Name", "Result"]] + [
                [t["class"], t["test_name"], t["result"]] for t in tests
            ],
            width=3,
        )

        file_sections += [h2(heading_text), file_table, paragraph()]

    # ── Failed Tests section ──
    if summary["failed_tests"]:
        failed_section = [
            callout(f"❌ {len(summary['failed_tests'])} test(s) failed on this run.", "❌"),
        ] + [
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {
                        "content": f"{t['class']}::{t['test_name']}"
                    }}]
                },
            }
            for t in summary["failed_tests"]
        ]
    else:
        failed_section = [callout(f"No failures — all {summary['total']} tests passed on this run.", "🎉")]

    # ── Environment table ──
    import subprocess as sp
    playwright_ver = "0.6.2"  # pytest-playwright version

    try:
        requests_ver = sp.check_output(
            ["python3", "-c", "import requests; print(requests.__version__)"],
            text=True
        ).strip()
    except Exception:
        requests_ver = "unknown"

    import pytest
    env_table = table(
        rows=[
            ["Property",  "Value"],
            ["App URL",   "http://192.168.49.2:31885/"],
            ["Platform",  "Minikube (local Kubernetes)"],
            ["Browser",   "Chromium (headless=False)"],
            ["Python",    platform.python_version()],
            ["pytest",    pytest.__version__],
            ["playwright", playwright_ver],
            ["requests",  requests_ver],
        ],
        width=2,
    )

    # ── Assemble all blocks ──
    children = [
        callout(top_callout_text, status_emoji),
        paragraph(),
        h1("Run Summary"),
        summary_table,
        paragraph(),
        divider(),
        h1("Results by File"),
        *file_sections,
        divider(),
        h1("Failed Tests"),
        *failed_section,
        paragraph(),
        divider(),
        h1("Environment"),
        env_table,
    ]

    return {
        "parent": {"page_id": NOTION_PAGE_ID},
        "properties": {
            "title": {"title": [{"type": "text", "text": {"content": title}}]}
        },
        "children": children,
    }


# ─────────────────────────────────────────────
# STEP 5 — Publish to Notion
# ─────────────────────────────────────────────

def publish_to_notion(summary):
    """POST the report page to Notion."""
    payload = build_notion_page(summary)
    response = requests.post(NOTION_API_URL, headers=HEADERS, json=payload)

    if response.status_code == 200:
        page_url = response.json().get("url", "")
        print(f"\nReport published to Notion: {page_url}")
    else:
        print(f"\nFailed to publish: {response.status_code}")
        print(response.text)


# ─────────────────────────────────────────────

if __name__ == "__main__":
    run_tests()
    summary = parse_report()
    print(f"\nResults: {summary['passed']}/{summary['total']} passed, {summary['failed']} failed")
    publish_to_notion(summary)
