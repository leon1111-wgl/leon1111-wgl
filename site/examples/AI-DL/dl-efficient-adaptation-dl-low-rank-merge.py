# Guoliang | Original learning example
# Compare separate and merged adapter paths
# Python 3.12+ | Run: python dl-efficient-adaptation-dl-low-rank-merge.py
# Install once with the same Python: python -m pip install numpy
import numpy as np
base = np.eye(3,4)
a = np.array([[1.,0.,-1.,0.]])
b = np.array([[0.1],[0.2],[0.3]])
x = np.array([1.,2.,3.,4.]); scale = 1.
separate = base @ x + scale*b @ (a @ x)
merged = (base+scale*b @ a) @ x
print('full entries:', base.size, 'adapter entries:', a.size+b.size)
print('output:', np.round(separate,6).tolist())
print('merged agrees:', bool(np.allclose(separate,merged)))
