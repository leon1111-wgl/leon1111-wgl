# AI / Agent：把会话快照写入 JSON 再读回
import json
from pathlib import Path

messages = [{"role": "user", "content": "学习函数"}]
path = Path("outputs/ai_chat_demo.json")
path.parent.mkdir(parents=True, exist_ok=True)
text = json.dumps(messages, ensure_ascii=False, indent=2)
path.write_text(text, encoding="utf-8")
restored = json.loads(path.read_text(encoding="utf-8"))
print(type(restored).__name__)
print(restored[0]["content"])
print(restored == messages)
