---
name: absence-check
description: Verify empty search results, missing files, zero counts, failed jobs, and skipped tests before reporting absence or failure. Use when asked "does this exist", "is anything left", "did it fail", or "did all tests pass" to give a scoped answer supported by live evidence.
---

# Absence Check

## When to use

Use before reporting "none", "zero", "does not exist", "failed", or "removed" from an empty result, old status report, unfinished job, or green test summary. Apply only to the claim being made and the sources the task permits you to read.

## Steps

1. State the exact claim and identify the source that could prove or disprove it. Ask whether your check could have shown the opposite result. If it could not, choose a check that can.
2. Validate the query. Run a control query for a known item using the same tool, credentials, root, and filters. Preserve errors and exit codes. If the control misses or the tool errors, report the query as unverified and diagnose that condition before interpreting the empty result.
3. Establish coverage. Name the searched source, roots, filters, included record states, snapshot time, and relevant exclusions. Resolve symlinked search roots when the tool does not follow them. Search plausible synonyms, spellings, or identifiers when the source's vocabulary varies. If an authorized semantic search is available, use it when literal terms cannot cover the claim.
4. Establish freshness. Read the current authoritative artifact where available. If you only have a snapshot, describe its timestamp and limits. A saved report or ticket records a prior observation; use it to locate evidence rather than treating it as present state.
5. Establish completion. Read the tool's terminal status or process exit code. For asynchronous work, poll to a stated limit appropriate to the tool and task. If the done signal has not arrived at that limit, report "pending" or "not visible after <observed limit>". Diagnose a terminal error before naming its cause.
6. Inspect actual coverage in test results. Report executed, passed, failed, and skipped checks separately. If relevant checks skipped or have no execution evidence, mark their coverage unverified, even when a summary says PASS.
7. Write the narrowest supported conclusion. If coverage is partial, say "not found in <scope>". If a complete, current source and valid query support an absence claim, qualify it with that source and observation time. If a consequential close or removal decision depends on the conclusion and the first check could not show the opposite, obtain a different check that can before recommending the action.

## Output shape

Return a short answer and this evidence when it affects the conclusion:

```text
Result: found | not found in scope | confirmed absent in scope | pending | failed | unverified
Claim: <what was checked>
Scope and freshness: <source, inclusion rules, exclusions, observation time>
Query evidence: <query, exit/status, control item and result>
Completion or coverage: <terminal signal; or executed/passed/failed/skipped>
Limit: <what this check cannot establish>
Next step: <only if needed to answer the original question>
```

## Conditions and actions

- If a source is incomplete, keep the answer scoped to that source. For a person's experience or history, ask the person when an authorized search cannot answer the question.
- If a file is absent immediately after an asynchronous write, inspect the job's status and documented settling behavior before declaring failure.
- If an empty result has a failing control, fix or report the query condition; make no absence claim from it.
- If command output is filtered or truncated, retrieve the complete relevant evidence and the original command's exit code before deciding.
- If a relevant check was skipped, report its coverage as unverified. A recorded skip is useful evidence about coverage.
- If an absence check requires a write, external call, or deletion outside the user's authorization, stop that action and report the evidence gap.

## Examples

- Request: "Is there a refund policy?" Action: search the permitted document collection for "refund", "returns", and relevant variants, and find a known page as a control. Answer: "Not found in this exported collection; the live website was not checked."
- Request: "Did the export fail?" Action: inspect its terminal status. Answer: "Pending: the job remains queued and has no terminal signal."
- Request: "Did all checks pass?" Action: read execution and skip counts. Answer: "The executed checks passed; skipped checks remain unverified."

## Credits

Original instructional pack by Auny LLC. No third-party code or repository material is included.
