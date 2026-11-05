# Leon | Original learning example
# Check translations and extraction rules on small models
# Python 3.12+ | Run: python quantifier-translation-quantifier-model-check.py
from itertools import product

# Part 1. English sentences checked on one small model.
people = ["Leon", "Mia", "Emma", "Jack"]
pairs = {("Leon", "Mia"), ("Mia", "Emma"), ("Emma", "Mia"), ("Jack", "Mia")}


def admires(x, y):
    return (x, y) in pairs


sentences = [
    ("Everyone admires someone", all(any(admires(x, y) for y in people) for x in people)),
    ("Someone is admired by everyone", any(all(admires(x, y) for x in people) for y in people)),
    ("Someone is admired by everyone else",
     any(all(admires(x, y) for x in people if x != y) for y in people)),
    ("Nobody admires themselves", all(not admires(x, x) for x in people)),
    ("Exactly one person admires Emma",
     any(admires(x, "Emma") and all(x == z for z in people if admires(z, "Emma"))
         for x in people)),
]
for text, value in sentences:
    print(f"{text}: {value}")

# Part 2. Test quantifier-extraction rules on every model with 0 to 3 objects.
# A model is a subset for P, a subset for Q and a truth value for R.
rules = [
    ("(all x P) and R  =  all x (P and R)",
     lambda D, P, Q, R: (all(P[x] for x in D) and R) == all(P[x] and R for x in D)),
    ("(exists x P) or R  =  exists x (P or R)",
     lambda D, P, Q, R: (any(P[x] for x in D) or R) == any(P[x] or R for x in D)),
    ("(all x P) -> R  =  exists x (P -> R)",
     lambda D, P, Q, R: ((not all(P[x] for x in D)) or R) == any((not P[x]) or R for x in D)),
    ("(exists x P) -> R  =  all x (P -> R)",
     lambda D, P, Q, R: ((not any(P[x] for x in D)) or R) == all((not P[x]) or R for x in D)),
    ("(all x P) or (all x Q)  =  all x (P or Q)",
     lambda D, P, Q, R: (all(P[x] for x in D) or all(Q[x] for x in D)) == all(P[x] or Q[x] for x in D)),
    ("(exists x P) and (exists x Q)  =  exists x (P and Q)",
     lambda D, P, Q, R: (any(P[x] for x in D) and any(Q[x] for x in D)) == any(P[x] and Q[x] for x in D)),
]
for label, rule in rules:
    verdict = "holds on every model with 1-3 objects"
    for size in (1, 2, 3):
        D = range(size)
        for p, q, r in product(product([False, True], repeat=size),
                               product([False, True], repeat=size), [False, True]):
            if not rule(D, p, q, r):
                verdict = f"fails: {size} objects, P={list(p)}, Q={list(q)}, R={r}"
                break
        if verdict.startswith("fails"):
            break
    empty = "" if rule(range(0), (), (), False) and rule(range(0), (), (), True) else "  (fails on 0 objects)"
    print(f"{label}: {verdict}{empty}")
