## Name

Absence Check: Verify Empty Results and Missing Files

## Summary

Give agents a clear way to verify missing results, pending jobs, and skipped checks before reporting a conclusion.

## Price

$1 standalone. Also in the $7.99 aunx bundle of all six paid skills.

## Full description

An empty search can mean the item is missing, the query missed a spelling, or the source covers only part of the question. A job can still be running. A test summary can say PASS while important checks were skipped.

Absence Check teaches your agent to test the query with a known item, describe the source's coverage and freshness, and inspect completion signals. You get an answer that says exactly what the evidence supports, plus the next check when more evidence is needed.

This pack is for developers, researchers, analysts, and anyone asking an agent whether something exists or whether work finished. It adds instructions rather than a search service. It works with the tools your agent can already use.

## Use cases

- Check an empty repository search before reporting a missing file.
- Describe what an exported document collection can establish.
- Inspect a queued job before calling it failed.
- Read executed and skipped test counts alongside a green summary.
- Confirm a removal claim against a current source and valid query.

## Demo request

"Does this exported handbook contain a refund policy? Did the handbook export fail? Did all checks pass?" The agent used a synthetic local snapshot containing published pages, a queued job, and a test summary.

## Demo result

The real local run found the known shipping-page control and zero matches for refund-related terms. The agent reported "not found in the synthetic handbook export" because drafts, archives, and the live website were excluded. It reported the export as pending because the job was queued without a terminal signal. It reported 1 executed check passed and 1 live-link check skipped, leaving that coverage unverified despite the PASS summary. Execution returned exit code 0 with untruncated output. Inputs, source, receipt, and actual output are in `demos/absence-check/` in the repository.

## FAQ

### How do I verify an empty search result?

Run a known-item control with the same tool and filters, then check whether the searched source covers your question. The skill guides the agent through those steps.

### Does no search result mean a file does not exist?

It means the query found no match in its searched scope. A broader claim needs complete coverage, current evidence, and a valid query.

### How can an AI agent tell whether a job failed?

It checks the tool's terminal status or process exit code. If completion has not arrived within an appropriate stated limit, it reports the job as pending or unverified.

### Do skipped tests count as passed tests?

Skipped checks provide no execution evidence for the behavior they cover. The skill reports executed and skipped checks separately.

### Does Absence Check install a search tool?

No. It is an instruction pack that uses the agent's existing authorized search and execution tools.

### Can I use Absence Check without network access?

Yes. Local files, logs, and snapshots can be checked offline. The answer remains scoped to those sources.

## Keywords

empty search results, missing files, verify absence, AI agent verification, zero results, failed jobs, pending jobs, skipped tests, test coverage, evidence checking, repository search, source freshness

## Tags

ai-agents, productivity, developer-tools, research, testing

## Compatibility

Claude Code, Codex CLI, Cursor, Gemini CLI, and any agent that reads SKILL.md. Requires tools capable of reading the sources being checked; no specific search provider is required.

## Permissions notes

Reads only sources authorized for the task. It may run search or inspection commands through the agent's existing tools. The pack has no executable helper and makes no network calls of its own. Remote searches need an available authorized connector. Saving a report or changing an artifact requires authorization for that destination.

## Credits

Original instructional pack by Auny LLC. No third-party code or repository material is included.

## Repo link

https://github.com/aunysillyme-dev/aunx-skills/tree/main/skills/absence-check
