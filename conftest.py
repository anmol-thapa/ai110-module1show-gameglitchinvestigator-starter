import sys
import os
from datetime import datetime

# Allow imports from project root (e.g. logic_utils)
sys.path.insert(0, os.path.dirname(__file__))

# Collect results for markdown report
_results = []


def pytest_runtest_logreport(report):
    if report.when == "call" or (report.when == "setup" and report.failed):
        if report.passed:
            status = "PASS"
        elif report.failed:
            status = "FAIL"
        else:
            status = "SKIP"

        _results.append({
            "name": report.nodeid,
            "status": status,
            "duration": f"{report.duration:.3f}s",
            "message": str(report.longrepr) if report.failed else "",
        })


def pytest_sessionfinish(session, exitstatus):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    passed = sum(1 for r in _results if r["status"] == "PASS")
    failed = sum(1 for r in _results if r["status"] == "FAIL")
    skipped = sum(1 for r in _results if r["status"] == "SKIP")

    lines = [
        f"# Test Results",
        f"",
        f"**Run at:** {now}  ",
        f"**Total:** {len(_results)} | **Passed:** {passed} | **Failed:** {failed} | **Skipped:** {skipped}",
        f"",
        f"| Status | Test | Duration |",
        f"|--------|------|----------|",
    ]

    for r in _results:
        icon = "✅" if r["status"] == "PASS" else ("❌" if r["status"] == "FAIL" else "⏭️")
        lines.append(f"| {icon} {r['status']} | `{r['name']}` | {r['duration']} |")

    failures = [r for r in _results if r["status"] == "FAIL"]
    if failures:
        lines += ["", "## Failures", ""]
        for r in failures:
            lines += [f"### `{r['name']}`", "```", r["message"], "```", ""]

    report_path = os.path.join(os.path.dirname(__file__), "test_results.md")
    with open(report_path, "w") as f:
        f.write("\n".join(lines) + "\n")

    print(f"\nMarkdown report written to test_results.md")