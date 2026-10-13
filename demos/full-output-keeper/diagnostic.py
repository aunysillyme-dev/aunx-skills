import sys

print("Starting asset audit")
for number in range(1, 13):
    print("ERROR missing icon: checkout.svg" if number == 11 else f"asset {number}: checked")
print("Audit complete")
sys.exit(7)
