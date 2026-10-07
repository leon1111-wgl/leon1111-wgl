# 第 12_06 题 读取数字文件
# 实现 read_numbers(path)，path 为 pathlib.Path，读 UTF-8 文本，每个非空行是合法整数，返回整数列表。演示时在临时目录建文件，内容 10、20，输出 [10,20]。
# 预期程序输出：
# [10, 20]

from pathlib import Path
from tempfile import TemporaryDirectory

def read_numbers(path):
    return [int(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]

with TemporaryDirectory() as folder:
    path = Path(folder) / "numbers.txt"
    path.write_text("10\n20\n", encoding="utf-8")
    print(read_numbers(path))
