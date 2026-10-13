#!/usr/bin/env python3
"""Read one synthetic documentation URL through a local, offline transport."""

import json
from pathlib import Path
import sys
from urllib.parse import urlsplit


def fetch(url):
    parsed = urlsplit(url)
    if parsed.scheme != "https" or parsed.netloc != "docs.example.test":
        raise ValueError("This transport accepts only the synthetic example origin")
    allowed = {
        "/llms.txt": "llms.txt",
        "/docs/llms.txt": "docs/llms.txt",
        "/docs/guides/retries.md": "docs/guides/retries.md",
        "/docs/guides/authentication.md": "docs/guides/authentication.md",
    }
    if parsed.path not in allowed:
        raise ValueError("URL is outside the documentation fixture map")
    fixture = Path(__file__).parent / "fixtures" / allowed[parsed.path]
    if not fixture.is_file():
        return {"url": url, "status": 404, "transport": "local fixture", "body": "Fixture not found"}
    return {"url": url, "status": 200, "transport": "local fixture", "body": fixture.read_text()}


if __name__ == "__main__":
    try:
        print(json.dumps(fetch(sys.argv[1]), indent=2))
    except (ValueError, IndexError) as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(2)
