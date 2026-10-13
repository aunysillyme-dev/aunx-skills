## Name

Retro to Rules: Learn from Repeated Agent Corrections

## Summary

Turn recurring feedback into evidenced proposals, then save the changes you approve.

## Price

$5 individually. Also in the $7.99 aunx bundle of all six paid skills.

## Full description

An agent can repeat a mistake even when the correction is somewhere in your session notes. Retro to Rules gives those notes a review process: read the entries that have not been reviewed, count repeated corrections, check existing rules, and propose specific behavior changes with source evidence.

The agent presents a numbered list before updating rules or memory. You approve the numbers you want, revise the wording, and defer the rest. After saving approved changes, the agent records the entries actually reviewed so the next sweep has a clear starting point. Late additions and deferred proposals remain visible.

This is for people who already keep session logs, project retrospectives, or agent feedback. It supplies instructions rather than a background service; your agent needs access to the logs and the destinations you authorize.

## Use cases

- Review repeated corrections across coding sessions.
- Propose improvements from project retrospectives.
- Check whether a proposed rule already exists in agent memory.
- Keep workspace-specific feedback within its original scope.
- Resume an incremental review after new log entries arrive.
- Approve selected changes while retaining deferred proposals.

## Demo request

"Review the synthetic logs after the saved watermark, check existing rules, and produce numbered proposals. Wait before changing rules or the watermark." The isolated demo then supplies a clearly labeled synthetic approval: approve proposal 1, defer proposal 2, and retain later additions for the next review.

## Demo result

In the real local agent run, six selected entries produced two new proposals, each supported by two separate sessions. A status-report instruction was already covered. Phase 1 left rules and the watermark unchanged, verified by matching hashes. After the synthetic approval, only proposal 1 was saved. Proposal 2 remained deferred, and a newly appended entry remained pending. The watermark advanced only through the reviewed entries. Requests, fixtures, separate phase results, and execution proofs are in [the demo folder](../../demos/retro-to-rules/). This was a synthetic local test, not a change to actual agent memory.

## FAQ

### How do I turn agent feedback into rules?

Ask the agent to review your logs with Retro to Rules. It finds repeated corrections, checks existing coverage, and proposes numbered changes with evidence.

### Does this skill update agent memory automatically?

It waits for your approval of specific proposal numbers before saving rules or memory. It has no scheduled process of its own.

### Can I approve only some proposed rules?

Yes. Select the numbers you want. Deferred proposals stay in the review record so they can be revisited.

### What is a synthesis watermark?

It records the review boundary and processed entries. The skill uses entry dates or IDs, so a mixed file can contain both reviewed and new material.

### What happens if new session logs arrive during a review?

The agent compares a baseline before applying changes. It either reads the affected entries or records them as pending; the watermark covers only reviewed material.

### Do I need a memory server or document service?

No specific service is required. Local files work when your agent can read them and save approved changes to authorized destinations.

### Can this skill commit changes to Git?

Saving approved changes does not imply a Git commit. The agent runs a version-control commit only when separately requested.

## Keywords

agent feedback, retrospective synthesis, session log review, agent memory rules, repeated corrections, behavior rules, incremental review, synthesis watermark, Claude Code memory, Codex skills, project retrospectives, approved rule updates

## Tags

ai-agents, productivity, documentation, llm-ops, project-management, workflow-automation

## Compatibility

Claude Code, Codex CLI, Cursor, Gemini CLI, and other agents that read SKILL.md. Requires tools that can read your authorized logs and rule files; saving approved changes requires write access. A calculator or code-execution tool verifies counts used for ranking.

## Permissions notes

Reads only the logs, rules, and memory stores you authorize. Writes approved behavior changes, synthesis records, and the reviewed-entry watermark to authorized destinations. May use local search and code execution to count or verify evidence. Makes no network calls of its own. No automatic Git commits, log deletion, or log archiving.

## Credits

Original workflow by Auny LLC. No upstream project was used.

## Repo link

https://github.com/aunysillyme-dev/aunx-skills/tree/main/skills/retro-to-rules
