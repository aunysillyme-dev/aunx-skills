"""Real demo and observable contract checks for the bundled aunx-keep helper."""

import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import time


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
HELPER = ROOT / "skills/full-output-keeper/scripts/aunx-keep"


def invoke(cache, *args):
    return subprocess.run([sys.executable, str(HELPER), *args], cwd=ROOT,
                          env={**os.environ, "AUNX_KEEP_CACHE": str(cache)},
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def ident(result):
    return re.search(rb"\[aunx-keep ([0-9a-f]{32}):", result.stdout).group(1).decode()


def main():
    with tempfile.TemporaryDirectory(prefix="aunx-keep-demo-") as demo_dir:
        cache = Path(demo_dir) / "cache"
        run = invoke(cache, "--head", "3", "--", sys.executable,
                     "demos/full-output-keeper/diagnostic.py")
        assert run.returncode == 7 and run.stderr == b"", (run.returncode, run.stderr)
        saved_id = ident(run)
        full = invoke(cache, "read", saved_id)
        search = invoke(cache, "read", saved_id, "--grep", "ERROR")
        sliced = invoke(cache, "read", saved_id, "--lines", "11:13")
        expected = subprocess.run([sys.executable, "demos/full-output-keeper/diagnostic.py"],
                                  cwd=ROOT, stdout=subprocess.PIPE).stdout
        assert full.returncode == 0 and full.stdout == expected
        assert search.stdout == b"12:ERROR missing icon: checkout.svg\n"
        assert sliced.stdout == b"asset 10: checked\nERROR missing icon: checkout.svg\nasset 12: checked\n"

    with tempfile.TemporaryDirectory(prefix="aunx-check-") as folder:
        cache = Path(folder) / "cache"
        binary = invoke(cache, "--tail", "1", "--max-bytes", "6", "--", sys.executable,
                        "-c", "import os; os.write(1, b'first\\nlast\\xff'); raise SystemExit(9)")
        binary_id = ident(binary)
        assert binary.returncode == 9 and binary.stdout.startswith(b"last\xff\n")
        assert invoke(cache, "read", binary_id).stdout == b"first\nlast\xff"
        assert invoke(cache, "read", binary_id, "--grep", "absent").stdout == b""
        meta_path = cache / (binary_id + ".json")
        metadata = json.loads(meta_path.read_text())
        metadata["created"] = time.time() - 604801
        meta_path.write_text(json.dumps(metadata))
        assert invoke(cache, "read", binary_id).returncode == 3
        for path in (meta_path, cache / (binary_id + ".log")):
            os.utime(path, (metadata["created"], metadata["created"]))
        assert invoke(cache, "--", sys.executable, "-c", "print('fresh')").returncode == 0
        assert not meta_path.exists() and not (cache / (binary_id + ".log")).exists()
        assert invoke(cache, "--", "aunx-no-such-command").returncode == 127
    print("PASS: real demo, child failure status, full-byte recall, range, search, tail, expiry, pruning, missing command")


if __name__ == "__main__":
    main()
