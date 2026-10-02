# Guoliang | Original learning example
# Slide a filter and add a shortcut
# Python 3.12+ | Run: python dl-convolution-dl-filter-residual.py
# Install once with the same Python: python -m pip install numpy
import numpy as np
x = np.array([[1.,0.,2.], [2.,1.,0.], [0.,3.,1.]])
kernel = np.array([[1.,0.], [0.,-1.]])
out = np.zeros((2,2))
for row in range(2):
    for col in range(2):
        out[row,col] = np.sum(x[row:row+2,col:col+2] * kernel)
residual_sum = np.array([2.,-1.]) + np.array([0.5,0.25])
print('filter output:', out.tolist())
print('residual sum:', residual_sum.tolist())
print('after ReLU:', np.maximum(0,residual_sum).tolist())
