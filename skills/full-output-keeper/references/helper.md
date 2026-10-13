# aunx-keep operating reference

## What it does

`aunx-keep` starts the requested process, merges stdout and stderr into one pipe, streams all bytes to a cache file, waits for completion, and displays a whole-line head or tail view. It then prints the saved output's size, exit status and retrieval id. Output order follows the child's writes and buffering.

Dependencies: Python 3.8 or newer with the standard library. Shell-string mode also requires `/bin/sh`. No package install or network call is performed by the helper. Child commands retain their own permissions and dependencies.

## Trigger and invocation chain

Invocation is explicit: agent or human -> `python3 scripts/aunx-keep.py` -> child process -> private cache -> bounded view -> footer -> process exit. No shell profile, hook, PATH entry, daemon or schedule is installed. What watches it: **nothing**. The caller checks its exit status and reads omitted evidence when needed.

Run from the skill folder or supply the helper's actual path. Default view: first 40 lines and at most 12000 source bytes. Set `--head`, `--tail`, or `--max-bytes` to change the view. A line larger than the byte budget is omitted intact. Retrieval preserves the original bytes, including a missing final newline. Search prefixes matching lines with their original line numbers; line ranges are 1-based and inclusive.

## Reads and writes

The helper reads command arguments, the child's merged output, and its existing cache entries. `AUNX_KEEP_CACHE` selects the full cache path. Otherwise it uses `${XDG_CACHE_HOME:-~/.cache}/aunx-keep`. It creates that directory with mode 0700 and output/metadata files with mode 0600. Existing cache directories with other modes, final-path symlinks, linked entry files and entries owned by another user are refused.

The helper writes only inside that cache directory: `.part` while capturing, `.log` for complete output, and `.json` for creation time, command status, line count and byte count. Commands themselves may read, write or make network calls as authorized by the caller. Command strings are not stored. Output is stored verbatim, without encryption or redaction.

Each id is valid for seven days from capture. Expired ids return exit 3 even if files remain. A new capture deletes recognized cache files older than seven days. There is no background expiry and no disk-size cap; choose a cache filesystem with capacity for the full command output. Unrelated files in that directory are left alone.

## Failures and recovery

- A completed child returns its own exit status. Signal termination returns `128 + signal number`.
- A command that cannot start returns 127 when missing, otherwise 126. Usage errors return 2.
- Cache setup failure prevents the command from starting and returns 1 with an error.
- A capture/storage failure after the child starts drains its output and retains the child's status; stderr reports the failure. Full retrieval may be unavailable. Do not infer capture success from the process status alone.
- A missing or expired retrieval id returns 3. Other retrieval errors return 1. A valid search with no match returns 0 and no matching lines.
- A closed display does not override the child's status. The caller still checks whether storage reported success.
- Capture waits until the merged pipe reaches EOF. Background descendants holding that pipe open can delay completion. The host should impose its normal execution deadline when appropriate.

## Hand-run verification

```sh
python3 scripts/aunx-keep.py --head 2 -c 'printf "start\nERROR demo\nend\n"; exit 7'
```

Check the returned status: 7. Copy the printed id into `python3 scripts/aunx-keep.py read ID --grep ERROR`. It must return `2:ERROR demo`. Run `read ID` without filters to retrieve all three lines. If any check fails, retain the error and command status and report the helper/version and a reproducible synthetic input.

Source of truth: `scripts/aunx-keep.py` defines runtime behavior; `SKILL.md` defines the agent workflow. This reference defines operation, retention and recovery.
