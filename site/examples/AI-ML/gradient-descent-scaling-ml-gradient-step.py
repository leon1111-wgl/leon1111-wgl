# Leon | Original learning example
# Standardize and take one step
# Python 3.12+ | Run: python gradient-descent-scaling-ml-gradient-step.py
# Install once with the same Python: python -m pip install numpy
import numpy as np
x = np.array([2., 6.]); y = np.array([1., 3.])
z = (x - x.mean()) / x.std()
w, b, rate = 0., 0., 0.1
error = w * z + b - y
gw = 2 * np.mean(error * z)
gb = 2 * np.mean(error)
w, b = w - rate * gw, b - rate * gb
print('scaled inputs:', z.tolist())
print(f'gradients: {gw:.1f}, {gb:.1f}')
print(f'weights: {w:.1f}, {b:.1f}')
print(f'loss: {np.mean((w * z + b - y) ** 2):.3f}')
