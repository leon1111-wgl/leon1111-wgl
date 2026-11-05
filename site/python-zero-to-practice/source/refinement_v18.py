"""v1.8：文本清理的匹配单位与位置；原创场景、数据、追踪和习题。"""
from course_data import example, exercise
from refinements import add_body


def apply_v18(chapters):
    add_body(chapters, 3, '''
### 文本清理精修：删的是空白、字符，还是一整段标记
前置只用本章的字符串、方法调用、赋值与 repr，不需要条件、循环或函数。处理用户输入或工具标签前，先把要求说具体：**删什么？从哪里删？最多删几次？** “把文本清理一下”还不足以决定代码。

| 要求 | 方法 | 匹配单位与位置 |
| --- | --- | --- |
| 去掉两端空白，保留中间空格 | `text.strip()` | 从左右两端连续去掉空白字符 |
| 去掉开头的一次完整标记 | `text.removeprefix("tool:")` | 完整的 tool:，必须位于开头，区分大小写 |
| 去掉结尾的一次完整标记 | `text.removesuffix(".txt")` | 完整的 .txt，必须位于结尾，区分大小写 |
| 从左端去掉指定字符，直到碰到别的字符 | `text.lstrip("tool:")` | t、o、l、: 中的任意字符，不要求组成 tool: |
| 替换所有出现的片段 | `text.replace("tool:", "")` | 完整片段，但不限开头；默认替换所有匹配 |

prefix 是“前缀”，suffix 是“后缀”。这两个 remove 方法从 Python 3.9 起提供，本教材的 Python 3.10+ 可以使用。没匹配到就保留原内容，不会报“找不到”的错误；匹配到也只去掉一次。传入空前缀或空后缀时内容不变。这里的所有字符串方法都不原地修改原字符串，想继续使用结果就要赋值接住。

### 逐字符追踪：为什么工具名 lookup 会变成 kup
离线约定：文本开头的 tool: 是标签，后面的 lookup 才是工具名。它只是预设文本，没有执行工具或调用大模型。

| 步骤 | 表达式 | 结果的 repr | 解释 |
| --- | --- | --- | --- |
| 原始输入 | `raw` | `'  tool:lookup  '` | 两边各有两个空格 |
| 清理空白 | `cleaned = raw.strip()` | `'tool:lookup'` | 中间内容保持原样 |
| 错误尝试 | `cleaned.lstrip("tool:")` | `'kup'` | 从左边连续删掉 t、o、o、l、:、l、o、o，遇到 k 才停 |
| 按完整标记处理 | `name = cleaned.removeprefix("tool:")` | `'lookup'` | 只删开头完整的五个字符 tool: |
| 回看原输入 | `raw` | `'  tool:lookup  '` | 原字符串并未被修改 |

**关键区别：** `lstrip("tool:")` 把参数中的字符当作“允许删除的字符名单”；名单顺序没有意义，重复写 o 也没有额外作用。这里说的名单只是帮助理解，不需要先学第 08 章的集合类型。把它换成 strip 会同时从左右两端做这种删除；换成 rstrip 则只从右端做。参数不自动附加空白，所以对原始 raw 直接调用 `lstrip("tool:")`，遇到第一个空格便停止，内容完全不变。

右端也有同类错误：`"report.txt".rstrip(".txt")` 从右边依次删掉 t、x、t、点，以及 report 本来就有的最后一个 t，结果是 'repor'。若约定只去掉结尾 .txt，应该用 removesuffix，得到 'report'。这只是已知文本标记的练习；真实文件路径的目录、扩展名和打开操作留到第 12 章用 pathlib 学习。

### 顺序也是规则：先保存中间值，再连成一行
习题 03_10 的约定是：先去两端空白，再去开头一次 tool:，最后去结尾一次 .txt；保留其余内容。用 cleaned、without_prefix、name 三个变量追踪，再考虑链式调用。下面每一行都独立从该行 raw 开始：

| raw 的 repr | cleaned | without_prefix | name 的 repr |
| --- | --- | --- | --- |
| `'  tool:lookup.txt  '` | tool:lookup.txt | lookup.txt | `'lookup'` |
| `'tool:tool:lookup.txt.txt'` | tool:tool:lookup.txt.txt | tool:lookup.txt.txt | `'tool:lookup.txt'` |
| `'memo:tool:lookup.txt'` | memo:tool:lookup.txt | memo:tool:lookup.txt | `'memo:tool:lookup'` |
| `'tool:report.txt.bak'` | tool:report.txt.bak | report.txt.bak | `'report.txt.bak'` |
| `'Tool:lookup.TXT'` | Tool:lookup.TXT | Tool:lookup.TXT | `'Tool:lookup.TXT'` |
| `'tool:.txt'` | tool:.txt | .txt | `''` |

第一行若先 removeprefix 再 strip，前缀检查时最左边还是空格，因此不会删除 tool:；后来去掉空格，也不会自动回头重做前缀检查。第三行用 `replace("tool:", "", 1)` 同样不对：虽然最多替换一次，它仍会删除中间的 tool:。**完整匹配不等于只匹配开头，删除一次也不等于删除前缀。**

空字符串和全空白输入经过这三步都得到 ''。`"tool: lookup.txt"` 的结果则是 ' lookup'，保留开头那个空格：它原本位于原字符串中间，第一次 strip 没删到它；后面没有第二次 strip。需不需要再去掉它，要由输入约定决定，不能偷偷加一步改变数据。

### 三层实操：预测、纠错、迁移
1. **预测：** 遮住示例 03_08 的输出，逐字符划掉允许删除的内容。用 repr 看清空白和空串；运行后逐行对照，不只看最后一行。
2. **纠错：** 将示例的 raw 改成 "topic:python"。预测 lstrip 的结果为 'pic:python'，而 removeprefix 保持 'topic:python'；再改成 "tool:tool:lookup"，观察按完整前缀只删除一次。把文件名改为 "report.txt.bak"，两个右端处理都应保持原样。
3. **迁移：** 独立完成习题 03_10，再用上表逐行替换 raw，每次只改输入。把空串、全空白和内部空格也试一遍。不要为得到正确显示结果，直接把预期答案写进 print。

知识连接：第 09 章可把三步封装成函数，第 13 章再验证结果是否非空、是否是允许的工具名。清理成功只表示执行了约定的字符串变换；空名称仍可能需要拒绝。这里没有真实 Agent，也不测 token 数。今后接入模型后，工具名格式符合规则也不保证工具存在、调用成功或任务正确。知识图谱的“字符串与切片 ↔ 异常与数据校验”连接帮助你回顾这条链路。
''')
    chapters[3]['checkpoint'].append('我能区分两端空白、字符名单与完整前后缀，并用中间值检查清理顺序。')
    example(chapters[3], '文本清理：工具标签为什么越删越多', '''
    raw = "  tool:lookup  "
    cleaned = raw.strip()
    wrong = cleaned.lstrip("tool:")
    name = cleaned.removeprefix("tool:")
    print(repr(raw))
    print(repr(cleaned))
    print(repr(wrong))
    print(repr(name))

    filename = "report.txt"
    print(repr(filename.rstrip(".txt")))
    print(repr(filename.removesuffix(".txt")))
    ''', """
    '  tool:lookup  '
    'tool:lookup'
    'kup'
    'lookup'
    'repor'
    'report'
    """, '前四行从原文本到清理空白，再比较按字符与按完整标记的结果。wrong 和 name 都从 cleaned 计算，不把已经损坏的 wrong 再传给 removeprefix；删掉的内容不会自动恢复。后两行独立比较右端处理。repr 额外显示引号，使空格看得见；引号不是字符串里的字符。这里仅模拟工具标签，没有执行工具。',
    '先把 raw 改成 "topic:python"，再改成 "tool:tool:lookup"；每次只改输入并重新手算。最后把 filename 改成 "report.txt.bak"，检查不是结尾的 .txt 会保留。')
    exercise(chapters[3], '工具记录名：按约定清理两端', '迁移',
    'raw = "  tool:lookup.txt  "。约定按顺序执行：去掉两端空白，保存为 cleaned；只去掉开头一次完整 tool:，保存为 without_prefix；只去掉结尾一次完整 .txt，保存为 name。大小写必须相符，未匹配到的标记与内部内容保留，不增加第二次空白清理。依次输出 repr(cleaned)、repr(without_prefix)、repr(name)、repr(raw)，各占一行。只用字符串、赋值、方法调用和 print，不写函数。本题练习文本变换，不检查工具名是否可用。',
    '每一步都接住前一步的结果。strip() 不传字符参数；后两步使用 removeprefix 和 removesuffix，不能用 lstrip、rstrip 或全局 replace 代替。', '''
    raw = "  tool:lookup.txt  "
    cleaned = raw.strip()
    without_prefix = cleaned.removeprefix("tool:")
    name = without_prefix.removesuffix(".txt")
    print(repr(cleaned))
    print(repr(without_prefix))
    print(repr(name))
    print(repr(raw))
    ''', """
    'tool:lookup.txt'
    'lookup.txt'
    'lookup'
    '  tool:lookup.txt  '
    """, '输入先变为 tool:lookup.txt，再变为 lookup.txt，最后才是 lookup；打印原始 raw 可确认它没被改写。把 raw 换成 "tool:tool:lookup.txt.txt"，name 应为 "tool:lookup.txt"：两个标记各去一次。换成 "memo:tool:lookup.txt" 应为 "memo:tool:lookup"，中间标记保留；换成 "tool:report.txt.bak" 应为 "report.txt.bak"。空串、全空白或 "tool:.txt" 都可得到空 name，本题允许这一变换结果；后续校验再决定是否拒绝。换成 "tool: lookup.txt" 得到 " lookup"，前面的空格仍在，用 repr 核对。第 04 章以后可思考怎样另行判断空名称，第 13 章再处理不合约定的值。')
