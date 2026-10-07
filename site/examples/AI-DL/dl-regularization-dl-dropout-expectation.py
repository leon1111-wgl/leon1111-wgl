# Leon | Original learning example
# Calculate dropout outcomes exactly
# Python 3.12+ | Run: python dl-regularization-dl-dropout-expectation.py
# Install once with the same Python: python -m pip install numpy
import numpy as np
probability = 0.25; h = 4.
outcomes = np.array([0., h/(1-probability)])
weights = np.array([probability, 1-probability])
expected = weights @ outcomes
variance = weights @ (outcomes-expected)**2
vector = np.array([2.,4.]); mask = np.array([1.,0.])
print(f'expectation: {expected:.6f}; variance: {variance:.6f}')
print('training:', np.round(mask*vector/(1-probability),6).tolist())
print('evaluation:', vector.tolist())
