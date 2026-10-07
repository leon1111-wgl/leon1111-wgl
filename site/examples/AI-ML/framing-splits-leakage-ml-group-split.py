# Leon | Original learning example
# Keep complete devices together
# Python 3.12+ | Run: python framing-splits-leakage-ml-group-split.py
groups = [device for device in range(12) for _ in range(10)]
train = [i for i, device in enumerate(groups) if device < 8]
valid = [i for i, device in enumerate(groups) if 8 <= device < 10]
test = [i for i, device in enumerate(groups) if device >= 10]
train_devices = {groups[i] for i in train}
test_devices = {groups[i] for i in test}
print('rows:', len(train), len(valid), len(test))
print('shared devices:', sorted(train_devices & test_devices))
print('test error:', 2 / len(test))
