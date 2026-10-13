## Name

Client Work to Template: Reuse Proven Methods

## Summary

Turn completed client work into a reusable method and blank template, with an explicit scan for identifying details.

## Price

$5 standalone. Also in the $7.99 aunx bundle of all six paid skills.

## Full description

Useful client work often stays buried in the final report. This skill helps your agent pull out the decision method, document structure, and lessons from corrections so you can use them again.

It is for consultants, agency teams, operators, and freelancers turning finished work into reusable process documents. The agent inventories identifying details before drafting, replaces client figures with variables or derivation rules, and searches the resulting files for every gathered token. It also reviews digit-bearing lines and distinctive anecdotes.

After installation, ask for a reusable template from an authorized source. You get a runnable method, blank structure, and scan report with coverage limits. The scan helps catch literal leaks; a human review still matters for indirect identification. The skill does not publish your output or establish permission to reuse client-owned material.

## Use cases

- Turn a completed campaign review into a blank review template.
- Extract a corrected onboarding process from finished work.
- Generalize a consulting checklist for a new engagement.
- Replace client-specific thresholds with evidence-based decision rules.
- Check a reusable process document for client names and figures.

## Demo request

"Turn the completed synthetic engagement in input.md into a reusable campaign review method and blank template. Keep all client identifying tokens and client figures out of the reusable document, and run a real case-insensitive token and digit scan."

## Demo result

A real local run produced demos/client-work-to-template/output.md: a reusable review method, blank comparison table, uncertainty checks, and rules for choosing the next test. The actual Python scan inventoried 13 identifying fields and searched 31 literal tokens and variants. It found 0 token hits and 0 digit-bearing output lines; exit code 0. All source data was invented. The run and coverage limits are recorded in demos/client-work-to-template/scan-result.md.

## FAQ

### How do I turn client work into a reusable template?

Ask your agent to use Client Work to Template on the finished files you authorize it to read. It extracts the repeatable method and writes a blank structure for another engagement.

### Does this skill anonymize every document automatically?

It guides your agent through token collection, literal searches, digit review, and semantic review. It does not provide a guarantee of anonymity or a standalone automatic redaction service.

### Can I keep the client's numbers as examples?

The reusable output uses named variables and rules instead of client numbers. A changed or invented number can still preserve a distinctive account story, so examples should explain the mechanism without carrying that story forward.

### Will it change or publish the original client files?

The workflow reads authorized source files and writes the requested reusable output. Editing originals or publishing to another destination requires that permission in your task.

### What happens if the process has never been used?

The agent labels the candidate as untested and keeps it outside the proven method. A proposed process can be organized separately if requested.

### What tools do I need for the leak check?

Your agent needs file access and a literal-search or code-execution tool, such as ripgrep or Python. The skill includes no dependency installation or network requirement.

## Keywords

client work to template, reusable consulting template, anonymize client work, client data leak check, extract business process, agency workflow template, consulting SOP, remove client names, reusable checklist, process documentation, client confidentiality, AI agent skills, blank campaign review

## Tags

ai-agents, documentation, productivity, business-operations, writing, workflow-automation

## Compatibility

Claude Code, Codex CLI, Cursor, Gemini CLI, and other agents that read SKILL.md. Requires authorized file access and a search or code-execution tool for verification. Agents differ in skill discovery and available tools; use their current setup instructions.

## Permissions notes

Reads only the client inputs and existing templates authorized by the task. Writes the requested reusable document and a scan report in the authorized workspace. May run local literal searches or code to check those outputs. Makes no network calls of its own. Keep identifying-token inventories private and separate from the reusable deliverable. Client reuse and publication rights remain the user's responsibility.

## Credits

Original generic workflow by Auny LLC. No external repository code or text is included in this pack. MIT license.

## Repo link

https://github.com/aunysillyme-dev/aunx-skills/tree/main/skills/client-work-to-template
