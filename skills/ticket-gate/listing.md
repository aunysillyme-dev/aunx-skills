## Name

Ticket Gate: File Actionable Issues with Clear Done Signals

## Summary

Turn findings into startable, deduplicated issues and verify the evidence before closing them.

## Price

$3 individual pack. Also in the $7.99 aunx bundle of all six paid skills.

## Full description

Reviews often produce more tickets than useful work. Ticket Gate gives your agent four questions to ask before filing: is the work person-sized, would you deliberately pick it, is there a real done-signal, and can someone start today?

It then searches open issues by the files or repository involved, routes repeated findings into a rolling issue, and gives each new ticket a testable acceptance condition. When you ask to close work, it checks the named artifact and records what it found.

This pack is for developers, project leads, and anyone who asks an agent to turn findings into issues. It works with the tracker tools you already have. Without tracker access, it produces drafts and tells you which searches or actions remain unverified.

## Use cases

- Triage findings from a code review before creating tickets.
- Add recurring link failures to an existing rolling issue.
- Replace vague completion language with a named artifact check.
- Find open issues touching the same file before filing another.
- Check a guide, commit, deployment, or URL before proposing closure.
- Keep a short decision in the conversation when a ticket adds no useful work.

## Demo request

Use Ticket Gate to triage synthetic candidates against a local open-issue fixture. Propose actions without tracker writes, verify the health guide's done-signal, and draft its closure comment.

## Demo result

The real local run inspected six candidates and both fixture issues. It drafted one new parser issue, proposed an update to the existing broken-link class, and routed the product rebuild, wording decision, and provider wait to planning or dependency notes. The guide matched its existing issue. File inspection confirmed the ready status and operator steps, producing an evidence-backed closure draft with the artifact's SHA-256. No live tracker actions were taken. See [request](../../demos/ticket-gate/request.md), [result](../../demos/ticket-gate/result.md), and [complete tool output](../../demos/ticket-gate/tool-proof.json).

## FAQ

### How do I stop an AI agent from creating too many tickets?

Use the four-question gate and the default five-new-issues session limit. More creations need your explicit approval of a higher limit.

### How do I avoid duplicate GitHub issues?

Have the agent search open issues by the touched file or repository and inspect likely matches before filing.

### Does Ticket Gate work with Jira or another tracker?

Yes, when your agent has suitable tracker tools. The instructions also work with GitHub Issues or a supplied local issue list.

### What is a done-signal for an issue?

It is a named, inspectable acceptance condition, such as a specific file with required content or a deployment running the requested version.

### Can an AI agent close an issue from a status report?

This skill tells the agent to inspect the named artifact first. A report alone is insufficient evidence for closure.

### Does this skill connect to my tracker automatically?

No. It uses your existing tools within your authorized scope, or returns drafts when access is unavailable.

## Keywords

issue triage, actionable tickets, duplicate issues, GitHub issue workflow, Jira task creation, issue review workflow, acceptance criteria, done signals, evidence-based closure, backlog cleanup, agent task management, recurring findings

## Tags

ai-agents, project-management, productivity, code-review, workflow-automation

## Compatibility

Claude Code, Codex CLI, Cursor, Gemini CLI, and agents that read SKILL.md. Tracker search and write tools are optional for drafting and required for live tracker actions.

## Permissions notes

Reads supplied findings, relevant project files, and open issues through your available tools. Writes drafts or authorized tracker updates. May run local artifact checks or your existing tracker tooling when authorized. The pack includes no executable helper and makes no network calls of its own; connected tracker tools and live URL checks may use the network with permission. It does not install integrations or schedule jobs.

## Credits

Original workflow by Auny LLC. No third-party code is included. See [repository credits](../../CREDITS.md).

## Repo link

https://github.com/aunysillyme-dev/aunx-skills/tree/main/skills/ticket-gate
