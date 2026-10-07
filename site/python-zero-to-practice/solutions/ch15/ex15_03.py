# 第 15_03 题 配置展开调用
# 实现 format_run(name,epochs)，返回 "名称:轮数"。用 config={"name":"demo","epochs":3} 的 ** 展开调用并打印。
# 预期程序输出：
# demo:3

def format_run(name, epochs):
    return f"{name}:{epochs}"

config = {"name": "demo", "epochs": 3}
print(format_run(**config))
