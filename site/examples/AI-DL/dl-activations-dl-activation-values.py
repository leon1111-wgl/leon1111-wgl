# Leon | Original learning example
# Print values and slopes
# Python 3.12+ | Run: python dl-activations-dl-activation-values.py
from math import exp
for z in [-2.,0.,2.]:
    relu = max(0.,z)
    sigmoid = 1/(1+exp(-z))
    slope = sigmoid*(1-sigmoid)
    print(f'z={z:.0f}: ReLU={relu:.1f}, sigmoid={sigmoid:.6f}, slope={slope:.6f}')
