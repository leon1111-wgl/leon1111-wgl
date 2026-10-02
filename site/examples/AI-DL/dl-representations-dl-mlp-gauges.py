# Guoliang | Original learning example
# Trace two hidden units
# Python 3.12+ | Run: python dl-representations-dl-mlp-gauges.py
# Install once with the same Python: python -m pip install numpy
import numpy as np
w1 = np.array([[1.,-1.], [-1.,1.]])
b1 = np.array([-1.,-1.])
w2 = np.array([1.,1.]); b2 = 0.
for values in [[3.,1.], [1.,3.], [2.,2.]]:
    x = np.array(values)
    hidden = np.maximum(0, w1 @ x + b1)
    output = w2 @ hidden + b2
    print('input:', values, 'hidden:', hidden.tolist(), 'output:', float(output))
print('parameters:', w1.size + b1.size + w2.size + 1)
