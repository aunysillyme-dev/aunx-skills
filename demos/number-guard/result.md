# Actual demo result

Tool: codecalc `execute_code`, language `python3`, local provider, requested no network.
Completion: verdict `OK`, exit code `0`.
The runtime reports that its no-network flag is best effort on this platform. The executed script contains no network operations or dependencies.

The agent read the pack, extracted the inputs from `request.md`, and executed `aunx-demo.py` with exact decimal arithmetic. The captured output is in `stdout.txt`. To reproduce the calculation with a local Python 3 interpreter, run:

```sh
python3 demos/number-guard/aunx-demo.py
```

Answer: the exact invoice total is $57.01311000 (5701311/100000 USD). The final bill is $57.01 after rounding once with ROUND_HALF_UP. The exact share of the rounded bill is $14.2525 (5701/400 USD); allocate $14.26 to the first person and $14.25 to each of the other three. The script asserted that the allocations total $57.01.

Inputs: three seats at $19.95, a 12% discount, 8.25% tax on the discounted subtotal, and four people. Formula: `(3 x 19.95) x (1 - 0.12) x (1 + 0.0825)`. This synthetic example validates arithmetic and rounding; it does not establish a tax rate or tax obligation.
