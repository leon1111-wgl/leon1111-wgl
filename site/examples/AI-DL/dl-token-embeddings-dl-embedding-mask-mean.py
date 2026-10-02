# Guoliang | Original learning example
# Look up tokens and ignore padding
# Python 3.12+ | Run: python dl-token-embeddings-dl-embedding-mask-mean.py
# Install once with the same Python: python -m pip install numpy
import numpy as np
table = np.array([[1.,0.], [0.,2.], [0.,0.]])
ids = np.array([0,1,2]); padding_id = 2
vectors = table[ids]
mask = ids != padding_id
pooled = (vectors*mask[:,None]).sum(axis=0)/mask.sum()
reversed_ids = np.array([1,0,2])
reversed_mean = table[reversed_ids][reversed_ids != padding_id].mean(axis=0)
print('vectors:', vectors.tolist())
print('real-token count:', int(mask.sum()))
print('masked mean:', pooled.tolist())
print('reversed mean:', reversed_mean.tolist())
