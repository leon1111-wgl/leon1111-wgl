# AI / Agent：解析、校验、有限次重试
import json

def read_answer(text):
    data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError("最外层必须是对象")
    answer = data.get("answer")
    if not isinstance(answer, str) or not answer.strip():
        raise ValueError("answer 必须是非空字符串")
    return answer.strip()

replies = ["not-json", '{"answer": 12}', '{"answer": "先学函数"}']
for attempt, reply in enumerate(replies, start=1):
    try:
        answer = read_answer(reply)
    except ValueError:
        print(f"第 {attempt} 次：格式或内容不合格")
        continue
    print(f"第 {attempt} 次：{answer}")
    break
else:
    print("已用完预设回复，停止")
