# Guoliang | Original learning example
# Inspect every nearest-neighbour vote
# Python 3.12+ | Run: python nearest-neighbours-ml-knn-vote.py
# Install once with the same Python: python -m pip install numpy
import numpy as np
x = np.array([[0.,0.], [1.,0.], [2.,0.], [4.,0.]])
y = np.array([0,0,1,1])
query = np.array([1.6,0.])
squared = np.sum((x - query) ** 2, axis=1)
order = np.argsort(squared, kind='stable')
print('squared distances:', np.round(squared, 2).tolist())
for k in [1,3]:
    labels = y[order[:k]]
    print('k:', k, 'labels:', labels.tolist(), 'prediction:', int(labels.mean() > 0.5))
