# Actual demo result

Read SKILL.md, request.md, input.json, and the named guide. Ran `python3 demos/ticket-gate/aunx_demo.py` from the repository root. Exit code: 0. The complete local inspection output is in tool-proof.json. Fixture search covered both supplied open issues; it does not establish the state of a live tracker.

Gate columns are: person-sized unit, deliberate board pick, independent done-signal, startable today.

| Candidate | Gates | Search and disposition | Done-signal or missing proof |
| --- | --- | --- | --- |
| Health guide | yes / yes / yes / yes | Exact path matches DEMO-01. DEMO-02 is a broader related docs issue, not a duplicate of the guide. Draft closure for DEMO-01. | `file-exists`: ready status and operator steps verified in the named artifact. |
| Additional broken links | yes / yes / yes / yes | Matches DEMO-02 by class and docs path. Propose adding the two findings to that rolling issue. | Keep its `manual` link-check report and maintainer confirmation condition. This demo supplies neither and proposes no closure. |
| Empty webhook parser | yes / yes / yes / yes | No match in the executed local fixture search. Draft one new issue. | `commit-touches-path`: src/webhook.py change plus regression evidence of the agreed 400 response. |
| Entire product rebuild | no / no / no / no | Keep in planning notes until bounded units and acceptance conditions are defined. | No independently verifiable condition supplied. |
| Setup wording choice | yes / no / no / yes | Search found a related docs issue. Handle the one-sentence decision in the review conversation. | No issue needed for this editorial choice. |
| Provider review wait | yes / no / no / no | Add a dependency comment to the parser draft, naming the provider response needed before integration. | Waiting is a trigger, not independently startable work. |

New issue draft:

**Handle empty webhook bodies**

Context: An empty request causes a parser exception in the supplied scenario. The review owner requested a fix that a developer can start today.

Action: Update src/webhook.py to return the agreed 400 response for an empty body and run a regression check.

Completion-signal: commit-touches-path - a commit changes src/webhook.py and a regression run demonstrates the agreed 400 response for an empty body.

Dependency comment draft: Integration work awaits the provider's review response. Implement and check local empty-body handling now; revisit integration when that response arrives.

Rolling issue update draft: Add docs/faq.md#setup and docs/start.md#usage to DEMO-02. The supplied fixture now identifies three affected links. Keep its existing link-check report and maintainer-confirmation done-signal.

Closure comment draft for DEMO-01:

Verified the ready status and operator steps against artifacts/docs/health-check.md. Evidence: file exists, `Status: ready` and `Operator steps:` are present. SHA-256: d48811a5ad4e5ac5d329159ae7d77221951f0ede836c37f19d319cf4d0dbeac3.

Session result: one new issue draft against the default limit of five. No issues created, updated, or closed in a live tracker. Closure evidence is verified locally; the closure itself remains a draft.
