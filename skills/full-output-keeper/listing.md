## Name

Full Output Keeper: Retrieve Truncated Command Logs

## Summary

Keep full command logs retrievable while showing a small head or tail view and preserving the command's exit status.

## Price

Free. Not part of the bundle.

## Full description

A long build or test log can hide the line that explains a failure. Full Output Keeper teaches your agent to run the command through a small local helper, show a manageable view, and keep the full output available by retrieval id.

It is for developers and agents working with terminal logs, test failures, build output, and large searches. After installation, the agent has instructions and a Python standard-library helper for preserving output, reading a line range, or finding an error later. The command's exit status stays visible, even when the displayed lines look ordinary.

The helper runs locally and keeps outputs for seven days. It needs Python 3 and an agent that can execute commands. Installing the skill adds guidance; it does not install a hook or change your shell.

## Use cases

- Read the start of a build log and retrieve a later error.
- Show a test summary while keeping earlier failures available.
- Search saved output for a warning with its original line number.
- Recover context around a matching diagnostic line.
- Share a short command result while retaining a local full log.

## Demo request

"Show the first three lines of the synthetic asset audit. Keep the process failure status, retrieve the hidden error with its original line number, and save the entire output for follow-up."

The real input is `demos/full-output-keeper/diagnostic.py` in this repository.

## Demo result

To run a fresh capture and read it back, create a temporary cache directory:

```sh
CACHE=$(mktemp -d)
AUNX_KEEP_CACHE="$CACHE" python3 skills/full-output-keeper/scripts/aunx-keep.py --head 3 -- python3 demos/full-output-keeper/diagnostic.py
AUNX_KEEP_CACHE="$CACHE" python3 skills/full-output-keeper/scripts/aunx-keep.py read <ID> --grep ERROR
```

The helper returned command exit **7**, displayed lines **1-3 of 14**, and retained all **258 bytes**. Running `read ID --grep ERROR` against the actual saved output returned `12:ERROR missing icon: checkout.svg`. Full retrieval with `read ID` matched the original command output byte for byte; lines 11-13 supplied the surrounding context.

Request, raw view, full output, matched error, range and run result are recorded in `demos/full-output-keeper/`. The demo uses invented data and runs locally.

## FAQ

### How do I recover truncated terminal output?

Run the command through the bundled helper before output is lost. Then retrieve the saved id in full, by line range, or by search. Already-lost output requires a safe, authorized rerun.

### Does piping a command into head preserve its exit code?

Many shells report the last pipeline command's status. This helper runs the child directly and returns its status. If you use shell-string mode, preserve the status of the command you care about inside that string.

### Can an AI agent search a saved build log?

Yes. The helper's `read ID --grep PATTERN` command returns matching lines with their original line numbers. The agent still decides which evidence supports its conclusion.

### How long are command logs kept?

Retrieval ids expire after seven days. A new capture removes recognized cache files older than seven days. No background cleanup runs.

### Where does Full Output Keeper save logs?

It uses `${XDG_CACHE_HOME:-~/.cache}/aunx-keep` by default. Set `AUNX_KEEP_CACHE` to choose another private cache directory.

### Does it send terminal logs to a server?

The helper makes no network calls. Your chosen command can make its own network calls. Logs stay in the selected local cache, with private file permissions and no encryption or automatic redaction.

### Does Full Output Keeper work with my agent?

The instructions work with agents that read SKILL.md. The helper requires Python 3.8 or newer on macOS or Linux and command-execution access; shell-string mode also needs `/bin/sh`.

## Keywords

truncated terminal output, full command output, AI agent logs, preserve exit code, build log search, test failure logs, head tail output, retrieve command logs, Python log helper, Claude Code skill, Codex CLI skill, terminal error recovery

## Tags

ai-agents, developer-tools, devops, testing, llm-ops, productivity

## Compatibility

Claude Code, Codex CLI, Cursor, Gemini CLI, and other agents that read SKILL.md and can execute local commands. Bundled helper: Python 3.8+ standard library on macOS or Linux. No Python packages are required.

## Permissions notes

Reads command arguments, the child's merged stdout/stderr, cache environment variables, and saved cache entries. Writes only helper output and metadata inside its stated cache directory; removes its recognized expired cache files when a new capture runs. Runs the command the user authorized. The helper makes no network calls of its own. Commands retain their own read, write and network behavior. Stored output is neither redacted nor encrypted.

## Credits

Inspired by the retrieval and tee technique in [rtk by rtk-ai](https://github.com/rtk-ai/rtk), Apache-2.0. The helper is reimplemented in Python; no upstream code was copied. Pack copyright: Auny LLC and contributors, MIT.

## Repo link

https://github.com/aunysillyme-dev/aunx-skills/tree/main/skills/full-output-keeper
