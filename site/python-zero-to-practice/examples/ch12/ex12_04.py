# JSON 往返
import json
config = {"name": "练习", "batch_size": 8, "enabled": True}
text = json.dumps(config, ensure_ascii=False)
restored = json.loads(text)
print(text)
print(restored == config)
