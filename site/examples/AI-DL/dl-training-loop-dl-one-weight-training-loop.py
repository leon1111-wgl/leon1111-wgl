# Leon | Original learning example
# Run five transparent training steps
# Python 3.12+ | Run: python dl-training-loop-dl-one-weight-training-loop.py
# Install once with the same Python: python -m pip install numpy
import numpy as np
x = np.array([-1.,0.,1.]); y = 2*x
valid_x = np.array([-1.5,1.5]); valid_y = 2*valid_x
weight = 0.; best_loss = float('inf'); best_weight = weight
for epoch in range(1,6):
    error = weight*x-y
    gradient = 2*np.mean(error*x)
    weight -= 0.3*gradient
    train_loss = np.mean((weight*x-y)**2)
    valid_loss = np.mean((weight*valid_x-valid_y)**2)
    if valid_loss < best_loss:
        best_loss, best_weight = valid_loss, weight
    print(f'epoch {epoch}: w={weight:.4f}, train={train_loss:.4f}, valid={valid_loss:.4f}')
print(f'best weight: {best_weight:.5f}')
