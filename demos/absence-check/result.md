# Actual result

Refund policy: not found in the synthetic handbook export. The query searched `refund`, `returns`, and `money back`; the same local query method found the known `shipping policy` control in the shipping page. The fixture covers published pages in its local snapshot at `2030-04-12T09:00:00Z`; it excludes drafts, archives, and the live website. This supports a scoped missing-result statement, not a universal absence claim.

Export status: pending. The job reports `queued` and `terminal: false`. The demo inspected a static snapshot once and performed no polls or wait. No terminal failure signal is present in that snapshot.

Checks: 1 executed and passed, 0 failed, and 1 skipped (`live-links`). The reported `PASS` does not establish live-link coverage. That check remains unverified.

## Run evidence

The local code-execution tool ran `aunx-demo.py` with the exact contents of `input.json` as stdin. It returned exit code 0, verdict OK, empty stderr, and untruncated output. The actual stdout is retained in `stdout.json`; the receipt summary is in `run-proof.json`.

Equivalent hand-run command from the repository root:

```sh
python3 demos/absence-check/aunx-demo.py < demos/absence-check/input.json
```

The command reads stdin and prints evidence. It writes no files and makes no network calls.
