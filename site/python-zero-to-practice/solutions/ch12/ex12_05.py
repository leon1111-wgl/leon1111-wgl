# 第 12_05 题 扩展名清单
# 实现 suffixes(names)，用 Path.suffix 返回各文件扩展名的列表；打印 ["a.txt","b.tar.gz","README"] 的结果。
# 预期程序输出：
# ['.txt', '.gz', '']

from pathlib import Path

def suffixes(names):
    return [Path(name).suffix for name in names]

print(suffixes(["a.txt", "b.tar.gz", "README"]))
