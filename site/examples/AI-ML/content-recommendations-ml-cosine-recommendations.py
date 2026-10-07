# Leon | Original learning example
# Rank three tagged videos
# Python 3.12+ | Run: python content-recommendations-ml-cosine-recommendations.py
# Install once with the same Python: python -m pip install numpy
import numpy as np
names = ['astronomy', 'robotics', 'mixed']
items = np.array([[1.,0.], [0.,1.], [1.,1.]])
profile = np.array([1.,1.])
scores = (items @ profile) / (np.linalg.norm(items, axis=1) * np.linalg.norm(profile))
order = np.argsort(-scores, kind='stable')
for index in order:
    print(f'{names[index]}: {scores[index]:.3f}')
