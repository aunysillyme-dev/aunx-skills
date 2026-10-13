---
name: client-work-to-template
description: Turn finished client work into a reusable process document, checklist, or template. Use when asked to extract a repeatable method, anonymize client work, create a reusable consulting template, or remove client details before sharing a workflow.
---

# Client Work to Template

Extract the method someone else can run on a new engagement. Keep the decision logic, reusable structure, variable formulas, and lessons from corrections.

## When to use

Use for completed work the user has authorized you to read and generalize. If the requested source or destination is ambiguous, resolve that scope before opening other client material. If the user wants a case study, use a case-study workflow instead.

## Steps

1. **Set the boundary.** Name the source files and intended output. Read existing templates in the authorized destination; extend a matching method instead of creating a duplicate.
2. **Gather identifying tokens before drafting.** Inventory client, brand, product, project, staff, and partner names; handles, emails, domains, URLs, file paths, IDs, dates, money, counts, measurements, and percentages. Include aliases, initials that identify a party, name fragments that remain identifying, and spelling or formatting variants. Keep this inventory in the user's authorized private workspace or transient memory, separate from the reusable document. If related source material needed for a complete inventory is unavailable, report that gap.
3. **Choose proven candidates.** Prefer methods actually used and improved by a correction. If a candidate is an untested idea, a one-off workaround, or a client preference, exclude it or explicitly label it as outside the proven method. Extracting no suitable method is a valid result.
4. **Generalize the mechanism.** Explain what decisions produced the result. Replace account-specific thresholds with a rule for choosing a threshold from the next account's evidence. Express calculations with named variables. Convert useful document structures into blank templates. Remove client draft copy, target lists, screenshots, and account reports rather than lightly paraphrasing them.
5. **Write a runnable document.** Include purpose, deliverable, principles, repeatable steps with decision conditions, templates, failure modes with preventive actions, and boundaries. State which steps require new evidence from the next engagement. Avoid implying that the prior client's results predict future outcomes.
6. **Run the leak check.** Search every new or modified output file case-insensitively for each collected token and its identifying variants. Use escaped literal searches, such as `rg -i -F -- "$token" "$output"`; a search with no matches must still run against a real readable output. Use digit boundaries for numeric tokens so a small number does not accidentally match a longer number; also check formatted variants such as separators, currencies, dates, and percentages. Inspect every digit-bearing line separately. Keep only structural numbering or generic formula notation, and explain each survivor. When a match identifies the client or repeats a client figure, rewrite it and scan the changed output again. A literal scan also needs a semantic review for distinctive anecdotes or combinations of facts that identify the engagement.
7. **Report evidence and limits.** Name the created or updated document, methods included and rejected, files actually scanned, whether all inventoried tokens were checked, digit survivors, and any source gaps. Report a limited scan as limited. Share the template only when it passes the stated checks and the user has authorized sharing.

## Output shape

```text
Purpose: [problem this method solves]
Produces: [reusable deliverable]
Principles: [why the decisions work]
Steps: [condition -> action -> required evidence]
Templates: [blank fields, schemas, checklists, variable formulas]
Failure modes: [observed pattern -> prevention]
Boundaries: [when the method applies and what requires fresh judgment]
```

Accompany the document with a short scan report. Keep the private token list and original client material out of the document and any public scan report.

## Conditions and actions

- If the source includes confidential material, use only the reading, writing, and tool permissions already granted; do not upload it to a third-party service to perform extraction.
- If a specific number came from the engagement, replace it with a named variable or the rule that derives it. Changing the number to a plausible invented number still produces an account-shaped example.
- If a name was removed but a handle, domain, unusual anecdote, or artifact reveals the client, remove that identifier or abstract the mechanism further.
- If a scan found zero matches but the inventory or files were incomplete, state the coverage gap and keep the result within that scope.
- If a numeric survivor represents a client measurement, remove it. If it represents a necessary structural count or formula notation, name and justify it in the scan report.
- If a public destination was not authorized, produce the reusable document in the authorized workspace and report it for review.

## Examples

**Request:** "Turn this completed campaign review into a template I can use with another client."

**Action:** Gather identifying tokens, extract the corrected decision method, replace measured results with named fields, and scan the new template for the collected tokens and digit-bearing lines.

**Result:** A blank review structure with rules for choosing the next test, plus a report of the exact files checked and any source limitations.

**Request:** "This is our first draft of a service we have never delivered. Extract a proven method."

**Result:** Explain that the draft is untested, and do not label it a proven method. Offer to organize it as a proposed process if that fits the user's request.

## Credits

Original generic workflow by Auny LLC. No external repository code or text is included in this pack.
