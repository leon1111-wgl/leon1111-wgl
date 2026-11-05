"""v1.6：切片方向、边界与消息条数；代码、数据和分层任务独立编写。"""
from course_data import example, exercise
from refinements import add_body


def apply_v16(chapters):
    add_body(chapters, 3, '''
### 切片精修：先画索引，再决定往哪边走
前置只用本章的字符串、索引、切片和 repr；不需要循环、列表或函数。先用 `s = "KLMNOP"` 在纸上画六个格子。窄屏上可横向滑动表格，查看后面的索引和结果：

| 字符 | K | L | M | N | O | P |
| --- | --- | --- | --- | --- | --- | --- |
| 正索引 | 0 | 1 | 2 | 3 | 4 | 5 |
| 负索引 | -6 | -5 | -4 | -3 | -2 | -1 |

负索引是从末尾定位的另一种写法，**不决定移动方向**。`s[-3:]` 从 N 开始，默认步长 +1，结果仍是 NOP。步长为负才向左走。读切片时依次问：从哪里出发？往哪边、每次几格？到哪个位置之前停止？

| 表达式 | 出发与方向 | 真正取到的正索引 | 结果的 repr |
| --- | --- | --- | --- |
| s[1:5:2] | 从 1 向右，每次 2 格 | 1、3 | 'LN' |
| s[4:1:-1] | 从 4 向左，每次 1 格，1 不取 | 4、3、2 | 'ONM' |
| s[1:4:-1] | 从 1 向左，但终点 4 在右边 | 无，一开始就不满足方向条件 | '' |
| s[5:0:-1] | 从 5 向左，0 不取 | 5、4、3、2、1 | 'PONML' |
| s[5::-1] | 从 5 向左，终点省略 | 5、4、3、2、1、0 | 'PONMLK' |
| s[5:-1:-1] | 末尾 -1 对应正索引 5；起点也是 5 | 无，起点等于排除的终点 | '' |

记忆顺序：**先方向，再定位；起点能取，终点不取。** 在这里有效索引范围内，正步长要求当前位置小于终点，负步长要求当前位置大于终点；起点等于终点时一个字符也不取。越界端点还会按序列长度调整，不能只拿原始数字相减猜长度。

### 为什么倒序时省略终点，不等于填写 -1
`s[5::-1]` 中空着的 stop 告诉 Python 沿负方向一直取到开头，包含索引 0。`s[5:-1:-1]` 中明确写出的 -1 会先按“倒数第一格”定位到 P，也就是正索引 5；从 5 出发又要在 5 之前停止，因此为空。不要把“省略终点”机械替换成 -1。

相同原则用于省略 start：正步长默认从开头出发，负步长默认从末尾出发。`s[::-1]` 可以完整倒序。空字符串 `""[::-1]` 仍是空字符串；`s[99:]` 也为空，但 `s[99]` 会越界报错。步长 0 不表示“不移动”，而是非法，会抛 ValueError；第 13 章再学如何处理异常。

### 三层练习：读懂、修边界、换场景
1. **预测：** 遮住示例 03_07 的输出，在上表每一行圈出索引。运行时用 repr 看清空字符串，避免把空白行误认为程序没有执行。
2. **修边界：** 想得到 ONML，应该把 `s[4:1:-1]` 的 stop 改成什么？先写取到的索引，再改示例副本。答案是 0：索引 4、3、2、1，排除 0。接着把 s 改成空字符串，预测所有切片都为空，再运行。
3. **迁移：** 完成习题 03_09 的设备短码。复杂切片可以先取一段，再反转这一段；多命名一个中间值，往往比挤在一行更容易检查。

学到第 05 章后再回来比较：`range(5, -1, -1)` 产生数字 5 到 0，里面的 -1 就是数字边界；字符串切片里的 -1 则会按序列末尾解释。因此不能把 range 的三个参数原样搬进切片。第 07 章把这套“位置与顺序”迁移到列表，第 09 章示例 09_11 再处理保留最近消息时的零值边界。
''')
    chapters[3]['checkpoint'].append('我能解释反向切片中省略 stop 与写 -1 为什么不同。')
    example(chapters[3], '切片追踪：同样倒着走，为何有时为空', '''
    s = "KLMNOP"
    print(repr(s[1:5:2]))
    print(repr(s[4:1:-1]))
    print(repr(s[1:4:-1]))
    print(repr(s[5:0:-1]))
    print(repr(s[5::-1]))
    print(repr(s[5:-1:-1]))
    ''', """
    'LN'
    'ONM'
    ''
    'PONML'
    'PONMLK'
    ''
    """, '每次 print 都从同一个 s 取片段，s 本身不变。第 3 行的方向不匹配；第 6 行的 -1 定位到索引 5，恰好等于起点。这两行都返回空字符串，repr 将它显示为两个引号。第 4 行排除了 K，第 5 行省略终点后才包含 K。',
    '先将第 2 行切片的 stop 从 1 改成 0，手算 ONML；恢复后将 s 改成空字符串，再预测六行输出。不要把切片替换成单个索引来判断空串是否安全。')
    exercise(chapters[3], '设备短码：先取一段，再反转', '迁移',
    '给定 code = "Q7M2R8"。保存 tail 为最后 3 个字符，head 为前 3 个字符。依次输出 tail、tail 的倒序、head 的倒序，每项一行。最后输出 repr(code[2:-1:-1])，并解释为何它不是前 3 个字符的倒序。本题只用字符串、赋值、切片和 print，不写函数。',
    '先用 [-3:] 与 [:3] 定位两段；在中间变量上再用 [::-1]。最后一行的显式 stop=-1 会定位到原字符串索引 5。', '''
    code = "Q7M2R8"
    tail = code[-3:]
    head = code[:3]
    print(tail)
    print(tail[::-1])
    print(head[::-1])
    print(repr(code[2:-1:-1]))
    ''', """
    2R8
    8R2
    M7Q
    ''
    """, '输入先得到 tail="2R8"、head="Q7M"，反转的是已经截取的片段。最后一行从索引 2 向左走，排除的终点却是索引 5，因此为空。想直接从索引 2 取到开头，可写 code[2::-1]。改成 code="Q7" 后，tail 与 head 都是 Q7，两个倒序都为 7Q；不足三项不报错。改成空串时前三行是空白行，最后一行显示两个引号。真实设备短码若有固定长度要求，还需要另写验证规则。')

    add_body(chapters, 9, '''
### 函数迁移：最近 N 条消息，为什么 N=0 不能直接切
前置：第 03 章切片、第 04 章 if、第 07 章列表与浅拷贝，以及本章参数和 return。这里只用字符串列表表示按时间从旧到新排列的消息，没有调用模型或网络服务。

先写函数约定：`latest_messages(messages, keep)` 接收字符串列表，keep 已由调用者保证为非负整数（不使用 bool）；返回一个新列表，包含最后至多 keep 条消息，保留原时间顺序。keep=0 表示本次不选历史，返回 []；keep 大于消息条数就选全部；原列表不变。这是本例的产品规则，不是所有聊天程序都必须采用的规则。

常见写法 `messages[-keep:]` 对正数有效，却在 0 时出错：**-0 仍是 0**，因此 `messages[-0:]` 等于 `messages[0:]`，得到全部。语法合法、程序不报错，也可能违反“保留零条”的任务要求。修复方法是先用 if 单独处理零值，并 return；只有正数才继续走末尾切片。

| 输入 messages 均为 ['先读题', '列步骤', '做检查'] | 中间判断 | 实际返回 | 原列表 |
| --- | --- | --- | --- |
| keep=2 | 不是 0；从倒数第二项向右取 | ['列步骤', '做检查'] | 不变 |
| keep=0 | 等于 0；立即 return [] | [] | 不变 |
| keep=5 | 不是 0；起点越过开头后截到有效范围 | 全部三条，仍按原顺序 | 不变 |

这不是 `messages[:keep]`（取最早的几条），也不是 `messages[::-1][:keep]`（把顺序反过来）。选中最近两条后，仍要先看到“列步骤”，再看到“做检查”。列表切片会新建外层列表，因此对返回列表 append 不会给原列表追加元素；如果以后消息是字典，切片并不会复制每个字典，仍要复习第 07 章的浅拷贝。

### 从保留消息迁移到分开历史：做完再看解析
1. **预测：** 运行示例 09_11 前写下 keep=2、0、5 时“直接切片”与“按约定选择”的结果，找出唯一不一致的一组。
2. **改写：** 在自己的副本里试 keep=1、空列表、只有一条消息。每次把原输入也打印出来，检查没有被改动。不要为方便调用而把 messages 设成共享默认列表。
3. **独立实现：** 完成习题 09_11 的 split_history，将更早与最近的消息分别返回。手算检验：older + recent 必须恰好等于原输入，不能丢失、重复或改变顺序。

本章不为负数、小数或字符串参数定义行为；这些违反上述前提。学完第 13 章后可在函数最前面加 `type(keep) is not int or keep < 0` 的检查并抛 ValueError，再补非法输入测试。第 14 章 RecentMessages 要求 limit 严格大于 0；本例允许 keep=0，约定不同，不要直接照抄边界。

**与大模型的联系：** 这里控制的是消息条数，不是字符数或 token 数。一条很长的消息仍然只算一条；截取成功不保证符合模型上下文长度，更不保证保留了任务所需信息。真实会话还可能需要保留系统规则、成对的工具调用与结果。先用本地规则学会明确输入、边界与返回，再在第二阶段学习具体模型和 tokenizer。
''')
    chapters[9]['checkpoint'].append('我能手算 keep=0 的消息选择，并检验旧消息与新消息能按顺序拼回输入。')
    example(chapters[9], 'AI / Agent：最近消息的零条边界', '''
    def latest_messages(messages, keep):
        if keep == 0:
            return []
        return messages[-keep:]

    messages = ["先读题", "列步骤", "做检查"]
    for keep in [2, 0, 5]:
        print("keep =", keep)
        print("直接切片：", messages[-keep:])
        print("按约定选择：", latest_messages(messages, keep))
    print("原消息：", messages)
    ''', '''
    keep = 2
    直接切片： ['列步骤', '做检查']
    按约定选择： ['列步骤', '做检查']
    keep = 0
    直接切片： ['先读题', '列步骤', '做检查']
    按约定选择： []
    keep = 5
    直接切片： ['先读题', '列步骤', '做检查']
    按约定选择： ['先读题', '列步骤', '做检查']
    原消息： ['先读题', '列步骤', '做检查']
    ''', 'for 只是安排三次独立调用。keep=0 时函数提前返回，所以不会再执行末尾的切片。keep=5 时选中全部也会新建外层列表；原 messages 不被删除或改序。所有输出由调用者 print，函数本身只返回数据。',
    '在自己的副本追加 result = latest_messages(messages, 2)，再对 result.append("新消息")；预测并打印两个列表。随后用 keep=0 和空 messages 重试，仍应互不追加。')
    exercise(chapters[9], 'AI / Agent：将更早历史与最近消息分开', '迁移',
    '实现 split_history(messages, keep)。messages 是按从旧到新排列的字符串列表；keep 保证为非负整数，不使用 bool。返回 (older, recent)：recent 是最后至多 keep 条且顺序不变，older 是前面的其余消息。keep=0 时 recent=[]、older 包含全部；keep 超过长度时 older=[]、recent 包含全部。两个返回值每次都是新的外层列表，不修改输入，也不在函数内打印。打印对 ["问候", "提问", "检索", "回答"] 分别取 keep=2 与 keep=0 的返回值。',
    '先处理 keep==0，此时用 messages[:] 复制全部。正数时，[:-keep] 是边界前的部分，[-keep:] 是边界后的部分。返回两个列表，调用者再 print。', '''
    def split_history(messages, keep):
        if keep == 0:
            return messages[:], []
        return messages[:-keep], messages[-keep:]

    messages = ["问候", "提问", "检索", "回答"]
    print(split_history(messages, 2))
    print(split_history(messages, 0))
    ''', '''
    (['问候', '提问'], ['检索', '回答'])
    (['问候', '提问', '检索', '回答'], [])
    ''', 'keep=2 的分界在索引 2：older 取 0、1，recent 取 2、3。keep=0 不能直接套同一组切片，否则得到 ([], 全部)，恰好与题意相反。返回 messages 本身虽然内容相同，却没有满足新列表约定；调用者 append 会改动原输入。keep 很大时两段分别为 [] 和全部。更早消息仍在返回结果里，不代表已经被删除、保存到磁盘或摘要化；这是本地列表拆分练习，不是真实模型记忆。',
    tests='''
    assert split_history([], 0) == ([], [])
    assert split_history([], 3) == ([], [])
    assert split_history(["一条"], 0) == (["一条"], [])
    assert split_history(["一条"], 1) == ([], ["一条"])
    assert split_history(["a", "b", "c"], 1) == (["a", "b"], ["c"])
    assert split_history(["a", "b", "c"], 3) == ([], ["a", "b", "c"])
    assert split_history(["a", "b", "c"], 9) == ([], ["a", "b", "c"])
    assert split_history(["重复", "重复", "末条"], 2) == (["重复"], ["重复", "末条"])
    for messages in ([], [""], ["a", "b", "c", "d"]):
        before = messages[:]
        for keep in (0, 1, len(messages), len(messages) + 2):
            pair = split_history(messages, keep)
            assert isinstance(pair, tuple) and len(pair) == 2
            older, recent = pair
            assert isinstance(older, list) and isinstance(recent, list)
            assert older + recent == before, "不能漏项、重复或改变原顺序"
            assert len(recent) == min(keep, len(messages))
            assert messages == before, "不能修改原输入"
            assert older is not messages and recent is not messages and older is not recent
            older.append("只追加到旧列表")
            assert recent == before[len(before) - min(keep, len(before)):]
            recent.append("只追加到新列表")
            assert messages == before, "返回列表追加内容不能污染输入"
    first = split_history(["a", "b"], 1)
    first[1].append("临时项")
    assert split_history(["a", "b"], 1) == (["a"], ["b"])
    import contextlib, io
    capture = io.StringIO()
    with contextlib.redirect_stdout(capture):
        split_history(["a"], 0)
        split_history(["a"], 1)
    assert capture.getvalue() == "", "函数只返回数据，不打印"
    ''')
