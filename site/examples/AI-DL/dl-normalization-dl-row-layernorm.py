# Leon | Original learning example
# Normalize features within each row
# Python 3.12+ | Run: python dl-normalization-dl-row-layernorm.py
# Install once with the same Python: python -m pip install numpy
import numpy as np
x = np.array([[1.,3.], [10.,14.]])
mean = x.mean(axis=1,keepdims=True)
variance = ((x-mean)**2).mean(axis=1,keepdims=True)
normalized = (x-mean)/np.sqrt(variance+1e-5)
print('means:', mean.ravel().tolist())
print('variances:', variance.ravel().tolist())
print('normalized:', np.round(normalized,6).tolist())
print('row means:', np.round(normalized.mean(axis=1),6).tolist())
