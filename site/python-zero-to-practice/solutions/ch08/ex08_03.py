# 第 08_03 题 读取可选配置
# config = {"batch_size":16}。读取缺失的 epochs，默认 3，输出 3；再输出字典，证明没有新增键。
# 预期程序输出：
# 3
# {'batch_size': 16}

config = {"batch_size": 16}
print(config.get("epochs", 3))
print(config)
