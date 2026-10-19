---
name: rename-sweep
description: Use when a user asks to rename a variable, path, slug, schema field, setting, or shared term across a project. Map every affected surface, update authorized references, and verify the old identifier across declared paths with explicit historical exceptions.
metadata:
  internal: true
---

# Rename Sweep

Treat a rename as a refactor. Map its references before editing, then verify the same surfaces after the change.

## When to use

Use for requests such as "rename this everywhere", "update all references", "change a config key", or "find stale links after moving a file". A request to explain a possible rename authorizes discovery only.

## Steps

1. **Define the change.** Record the old and new identifier, exact scope, intended spelling variants, compatibility requirements, and any historical records the user wants preserved. Treat a public API, database field, or deployed setting as a compatibility change: identify consumers and required migration or alias before editing.
2. **Declare the search roots.** Map code, documentation, configuration, tests, CI, instructions, notes, and open tickets that refer to the old name or behavior. Search filenames, content, and links. Resolve symlink roots to their actual targets, or explicitly follow them. Search declared paths rather than assuming one project-root walk covers linked directories. If a category is absent, record how you checked. If a category is inaccessible, label it unverified.
3. **Read and classify the hits.** Inspect their context. Record each active reference, generated reference, historical exception, and unrelated match in a checklist. Identify the generator for generated files. Use literal search for literal identifiers and separate searches for casing, separator variants, and references by concept when relevant.
4. **Apply the authorized changes.** Update the source that owns each value, its consumers, links, examples, tests, and active ticket wording. Preserve unrelated edits. Rename paths and repair callers when the task includes paths. Regenerate derived files using the project's documented command. If permission is missing for a surface, provide the precise proposed change as a handoff and continue independent authorized work.
5. **Verify the same roots.** Search the old identifier and mapped variants in every declared path, including filenames. Record command, paths, exit status, and output. With `rg`, exit 1 means no matches; exit 2 means the check failed. Accept zero active hits only when the search ran successfully and covered every declared surface. Name each preserved historical match with its path and reason.
6. **Check behavior.** Run the project's relevant validation for changed imports, links, config readers, tests, and consumers. If a surface is unavailable or a compatibility step remains pending, report the rename as partial and name the missing evidence. A local change alone does not prove deployed consumers use the new name.

For a literal search with ripgrep, a useful starting point is `rg -n -F -- 'old_identifier' path/to/src path/to/docs path/to/config`. Use the equivalent available tool if ripgrep is absent. Repeat the verified command over the same paths after editing. Search path names separately, since content search does not check filenames. Resolve each linked root before interpreting an empty result.

## Output shape

Report:

- **Change:** old identifier to new identifier and scope.
- **Map:** each surface, declared path or source, search method, and status.
- **Updates:** changed files, repaired callers, and generated outputs.
- **Verification:** final old-name search and relevant behavior checks, with exit codes.
- **Exceptions:** named historical records and unrelated matches with reasons.
- **Handoffs:** exact remaining changes, required permission or unavailable access, and verification needed.
- **Verdict:** complete in the verified scope, partial, or discovery only.

## Conditions and actions

- If the only evidence is an empty tree walk, verify the real roots before claiming a clean rename.
- If a match is in a generated file, edit its owning source and regenerate it.
- If a broad substitution would alter unrelated meanings, make context-specific edits.
- If tickets, notes, deployment, or schema changes fall outside the mandate, report those surfaces as pending; a rename request does not grant unrelated external actions.
- If historical material is preserved, name each exception; an entire active folder is not a historical exception.
- If an approved compatibility alias retains the old identifier, document it as an active exception and report the final retirement step as pending.

## Examples

**Config key:** Rename `cargo_delay` to `dispatch_delay`. Map the config reader, JSON sample, user guide, test fixture, CI command, and local ticket note. Update those active surfaces, run the affected config check, and report a preserved release note by path.

**Folder:** Move `docs/guide/` to `docs/manual/`. Search imports, navigation, links, CI paths, and filenames, repair callers, and verify link targets resolve. If a separate documentation site is inaccessible, give its owner the proposed path updates and report that part as unverified.

## Credits

Original workflow packaging by Auny LLC. No third-party code is included in this pack.
