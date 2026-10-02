# Guoliang | Original learning example
# Compare allowed and masked context
# Python 3.12+ | Run: python dl-attention-dl-attention-mask.py
# Install once with the same Python: python -m pip install numpy
import numpy as np
q = np.array([[np.sqrt(2.),0.]])
k = np.array([[1.,0.], [0.,1.]])
v = np.array([[2.,0.], [0.,4.]])
scores = q @ k.T / np.sqrt(k.shape[1])
def softmax(row):
    values = np.exp(row-row.max(axis=-1,keepdims=True))
    return values/values.sum(axis=-1,keepdims=True)
weights = softmax(scores)
masked = softmax(scores + np.array([[0.,-np.inf]]))
print('weights:', np.round(weights,6).tolist())
print('output:', np.round(weights @ v,6).tolist())
print('masked output:', (masked @ v).tolist())
