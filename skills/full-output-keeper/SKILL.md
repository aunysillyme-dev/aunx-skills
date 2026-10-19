---
name: full-output-keeper
description: Use when command output is too long, terminal logs are truncated, or an error may be hidden in omitted lines. Run commands with a bounded head or tail display, preserve their exit status, and retrieve the full saved output by line range or search.
metadata:
  internal: true
---

# Full Output Keeper

## When to use

When a build, test, search, or diagnostic command may produce more output than the agent can read at once, use the bundled Python 3 standard-library helper. When earlier output is already lost, rerun only if the command is safe and the user authorized its effects.

## Steps

1. Resolve `scripts/aunx-keep.py` relative to this skill folder. Read [the operating reference](references/helper.md) when setting a cache location or investigating a helper failure.
2. Choose a useful view: `--head N` for opening context or `--tail N` for a final summary. Add `--max-bytes N` when lines may be large. The footer is outside that display budget.
3. Run the authorized command directly after `--`. Use `-c` only when shell syntax is needed. Preserve the command's returned status.
4. Read the footer: retrieval id, line range, total size and exit code. If storage failed, report the stated failure and avoid promising full recall.
5. Before making a conclusion about omitted errors or warnings, retrieve the relevant range or search the saved output. Keep the id alongside the result so a later turn can retrieve more.

From the skill folder:

```sh
python3 scripts/aunx-keep.py --head 5 -- python3 build.py
python3 scripts/aunx-keep.py --tail 10 -c 'python3 build.py; status=$?; exit "$status"'
python3 scripts/aunx-keep.py read RETRIEVAL_ID --lines 10:30
python3 scripts/aunx-keep.py read RETRIEVAL_ID --grep 'error|failed' -i
python3 scripts/aunx-keep.py read RETRIEVAL_ID
```

Replace `RETRIEVAL_ID` with the id printed by the run. Keep the same cache environment for run and retrieval.

## Output shape

Report `Command exit: N`, the displayed range, total lines and bytes, the retrieval id, and the evidence retrieved to support your conclusion. An exit code proves the command's status; a clean-looking tail alone does not prove success.

## Conditions and actions

- If a command must preserve its exit status, wrap it with the helper instead of piping it into `head` or `tail`.
- If using a shell string with several commands, explicitly preserve the status of the command being evaluated. The helper returns the shell's final status.
- If a command can output credentials or private material, remove or redact them at the source before capture. Cache files are private by permission but are not encrypted or redacted.
- If a retrieval id expires or is missing, report that saved evidence is unavailable. An empty search means no match in that saved output.
- If the command is still running, wait for completion according to the host's time limits. The helper prints after completion and supplies no timeout.

## Example

Request: "Show the first three lines of this diagnostic run and find the error hidden later in the log. Keep its failure status."

Run the diagnostic with `--head 3`. If its footer reports exit 7, retain that failure. Search the retrieval id with `--grep ERROR` and cite the matching original line number before explaining the error.

## Credits

The full-output retrieval and tee pattern is inspired by [rtk by rtk-ai](https://github.com/rtk-ai/rtk), licensed Apache-2.0. This helper is a fresh Python implementation; no upstream code was copied.
