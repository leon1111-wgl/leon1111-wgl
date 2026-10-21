"""v1.2：显式传递状态，以及逐行数据错误定位。"""
from course_data import example, exercise
from refinements import add_body


def apply_v12(chapters):
    chapters[9]["goals"].append("追踪连续调用中的旧值、返回值与接收位置")
    chapters[9]["checkpoint"].append("我能解释丢弃返回值与保存返回值时，外部计数为什么不同。")
    chapters[13]["goals"].append("逐行检查 JSONL，记录原始行号并保留后续合法数据")
    chapters[13]["checkpoint"].append("我能区分 JSON 解析错误、字段类型错误和业务取值错误。")
    add_body(chapters, 9, '''
### 精讲：为什么函数调用了三次，外面的计数仍是 0
假设 next_round(current) 返回 current + 1。写 `next_round(rounds)` 只计算出新值，没有把它存回 rounds；写 `rounds = next_round(rounds)` 才会更新调用位置的名字。记住这条完整路线：**旧值作为实参进入 → 函数算出新值 → return 交回 → 调用者赋值保存**。

| 写法 | 三次调用各自收到的 current | 三次返回值 | 最后的 rounds |
| --- | --- | --- | --- |
| 只写 next_round(rounds) | 0、0、0 | 1、1、1，但没保存 | 0 |
| 写 rounds = next_round(rounds) | 0、1、2 | 1、2、3，逐次保存 | 3 |

这两行写法可以放进相同的 for 循环，分别运行验证。每次普通函数调用都有自己的局部名字；整数值不会因为函数里给形参重新赋值，就自动改变调用者的名字。第 09 章新增示例 09_10 让你同时观察两个调用方式。

### 实操：把任务预算写成明确的输入与返回值
想象一个离线 Agent 练习，每做一步扣掉一部分预算。先定义 remaining_budget(remaining, used) 只负责计算“还剩多少”，再由外面决定是否保存新预算、打印或继续执行。这样可以分别手算单步结果和连续多步的结果。

给自己画三列：调用前余额、传入的 used、返回的新余额。先从 60 扣 15，再从新余额扣 50；按本题约定余额最低为 0，应得到 45、0。若两次都拿原始 60 作为输入，第二次会得到 10，那是调用方的数据流写错了，未必是函数公式写错。

**闭卷检查：** return 是否等于“修改调用者变量”？不等于。修改列表对象、重新绑定局部名字、返回一个值，是三个需要分别观察的动作。

### 作用域报错的下一站
在函数里直接写 `rounds += 1`，却没有把 rounds 设成参数或先在本次调用中赋值，会涉及 UnboundLocalError。第 13 章的示例 13_07 提供可运行的错误与修复对照；它会用该章学过的 try/except 捕获错误，便于继续观察修复结果。此处先练好参数与返回值，不必提前记异常处理语法。
''')
    example(chapters[9], 'AI / Agent：返回的新轮数要由调用者接住', '''
    def next_round(current):
        return current + 1

    rounds = 0
    for _ in range(3):
        next_round(rounds)
    print(f"未接收：{rounds}")

    for _ in range(3):
        rounds = next_round(rounds)
        print(f"保存后：{rounds}")
    ''', '''
    未接收：0
    保存后：1
    保存后：2
    保存后：3
    ''', '第一个循环每次都传入 0，并得到 1，但没有变量接收这三个返回值。第二个循环的右边先计算 next_round(rounds)，然后左边 rounds 才绑定新值；所以下一轮能接着上次的结果计算。下划线只是一个变量名，表示本例不需要循环索引。这是离线计数实验，没有执行真实 Agent 或模型调用。',
    '把初始 rounds 改为 5，先写出全部四行输出再运行。随后只删掉第二个循环中的赋值，解释为什么三次打印都不再增长。')
    exercise(chapters[9], 'AI / Agent：把剩余预算逐步传下去', '迁移',
    '实现 remaining_budget(remaining, used)，两个输入保证为非负整数，返回扣减后的余额，最低为 0；函数不得打印或依赖全局余额。先设 budget=60，接收扣 15 的结果并打印；再接收扣 50 的结果并打印。',
    '函数先计算 remaining - used，负数返回 0，否则返回计算值。调用时要把返回值赋给 budget，再进行下一次调用。',
    '''
    def remaining_budget(remaining, used):
        result = remaining - used
        if result < 0:
            return 0
        return result

    budget = 60
    budget = remaining_budget(budget, 15)
    print(budget)
    budget = remaining_budget(budget, 50)
    print(budget)
    ''', '45\n0',
    '第一步 60-15 得到 45，第二步把 45 传回函数，45-50 小于 0，按约定返回 0。若没有保存第一次的返回值，就会错误地从 60 再扣 50。本题的预算是人为设定的整数额度，不是 API 账单或模型 token 数。边界：扣 0 不变、恰好扣完为 0、超过余额也为 0；重复输入应得到相同结果。',
    tests='''
    assert remaining_budget(0, 0) == 0
    assert remaining_budget(10, 0) == 10
    assert remaining_budget(10, 10) == 0
    assert remaining_budget(10, 11) == 0
    assert remaining_budget(60, 15) == 45
    assert remaining_budget(60, 15) == 45, "函数不能偷偷累积全局余额"
    assert remaining_budget(remaining_budget(60, 15), 50) == 0
    import contextlib, io
    capture = io.StringIO()
    with contextlib.redirect_stdout(capture):
        remaining_budget(3, 1)
    assert capture.getvalue() == "", "函数负责返回，显示交给调用者"
    ''')
    add_body(chapters, 13, '''
### 修复实验：函数里为什么读不到外面的计数
先看新增示例 13_07 的 broken_round。函数体中出现 `rounds += 1`，Python 会把这里的 rounds 视为这个函数的局部名字；而 += 又要先读取旧值，所以在局部值尚未建立时抛出 UnboundLocalError。即使外面已有 rounds=0，也不能在这处读取中自动补上局部值。

示例专门捕获这一个异常并打印它的类型，随后显示外面的 rounds 仍是 0。修复版显式接收 current 并返回 current+1，再由外面赋值保存。这样每一次调用的输入和结果都能单独测试。

想看完整 Traceback，可以在临时副本里只保留 rounds、broken_round 的定义及 `broken_round()` 调用，去掉捕获部分再运行。此时出现异常并退出是预期现象。不同 Python 版本的错误措辞可能有差别；先看类型、文件行号和出错表达式，不必背整句英文。

### 实操：JSONL 的一行数据要经过三道检查
下面训练记录的约定由本教材自行制定：每行是一个对象；text 是字符串，去首尾空白后非空；label 是整数 0 或 1，不能是 True/False。它只是小型练习格式，不代表任何模型厂商的训练接口。

| 检查层 | 当前拿到什么 | 失败例子 | 本例错误类别 |
| --- | --- | --- | --- |
| JSON 解析 | 原始的一行字符串 | 缺少右花括号 | json |
| 结构与字段类型 | loads 得到的 Python 值 | 最外层是列表，或 text 是数字 | schema |
| 业务取值 | 类型已正确的字段 | text 仅空白，或 label 为 2 | value |

先确保最外层是字典，才能按字段读取；先确保 text 是字符串，才能 strip；先确保 label 是本题允许的整数类型，才能检查值域。**格式能解析、字段类型正确、符合使用约定，是三件事。**

### 为什么原始行号必须在跳过空行之前取得
用 `enumerate(text.splitlines(), start=1)` 先得到物理行号，再跳过空行。如果先删掉空行再编号，第 3 行的错误就可能被写成第 2 行，回原文件时会找错位置。

新增示例 13_08 有 6 行：第 1 行合法、第 2 行为空、第 3 行 JSON 损坏、第 4 行字段类型错误、第 5 行 label 超范围、第 6 行合法。先手算：保留 2 条、跳过 1 行、记录 3 个错误，错误行号应为 3、4、5。运行后逐个比对。

### 坏行之后还能继续，是因为明确选择了 continue
解析失败后先保存行号和错误类别，再 continue 到下一行；合法行才加入 records。try 只包住 json.loads，并只捕获 JSONDecodeError。若把整个处理函数都包进宽泛的 except 后默默跳过，拼错变量名等程序缺陷也可能被隐藏。

这个例子处理内存字符串，所以每次运行不改任何数据文件。接入第 12 章文件读取时，可以把 `Path(...).read_text(encoding="utf-8")` 的结果交给函数。文件不存在或编码不对属于读取层错误，不能冒充“某一行 JSON 不合法”；大文件逐行流式读取留作后续改写。
''')
    example(chapters[13], '作用域排错：先复现，再用参数和返回值修复', '''
    rounds = 0

    def broken_round():
        rounds += 1
        return rounds

    try:
        broken_round()
    except UnboundLocalError as error:
        print(type(error).__name__)
    print(f"外部轮数：{rounds}")

    def fixed_round(current):
        return current + 1

    rounds = fixed_round(rounds)
    rounds = fixed_round(rounds)
    print(f"修复后：{rounds}")
    ''', '''
    UnboundLocalError
    外部轮数：0
    修复后：2
    ''', 'broken_round 的 += 要读取还不存在的局部 rounds，赋值未能完成就出错。捕获异常后，外部 rounds 仍为 0。fixed_round 两次分别收到 0 和 1，返回 1 和 2，调用者保存返回值后得到 2。捕获错误本身没有修复逻辑；修复来自明确的参数和返回值。',
    '把第二次修复调用改成单独的 fixed_round(rounds)，不接收返回值，预测最后输出。再对照第 09 章 09_10，解释“报错”和“能运行但没保存结果”的区别。')
    exercise(chapters[13], '作用域修复：统计工具执行成功次数', '场景',
    '坏思路是在函数中直接给外部 total += 1。请改为实现 count_successes(results, start=0)：results 保证是布尔列表，start 保证为非负整数。以 start 为起点，只为 True 增加 1，返回新计数，不修改 results，不依赖全局计数，不打印。设 total=10，用 [True, False, True] 调用后保存到 total 并打印。',
    '进入函数先用 count=start 建立局部计数；循环中按结果更新 count，最后 return。外面用 total = count_successes(..., start=total)。',
    '''
    def count_successes(results, start=0):
        count = start
        for succeeded in results:
            if succeeded:
                count += 1
        return count

    total = 10
    total = count_successes([True, False, True], start=total)
    print(total)
    ''', '12',
    '局部 count 有明确初始值，所以 += 有旧值可读。三次判断后依次是 11、11、12；调用者再把返回的 12 存为 total。空列表应原样返回 start；全 False 不增加；重复调用默认 start=0 时不能记住上一次结果。这里的 True/False 是固定输入，只表示练习中的状态标记，不证明真实模型回答质量。',
    tests='''
    assert count_successes([]) == 0
    assert count_successes([], start=7) == 7
    assert count_successes([False, False], start=3) == 3
    assert count_successes([True, True]) == 2
    assert count_successes([True]) == 1
    assert count_successes([True]) == 1, "多次调用不能共享全局计数"
    data = [True, False, True]
    assert count_successes(data, start=10) == 12
    assert data == [True, False, True]
    import contextlib, io
    capture = io.StringIO()
    with contextlib.redirect_stdout(capture):
        count_successes([True])
    assert capture.getvalue() == ""
    ''')
    add_jsonl(chapters)


