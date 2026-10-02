# Guoliang | Original learning example
# Compare a full pass and a shortlist
# Python 3.12+ | Run: python efficient-evidence-systems-cascade-budget.py
candidate_count = 100
cheap_cost, expensive_cost = 1, 10
shortlist_size = 5
full_cost = candidate_count * expensive_cost
cascade_cost = candidate_count * cheap_cost + shortlist_size * expensive_cost
print("costs:", full_cost, cascade_cost)
print(f"saved fraction={1 - cascade_cost / full_cost:.2f}")
evidence_tokens = [80, 60, 90]
budget = 150
used = 0
kept = []
for index, count in enumerate(evidence_tokens):
    if used + count <= budget:
        kept.append(index)
        used += count
print("kept evidence indices:", kept, "tokens:", used)
