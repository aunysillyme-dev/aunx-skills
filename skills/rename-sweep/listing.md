## Name

Rename Sweep: Update Every Reference After a Rename

## Summary

Map a rename across code, docs, configuration, tests, and project notes, then check the old name in the same scope.

## Price

$3 standalone. Included in the $7.99 ten-skill bundle.

## Full description

A rename can look finished while a config sample, CI command, or documentation link still uses the old name. Rename Sweep gives your agent a practical checklist: map the references, read their context, update the surfaces you authorized, then search the old name again across those same paths.

It is for developers and project maintainers who want changes to stay consistent across code and the material around it. After install, the agent is instructed to record search roots, handle symlinked directories, preserve named historical records, and tell you which surfaces it could not verify. It works with your existing search and validation tools. It does not automatically migrate a database, update a remote tracker, or deploy a service.

## Use cases

- Rename a configuration key and update its reader, sample, docs, and tests.
- Move a documentation folder and repair navigation and internal links.
- Change a shared term across code, project instructions, and active notes.
- Map the consumers of a schema field before deciding on a migration.
- Find stale identifiers in linked directories and CI configuration.
- Preserve historical release notes while updating active references.

## Demo request

"Use Rename Sweep to change `cargo_delay` to `dispatch_delay` throughout the synthetic project. Update code, docs, configuration, tests, CI, and the local ticket note. Keep `history/release-notes.md` unchanged as a historical record."

The full request and reproducible fixture are in `demos/rename-sweep/` in the repository. This demo uses invented local files and no external tracker or deployment.

## Demo result

A real local run changed six active fixture files across `src`, `config`, `docs`, `tests`, `ci`, and `notes`. The control search found the seeded old identifier before the change. A Python stdlib search over those declared directories then reported:

```text
Final active old-identifier hits: 0; search completed successfully.
Historical exception (preserved byte-for-byte):
history/release-notes.md:3: The sample originally used cargo_delay.
Behavior command: python3 tests/test_settings.py
PASS: config reader returns the expected delay
Behavior exit code: 0
```

Actual captured output is in `demos/rename-sweep/result.txt`, with before and after files beside it. The CI text was updated; no CI service was run. The ticket surface was a local synthetic note.

## FAQ

**How do I rename a variable everywhere with an AI agent?**
Ask the agent to use Rename Sweep, name the old and new identifier, and define the project scope. The skill directs it to map references before editing and search those same paths afterward.

**Does this work for filenames and folder paths?**
Yes. It instructs the agent to search filenames and repair callers and links when paths are part of your request. Content search alone does not cover filenames.

**Can it update GitHub Issues, Jira, or another issue tracker?**
It can guide an agent that already has tracker access and permission. This pack supplies no tracker connector and grants no external write permission.

**How does it handle old names in release notes?**
The agent names the exact records you want preserved and reports their remaining matches separately. Active references still need updates or an explicit compatibility plan.

**Does an empty search prove the rename is complete?**
Only within the roots that were successfully checked. The agent must account for linked directories and unavailable surfaces, and verify changed behavior with relevant project checks.

**Will this migrate my database or deploy the new setting?**
The skill maps those dependencies and reports the required steps. Migrations and deployments need their own authorization, tools, and compatibility checks.

## Keywords

rename everywhere, update all references, AI agent refactor, stale identifiers, configuration key rename, path rename, folder rename, schema field rename, documentation links, symlink search, refactor checklist, rename verification, old variable name

## Tags

ai-agents, developer-tools, documentation, testing, workflow-automation, code-review

## Compatibility

Claude Code, Codex CLI, Cursor, Gemini CLI, and other agents that read SKILL.md. The instructions use available local search and validation tools; ripgrep is an optional example. Install this folder using the skill mechanism supported by your agent.

## Permissions notes

Reads authorized code, documentation, configuration, tests, CI files, instructions, notes, and ticket sources. Writes only references within the user's granted scope. Runs local search and relevant project validation through the agent's existing tools. The pack has no executable helper and makes no network calls of its own. Remote issue reads or writes require the user's existing connectors and permission.

## Credits

Original workflow packaging by Auny LLC. No third-party code is included in this pack. The pack is distributed under the MIT License.

## Repo link

https://github.com/aunysillyme-dev/aunx-skills/tree/main/skills/rename-sweep
