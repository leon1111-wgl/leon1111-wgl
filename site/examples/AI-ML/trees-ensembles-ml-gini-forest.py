# Guoliang | Original learning example
# Score a split and average trees
# Python 3.12+ | Run: python trees-ensembles-ml-gini-forest.py
def gini(positive, total):
    p = positive / total
    return 2 * p * (1 - p)
parent = gini(6, 10)
children = 0.5 * gini(4, 5) + 0.5 * gini(2, 5)
probabilities = [0.2, 0.7, 0.9]
print(f'parent: {parent:.2f}; children: {children:.2f}')
print(f'gain: {parent - children:.2f}')
print(f'forest probability: {sum(probabilities) / len(probabilities):.2f}')
