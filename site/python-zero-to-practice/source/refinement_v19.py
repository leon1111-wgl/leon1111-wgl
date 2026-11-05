"""v1.9：遍历时删除导致漏项；原创追踪、边界与离线请求分类练习。"""
from course_data import example, exercise
from refinements import add_body


def apply_v19(chapters):
    add_body(chapters, 7, '''
### 列表筛选精修：列表变短了，下一次还取原来的位置吗
前置：第 04 章条件、第 05 章 for，以及本章的索引、append、remove 和 copy。这里不用函数、推导式或深拷贝。目标约定：给定整数列表，保留所有非负数，包括 0；保持它们出现的顺序和次数，原输入不变。

先看示例 07_08 的错误尝试：输入是 `[-2, -1, 0, 4]`，wrong 是它的副本。循环读到负数就调用 `wrong.remove(value)`。这段代码能运行结束，但结果里仍有 -1。为什么“每次遇到负数都删了”，却没删完？

### 追踪错误：元素向左挪，取值位置仍向右走
本例的列表遍历可按“下次要读哪个索引”来追踪；列表被删短时，这个位置不会自动退回。表中的位置用于解释过程，代码中不需要自己维护它。visited 只记录实际进入过循环体的 value。

| 本次取值位置 | 取值前的 wrong | 拿到的 value | 动作与取值后的 wrong | 下一次取值位置 |
| --- | --- | --- | --- | --- |
| 0 | `[-2, -1, 0, 4]` | -2 | 删除 -2，变成 `[-1, 0, 4]` | 1 |
| 1 | `[-1, 0, 4]` | 0 | 不删除，仍为 `[-1, 0, 4]` | 2 |
| 2 | `[-1, 0, 4]` | 4 | 不删除，仍为 `[-1, 0, 4]` | 3 |
| 3 | `[-1, 0, 4]` | 无 | 当前长度为 3，遍历结束 | 不再取值 |

删掉索引 0 后，-1 从原来的索引 1 移到索引 0。下一次却读索引 1，于是直接读到 0，**-1 从未进入判断**。实际访问顺序是 `[-2, 0, 4]`，不是原输入的四项。循环正常走完，只说明没有继续取到元素，不能证明每个原始元素都检查过。

`remove(value)` 按值删除第一个相等元素；`pop(index)` 按位置删除。换成 pop 仍会让后续元素移位，不能靠换一个删除方法修好这个循环。把 wrong 写成原列表的别名还会连带修改原输入，因此示例先 copy，只是为了隔离错误演示；**复制了 wrong，并没有让“遍历 wrong 时修改 wrong”变正确。**

### 修正：从原列表读，向新列表写
先创建 `kept = []`。每次从 values 取一项，通过 `value >= 0` 才向 kept 追加；不从正在遍历的 values 中删除东西。原输入的四项都会被依次访问。

| 当前 value | value >= 0 | 本轮动作 | 本轮结束后的 kept |
| --- | --- | --- | --- |
| -2 | False | 不追加 | `[]` |
| -1 | False | 不追加 | `[]` |
| 0 | True | append(0) | `[0]` |
| 4 | True | append(4) | `[0, 4]` |

记忆法：**读一份，写另一份；先判定，再追加。** “不追加”就完成了过滤，不需要先复制所有数据再删掉坏项。kept 在循环前初始化，否则每轮都会清空之前的结果。`if value:` 不符合本题规则：它会丢掉合法的 0，也会把负数当作真；应明确比较数值范围。

还有一种做法是遍历副本、删除原列表里的元素，它可以避免遍历对象本身缩短，但会修改原输入，和本题约定不同。先写清是否允许修改输入，再选实现。筛选也不是深拷贝：本例元素是整数；将来若元素换成字典，append 保存的仍是那条字典的引用，修改字段前要回顾本章的浅拷贝。

### 先改输入，再判断修正是否可靠
1. **预测：** 遮住示例 07_08 的输出，在纸上逐轮写出 wrong 和下一次取值位置。用 visited 找出哪项从未被检查，而不是只盯着最后的列表。
2. **纠错：** 把输入依次换成 `[-2, -1]`、`[-2, 0, -1, 4]` 和 `[0, 4]`。错误版本分别得到 `[-1]`、`[0, 4]`、`[0, 4]`；后两组碰巧正确，不代表程序可靠。正确版本依次得到 `[]`、`[0, 4]`、`[0, 4]`。
3. **补边界：** 空输入 `[]` 的两个循环都执行零次，kept 仍为 `[]`；`[0, 0, -1, 4, 4]` 应保留 `[0, 0, 4, 4]`。重复的有效项仍要保留，这道题不要求去重。再打印 values，确认原输入没变。
4. **迁移：** 完成习题 07_09，把一批工具请求按名称分到 accepted 和 rejected。两个列表分别初始化，不能用 `accepted = rejected = []`，否则两个名字会指向同一列表。

### 把筛选迁移到 Agent 的候选请求
`name in allowed` 表示 name 是否等于 allowed 列表中的某一项；本题精确匹配字符串，区分大小写，不做 strip 或 lower。每次请求只进入 if/else 的一个分支，分别 append 到新列表；两个结果各自保留原有相对顺序和重复次数。

可以先用 `len(accepted) + len(rejected) == len(requests)` 检查总数是否相符，再检查各组内容与顺序。长度相同不能单独证明分类正确。`accepted + rejected` 通常也不等于原 requests，因为交错的请求已被分开；这里没有要求保留两组之间的交错位置。以后需要还原完整顺序时，再记录原位置或请求 ID。

这些名称都是预先写好的字符串，accepted 仅表示“名称在本题允许名单中”。本练习没有发出工具调用、调用模型或读取外部数据，也没有验证参数、权限和结果质量。第 08 章可将每条请求改为字典，第 13 章学习字段校验，第 16 章再连接执行与结果判断。知识图谱的“列表与顺序 ↔ Agent 工具流程”串起这条学习链路。
''')
    chapters[7]['checkpoint'].append('我能追踪删除后漏掉的元素，并通过建立新列表完成保序筛选与分类。')
    example(chapters[7], '列表筛选：为什么连续的负数漏掉一个', '''
    values = [-2, -1, 0, 4]
    wrong = values.copy()
    visited = []
    for value in wrong:
        visited.append(value)
        if value < 0:
            wrong.remove(value)

    kept = []
    for value in values:
        if value >= 0:
            kept.append(value)

    print("错误遍历访问：", visited)
    print("错误结果：", wrong)
    print("保留结果：", kept)
    print("原输入：", values)
    ''', '''
    错误遍历访问： [-2, 0, 4]
    错误结果： [-1, 0, 4]
    保留结果： [0, 4]
    原输入： [-2, -1, 0, 4]
    ''', 'wrong 删除 -2 后，-1 移到了刚读过的位置，所以 visited 没有它；没有运行错误也可能漏掉数据。正确循环始终读 values，只向 kept 写入，0 和 4 被依次追加。原输入保留，是因为错误尝试在副本上进行，正确尝试没有修改 values。',
    '依次试连续负数、间隔负数、全有效、空列表和重复有效项。每次只修改 values 的初始值，同时核对 visited、wrong、kept 与原输入。')
    exercise(chapters[7], 'Agent 候选请求：分到两份新列表', '迁移',
    'allowed = ["search", "count"]，requests = ["search", "skip", "skip", "count", "search"]，输入保证为字符串列表。用普通 for 和 if/else，把名称在 allowed 中的请求追加到新列表 accepted，其余追加到另一个新列表 rejected。精确匹配，区分大小写，不清理空白；每组保持原有相对顺序和重复次数，不修改 allowed 或 requests，不执行工具。依次打印 accepted、rejected、requests，各占一行。不写函数、集合或推导式。',
    '循环前分别写 accepted = [] 和 rejected = []；用 name in allowed 判断，两个分支各追加一次。不要边遍历边 remove，也不要让两个结果共享同一列表。', '''
    allowed = ["search", "count"]
    requests = ["search", "skip", "skip", "count", "search"]
    accepted = []
    rejected = []
    for name in requests:
        if name in allowed:
            accepted.append(name)
        else:
            rejected.append(name)
    print(accepted)
    print(rejected)
    print(requests)
    ''', '''
    ['search', 'count', 'search']
    ['skip', 'skip']
    ['search', 'skip', 'skip', 'count', 'search']
    ''', '五次循环依次把 search 放入 accepted、两次 skip 分别放入 rejected、count 放入 accepted、最后的 search 再放入 accepted。重复请求不合并。空 requests 得到两份独立的空列表；全不支持时 accepted 为空，rejected 保留所有原项；allowed 为空时同样全部进入 rejected。"Search"、" search " 和空串都不匹配默认名单。总数相符只是第一步，还要核对内容、顺序和原输入。在分类后向 accepted 追加一个标记，rejected 与 requests 都不应变化；随后恢复代码再自检。名称可接受不代表工具已执行或任务成功。')
