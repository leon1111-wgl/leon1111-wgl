# Leon | Original learning example
# Compare a line and a constant
# Python 3.12+ | Run: python linear-regression-mse-ml-line-loss.py
# Install once with the same Python: python -m pip install numpy
import numpy as np
x = np.array([1., 2., 3.])
y = np.array([3., 5., 8.])
prediction = 1 + 2 * x
residual = prediction - y
mse = np.mean(residual ** 2)
baseline_mse = np.mean((y.mean() - y) ** 2)
print('prediction:', prediction.tolist())
print(f'MSE: {mse:.6f}; RMSE: {np.sqrt(mse):.6f}')
print(f'constant MSE: {baseline_mse:.6f}')
