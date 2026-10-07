# 集合关系
train_ids = {1, 2, 3}
test_ids = {3, 4}
print(sorted(train_ids & test_ids))
print(sorted(train_ids | test_ids))
print(sorted(train_ids - test_ids))
