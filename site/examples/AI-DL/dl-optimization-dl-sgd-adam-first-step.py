# Guoliang | Original learning example
# Compare the first SGD and Adam steps
# Python 3.12+ | Run: python dl-optimization-dl-sgd-adam-first-step.py
# Install once with the same Python: python -m pip install numpy
import numpy as np
targets = np.array([2.,4.]); theta = 0.; rate = 0.1
gradient = np.mean(theta-targets)
sgd = theta-rate*gradient
beta1, beta2 = 0.9, 0.999
m = (1-beta1)*gradient; v = (1-beta2)*gradient**2
m_hat = m/(1-beta1); v_hat = v/(1-beta2)
adam = theta-rate*m_hat/(np.sqrt(v_hat)+1e-8)
for name, value in [('SGD',sgd), ('Adam',adam)]:
    loss = np.mean(0.5*(value-targets)**2)
    print(f'{name}: parameter {value:.6f}; loss {loss:.6f}')
