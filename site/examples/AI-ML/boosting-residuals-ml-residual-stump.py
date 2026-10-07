# Leon | Original learning example
# Fit one residual stump
# Python 3.12+ | Run: python boosting-residuals-ml-residual-stump.py
# Install once with the same Python: python -m pip install numpy
import numpy as np
x = np.array([0.,1.,2.,3.]); y = np.array([1.,1.,3.,3.])
prediction = np.full_like(y, y.mean())
residual = y - prediction
left = x < 2
correction = np.where(left, residual[left].mean(), residual[~left].mean())
updated = prediction + 0.5 * correction
print('residual:', residual.tolist())
print('updated:', updated.tolist())
print(f'MSE before: {np.mean((prediction-y)**2):.2f}')
print(f'MSE after: {np.mean((updated-y)**2):.2f}')
