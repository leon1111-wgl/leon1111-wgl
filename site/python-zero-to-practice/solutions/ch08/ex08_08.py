# 第 08_08 题 读取嵌套配置
# config={"training":{"batch_size":8,"epochs":3}}，输出 batch_size 与 epochs 的乘积 24。
# 预期程序输出：
# 24

config = {"training": {"batch_size": 8, "epochs": 3}}
training = config["training"]
print(training["batch_size"] * training["epochs"])
