"""Fabricated burn-in data: 500 sensor summaries per unit, label 1 = the unit failed burn-in.

Everything here is invented. The `Plant` fixes the hidden process once (which columns
carry signal, each sensor's scale and offset), so a later batch comes from the same world.
"""
import numpy as np

N_FEATURES = 500
N_SIGNAL = 5


class Plant:
    def __init__(self, seed=100):
        rs = np.random.RandomState(seed)
        self.scale = rs.uniform(0.5, 40.0, N_FEATURES)    # sensors report in different units
        self.offset = rs.uniform(-100.0, 100.0, N_FEATURES)
        self.signal_columns = rs.choice(N_FEATURES, N_SIGNAL, replace=False)
        self.shift = rs.uniform(0.35, 0.6, N_SIGNAL) * rs.choice([-1.0, 1.0], N_SIGNAL)

    def batch(self, n, seed):
        """Return X (n x 500) and y (n,), half of the units failing."""
        rs = np.random.RandomState(seed)
        y = rs.permutation(np.arange(n) % 2)
        z = rs.normal(size=(n, N_FEATURES))
        z[:, self.signal_columns] += y[:, None] * self.shift
        return z * self.scale + self.offset, y