def add_jsonl(chapters):
    example(chapters[13], 'AI 数据排错：保留坏行位置，继续处理下一行', r'''
    import json

    def read_training_lines(text):
        records, errors = [], []
        blank_lines = 0
        for line_number, line in enumerate(text.splitlines(), start=1):
            if not line.strip():
                blank_lines += 1
                continue
            try:
                item = json.loads(line)
            except json.JSONDecodeError:
                errors.append({"line": line_number, "kind": "json"})
                continue
            if not isinstance(item, dict):
                errors.append({"line": line_number, "kind": "schema"})
                continue
            content = item.get("text")
            label = item.get("label")
            if not isinstance(content, str) or type(label) is not int:
                errors.append({"line": line_number, "kind": "schema"})
                continue
            if not content.strip() or label not in (0, 1):
                errors.append({"line": line_number, "kind": "value"})
                continue
            records.append({"text": content.strip(), "label": label})
        return records, errors, blank_lines

    text = '\n'.join([
        '{"text": " Python ", "label": 1}',
        '',
        '{"text": "broken", "label": 0',
        '{"text": 42, "label": 0}',
        '{"text": "hello", "label": 2}',
        '{"text": "Agent", "label": 0}',
    ])
    records, errors, blank_lines = read_training_lines(text)
    print(f"保留 {len(records)} 条，跳过 {blank_lines} 个空行")
    for error in errors:
        print(f"第 {error['line']} 行：{error['kind']}")
    print(records)
    ''', '''
    保留 2 条，跳过 1 个空行
    第 3 行：json
    第 4 行：schema
    第 5 行：value
    [{'text': 'Python', 'label': 1}, {'text': 'Agent', 'label': 0}]
    ''', '输入文本先分行并编号；空行跳过但保留原行号；每行依次经过解析、类型和取值检查；只有合格记录进入 records。坏行的类别与行号进入 errors，不影响第 6 行被保留。多个字段同时出错时，只报告本程序最先检查到的类别，不代表已经列出所有问题。这里只检查数据格式，没有训练模型。',
    '把第 4 行的 label 改为 true、text 改为 "ok"，预测它仍属于 schema；再把第 5 行 text 改为空白且 label 改为 0，预测属于 value。最后在首行前加一个空行，核对所有原错误行号加 1。')
    exercise(chapters[13], 'AI / Agent：逐行检查工具日志并记录错误', '综合',
    '实现 read_tool_log(text)，输入保证是字符串。每个非空行应为 JSON 对象，tool 为非空字符串，ok 为 bool。跳过空行；合法记录将 tool.strip() 后保存为只含 tool、ok 的新字典。返回 (records, errors)，errors 每项为 {"line":原始行号,"kind":类别}；坏 JSON 类别为 json，非字典/缺字段/类型错误为 schema，tool 仅空白为 value。每行最多报一个错误，按上述顺序检查。五行依次为 {"tool":" search ","ok":true}、空行、bad-json、{"tool":"count","ok":1}、{"tool":"save","ok":false}。最后打印 records 和 errors，各占一行。',
    '沿用示例的 enumerate → 跳空行 → try loads → 检查类型 → 检查取值顺序；ok=1 不是本题允许的 bool。不要在编号之前删除空行。',
    r'''
    import json

    def read_tool_log(text):
        records, errors = [], []
        for line_number, line in enumerate(text.splitlines(), start=1):
            if not line.strip():
                continue
            try:
                item = json.loads(line)
            except json.JSONDecodeError:
                errors.append({"line": line_number, "kind": "json"})
                continue
            if not isinstance(item, dict):
                errors.append({"line": line_number, "kind": "schema"})
                continue
            tool = item.get("tool")
            ok = item.get("ok")
            if not isinstance(tool, str) or not isinstance(ok, bool):
                errors.append({"line": line_number, "kind": "schema"})
                continue
            if not tool.strip():
                errors.append({"line": line_number, "kind": "value"})
                continue
            records.append({"tool": tool.strip(), "ok": ok})
        return records, errors

    text = '\n'.join([
        '{"tool":" search ","ok":true}',
        '',
        'bad-json',
        '{"tool":"count","ok":1}',
        '{"tool":"save","ok":false}',
    ])
    records, errors = read_tool_log(text)
    print(records)
    print(errors)
    ''', '''
    [{'tool': 'search', 'ok': True}, {'tool': 'save', 'ok': False}]
    [{'line': 3, 'kind': 'json'}, {'line': 4, 'kind': 'schema'}]
    ''', '第 2 行为空，但第 3 行仍编号为 3。第 4 行 ok 是整数 1，不能当作 bool。第 5 行 ok=False 表示日志记录的工具状态失败，但这条日志本身格式合法，所以应保留。日志的格式合格与记录的操作成功是两件事；额外字段按题目约定不进入新记录。本题既不重新执行工具，也不证明日志内容真实。',
    tests=r'''
    assert read_tool_log("") == ([], [])
    assert read_tool_log(" \n\r\n") == ([], [])
    good = '{"tool":" save ","ok":false,"extra":1}'
    assert read_tool_log(good) == ([{"tool":"save","ok":False}], [])
    text = '\r\n'.join(['', 'bad', good])
    assert read_tool_log(text) == ([{"tool":"save","ok":False}], [{"line":2,"kind":"json"}])
    bad_schema = ['[]', 'null', '{}', '{"tool":"a","ok":1}', '{"tool":1,"ok":true}', '{"tool":"a","ok":"false"}']
    for line in bad_schema:
        assert read_tool_log(line) == ([], [{"line":1,"kind":"schema"}]), line
    assert read_tool_log('{"tool":"  ","ok":true}') == ([], [{"line":1,"kind":"value"}])
    both_bad = '{"tool":" ","ok":0}'
    assert read_tool_log(both_bad) == ([], [{"line":1,"kind":"schema"}])
    assert read_tool_log(good + '\n' + good) == ([{"tool":"save","ok":False}, {"tool":"save","ok":False}], [])
    assert read_tool_log(good) == ([{"tool":"save","ok":False}], []), "不同调用不能共用结果列表"
    ''')
