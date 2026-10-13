## Name

Number Guard: Check AI Math with a Calculator

## Summary

Give your agent a clear method for tool-calculated numbers, exact results, and explained rounding.

## Price

Free ($0). Not part of the bundle.

## Full description

An agent can sound certain while getting a percentage, invoice total, or unit conversion wrong. Number Guard teaches it to send consequential arithmetic through a calculator or code execution tool before presenting the answer.

It maps common questions to the right kind of calculation, checks the result against the inputs, and keeps the exact value beside the rounded answer. It also makes the agent state details that change a result, such as the percentage denominator, tax base, time zone, and rounding stage.

Use it if you ask an agent to work with budgets, project estimates, statistics, dates, invoices, or token costs. You bring the calculator or execution tool already available in your environment. codecalc is one optional choice. The pack supplies instructions rather than a calculator service.

## Use cases

- Check invoice totals, discounts, and tax calculations with a stated rounding policy.
- Compare prices using a clear baseline and denominator.
- Estimate token costs from supplied counts and dated unit prices.
- Convert units while keeping source and target units visible.
- Calculate date spans or statistics with the relevant assumptions stated.

## Demo request

Calculate a synthetic invoice for three seats at $19.95 each, apply a 12% discount, then add 8.25% sales tax. Round only the final bill to cents with ROUND_HALF_UP. Split that rounded bill between four people, allocate any leftover cent to the first person, and show exact values beside rounded ones.

## Demo result

A real local codecalc Python run returned `OK` and exit code `0`. The exact total was $57.01311000 (5701311/100000 USD); the final rounded bill was $57.01. The exact share of the rounded bill was $14.2525 (5701/400 USD). The cent allocations were $14.26, $14.25, $14.25, and $14.25; the script confirmed that they total $57.01.

The synthetic request, executable calculation, captured stdout, and result are available in `demos/number-guard/` in the repository. This demo checks arithmetic and rounding, not tax applicability.

## FAQ

### How do I make an AI agent check its math?

Install the pack and give the agent a calculator or code execution tool. The instructions route consequential calculations through that tool and ask the agent to report its inputs and formula.

### Does Number Guard include a calculator?

No. It works with the calculator or code execution tool available to your agent, including calculator MCPs and local Python execution.

### Can I use Number Guard without codecalc?

Yes. codecalc is an optional recommendation. The question-to-tool map uses operation categories rather than requiring a particular API.

### Can it check invoice tax and discounts?

It can calculate from the inputs and billing policy you provide. It does not determine which tax laws or rates apply to you.

### Why show exact and rounded values together?

Rounding can change comparisons or split payments. Keeping both values makes the rounding choice visible and the result easier to reproduce.

### Will Number Guard guarantee every number is correct?

No. Correctness still depends on valid inputs, the formula, the available tool, and the agent following the instructions. The pack adds calculation evidence and makes assumptions visible.

## Keywords

check AI math, AI calculator skill, agent arithmetic, calculator MCP, exact decimals, invoice calculation, percentage change, token cost calculation, unit conversion, date arithmetic, rounding money, codecalc

## Tags

ai-agents, productivity, developer-tools, business-operations, testing

## Compatibility

Plain SKILL.md instructions for Claude Code, Codex CLI, Cursor, Gemini CLI, and other agents that read SKILL.md. Activation and discovery depend on the host. Numerical work requires an available calculator or code execution tool.

## Permissions notes

Reads the inputs and data you provide and inspects available tool capabilities. Runs calculations through your chosen tool. Writes results only where the task authorizes. The pack includes no executable helper and makes no network calls of its own. A selected tool or a request for current rates may involve network access under your existing permissions.

## Credits

[codecalc](https://github.com/The-40-Thieves/codecalc) by The-40-Thieves (Apache-2.0) is recommended as one optional execution tool and was used for the demo. This MIT-licensed pack contains original instructions and copies no upstream code.

## Repo link

https://github.com/aunysillyme-dev/aunx-skills/tree/main/skills/number-guard
