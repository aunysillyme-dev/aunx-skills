# Decompose

Split tasks into steps, check dependencies and write paths, and show what can
run in parallel. Claude writes the plan; a Python helper validates it. Python
3.8+ and the standard library are enough. No API keys or Python packages needed.

## Install

```bash
claude plugin marketplace add aunysillyme-dev/aunx-skills
claude plugin install aunx-decompose@aunx
```

Use `/decompose <task>` (namespaced as `/decompose:decompose` in Claude Code),
or ask Claude to split a task into steps, plan dependencies, or check write-path
overlap. The plugin plans work and does not execute the plan.

## Example

From `plugins/aunx-decompose` in this repository, create `CARD.md`:

```markdown
---
kind: audit
ask: "Review the parser"
---
```

Run:

```bash
python3 skills/decompose/scripts/decompose.py CARD.md --waves
```

Actual output, exit 0:

```json
[
  [
    {
      "id": "audit",
      "kind": "audit",
      "inputs": [
        "ask"
      ],
      "outputs": [
        "audit-result"
      ],
      "deps": [],
      "paths": [],
      "needs": {
        "cpu": 1,
        "ram_gb": 1,
        "gpu": false,
        "disk_gb": 1,
        "tools": []
      }
    }
  ]
]
```

Each outer array entry is a wave. Independent steps share a wave; every
prerequisite finishes in an earlier wave. Resource and tool availability still
limit execution. Bundled card recipes are `build`, `fix`, `research`, `read`,
and `audit`. Set `ship: no` or `push: no` in a card to omit shipping.

For a custom plan, create a fresh temporary directory:

```bash
steps_dir=$(mktemp -d) || exit 1
steps_file="$steps_dir/steps.json"
```

Write the plan to that new `"$steps_file"` path using the schema in
[SKILL.md](skills/decompose/SKILL.md). Never overwrite an
existing file. Use the same path for each command:

```bash
python3 skills/decompose/scripts/decompose.py --validate "$steps_file" --waves
python3 skills/decompose/scripts/decompose.py --validate "$steps_file" --save-recipe my-plan
```

Exit codes: `0` valid, `2` error, `3` no matching card recipe (a schema is printed
so Claude can write the steps). Validation checks the required fields, known
kinds, unique IDs, known dependencies, cycles, absolute write paths, and
write-path overlap, including parent/child paths, symlink aliases, and existing
paths that refer to the same file. Each part of a resolved path is normalized
to Unicode NFC and case-folded, so paths differing only by Unicode normalization
or letter case are conservatively rejected even when they do not yet exist or
the filesystem treats them as distinct.
Overlapping writes are rejected even between dependent steps. Combine those
writes into one step. Empty `paths` declares no writes.

Recipes save to `$DECOMPOSE_RECIPES` or `~/.claude/decompose/recipes.json`,
creating directories as needed. User recipes override bundled recipes by name;
`tools_by_kind` and `scopes` merge by kind. Saved names must be new. Saved
steps retain their literal inputs and paths. The helper never writes recipes
inside the plugin directory, including case variants and directory aliases.
Concurrent saves hold an exclusive lock beside the recipe store across reading,
checking names, merging, and atomic replacement. On systems without `fcntl`, an
exclusive lock file retries for up to 10 seconds, then reports an error. A stale
lock file left by an interrupted save on those systems must be removed before
saving again.

## What it runs and writes

- Claude runs one Python 3 script, `skills/decompose/scripts/decompose.py`, on the files you name. It uses only the standard library.
- It makes no network requests, sends no data anywhere, installs no packages, and starts no other programs. The plugin has no hooks and no MCP servers.
- It reads the steps or card file you pass and the bundled `recipes.json`.
- It writes only when you save a recipe: to `$DECOMPOSE_RECIPES` or `~/.claude/decompose/recipes.json`, plus a `.lock` file and a temporary file beside it. It never writes inside the plugin folder.
- Claude is told to keep its working `steps.json` in a new temporary directory, so it does not overwrite your files.

## Step kinds

| Kind | Purpose |
| --- | --- |
| `frame` | Plan changes by file. |
| `code` | Make scoped changes. |
| `test-run` | Run the specified checks. |
| `audit-needed` | Decide whether an audit is needed. |
| `ship` | Prepare an authorized release operation. |
| `reproduce` | Reproduce an issue. |
| `search` | Find evidence. |
| `fetch` | Retrieve sources. |
| `extract` | Extract information. |
| `synthesize` | Combine evidence. |
| `read` | Read supplied material. |
| `audit` | Review supplied material. |

Only `code` and `ship` are write kinds. Their `paths` must be absolute and
disjoint across steps. Tool names describe required capabilities, not installed
integrations. Bundled search and fetch steps request `web`.

## Development

From the repository root:

```bash
python3 -m unittest discover -s tests -p test_decompose_plugin.py
claude plugin validate .
claude plugin validate plugins/aunx-decompose
```

For local use without a marketplace install, launch
`claude --plugin-dir ./plugins/aunx-decompose` from the repository root. MIT licensed. See [LICENSE](LICENSE).
