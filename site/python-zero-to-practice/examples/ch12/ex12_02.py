# 逐行读取与清理
from pathlib import Path
folder = Path("outputs")
folder.mkdir(exist_ok=True)
path = folder / "example12_02.txt"
path.write_text(" Python \n\n AI \n", encoding="utf-8")
with path.open(encoding="utf-8") as file:
    for line in file:
        clean = line.strip()
        if clean:
            print(clean)
