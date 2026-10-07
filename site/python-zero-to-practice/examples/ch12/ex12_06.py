# 仅解析路径
from pathlib import Path
path = Path("data") / "train.jsonl"
print(path.name)
print(path.stem)
print(path.suffix)
