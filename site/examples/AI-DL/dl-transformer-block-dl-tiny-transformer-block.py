# Guoliang | Original learning example
# Run a complete toy pre-norm block
# Python 3.12+ | Run: python dl-transformer-block-dl-tiny-transformer-block.py
# Install once with the same Python: python -m pip install numpy
import numpy as np
def layer_norm(values):
    centered = values-values.mean(axis=-1,keepdims=True)
    return centered/np.sqrt((centered**2).mean(axis=-1,keepdims=True)+1e-8)
x = np.array([[1.,-1.], [1.,-1.]])
u = layer_norm(x)
scores = u @ u.T / np.sqrt(u.shape[1])
allowed = np.tril(np.ones((len(x),len(x)),dtype=bool))
scores = np.where(allowed,scores,-np.inf)
weights = np.exp(scores-scores.max(axis=1,keepdims=True))
weights /= weights.sum(axis=1,keepdims=True)
y = x + weights @ u
w1 = np.eye(2); w2 = 0.5*np.eye(2)
z = y + np.maximum(0,layer_norm(y) @ w1) @ w2
print('attention:', np.round(weights,6).tolist())
print('first residual:', np.round(y,6).tolist())
print('block output:', np.round(z,6).tolist())
