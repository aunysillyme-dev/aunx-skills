---
name: ticket-gate
description: Decide what deserves an issue before filing tasks in GitHub Issues, Jira, or another tracker. Use for issue triage, duplicate tickets, actionable backlog items, acceptance criteria, and evidence-based issue closure.
---

# Ticket Gate

## When to use

Apply this skill when asked to create issues from findings, turn a review into tasks, reduce duplicate tickets, or check whether work is ready to close. Use the user's tracker and existing workflow.

## Steps

1. Read the request and identify the files or repository each candidate touches. Confirm which tracker actions the user authorized. If access or authorization is absent, return drafts and state their status.
2. Search open issues by those files or repository before proposing a new issue. Confirm the search ran and covers the relevant project. Read likely matches. If search access is absent, label deduplication unverified and leave creation pending.
3. Ask these four questions for every candidate. File only when all four answers are yes:
   - Is this a person-sized unit of work?
   - Would the user pick it off the board on purpose?
   - Does it have a done-signal that does not restate the title?
   - Can someone start it today?
4. If any answer is no, place the observation in the review notes or owning documentation. If it is a wait or trigger, add an authorized comment to its dependency issue. If a decision fits in one sentence, handle it in the conversation. Split broad work into independently useful units before reassessing it.
5. If a relevant open issue exists, update or propose an update to that issue. For repeating findings, maintain one rolling issue per finding class and refresh its count, affected items, and remaining work. Preserve existing scope when the match is only related rather than duplicate.
6. Give each new issue a concrete title, context, affected paths, action, owner if known, and a `Completion-signal:` line with a named type from the table below. Follow the tracker's existing labels and state conventions.
7. Limit new issues to five per session by default. Count creations across batches. If more qualify, show the remaining candidates and ask the user to approve a higher session limit before creating them. Updates to existing issues do not consume this creation limit.
8. Before closing an issue, read its current done-signal and inspect the named artifact. Record the evidence and compare it with the signal. If it matches and closure is authorized, close with an evidence comment. If the artifact is missing, stale, inaccessible, or inconclusive, leave the issue open and name the missing proof. For `manual`, obtain the specified person's confirmation as well as the named artifact.

### Done-signal types

| Type | Required proof |
| --- | --- |
| `commit-touches-path` | A commit identifier and inspection showing the specified path changed. Add behavioral verification when the requested outcome requires it. |
| `file-exists` | The named file at the agreed location, inspected for any stated content requirement. |
| `deploy-version` | A deployment identifier and live or authoritative deployment evidence for the requested version. |
| `url-live` | A request to the named URL showing the agreed response or content, using available network permission. |
| `manual` | The named artifact and the specified person's confirmation of the acceptance condition. |

Write the condition explicitly, for example: `Completion-signal: file-exists - docs/health-check.md contains the ready status and operator steps.` A type alone is insufficient. A successful tool call proves only the operation it performed, so select proof that covers the actual acceptance condition.

## Output shape

Return a compact table: candidate, four gate answers, open-issue match, decision, done-signal, and evidence or missing proof. Distinguish created issues from drafts, updated issues from suggested updates, and verified closure from closure proposals. Include the session creation count and limit when filing.

For a closure comment, use: `Verified <condition> against <artifact and identifier>. Evidence: <observed result>.` Include useful retrievable references and omit unrelated private data.

## Conditions and actions

- If a finding repeats, group it under its existing rolling class instead of creating one issue per occurrence.
- If a report says the work is complete, inspect the artifact before closing.
- If a query returns no matches, check its execution and scope before claiming there is no duplicate.
- If an issue must be canceled or its scope changed, follow the user's authorization and tracker conventions; a failed gate alone does not authorize deleting existing work.
- If a tracker tool is unavailable, provide reviewable drafts and identify the unverified search or write.

## Examples

**Filing:** "Turn these review findings into GitHub issues." Search open issues by the touched paths. Route a one-sentence naming decision to the conversation, add repeated link failures to their rolling issue, and draft a startable parser fix with a concrete done-signal.

**Closing:** "Can we close the setup guide ticket?" Read its `file-exists` condition, inspect the guide and required content, and return an evidence-backed closure or the precise unmet condition.

## Credits

Original workflow by Auny LLC. This pack uses generic issue-triage techniques and includes no tracker integration code.
