---
name: number-guard
description: Use when a user asks to check AI math, calculate invoice totals, compare percentages, estimate token costs, convert units, or compute dates. Route consequential arithmetic through an available calculator or code execution tool and report exact values beside rounded results.
---

# Number Guard

## When to use

If a number affects money, a decision, a comparison, a deadline, a measurement, or a published claim, calculate it with a tool before presenting it. Use this workflow for tax, budgets, rates, percentages, statistics, dates, token costs, unit conversions, and symbolic work. Trivial single-digit sums may be answered directly.

## Steps

1. Extract the supplied inputs, units, formula, and assumptions. If a missing input changes the answer, ask for it or label a scenario explicitly. If an input varies over time, use a dated source available within the task's permissions.
2. Inspect the calculator or code execution tools available in this session. Choose the operation by the question below. Use the tool's actual schema; these are operation categories, not required API names. A calculator MCP, a spreadsheet calculation tool, or local code execution can serve the same purpose. [codecalc](https://github.com/The-40-Thieves/codecalc) is one optional code execution tool.
3. Run the calculation. Use decimal strings or exact fractions for decimal money and ratios. Specify rounding mode, decimal places, and the stage where rounding occurs. Use a calendar and time-zone library for dates; use a symbolic tool when an exact symbolic result is needed.
4. Read the tool's result and successful completion signal. Check units, denominator, sign, and order of operations against the question. If an error, missing runtime, or incomplete run prevents computation, report the limitation and the uncomputed formula.
5. Present the exact value and the rounded value with its framing. Keep an exact fraction when a decimal repeats; label any finite decimal approximation. If independent rounding creates a remainder in a split bill, show how the remainder is allocated and confirm the allocations total the rounded bill.

## Question-to-tool map

| User's question | Operation or code approach |
| --- | --- |
| What percentage is this part of the total? | Part / total x 100; state the denominator. |
| How much did this increase or decrease? | (After - before) / before x 100; state when the baseline is zero. |
| Which is larger, and by how much? | Exact comparison, difference, and requested ratio. |
| What are the mean, median, spread, or percentiles? | Statistics operation; specify sample versus population and percentile method. |
| Convert a duration, size, mass, or temperature. | Unit conversion; state source and target units, including binary versus decimal data units. |
| Add several values or estimate token costs. | Worksheet or code with named inputs; bind each token category to the relevant dated unit price. |
| What is the deadline or elapsed time? | Calendar/date operation; state time zone, inclusive/exclusive endpoints, and holiday calendar for business days. |
| Calculate tax, margin, markup, break-even, or payback. | Business formula or code; identify the tax base and distinguish margin from markup. |
| Is this decimal equality safe? | Exact decimal/fraction comparison; report floating-point behavior separately when relevant. |
| Solve, simplify, differentiate, or integrate. | Symbolic operation; record domains and assumptions. |
| Does this color pair meet a contrast threshold? | Contrast calculation; state the threshold and applicable text size. |
| Round this result. | Rounding operation; show the exact value and chosen precision together. |

## Output shape

Return the answer first, then inputs and formula, exact result, rounded result and policy, and the tool used. Include assumptions or missing information that changes the answer. Keep enough of the calculation to reproduce it without exposing private data.

## Conditions and actions

- If a consequential result has not been computed by a tool, label it uncomputed and stop before using it as a recommendation.
- If money involves multiple rounding stages, follow the stated billing policy; when no policy is given, state the scenario rather than silently inventing one.
- If a user gives an approximate input, preserve that uncertainty. Exact computation does not make the input exact.
- If a phrase uses a number for emphasis, preserve the speaker's meaning; calculate only a numerical question or consequential claim.
- If a tool requires network access, installation, or file writes outside the task's permissions, use an available permitted alternative or report the missing capability.

## Examples

- "Check this invoice: three seats at $19.95, 12% off, then 8.25% tax." Use exact decimals; apply the discount before tax and state the final rounding rule.
- "Is the new plan 20% cheaper?" Compute (old - new) / old x 100, and distinguish the percentage from the old/new price ratio.
- "What is 37 divided by 210 as a percentage?" Return the exact fraction 370/21 percent and a tool-computed decimal approximation beside it.

## Credits

[codecalc](https://github.com/The-40-Thieves/codecalc) by The-40-Thieves, licensed under Apache-2.0, is recommended as one optional execution tool. This pack contains original instructions and copies no upstream code. The pack is licensed under MIT; optional tools retain their own licenses.
