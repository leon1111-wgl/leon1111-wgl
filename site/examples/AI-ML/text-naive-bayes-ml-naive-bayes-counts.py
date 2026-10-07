# Leon | Original learning example
# Compute a two-word classifier
# Python 3.12+ | Run: python text-naive-bayes-ml-naive-bayes-counts.py
# Install once with the same Python: python -m pip install numpy
import numpy as np
counts = np.array([[3.,1.], [1.,3.]])
word_prob = (counts + 1) / (counts.sum(axis=1, keepdims=True) + 2)
query = np.array([1.,0.])
log_scores = np.log([0.5,0.5]) + np.log(word_prob) @ query
weights = np.exp(log_scores - log_scores.max())
probabilities = weights / weights.sum()
print('word probabilities:', np.round(word_prob, 3).tolist())
print('class probabilities:', np.round(probabilities, 3).tolist())
print('class:', ['spam','ordinary'][int(np.argmax(probabilities))])
