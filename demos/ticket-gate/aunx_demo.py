"""Inspect synthetic local issue data and the named closure artifact."""

import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parent
data = json.loads((root / "input.json").read_text())
matches = {}
for candidate in data["candidates"]:
    found = []
    for issue in data["open_issues"]:
        same_class = candidate.get("class") and candidate.get("class") == issue.get("class")
        same_path = any(
            path == known or (known.endswith("/") and path.startswith(known))
            for path in candidate["paths"]
            for known in issue["paths"]
        )
        if same_class or same_path:
            found.append(issue["id"])
    matches[candidate["key"]] = found

artifact = root / "artifacts" / "docs" / "health-check.md"
raw = artifact.read_bytes()
content = raw.decode()
proof = {
    "query_executed": True,
    "scope": "both open issues in the supplied local fixture",
    "matches": matches,
    "artifact": "artifacts/docs/health-check.md",
    "file_exists": artifact.is_file(),
    "ready_status_found": "Status: ready" in content,
    "operator_steps_found": "Operator steps:" in content,
    "sha256": hashlib.sha256(raw).hexdigest(),
    "tracker_writes": False,
}
print(json.dumps(proof, indent=2))
