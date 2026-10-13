## Name

Instruction Weight: Save Preferences at the Right Level

## Summary

Help your agent preserve the difference between a passing idea, a preference, a working habit, and a firm rule.

## Price

$3 individually. Also in the $7.99 aunx bundle of all six paid skills.

## Full description

You say "I like short paragraphs," and a future agent treats long paragraphs as forbidden. You ask for a table once, and every answer becomes a table. Instruction Weight gives the agent a way to preserve what you actually meant before saving guidance.

The skill sorts statements into four levels: gesture, preference, practice, and rule. It also checks scope separately, so a firm instruction for one task can stay a one-off. Explicit musts and prohibitions retain their strength. A correction that narrows a task keeps unrelated standing instructions in force.

Use it with agents that save preferences or edit instruction files. After installation, the agent has a concrete interpretation workflow and a proposed-entry format. It changes guidance only within your authorization and the host agent's permissions.

## Use cases

- Review proposed agent memory entries before they become defaults.
- Keep a writing preference flexible while preserving explicit requirements.
- Capture a repeatable working habit with the conditions that make it useful.
- Apply a one-off format request without changing future answers.
- Interpret a scope correction while preserving other project instructions.
- Preserve rhetorical emphasis while separating actionable quantities.

## Demo request

Classify nine invented statements covering the four levels, a one-off table request, an emphatic number, a scoped correction, and a quoted instruction. Propose persistence decisions; do not write memory or instruction files. Full input: [request.json](../../demos/instruction-weight/request.json).

## Demo result

Applied to nine invented statements, the skill produced a classification table. "I like short paragraphs" became a preference; "I always outline" remained a practice; "never include customer email addresses" remained a rule. The table request stayed scoped to one answer. "100x easier" stayed rhetorical, and the headline-only correction preserved the existing privacy instruction. Two candidate memory entries were proposed; none were saved. Actual output: [result.md](../../demos/instruction-weight/result.md).

## FAQ

### How do I stop an AI agent from turning preferences into rules?

Have it classify the wording and scope before saving guidance. This skill treats "I like" as a preference and explicit "must" or "never" wording as a rule.

### Can this skill help with CLAUDE.md and AGENTS.md?

Yes. It helps an agent decide the appropriate wording and scope before editing those files. File edits still require your authorization and the agent's write permissions.

### Does one request become a permanent agent instruction?

A one-off request stays with that task. Persistence requires a separate request to save it or an already authorized memory workflow.

### What is the difference between a practice and a rule?

A practice describes a repeatable method and its conditions. A rule states a requirement or prohibition. "I always outline case studies" describes a practice; "never publish customer email addresses" states a rule.

### Does Instruction Weight save memories automatically?

The pack contains instructions, not a memory service. It can guide authorized writes through the host agent's existing tools or return proposed entries for review.

### How does it handle phrases like 100x easier?

It preserves clear rhetorical emphasis. Actionable quantities such as prices or limits follow a calculation workflow instead.

### Does a scope correction cancel other project rules?

The agent narrows the corrected task and continues applying unrelated standing requirements.

## Keywords

agent memory, AI preferences, instruction hierarchy, CLAUDE.md, AGENTS.md, remember my preferences, one-off instructions, standing rules, scope correction, prompt instructions, agent behavior, memory review, user intent

## Tags

ai-agents, productivity, llm-ops, writing, developer-tools, business-operations

## Compatibility

Claude Code, Codex CLI, Cursor, Gemini CLI, and agents that can load SKILL.md instructions. Discovery and installation paths depend on the host. No calculator or memory connector is required for classification.

## Permissions notes

Reads the supplied statements, conversation context, and relevant existing instructions when available. Writes only to a destination authorized by the user; interpretation-only requests produce a report. Contains no executable helper and makes no network calls of its own. A host agent may use its existing memory or file tools when a write is authorized.

## Credits

Original guidance by Auny LLC and contributors. No third-party code or external dependency is included. Distributed under MIT.

## Repo link

https://github.com/aunysillyme-dev/aunx-skills/tree/main/skills/instruction-weight
