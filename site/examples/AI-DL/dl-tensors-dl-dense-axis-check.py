# Leon | Original learning example
# Name the axes of a dense layer
# Python 3.12+ | Run: python dl-tensors-dl-dense-axis-check.py
# Install once with the same Python: python -m pip install numpy
import numpy as np
x = np.array([[2.,1.,0.], [0.,3.,1.]])
w = np.array([[1.,-1.], [2.,0.], [0.,3.]])
b = np.array([0.5,-0.5])
out = x @ w + b
print('shape:', out.shape)
print('output:', out.tolist())
print('mean per feature:', out.mean(axis=0).tolist())
print('mean per recording:', out.mean(axis=1).tolist())
