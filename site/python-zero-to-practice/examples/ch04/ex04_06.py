# AI / Agent：按明确规则选择处理路径
request = " 请解释列表 "
cleaned = request.strip()
if cleaned == "":
    route = "请先输入问题"
elif "计算" in cleaned:
    route = "交给计算工具"
else:
    route = "进入文字讲解"
print(route)
