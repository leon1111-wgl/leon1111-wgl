# Leon | Original learning example
# Train a head on fixed features
# Python 3.12+ | Run: python dl-transfer-dl-frozen-feature-head.py
# Install once with the same Python: python -m pip install numpy
import numpy as np
z = np.array([2.,-1.]); w = np.array([0.1,0.2]); b = 0.; y = 1.
def probability(weights, bias):
    return 1/(1+np.exp(-(weights @ z+bias)))
p = probability(w,b)
gw = (p-y)*z; gb = p-y
w, b = w-0.1*gw, b-0.1*gb
new_p = probability(w,b)
print('new weights:', np.round(w,3).tolist())
print(f'new bias: {b:.3f}; new probability: {new_p:.6f}')
print(f'loss before: {-np.log(p):.6f}; after: {-np.log(new_p):.6f}')
print('fixed features:', z.tolist())
