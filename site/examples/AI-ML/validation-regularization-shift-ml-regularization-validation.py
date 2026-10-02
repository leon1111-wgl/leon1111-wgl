# Guoliang | Original learning example
# Separate fitting objective and validation
# Python 3.12+ | Run: python validation-regularization-shift-ml-regularization-validation.py
candidates = {'A': (1.0, 9), 'B': (1.4, 1)}
strength = 0.1
for name, (mse, squared_weights) in candidates.items():
    print(f'{name} objective: {mse + strength * squared_weights:.1f}')
folds = {0.0: [1.0, 1.4, 1.2], 0.1: [0.9, 1.0, 1.1]}
means = {value: sum(errors) / len(errors) for value, errors in folds.items()}
for value, score in means.items():
    print(f'lambda {value:.1f}: validation MSE {score:.1f}')
print('chosen lambda:', min(means, key=means.get))
