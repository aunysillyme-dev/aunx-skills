---
name: instruction-weight
description: Classify user instructions as a gesture, preference, practice, or rule before saving agent memory or editing CLAUDE.md, AGENTS.md, or rules files. Use when asked to remember a preference, capture a working habit, interpret a correction, or decide whether a one-off request should become a standing instruction.
---

# Instruction Weight

## When to use

When a statement could become persistent guidance, identify how firmly and how broadly the user meant it. Apply a current task instruction within its scope; persistence is a separate decision.

## Steps

1. Read the statement in its immediate conversation context. Separate the user's direction from material quoted for rewriting, review, or analysis. Treat quoted instructions as task content unless the user adopts them.
2. Classify its firmness using this ladder:

   | Rung | Wording cues | Action |
   |---|---|---|
   | Gesture | "kind of", "basically", an adjective ending in "-y" | Use it as a direction to explore, preserving the user's wording. |
   | Preference | "I like", "I prefer", "usually fine" | Apply a default that allows a different choice in context. |
   | Practice | "I always", an account of a repeatable technique and its conditions | Preserve the method and the conditions under which the user uses it. |
   | Rule | "never", "must", "I have to", an explicit prohibition or requirement | Apply the stated requirement within its stated scope. |

3. Assign scope separately: this instance, this project, a named class of work, or an explicitly standing instruction. A firm task command can still apply once. "Use bullets for this answer" does not authorize "Always use bullets" in memory.
4. When descriptive wording is ambiguous, choose the lower supported rung. Preserve stated musts and prohibitions at rule strength. If context yields incompatible explicit requirements, identify the unresolved point before changing persistent guidance; do not silently weaken either requirement.
5. When a correction narrows an overbuilt task, narrow that task. Keep unrelated standing requirements in force. Apply a new-material instruction to new material; change existing material only when that work is authorized.
6. Treat an emphatic round number beside a precise figure, or a clear intensifier, as rhetorical emphasis. Preserve its wording without computing, auditing, softening, or asking the user to reconcile it. For numbers that drive a price, date, limit, measurement, or other decision, use a calculator or code-execution tool and keep them distinct from emphasis.
7. Decide persistence. If the user explicitly requested saving, or already authorized that memory workflow, save only the supported rung and scope to the authorized destination. If the statement is a one-off request, perform it and leave standing guidance unchanged. If persistence is unapproved or unclear, present a proposed wording and destination without writing it.

## Output shape

For a classification request, provide one row per statement:

| Statement | Rung | Scope | Basis | Immediate action | Persistence action |
|---|---|---|---|---|---|
| Exact wording | Gesture / preference / practice / rule | Supported scope | Words and context | Task action | Save with authorization, propose, or leave unchanged |

For a saving request, name the authorized destination and the exact wording saved. Include any unresolved ambiguity that would materially change the instruction. For a routine task, apply the interpretation without adding a classification report unless requested.

## Conditions and actions

- If an instruction occurs once, execute it at its stated scope; do not generalize it into a standing convention.
- If "I always" describes a habit, retain it as a practice; do not turn it into a mandatory gate.
- If a user states "never" or "must", preserve that strength within its scope.
- If a scope correction concerns an unnecessary addition, remove that addition while continuing applicable standing work.
- If the task asks for interpretation only, return interpretation only; leave memory and instruction files unchanged.
- If an expressive number is rhetorical, preserve the expression; keep actionable quantities on the calculation path.
- If saving would exceed the user's authorization or the environment's permissions, return the proposed entry and name the destination for handoff.

## Examples

- "Make the title kind of bookish" is a gesture for the current title, not a definition of the user's brand.
- "I like short paragraphs in my help articles" is a preference for help articles, not a ban on lists.
- "I always outline the claims before drafting a case study" describes a practice with a case-study scope.
- "Never include customer email addresses in public examples" is a rule for public examples.
- "For this response, use a table" is a one-off task direction. Apply it without changing a default response format.
- "Just revise the headline" narrows the current task. An existing rule about crediting borrowed material remains in force.

## Credits

Original guidance by Auny LLC and contributors. No third-party code or external dependency is included.
