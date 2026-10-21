# 第 13_10 题 AI / Agent：汇总本地工具耗时 CSV
# 实现 tool_time_total(text)，严格要求表头为 tool,ms，否则抛出 ValueError（包括空文本）。用 csv.reader 解析，忽略完全空行；逐条按顺序检查：恰好两列、工具名 strip 后非空、ms 能经 int 转换、ms 不小于 0。失败只记录第一项原因，代码依次为 columns、tool、integer、range，位置为该记录结束物理行号。返回 (合法耗时之和, 错误列表)，错误项为 (结束行号, 原因)。不打印，不写文件。打印对 'tool,ms\n"lookup,local",12\n\nfetch,bad\ncache,-1\nsave\nfinish,0\n' 的返回值。严重 CSV 语法错误交给 csv 模块抛出。
# 预期程序输出：
# (12, [(4, 'integer'), (5, 'range'), (6, 'columns')])

import csv
import io

def tool_time_total(text):
    reader = csv.reader(io.StringIO(text, newline=""), strict=True)
    if next(reader, None) != ["tool", "ms"]:
        raise ValueError("表头必须为 tool,ms")
    total, errors = 0, []
    for row in reader:
        end_line = reader.line_num
        if not row:
            continue
        if len(row) != 2:
            errors.append((end_line, "columns"))
            continue
        if not row[0].strip():
            errors.append((end_line, "tool"))
            continue
        try:
            ms = int(row[1].strip())
        except ValueError:
            errors.append((end_line, "integer"))
            continue
        if ms < 0:
            errors.append((end_line, "range"))
            continue
        total += ms
    return total, errors

text = 'tool,ms\n"lookup,local",12\n\nfetch,bad\ncache,-1\nsave\nfinish,0\n'
print(tool_time_total(text))
