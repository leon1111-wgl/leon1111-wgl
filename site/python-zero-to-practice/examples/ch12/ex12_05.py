# 逐行 JSONL
import json
from pathlib import Path
folder = Path("outputs")
folder.mkdir(exist_ok=True)
path = folder / "example12_05.jsonl"
records = [{"id": 1, "text": "你好"}, {"id": 2, "text": "Python"}]
with path.open("w", encoding="utf-8") as file:
    for record in records:
        file.write(json.dumps(record, ensure_ascii=False) + "\n")
with path.open(encoding="utf-8") as file:
    for line in file:
        record = json.loads(line)
        print(record["id"], record["text"])
