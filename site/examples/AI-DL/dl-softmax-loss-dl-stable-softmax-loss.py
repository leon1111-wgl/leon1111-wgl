# Guoliang | Original learning example
# Compute stable probabilities and cross-entropy
# Python 3.12+ | Run: python dl-softmax-loss-dl-stable-softmax-loss.py
# Install once with the same Python: python -m pip install numpy
import numpy as np
logits = np.array([2.,1.,0.]); target = 0
def softmax(values):
    shifted = values-values.max()
    weights = np.exp(shifted)
    return weights/weights.sum()
probabilities = softmax(logits)
loss = -np.log(probabilities[target])
print('probabilities:', np.round(probabilities,6).tolist())
print(f'sum: {probabilities.sum():.6f}; loss: {loss:.6f}')
print('shift unchanged:', bool(np.allclose(probabilities,softmax(logits+1000))))
