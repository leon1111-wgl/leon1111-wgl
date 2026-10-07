# 写入与读回文本
from pathlib import Path
folder = Path("outputs")
folder.mkdir(exist_ok=True)
path = folder / "example12_01.txt"
path.write_text("第一天：变量\n第二天：循环\n", encoding="utf-8")
text = path.read_text(encoding="utf-8")
print(text, end="")
