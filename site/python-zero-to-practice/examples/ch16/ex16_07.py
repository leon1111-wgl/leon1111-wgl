# AI / Agent：串起决策、工具、观察和结束
def search_notes(query):
    notes = [
        {"keyword": "列表", "text": "列表保存有顺序的元素。", "source": "note-01"},
        {"keyword": "函数", "text": "return 把结果交回调用位置。", "source": "note-02"},
    ]
    for note in notes:
        if note["keyword"] in query:
            return {"text": note["text"], "source": note["source"]}
    return {"text": "没有找到相关笔记。", "source": None}

def decide(state):
    if state["observation"] is None:
        return {"action": "search", "query": state["query"]}
    return {"action": "finish"}

state = {"query": "怎么理解函数？", "observation": None}
finished = False
for step in range(1, 4):
    decision = decide(state)
    print(f"第 {step} 步：{decision['action']}")
    if decision["action"] == "search":
        state["observation"] = search_notes(decision["query"])
    elif decision["action"] == "finish":
        print(state["observation"]["text"])
        print(f"来源：{state['observation']['source']}")
        finished = True
        break
    else:
        raise ValueError("未知动作")
if not finished:
    print("达到步数上限，尚未完成")
