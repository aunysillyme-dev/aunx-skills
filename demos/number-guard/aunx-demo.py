from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction

seat_count = 3
seat_price = Decimal("19.95")
discount_rate = Decimal("0.12")
tax_rate = Decimal("0.0825")
people = 4
cent = Decimal("0.01")

subtotal = seat_count * seat_price
discount = subtotal * discount_rate
tax_base = subtotal - discount
tax = tax_base * tax_rate
exact_total = tax_base + tax
rounded_total = exact_total.quantize(cent, rounding=ROUND_HALF_UP)
exact_share = exact_total / people
bill_share = rounded_total / people
total_cents = int(rounded_total / cent)
base_cents, remainder = divmod(total_cents, people)
allocations = [Decimal(base_cents + (i < remainder)) * cent for i in range(people)]
assert sum(allocations) == rounded_total

print("Synthetic invoice, USD; discount applied before tax")
print(f"Subtotal: {subtotal}")
print(f"Discount: {discount}")
print(f"Tax base: {tax_base}")
print(f"Tax: {tax}")
print(f"Exact total: {exact_total} ({Fraction(exact_total)})")
print(f"Rounded bill: {rounded_total} (ROUND_HALF_UP, final total only)")
print(f"Exact share of unrounded total: {exact_share} ({Fraction(exact_share)})")
print(f"Exact share of rounded bill: {bill_share} ({Fraction(bill_share)})")
print("Cent allocations: " + ", ".join(f"{amount:.2f}" for amount in allocations))
print(f"Allocation total: {sum(allocations):.2f}")
