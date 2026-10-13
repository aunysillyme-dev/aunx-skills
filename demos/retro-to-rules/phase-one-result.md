# Phase 1 result from the agent demo

Scope: read entries e03-e08 from `session-log.json`, dated 2030-04-03 through 2030-04-04. Excluded e01 and e02 as reviewed by the prior watermark, 2030-04-02. Baseline: 8 entries; all 6 selected entries read. Counts were computed with a local code-execution tool and the grouped IDs checked against the readable entries. See `baseline.json` and `count-tool-proof.json`.

Already covered: concise status is owned by `rules.md:3`. Entries e04 and e07 each repeat that instruction in separate sessions. Keep the existing wording. Investigation of an enforcement mechanism could be a follow-up; no duplicate rule is proposed in this limited demo.

1. COMPLETION: Before calling a task complete, cite its successful acceptance check. Evidence: e03, "called the export complete before checking"; e06, "before its acceptance check passed". Two occurrences across sessions gamma and delta. Scope: this synthetic workspace. Target/action: append to the existing `rules.md` owner (rewrite). Why: an unchecked output was reported ready twice.
2. REFERENCES: When quoting a reference in this workspace, include its source link. Evidence: e05 and e08, "include the source link when quoting a reference". Two occurrences across sessions gamma and delta. Scope: this synthetic workspace. Target/action: append to `rules.md` (rewrite). Why: source pointers were requested repeatedly.

Pending: proposals 1 and 2 require specific-number approval. No selected source entries remain unread. Baseline recheck was unchanged when this proposal was prepared.

Stopped before persistent writes: `rules.md` and `state.json` remain unchanged. Only this explicitly requested proposal artifact and demo proof artifacts were written. See `phase-one-proof.json` for before/after hashes.
