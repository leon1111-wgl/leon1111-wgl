"""v1.3：CSV 的字段、类型、范围检查；数据与练习独立编写。"""
from course_data import example, exercise
from refinements import add_body


def apply_v13(chapters):
    chapter = chapters[13]
    chapter["goals"].append("将 CSV 字段分步转换，保留坏记录的结束行号")
    chapter["checkpoint"].append("我能解释 CSV 空行、缺列、空字段与数字 0 的区别。")
    add_body(chapters, 13, '''
### CSV 精修：从文本到可以计算的数字，中间发生了什么
前置：第 07 章列表、第 09 章函数、第 12 章 csv 和 StringIO，以及本章的 ValueError。先完成 12_03 的 CSV 字符串求和，再做下面的坏数据练习。StringIO 把内存字符串包装成可读取的文本流，不会创建文件。

本例约定表头严格为 name,score，顺序也相同；每条记录两列，姓名去掉首尾空白后非空，成绩是 int 能转换的整数字符串，范围 0 到 100。先检查列数，再检查姓名，再转换成绩，最后检查范围。第一处失败就记下原因并 continue，不能把同一条坏记录加进 valid。

| 当前步骤 | 当前值 | 类型或含义 | 下一步 |
| --- | --- | --- | --- |
| csv.reader 解析一条记录 | ['小何', '0'] | 两个字符串组成的列表 | 检查 len(row) |
| row[1].strip() | '0' | 字符串，不是数字 | int 转换 |
| int 得到结果 | 0 | 整数，转换成功 | 检查 0 <= score <= 100 |
| 加入 valid | {'name': '小何', 'score': 0} | 可以交给统计函数的字典 | 继续下一条 |

**0 是有效成绩。** 不要用 `if not score` 判断“没有填成绩”，因为整数 0 的真假值为 False。应在转换前看字符串是否为空，或让 int('') 抛出 ValueError。`int('80.5')` 也会失败；`int(' 80 ')` 和 `int('+80')` 可以成功，本题接受 int 的这些常规写法。

### 为什么不直接 split(',') 或按记录数冒充行号
`"林,一",80` 的姓名中含逗号，csv.reader 能把它读成两列；split(',') 会错误拆成三部分。CSV 的引号内还可以合法换行，所以“第几条记录”和“原文件第几行”并不总相同。

示例 13_09 使用 reader.line_num，表示解析完当前记录时已经读到的物理行号，即**记录结束行号**。完全空的物理行（没有任何字符）解析成 [] 后跳过；`小李` 是一列，不是空行；`小李,` 是两列，第二列是空字符串，属于整数转换失败。坏记录只报告第一处错误。

| 示例原始行 | 数据情况 | 处理结果 |
| --- | --- | --- |
| 1 | name,score | 表头，只检查一次 |
| 2 | 姓名含英文逗号，成绩 80 | 保留 |
| 3 | 完全空的物理行 | 跳过 |
| 4 | 成绩 bad | integer |
| 5 | 成绩 101 | range |
| 6 | 只有姓名，没有成绩列 | columns |
| 7 | 成绩 0 | 保留 |

### 三层实操：每次只增加一种困难
1. **读懂：** 先预测示例 13_09 保留几条、错误几条，以及错误行号。运行后逐项对照上表。两个列表不是重复数据：valid 给统计层，errors 给修复原始数据的人。
2. **改写：** 将 bad 改为 90，预测合法记录变为 3 条；将 101 改为 100，预测它通过；将 0 改为 -1，预测 range 错误；把“小李”改为“小李,”，预测错误从 columns 变为 integer。每次只改一项，保留其他输入。
3. **迁移：** 完成习题 13_10 的离线工具耗时汇总。沿用检查顺序，但独立写出函数和边界；不看成绩例子的代码也能说明每层输入与输出，再接第 17 章成绩表清洗项目。

本例会继续处理字段错误，但错误表头会直接抛出 ValueError。严重引号错误可能让 csv.reader 抛出 csv.Error；该异常向调用者报告并停止，因为无法确定下一条记录从哪里开始。不要将所有 CSV 错误都理解成“可以安全跳过一行”。读取真实文件时使用 `open(path, encoding="utf-8", newline="")`，让 csv 模块处理换行。
''')
    example(chapter, 'CSV 清洗：空行、缺列与零分分别处理', r'''
    import csv
    import io

    def clean_scores_csv(text):
        reader = csv.reader(io.StringIO(text, newline=""), strict=True)
        if next(reader, None) != ["name", "score"]:
            raise ValueError("表头必须为 name,score")
        valid, errors = [], []
        for row in reader:
            end_line = reader.line_num
            if not row:
                continue
            if len(row) != 2:
                errors.append((end_line, "columns"))
                continue
            name = row[0].strip()
            if not name:
                errors.append((end_line, "name"))
                continue
            try:
                score = int(row[1].strip())
            except ValueError:
                errors.append((end_line, "integer"))
                continue
            if not 0 <= score <= 100:
                errors.append((end_line, "range"))
                continue
            valid.append({"name": name, "score": score})
        return valid, errors

    text = 'name,score\n"林,一",80\n\n小陈,bad\n小周,101\n小李\n小何,0\n'
    valid, errors = clean_scores_csv(text)
    print(valid)
    for end_line, reason in errors:
        print(f"结束行 {end_line}：{reason}")
    ''', '''
    [{'name': '林,一', 'score': 80}, {'name': '小何', 'score': 0}]
    结束行 4：integer
    结束行 5：range
    结束行 6：columns
    ''', 'reader 先把文本解析成字段列表。列数与姓名合格后才尝试 int，只有转换成功才判断分数范围。第 3 行空行不应挤掉后面的物理行号，所以从 reader.line_num 取得结束行。第 7 行的 0 转换成功且在范围内，必须保留。所有错误分支都 continue，因此错误记录不会落入最后的 valid.append。',
    '先做正文的四次单项改写，再试只有表头的输入，确认返回两个空列表；改错表头时应得到 ValueError。最后用带引号换行的姓名，观察结束行号为什么可能跳两个数。')
    exercise(chapter, 'AI / Agent：汇总本地工具耗时 CSV', '迁移',
    '实现 tool_time_total(text)，严格要求表头为 tool,ms，否则抛出 ValueError（包括空文本）。用 csv.reader 解析，忽略完全空行；逐条按顺序检查：恰好两列、工具名 strip 后非空、ms 能经 int 转换、ms 不小于 0。失败只记录第一项原因，代码依次为 columns、tool、integer、range，位置为该记录结束物理行号。返回 (合法耗时之和, 错误列表)，错误项为 (结束行号, 原因)。不打印，不写文件。打印对 \'tool,ms\\n"lookup,local",12\\n\\nfetch,bad\\ncache,-1\\nsave\\nfinish,0\\n\' 的返回值。严重 CSV 语法错误交给 csv 模块抛出。',
    '先读表头；total=0、errors=[]。每次 next(reader) 由 for 自动完成后，reader.line_num 已指向记录结束行。所有检查通过才 total += ms。不要把合法的 0 当作缺失。',
    r'''
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
    ''', "(12, [(4, 'integer'), (5, 'range'), (6, 'columns')])",
    '两条合法记录的耗时为 12 与 0，所以合计 12。空行不参与求和，错误仍对应第 4、5、6 物理行。缺失第二列属于 columns，存在第二列但为空属于 integer。额外列也必须拒绝。只有表头返回 (0, [])；空文本连表头都没有，应抛出 ValueError。这是人为填写的离线日志，毫秒不是 token；记录格式合法和耗时非负，不代表工具执行成功，也不代表最终任务正确。',
    tests=r'''
    assert tool_time_total("tool,ms\n") == (0, [])
    assert tool_time_total("tool,ms\na,0\nb, 8 \n") == (8, [])
    assert tool_time_total('tool,ms\n"a,b",3\n') == (3, [])
    assert tool_time_total("tool,ms\n\na,no\nb,2\n") == (2, [(3, "integer")])
    assert tool_time_total("tool,ms\na\nb,\nc,-2\n,3\nd,1,extra\n") == (0, [(2, "columns"), (3, "integer"), (4, "range"), (5, "tool"), (6, "columns")])
    assert tool_time_total('tool,ms\n"two\nlines",bad\nend,2\n') == (2, [(3, "integer")])
    assert tool_time_total("tool,ms\r\na,2\r\nb,x\r\n") == (2, [(3, "integer")])
    assert tool_time_total("tool,ms\n   ,bad\na,1.5\n") == (0, [(2, "tool"), (3, "integer")])
    assert tool_time_total("tool,ms\na,2\n") == (2, [])
    assert tool_time_total("tool,ms\na,2\n") == (2, []), "多次调用不能累积上次的合计"
    for invalid in ["", "tool,cost\na,3\n", "ms,tool\n3,a\n"]:
        try:
            tool_time_total(invalid)
        except ValueError:
            pass
        else:
            raise AssertionError("错误表头必须抛出 ValueError")
    import contextlib, io
    capture = io.StringIO()
    with contextlib.redirect_stdout(capture):
        tool_time_total("tool,ms\na,1\n")
    assert capture.getvalue() == "", "返回数据，打印交给调用者"
    ''')
