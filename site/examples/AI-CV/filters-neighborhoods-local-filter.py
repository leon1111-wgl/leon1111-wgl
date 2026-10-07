# Leon | Original learning example
# Average a small patch
# Python 3.12+ | Run: python filters-neighborhoods-local-filter.py
patch = [10, 10, 10, 10, 19, 10, 10, 10, 10]
mean = sum(patch) / len(patch)
row = [2, 5, 8]
weights = [-1, 0, 1]
response = sum(value * weight for value, weight in zip(row, weights))
print(f"mean={mean:.1f}")
print("edge response:", response)
