# CSV 写读转换
import csv
from pathlib import Path
folder = Path("outputs")
folder.mkdir(exist_ok=True)
path = folder / "example12_03.csv"
with path.open("w", encoding="utf-8", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["name", "score"])
    writer.writeheader()
    writer.writerows([{"name": "小林", "score": 80}, {"name": "小陈", "score": 90}])
with path.open(encoding="utf-8", newline="") as file:
    rows = list(csv.DictReader(file))
print(type(rows[0]["score"]).__name__)
print(sum(int(row["score"]) for row in rows))
