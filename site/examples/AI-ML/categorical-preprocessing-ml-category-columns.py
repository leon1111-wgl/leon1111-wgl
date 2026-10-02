# Guoliang | Original learning example
# Encode known and unseen categories
# Python 3.12+ | Run: python categorical-preprocessing-ml-category-columns.py
vocabulary = ['paper', 'wood']
def encode(value):
    return [int(value == name) for name in vocabulary] + [int(value not in vocabulary)]
print('columns:', vocabulary + ['unknown'])
for value in ['wood', 'paper', 'metal']:
    row = encode(value)
    print(value, row, 'sum:', sum(row))
