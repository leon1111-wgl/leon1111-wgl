# Guoliang | Original learning example
# Print the shape at every layer
# Python 3.12+ | Run: python dl-shape-tracing-dl-shape-path.py
# Install once with the same Python: python -m pip install numpy
import numpy as np
images = np.arange(8,dtype=float).reshape(2,2,2)
flat = images.reshape(images.shape[0],-1)
w1 = np.ones((4,3)); b1 = np.zeros(3)
w2 = np.ones((3,2)); b2 = np.zeros(2)
hidden = np.maximum(0,flat @ w1+b1)
logits = hidden @ w2+b2
assert flat.shape == (2,4)
for name, array in [('images',images),('flat',flat),('hidden',hidden),('logits',logits)]:
    print(name, array.shape)
print('first flattened image:', flat[0].tolist())
print('parameters:', w1.size+b1.size+w2.size+b2.size)
