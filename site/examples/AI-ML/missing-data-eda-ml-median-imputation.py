# Guoliang | Original learning example
# Fit a median, then reuse it
# Python 3.12+ | Run: python missing-data-eda-ml-median-imputation.py
# Install once with the same Python: python -m pip install numpy
import numpy as np
train = np.array([2., np.nan, 6., 4.])
test = np.array([np.nan, 10.])
missing = np.isnan(train)
median = np.median(train[~missing])
filled_train = np.where(missing, median, train)
filled_test = np.where(np.isnan(test), median, test)
print(f'training missing fraction: {missing.mean():.2f}')
print('training flag:', missing.astype(int).tolist())
print('filled training:', filled_train.tolist())
print('filled test:', filled_test.tolist())
