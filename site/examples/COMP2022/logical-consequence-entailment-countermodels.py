# Leon | Original learning example
# Find every countermodel
# Python 3.12+ | Run: python logical-consequence-entailment-countermodels.py
from itertools import product

rows = []
for p, q in product([False, True], repeat=2):
    premise = (not p) or q
    conclusion = q or p
    if premise and not conclusion:
        rows.append((p, q))
print("Countermodels:", rows)
assert rows == [(False, False)]
