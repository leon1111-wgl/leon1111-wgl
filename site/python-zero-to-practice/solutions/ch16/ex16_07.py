# 第 16_07 题 AI / Agent：实现可测试的两步工具流程
# 实现 lookup_agent(query, max_steps=2)。query 必须是字符串；max_steps 必须是非负 int（不接受 bool），否则 raise ValueError。固定笔记字典为 {"列表":"有序容器", "函数":"可复用的处理步骤"}，按 query 完全匹配查找。第 1 步保存查找结果；第 2 步返回 {"status":"done", "answer":结果或"未找到", "steps":2}。若步数不够，返回 {"status":"limit", "answer":None, "steps":已执行步数}。只需这两种动作，最多执行两步。调用 "函数" 并依次输出 status、answer、steps。
# 预期程序输出：
# done
# 可复用的处理步骤
# 2

def lookup_agent(query, max_steps=2):
    if not isinstance(query, str):
        raise ValueError("query 必须是字符串")
    if type(max_steps) is not int or max_steps < 0:
        raise ValueError("max_steps 必须为非负整数")
    notes = {"列表": "有序容器", "函数": "可复用的处理步骤"}
    observation = None
    steps = 0
    for step in range(1, max_steps + 1):
        steps = step
        if step == 1:
            observation = notes.get(query, "未找到")
        else:
            return {"status": "done", "answer": observation, "steps": steps}
    return {"status": "limit", "answer": None, "steps": steps}

result = lookup_agent("函数")
print(result["status"])
print(result["answer"])
print(result["steps"])
