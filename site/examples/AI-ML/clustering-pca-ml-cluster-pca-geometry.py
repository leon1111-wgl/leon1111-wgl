# Guoliang | Original learning example
# Measure groups and PCA variance
# Python 3.12+ | Run: python clustering-pca-ml-cluster-pca-geometry.py
# Install once with the same Python: python -m pip install numpy
import numpy as np
x = np.array([[0., 0.], [0., 2.], [4., 0.], [4., 2.]])
centers = np.array([[0., 1.], [4., 1.]])
assignment = np.array([0, 0, 1, 1])
loss = np.sum((x - centers[assignment]) ** 2)
centered = x - x.mean(axis=0)
covariance = centered.T @ centered / len(x)
values = np.linalg.eigvalsh(covariance)
print(f'cluster loss: {loss:.1f}')
print('covariance:', covariance.tolist())
print(f'first variance share: {values[-1] / values.sum():.2f}')
