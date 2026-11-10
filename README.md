# aunx-skills

[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/aunysillyme-dev/aunx-skills/badge)](https://scorecard.dev/viewer/?uri=github.com/aunysillyme-dev/aunx-skills)

Ten standalone agent skills for things agents quietly get wrong: lost command output, unchecked numbers, incomplete renames, premature failure claims, and lessons saved as rules too soon.

The repository also hosts **Decompose**, a Claude Code plugin that splits a task into checked steps and parallel waves. See [Plugins](#plugins).

Made by Auny LLC. Four packs are free. Six have individual marketplace prices. The bundle of all six paid skills is **$7.99** on Agensi when published. This public repository contains the skill instructions and source under the [MIT license](LICENSE); a marketplace purchase does not grant exclusive access or change those license rights.

## Choose a skill

| Skill | What changes | Price |
|---|---|---|
| [Full Output Keeper](skills/full-output-keeper/SKILL.md) | Keep full command logs, display a bounded view, and retrieve hidden errors. | Free |
| [Number Guard](skills/number-guard/SKILL.md) | Calculate consequential numbers and keep exact values beside rounded ones. | Free |
| [X Spaces Transcriber](skills/x-spaces-transcriber/SKILL.md) | Set up space-tape and transcribe an X Space with speaker labels. | Free |
| [Docs Fetch Ladder](skills/docs-fetch-ladder/SKILL.md) | Find documentation through indexes and Markdown before escalating to scraping. | Free |
| [Absence Check](skills/absence-check/SKILL.md) | Verify query scope, freshness, and completion before reporting absence or failure. | $1 |
| [Instruction Weight](skills/instruction-weight/SKILL.md) | Preserve the difference between a gesture, preference, practice, and rule. | $3 |
| [Rename Sweep](skills/rename-sweep/SKILL.md) | Map a rename across code, docs, settings, and tickets, then verify remaining references. | $3 |
| [Ticket Gate](skills/ticket-gate/SKILL.md) | File actionable issues with artifact-based completion signals. | $3 |
| [Client Work to Template](skills/client-work-to-template/SKILL.md) | Extract a reusable method and check it for client-specific details. | $5 |
| [Retro to Rules](skills/retro-to-rules/SKILL.md) | Turn repeated corrections into numbered proposals for user approval. | $5 |

[Agensi creators](https://agensi.io/creators/aunysillyme)

## Install a pack

Copy one folder from `skills/` into your agent's skills directory. Keep its `SKILL.md`, `LICENSE.txt`, and any `scripts/` or `references/` together. Marketplace `listing.md` is for humans and can be left out of an installation.

| Agent | User directory | Project directory |
|---|---|---|
| Claude Code | `~/.claude/skills/` | `.claude/skills/` |
| Codex CLI | see your agent's skills documentation | `.agents/skills/` |
| Cursor | see your agent's skills documentation | see your agent's skills documentation |
| Gemini CLI | see your agent's skills documentation | see your agent's skills documentation |

Directory discovery varies by installed agent version and configuration. If your version does not discover a pack automatically, ask the agent to read that pack's `SKILL.md` directly. The instructions work with any agent that can read Markdown; shell helpers and network tools require the separate capabilities stated in each pack.

For example, from this repository:

```sh
mkdir -p ~/.claude/skills
cp -R skills/number-guard ~/.claude/skills/
```

Then request: "Use Number Guard to calculate this invoice and show the exact and rounded totals."

## What runs and what changes

These packs are instructions, not background services. Installing them creates no schedule and sends no telemetry. Your agent runs tools only while carrying out a request within your permissions.

Full Output Keeper includes the Python 3 standard-library helper `aunx-keep`. It retains command output in a stated local cache for seven days; commands you choose can have their own side effects. Number Guard uses an available calculator or code tool. X Spaces Transcriber installs and invokes the separate space-tape CLI; package installation and actual transcription need network access, dependencies, and storage. Docs Fetch Ladder uses your available fetch or crawl tools when network access is authorized. The other packs read the task artifacts and write only the destinations you authorize. Read each pack's permissions notes before use.

## Plugins

Plugins are installable bundles for one agent's marketplace. They are separate from the ten skill packs above and are adapted per agent, one folder each under `plugins/`.

| Plugin | Agent | What it does |
|---|---|---|
| [Decompose](plugins/aunx-decompose/README.md) | Claude Code | Split a task into the smallest checkable units, check real data edges, clause coverage, cycles and write-path overlap, show parallel waves and the critical path, and flag big maps for an advisor review. Free, MIT. |

### Decompose: split a task into checked units and parallel waves

Decompose is a free Claude Code plugin that turns a task into the smallest units that can each be checked, and shows which units can run at the same time. Claude writes the plan. A Python helper that uses only the standard library rejects dependency cycles, false and missing data edges, clauses of the ask with no unit, relative write paths and overlapping writes. It prints a plan table with waves, the critical path and clause coverage, and flags big or serial maps for an advisor review before models and machines are picked. A written method covers those picks.

**Use it when** a task has several steps, some steps can run in parallel, more than one agent or subagent may edit files, or you want a plan that a script can verify instead of a plan that only reads well.

**Skip it when** the task is a single step or you only need a prose outline. It works alongside plan mode and to-do lists and does not replace them.

**Privacy.** It runs on your machine. It makes no network requests, sends no data, and has no hooks or MCP servers. It writes only when you save a recipe, to `~/.claude/decompose/recipes.json`.

Install from the Claude Code marketplace in this repository:

```sh
claude plugin marketplace add aunysillyme-dev/aunx-skills
claude plugin install aunx-decompose@aunx
```

Or install it as a standalone skill with `npx aunx-decompose install` (npm) or `npx skills add aunysillyme-dev/aunx-skills --skill decompose` (skills.sh).

Then ask Claude to split a task into steps, or run `/aunx-decompose:decompose <task>`.

## Demos and packaging

[Demos](demos/) contain synthetic sample inputs and actual results. The X Spaces demo demonstrates offline installation and CLI help only. The documentation demo uses local fixtures, so it proves the selection workflow rather than live site access. None of the demos use client records.

```sh
python3 scripts/check.py
python3 scripts/pack.py
```

The packager writes ten versioned zip files to `dist/`, one per skill. Each zip has an installable folder containing `SKILL.md`, `LICENSE.txt`, and any references or scripts. Listings, logos, and demos remain outside the pack zips. `dist/` is ignored by git. Use `--version 1.0.1` to set a release version. The checker also accepts `--scrub /path/to/private-patterns.txt`, with one case-insensitive regex per non-comment line; keep that file outside the repository. It scans repo text and generated zip members and reports locations without echoing private patterns.

Repository scripts require Python 3.9 or later and its standard library; the checker also uses read-only git file enumeration. The checker reads artifacts and reports every failure with a nonzero exit status. It writes no report files. The packager reads pack files and writes or replaces only the selected version's archives. After editing a pack, rebuild its archives and run the checker with any authorized external scrub list before release. Nothing watches these scripts: the caller starts them and checks their exit codes. `scripts/check.py` and `scripts/pack.py` define their behavior. To regenerate the original logo family, run `python3 scripts/aunx-logos.py` with `rsvg-convert` installed; it writes SVG and PNG files under `logos/`.

## Questions people ask

### What is an agent skill pack?

A folder with `SKILL.md` instructions that teach an agent when and how to use a repeatable method. A pack may include a helper script or reference document.

### Do these skills work with Claude Code, Codex, Cursor, and Gemini CLI?

They use plain Markdown with YAML `name` and `description` fields. Those agents can read them, though discovery paths and available execution tools depend on the installed version. Cross-agent automatic activation has not been tested in this repository.

### Which AI agent skills are free?

Full Output Keeper, Number Guard, and Docs Fetch Ladder have free marketplace listings. X Spaces Transcriber is in this repo only. All repository source is public under MIT.

### How much is the paid skill bundle?

The marketplace bundle price is $7.99 for all six paid packs. Publishing and checkout availability are separate from this source repository.

### Can I use a skill without installing an MCP server?

Yes. Most packs use your agent's existing file and command tools. Number Guard can use ordinary code execution or a calculator. X Spaces Transcriber needs space-tape, and live documentation retrieval needs a fetch tool.

### Will a skill edit my rules or file tickets automatically?

The instructions keep actions within the request. Retro to Rules requires approval of specific numbered changes before updating persistent behavior files. Ticket Gate evaluates a candidate before filing and uses artifact evidence before closing.

### What does the Decompose plugin do?

It splits a task into small typed units, checks them for dependency cycles, false or missing data edges, uncovered clauses and overlapping writes, and shows which units can run in parallel. The plugin plans work and does not run it. See [Plugins](#plugins).

### How do I install the Decompose plugin or skill?

Run `claude plugin marketplace add aunysillyme-dev/aunx-skills`, then `claude plugin install aunx-decompose@aunx`. As a standalone skill, run `npx aunx-decompose install` or `npx skills add aunysillyme-dev/aunx-skills --skill decompose`. It needs Python 3.8 or later.

### Does Decompose send my tasks anywhere?

No. It makes no network requests and has no hooks or MCP servers. Your steps are read from files on your machine, and only saved recipes are written, to `~/.claude/decompose/recipes.json`.

### What counts as a conflict between two steps?

Two steps that write to the same file or to a parent and child path, compared without regard to letter case or Unicode form. Decompose rejects the plan and names both steps, so you merge them into one step.

### Where are creator credits?

Each applicable pack and marketplace listing carries credits, with the full source, creator, license, and usage table in [CREDITS.md](CREDITS.md).

## Related projects

- [Model Orchestrator](https://github.com/aunysillyme/model-orchestrator): agent model orchestration.
- [Website Build Skill](https://github.com/aunysillyme/website-build-skill): a companion website building skill.
- [Agent Personalizer](https://github.com/aunysillyme/agent-personalizer): agent personalization.

## Credits and license

Technique and tool credits: [rtk by rtk-ai](https://github.com/rtk-ai/rtk), [space-tape by hovtgc](https://github.com/hovtgc/x-spaces-transcription), [codecalc by The-40-Thieves](https://github.com/The-40-Thieves/codecalc), [llms.txt by AnswerDotAI](https://github.com/AnswerDotAI/llms-txt), and [Crawl4AI by unclecode](https://github.com/unclecode/crawl4ai). See [CREDITS.md](CREDITS.md) for licenses and how each is used. The aunx-skills instructions and original helper are [MIT licensed](LICENSE), Copyright (c) 2026 Auny LLC and contributors.
