# Guoliang | Original learning example
# Score the correct partners both ways
# Python 3.12+ | Run: python clip-contrastive-contrastive-table.py
import math
similarity = [[0.8, 0.2], [0.1, 0.7]]
temperature = 0.2
scores = [[x / temperature for x in row] for row in similarity]
def loss(row, correct):
    weights = [math.exp(x - max(row)) for x in row]
    probability = weights[correct] / sum(weights)
    return -math.log(probability)
row_loss = sum(loss(row, i) for i, row in enumerate(scores)) / 2
columns = list(zip(*scores))
column_loss = sum(loss(column, i) for i, column in enumerate(columns)) / 2
print(f"image to text={row_loss:.4f}")
print(f"text to image={column_loss:.4f}")
print(f"combined={(row_loss + column_loss) / 2:.4f}")
