#!/usr/bin/env python3
"""Inspect a synthetic export snapshot without external calls."""
import json
import sys


data = json.load(sys.stdin)
control = [page["slug"] for page in data["pages"] if "shipping policy" in page["text"].lower()]
terms = ("refund", "returns", "money back")
matches = [page["slug"] for page in data["pages"] if any(term in page["text"].lower() for term in terms)]
checks = data["checks"]
result = {
    "query": {
        "ran": True,
        "terms": list(terms),
        "control_term": "shipping policy",
        "control_matches": control,
        "target_matches": matches,
    },
    "scope": {
        "source": data["source"],
        "snapshot_time": data["snapshot_time"],
        "included": data["included"],
        "excluded": data["excluded"],
        "complete": data["complete"],
    },
    "job": data["job"],
    "checks": {
        "reported_verdict": data["reported_verdict"],
        "executed": sum(check["status"] in ("passed", "failed") for check in checks),
        "passed": sum(check["status"] == "passed" for check in checks),
        "failed": sum(check["status"] == "failed" for check in checks),
        "skipped": [check for check in checks if check["status"] == "skipped"],
    },
}
print(json.dumps(result, indent=2))
