# Guoliang | Original learning example
# Inspect a probability bin
# Python 3.12+ | Run: python calibration-monitoring-ml-calibration-bin.py
# Install once with the same Python: python -m pip install numpy
import numpy as np
probability = np.array([0.8,0.8,0.8,0.8])
label = np.array([1.,1.,0.,0.])
brier = np.mean((probability - label) ** 2)
print('bin count:', len(label))
print(f'mean probability: {probability.mean():.2f}')
print(f'observed positive fraction: {label.mean():.2f}')
print(f'Brier score: {brier:.2f}')
