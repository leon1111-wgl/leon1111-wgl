"""v1.1 教学增补：保留旧题号，在已有章节末尾增加场景示例和练习。"""
from textwrap import dedent
from course_data import example, exercise


def add_body(chapters, number, text):
    chapters[number]["body"] += "\n\n" + dedent(text).strip()


def apply_refinements(chapters):
    add_body(chapters, 0, """
### AI / Agent 穿插内容怎样学
主页的“部分内容为info1110课程”用于标记你的课程关联。基础语法可以配合课堂复习；v1.1 新增的 AI / Agent 场景是自编延伸练习，不据此推定课程的考核范围。

保持原来的顺序：先学本章语法，完成普通示例，再做本章最后的“AI / Agent”示例与练习。遇到暂时不懂的 AI 名词，先关注代码中的字符串、列表、判断和函数；不需要先学神经网络。

本轮的小实验只使用 Python 标准库，完全离线。提示词是给模型的文字要求；大模型（LLM）根据上下文生成内容；工具（tool）是程序可以调用的函数；Agent 则围绕目标组织决策、工具执行和结果反馈。这里用固定数据和规则模拟部分流程，**没有调用真实模型、没有网络推理、没有产生 API 费用**。

| 章节 | 穿插的场景 | 这次真正练的 Python |
| --- | --- | --- |
| 03 / 04 | 组织提示词、选择处理路径 | 字符串、f-string、条件顺序 |
| 06 / 08 | 限制执行步数、保存对话 | while、break、列表套字典 |
| 09 / 12 | 工具参数与结果、保存会话 | 函数返回值、JSON 文件 |
| 13 / 14 | 检查结构化输出、独立会话 | 异常、输入校验、实例属性 |
| 15 / 16 | 模拟流式片段、检索工具循环 | yield、状态更新、可追踪的执行过程 |

每个场景示例都有 `.py` 文件，新增练习仍可用同一自检器检查。旧题号和进度文件格式保留；在本版导入旧进度后，新题会显示为未完成。
""")
    add_body(chapters, 7, """
### 精讲：列表复制，到底复制到哪一层
先把名字想成指向对象的箭头。`b = a` 多画了一根箭头，并没有新建列表；`b = a.copy()` 新建一个外层列表，但外层里面装着的元素仍指向原来的对象。

以 `a = [[1], [2]]`、`b = a.copy()` 为例，先在纸上画出两个外层方框，再画两个内层方框。两个外层各自独立，但它们都指向那两个内层方框。

| 操作（各行都从上面的初始状态重新开始） | a | b | 原因 |
| --- | --- | --- | --- |
| b.append([3]) | [[1], [2]] | [[1], [2], [3]] | 只改 b 的外层 |
| b[0].append(9) | [[1, 9], [2]] | [[1, 9], [2]] | 改了共享的内层 |
| b[0] = [9] | [[1], [2]] | [[9], [2]] | 只换 b 外层第 0 格的箭头 |

回到示例 07_05，逐行运行，再分别替换成表中的操作。不要把三个操作连着执行后拿结果与表比较：表中每一行都假设你重新初始化了 a 和 b。

**迁移到会话记录：** `messages` 常是“列表里面装字典”。外层 `.copy()` 不能隔离每条字典里的修改。如果只是给复制后的列表追加新消息，外层复制常已够用；如果还要修改旧消息里的字段，就需要明确哪些层应独立。第 08 章先学会读写字典，第 14 章再处理不同会话的独立状态。
""")
    add_body(chapters, 9, """
### 精讲：把一次函数调用拆成五个时刻
读示例 09_01 时，按“实参 → 形参 → 函数体 → 返回值 → 接收位置”追踪。对于 `answer = add(2, 3)`：

| 时刻 | 正在发生什么 | 目前能知道什么 |
| --- | --- | --- |
| 1 | 计算调用括号里的 2 和 3 | 准备两个实参 |
| 2 | 进入 add，建立局部名字 a 和 b | a 是 2，b 是 3 |
| 3 | 计算 a + b | 得到 5，但外面的赋值尚未完成 |
| 4 | 执行 return 5 | 本次调用结束，add(2, 3) 的值是 5 |
| 5 | 调用位置继续赋值 | answer 现在是 5 |

`def` 出现时先定义函数，函数体要等调用才运行。形参是函数定义里的名字，实参是调用时提供的值。第二次调用会有新的一次局部执行环境。

### 精讲：print 与 return 分别通向哪里
可以把 `print` 看作显示窗口，把 `return` 看作把结果交回调用位置。函数可以一边打印、一边返回，两件事互不替代。没有执行到带值的 return 时，正常结束的函数返回 None；None 是一个值，表示这里没有提供具体结果，不是字符串 `"None"`。

先运行示例 09_02，只把函数体中的 `print(x * 2)` 改成 `return x * 2`，预测输出会从几行变为几行。外面的 `print(answer)` 保持原样，这样才能单独观察返回值的变化。

**为什么 AI 工具要 return？** 后面的程序需要拿到结果继续处理。若工具只打印“找到 3 条记录”，调用者拿到的可能是 None，不能把它当成列表遍历。调试日志可以 print；供下游使用的数据要设计明确的返回结构。

### 精讲：局部名字变化与共享对象变化
示例 09_05 中 `value = value + 10` 让局部名字 value 指向新整数，外面的 score 仍指向旧整数。示例 09_06 中 `items.append(...)` 修改双方指向的同一个列表。两者都符合“参数先绑定到传入的对象”，不需要死记“列表传引用、整数传值”这种容易误导的口诀。

默认列表陷阱的检查方法：连续调用两次，再观察第二次是否带上第一次的记录。修复时用 `items is None` 判断有没有提供列表；不要用 `if not items`，否则调用者明确传入的空列表也会被替换。这在需要修改调用者列表时会改变约定。

**闭卷小问：** 函数中有三个 return，一次调用最多执行几个？答案是一个；执行到第一个 return 后，本次调用就结束。不同输入可以走到不同的 return。
""")
    add_body(chapters, 12, """
### 精讲：路径正确，文件才会出现在你预期的位置
`Path("data/input.json")` 从当前工作目录开始寻找；当前工作目录由你怎样启动程序决定。`Path(__file__).resolve().parent` 从脚本文件的位置定位。把项目放到另一台电脑后，后者更适合寻找随项目一起复制的数据。`__file__` 用于脚本；在交互窗口或某些笔记本里不要假设它存在。

请从学习包根目录运行示例 12_06，再换一个目录用完整路径运行同一个文件，观察它打印的路径字段。该示例只解析路径，不会创建文件。真正需要写文件时，先确认目标目录；`mkdir(parents=True, exist_ok=True)` 可以创建缺失目录。

| 模式 | 目标文件不存在时 | 目标文件已存在时 | 常见用途 |
| --- | --- | --- | --- |
| r | 报 FileNotFoundError | 读取，不截断 | 读课件或已有记录 |
| w | 创建文件 | 一打开就截断原内容 | 重写完整快照 |
| a | 创建文件 | 在末尾追加 | 每行一条的日志 |

“先读再改再写完整 JSON”与“每行追加一条 JSONL”是两种不同设计。不要在 JSON 数组末尾直接追加另一个 JSON 对象；拼在一起通常不再是一个合法的 JSON 文档。JSONL 则约定一行一个 JSON 值，读取时逐行解析。本教材日志只使用一行一个对象。

### 精讲：字符串看起来像数字，不等于已经是数字
CSV 读回的 `"80"` 是字符串；先用 int 转换再计算。JSON 读回的值则取决于原 JSON 的类型：`80` 读成整数，`"80"` 仍是字符串，`null` 读成 None。成功解析文件只说明格式可以读取，不能证明字段类型和业务范围正确。

编码统一使用 UTF-8。CSV 文件使用 `newline=""` 交给 csv 模块处理换行；来自部分表格软件的 UTF-8 BOM 文件可以按明确需求用 `utf-8-sig` 读取。不要靠到处删首字符来修复表头。

**自查顺序：** 找到文件 → 确认编码 → 解析格式 → 检查字段 → 转换类型 → 执行业务。后面 JSON 会话示例先解决保存与读回；第 13 章补上输入校验。
""")
    add_body(chapters, 13, """
### 精讲：Traceback 从哪里开始读
遇到报错先保留完整输出，再读最后一行的异常类型和原因。往上找你自己代码对应的文件名、行号和那一行表达式。最靠近末尾的调用帧通常是异常出现的地方；更上面的调用帧解释程序怎样走到那里。

练习时建立一个临时文件，只写 `value = int("abc")` 并运行。你应看到 ValueError。现在把输入改成 `"12"` 再运行：异常消失，但没有 print 就不会显示 12。这说明“运行成功”和“输出符合需求”要分别检查。不要为了看到内容而把所有函数都改成 print。

| 现象 | 首先检查 | 下一步实验 |
| --- | --- | --- |
| NameError | 名字拼写、定义是否执行 | 在调用前确认名字已定义 |
| UnboundLocalError | 函数内是否给同名变量赋值后又提前读取 | 把依赖改成显式参数并 return 新值 |
| TypeError | 当前操作两边实际是什么类型 | 临时打印 type(value) |
| IndexError / KeyError | 索引、键、输入是否为空或缺字段 | 手工构造最小的空输入 |
| 输出不对但无异常 | 条件边界、更新顺序、数据约定 | 列输入 → 中间值 → 预期输出表 |

### 精讲：解析成功只是第一道检查
`json.loads` 可以读出列表、数字、字符串或字典。因此不能在解析后直接假设结果有 `result["answer"]`。结构化模型输出也需要检查：最外层类型是什么、必需字段是否存在、字段类型是否符合约定、值是否在范围内。

Python 中 bool 是 int 的子类。如果约定“次数必须是整数，不能是 True”，仅 `isinstance(value, int)` 会把 True 放进来。可以使用 `type(value) is int`，或在 isinstance 检查之外明确排除 bool。请理解约定后选择，不要机械地把所有 isinstance 改掉。

只有可恢复的错误才适合重试。格式错误可以要求重新生成；重复执行一个已经成功写入的工具可能造成重复记录。后面的离线示例只重试读取预设回复，最多三次；它不代表网络重试或有副作用工具的完整策略。

### 精讲：自检失败时怎样缩小问题
输出比较失败时，自检器会显示第一处不同的行，用引号让行首行尾空格可见。先比这一行，再检查多余的提示语和换行。函数测试失败时，Traceback 会显示 assert 对应的条件；把那组输入单独送进自己的函数，逐步打印中间值。

assert 适合本教材的开发检查。运行 Python 时若使用 `-O`，断言可能被移除；真正需要始终执行的外部输入校验，应写 if 和 raise。
""")
    add_body(chapters, 14, """
### 精讲：self 是哪一个对象
对本章普通实例方法，调用 `a.add("hello")` 时，方法中的 self 就是 a；调用 `b.add("hello")` 时，self 就是 b。self 是惯用的形参名，不是“所有实例共用的总对象”。

`self.messages = []` 放在 `__init__` 中，每新建一个实例就执行一次，创建各自的列表。如果把 `messages = []` 直接放在 class 缩进内、方法外，这个类属性通常会被尚未设置同名实例属性的实例共同访问。聊天程序中，这会造成不同会话混用记录。

检查这种错误时不要只建一个对象。建立 a、b 两个对象，只向 a 添加一条记录，然后分别检查两者长度。a 应为 1，b 应为 0。再考虑返回值：若方法直接 return 内部列表，调用者就可以从外部修改内部状态。后面的练习要求返回列表长度，使这个约定简单而明确。

第 07 章对象关系、第 09 章参数、第 14 章 self 讲的是同一个基础：名字指向对象，修改对象与重新绑定名字要分清。先在纸上画箭头，再看代码。
""")
    add_body(chapters, 16, """
### 开源项目启发：先把工具流程拆成能单独检查的部分
参考微软 AI Agents for Beginners 的工具使用章节，我们把“提出动作”和“执行动作”分别写清楚。后面的自编离线示例用 decide 选择动作，用 search_notes 执行检索。把函数分开后，可以先检查工具本身，再检查控制流程；接入真实模型时，也更容易发现问题发生在哪一层。

| 时刻 | 输入或已有状态 | 本步动作 | 可检查的结果 |
| --- | --- | --- | --- |
| 开始 | query 是“怎么理解函数？” | observation 初始化为 None | 还没有执行检索 |
| 第 1 步 | observation 为 None | decide 提出 search，执行器调用工具 | 得到正文与 note-02 来源 |
| 第 2 步 | observation 已有工具结果 | decide 提出 finish | 输出正文与来源，停止 |
| 只允许 1 步 | 第 1 步后预算用完 | 不再执行第 2 步 | 报告尚未完成，不能冒充已交付 |

参考 smolagents 的循环实现，我们保留两个独立条件：是否已经结束、是否还有执行步数。这里仅借鉴可检查的循环结构，所有代码和数据均为本教材重新编写。工具超时、网络失败、真实模型调用还没有实现，后续阶段再逐层补齐。

### 从文本到模型：提前分清四种数量
LLMs-from-scratch 的文本处理章节把文本、token ID、取样与嵌入逐步连接起来。当前阶段先练清楚数据的形状，后续再学习算法和 PyTorch。

| 名称 | 此阶段可以观察什么 | 不应混淆什么 |
| --- | --- | --- |
| 字符串长度 | len("hi AI") 为 5 | 不代表模型 token 数 |
| 空白分词数 | "hi AI".split() 得到 2 项 | 不是通用 tokenizer |
| 词表 ID | 自己给词分配整数编号 | 编号不是向量，也没有“越大越相似”的意义 |
| batch 大小 | 一次取几条样本 | 不是每条样本长度 |

本章原有的词表、填充和批次示例继续使用教学用小数据。完成后再阅读真实 tokenizer 的输出，比较同一个字符串为什么可能被分成不同数量的 token。

### 实操：把“流程跑通”与“任务做对”分别验收
为后面的检索流程写四张测试卡：已知关键词、未知关键词、零步预算、一步预算。每张卡先写你预期的 status、answer 和 steps，再运行。本章新增综合题会自动检查这些边界。

再手动试“列表和函数有什么不同？”：示例检索器只取第一个命中，不能完整回答比较题。把它记在错题本中，说明“程序按规则执行成功”与“满足用户需求”为什么不同。未来加入模型后，这种对照样例仍有用，不能只根据程序没有报错来判断回答质量。
""")
    add_body(chapters, 18, """
### AI / Agent 穿插练习后的自测
请先不运行代码，用自己的话回答，再到对应章节验证。

1. f-string 拼出一段提示词，是否已经调用了大模型？没有，只生成了 Python 字符串。
2. 对中文文本直接 split()，能否算出模型 token 数？不能。默认 split 按空白切分；具体模型使用的 tokenizer 有自己的规则。
3. 列表里的 role 字段会自动触发某种模型权限吗？不会；它在本教材里只是普通数据。实际服务如何解释字段要看它自己的接口约定。
4. 工具返回 `{"count": 3}`，与打印这段文字有何不同？返回值可供调用方继续取字段；打印本身不把这个字典作为函数结果交回。
5. 模型回复能被 json.loads 解析，是否一定能执行？不能。还要检查结构、参数和允许的工具名；不能把回复直接交给 eval 或 exec。
6. 规则检索返回了一篇文档，是否说明回答可靠？不能。还要看检索是否相关、答案是否由证据支持；本章小程序只演示流程。

### 后续学习的连接点
掌握字符串、列表和字典后，再学习 tokenizer、张量和批次；掌握函数、异常和文件后，再学习真实 API 的请求、响应、失败处理与日志；掌握类和生成器后，再阅读 Agent 框架中的状态对象与流式事件。每次只替换一层，例如先保留现有工具函数，只把固定决策函数换成真实模型接口，便于定位问题。

官方延伸资料需要联网；阅读教材和运行本轮代码不需要联网。以下是概念核对入口，不要求你现在背诵接口字段：

- [Python 官方：函数与默认参数](https://docs.python.org/3/tutorial/controlflow.html)
- [Python 官方：类与实例变量](https://docs.python.org/3/tutorial/classes.html)
- [Python 官方：JSON 编码与解码](https://docs.python.org/3/library/json.html)
- [Python 官方：错误与异常](https://docs.python.org/3/tutorial/errors.html)
- [OpenAI 官方：工具调用流程](https://developers.openai.com/api/docs/guides/function-calling)

本教材的工具调用字典是为教学自定义的简化格式，不能直接当作任何厂商的 API 请求格式使用。
""")
    add_body(chapters, 18, """
### 高星 GitHub 项目：v1.1 的参考记录
星数只反映关注量，不能代替对代码、解释和前置知识的检查。v1.1 制作时先读取项目原始内容与许可证，再选择适合第一阶段的部分。以下星数是 2026-10-20 查询 GitHub API 的快照，后续会变化。

| 项目与星数快照 | 参考范围 | 本教材中的具体落点 |
| --- | --- | --- |
| [Python-100-Days](https://github.com/jackfrued/Python-100-Days) · 187,325 | 基础语法到应用练习的课程组织 | 保留先语法、再场景、再独立作答的顺序；增加逐步分析和边界输入 |
| [AI Agents for Beginners](https://github.com/microsoft/ai-agents-for-beginners) · 77,523 | 工具、参数、执行结果和状态之间的关系 | 第 09 / 13 / 16 章：工具返回字典、数据校验、决策与执行分开 |
| [LLMs-from-scratch](https://github.com/rasbt/LLMs-from-scratch) · 106,931 | 第 2 章的文本数据与取样衔接 | 第 03 / 15 / 16 章：字符、词、token、流片段和批次之间的区别 |
| [smolagents](https://github.com/huggingface/smolagents) · 29,947 | Agent 运行循环的停止条件 | 第 06 / 16 章：完成状态、步数上限、未完成时的明确返回 |

v1.1 采用概念与教学组织参考，示例、题目、数据和解析重新编写，未搬入这些项目的框架源码、书籍或图片。Python-100-Days 在该次检查中未发现仓库级许可证，因此仅参考公开目录结构并链接原作；微软项目为 MIT，smolagents 为 Apache-2.0；LLMs-from-scratch 的 LICENSE.txt 含书籍和相关图片的排除条款，不能笼统当作所有材料都可复制。

学习包中的 `开源参考与改编说明.md` 记录作者、精确提交版本、对应文件及许可证链接，方便将来逐项核对。阅读原项目需要联网；运行当前教材不依赖它们。
""")
    add_ai_examples(chapters)


def add_ai_examples(chapters):
    """内容只用所属章节已介绍的语法；后续章节再逐步增加校验。"""
    example(chapters[3], "AI / Agent：用字符串组织提示词", '''
    topic = "  Python 列表  "
    level = "零基础"
    clean_topic = topic.strip()
    prompt = f"请面向{level}读者解释：{clean_topic}。"
    print(prompt)
    print(f"主题字符数：{len(clean_topic)}")
    ''', '''
    请面向零基础读者解释：Python 列表。
    主题字符数：9
    ''', "输入是带首尾空格的 topic。strip 返回去掉首尾空白的新字符串，原 topic 不会被自动修改；赋值后 clean_topic 是 'Python 列表'。f-string 把两个变量的值插入文字，print 才显示结果。len 在这里数 Python 字符串的 Unicode 码位，空格也算一个；它不是模型 token 数。本例只生成提示词，没有模型回复。",
    "先把 topic 改成只有三个空格，预测清理后的字符数。再把模板改成要求输出一个例子，观察引号内文字与变量名各在哪里。")
    exercise(chapters[3], "AI / Agent：整理检索问题", "迁移",
    '给定 question = "  What is Python?  "，先去掉首尾空白，再变成小写，保存为 cleaned。输出 cleaned，下一行输出它的字符数。只练字符串处理，不做真实搜索。',
    '先写 cleaned = question.strip().lower()。方法从左到右执行；len 统计的是清理后字符串。',
    '''
    question = "  What is Python?  "
    cleaned = question.strip().lower()
    print(cleaned)
    print(len(cleaned))
    ''', '''
    what is python?
    15
    ''', "原始文字 → strip 去边缘空白 → lower 统一英文大小写 → len 计数。中间的两个空格和问号都保留。常见错误是对原 question 求长度，或忘了接住方法返回的新字符串。边界试验：空字符串清理后仍为空，长度为 0；中文不因为 lower 而变成英文。")

    example(chapters[4], "AI / Agent：按明确规则选择处理路径", '''
    request = " 请解释列表 "
    cleaned = request.strip()
    if cleaned == "":
        route = "请先输入问题"
    elif "计算" in cleaned:
        route = "交给计算工具"
    else:
        route = "进入文字讲解"
    print(route)
    ''', '进入文字讲解',
    "先清理 request，再从上到下尝试条件。当前内容非空且不含“计算”，所以进入 else。这叫规则路由：由你写的条件决定走哪条路径，不包含模型理解。后面的章节会把这些文字路径换成函数调用。包含“不要计算”的句子也会命中关键词，说明关键词判断有明确局限。",
    "依次替换 request 为三个空格、“请计算 2 + 3”、“不要计算，只解释”。记录实际路线，再写一句话说明这种规则为什么不能代表理解了用户意图。")
    exercise(chapters[4], "AI / Agent：输出长度约定", "迁移",
    '给定 reply = "  hello  "、limit = 5。清理首尾空白后：空内容输出 empty；字符数超过 limit 输出 too_long；否则输出 ok。条件按此顺序组织。',
    "长度恰好等于 5 应通过，比较符号应是 >。先判断空内容，可以把两种错误明确区分。",
    '''
    reply = "  hello  "
    limit = 5
    cleaned = reply.strip()
    if cleaned == "":
        print("empty")
    elif len(cleaned) > limit:
        print("too_long")
    else:
        print("ok")
    ''', "ok", "清理后 hello 长度为 5，没有超过上限，因此输出 ok。请分别用空白、四字符、五字符、六字符测试。这是我们自己制定的字符长度规则，不是实际模型的上下文长度限制；模型上下文一般需要按对应 tokenizer 的 token 计算。")

    example(chapters[6], "AI / Agent：最多执行三轮的任务循环", '''
    step = 0
    max_steps = 3
    finished = False
    while step < max_steps:
        step += 1
        print(f"第 {step} 轮")
        if step == 2:
            finished = True
            break
    print(f"已完成：{finished}")
    print(f"实际轮数：{step}")
    ''', '''
    第 1 轮
    第 2 轮
    已完成：True
    实际轮数：2
    ''', "step 从 0 开始，每轮先加 1；第 1 轮未完成，重新判断 while；第 2 轮把 finished 改为 True 后 break，跳到循环后。max_steps 限制最多启动几轮；finished 单独记录是否完成。运行了两轮和任务完成是两个不同事实。本例用 step == 2 模拟完成条件，真实 Agent 需要根据执行结果判断。",
    "把完成条件改成 step == 5，max_steps 保持 3。应执行三轮且 finished 为 False。再把 max_steps 改成 0，说明为什么循环体一次也不执行。")
    exercise(chapters[6], "AI / Agent：完成前先扣减工作量", "迁移",
    "给定 remaining = 5、steps = 0。每轮处理一项，remaining 减 1，steps 加 1；只要有剩余且 steps 小于 3 就继续。最后分别输出 steps、remaining。不要写无限循环。",
    "while 条件同时检查 remaining > 0 和 steps < 3。两个计数器都在循环体中更新。",
    '''
    remaining = 5
    steps = 0
    while remaining > 0 and steps < 3:
        remaining -= 1
        steps += 1
    print(steps)
    print(remaining)
    ''', '''
    3
    2
    ''', "执行前为 (steps, remaining) = (0, 5)，三轮后依次为 (1, 4)、(2, 3)、(3, 2)。下一次条件检查因 steps < 3 为 False 停止。没有完成的两项仍保留，不能把达到轮数上限写成“任务完成”。改 remaining 为 0 和 1，分别应得到 0/0 与 1/0。")

    example(chapters[8], "AI / Agent：列表保存顺序，字典保存消息字段", '''
    messages = [
        {"role": "user", "content": "什么是列表？"},
        {"role": "assistant", "content": "列表保存有顺序的元素。"},
    ]
    messages.append({"role": "user", "content": "给我一个例子。"})
    for message in messages:
        print(f"{message['role']}: {message['content']}")
    print(len(messages))
    ''', '''
    user: 什么是列表？
    assistant: 列表保存有顺序的元素。
    user: 给我一个例子。
    3
    ''', "messages 外层列表保存时间顺序；每个内层字典保存一条消息。messages[0] 取得第一条字典，再用 ['content'] 取得正文；for 每次让 message 指向一条字典。这里 role 只是我们约定的字段，assistant 文字是预先写好的，没有模型参与。真实服务的消息格式和角色语义要查对应接口。",
    "只输出 role 为 user 的消息，再统计用户消息的条数。不要删除遍历中的元素；先用 if 选择要处理的记录。")
    exercise(chapters[8], "AI / Agent：统计用户消息", "迁移",
    'messages 为 [{"role": "user", "content": "hi"}, {"role": "assistant", "content": "hello"}, {"role": "user", "content": "bye"}]。只输出用户消息正文，并在最后输出用户消息数。所有记录都保证有这两个键。',
    "count 从 0 开始；只有 role 等于 user 时才打印正文并加 1。",
    '''
    messages = [
        {"role": "user", "content": "hi"},
        {"role": "assistant", "content": "hello"},
        {"role": "user", "content": "bye"},
    ]
    count = 0
    for message in messages:
        if message["role"] == "user":
            print(message["content"])
            count += 1
    print(count)
    ''', '''
    hi
    bye
    2
    ''', "先取 role 决定是否进入分支，再取 content。count 不应在分支外增加，否则会把 assistant 也算进去。空列表没有任何正文输出，最后应输出 0；将所有 role 改为 assistant 也应得到 0。字段缺失的处理留到第 13 章，不能把本题的输入保证推广到任何外部数据。")

    example(chapters[9], "AI / Agent：工具函数把结果交回调用者", '''
    def count_words(text):
        words = text.split()
        return {"count": len(words), "empty": len(words) == 0}

    result = count_words("  learn Python   today ")
    print(result["count"])
    print(result["empty"])
    print(count_words("")["count"])
    ''', '''
    3
    False
    0
    ''', "输入字符串进入 text；split 得到三个按空白分开的词；函数构造字典并 return；外层 result 接收字典后取字段。函数体不打印，所以可以重复用于统计、测试或保存文件。它要求 text 是字符串；第 13 章再学习怎样验证来自外部的数据。按空白分词只适合此处演示，既不是通用中文分词器，也不是模型 tokenizer。",
    "把 return 改成 print 字典，再运行，观察 result 的值为什么变成 None。修复后传入纯空白字符串，预测 count 和 empty。")
    exercise(chapters[9], "AI / Agent：先约定工具的输入和返回结构", "场景",
    '实现 summarize_text(text)，输入保证是字符串。先 strip；返回字典，字段 chars 为清理后的长度、preview 为前 4 个字符、empty 表示是否为空。函数不能打印。用 "  Python  " 调用，依次打印三个字段。',
    '先保存 cleaned，再构造一个字典 return。切片 [:4] 遇到不足 4 个字符时不会越界报错。',
    '''
    def summarize_text(text):
        cleaned = text.strip()
        return {
            "chars": len(cleaned),
            "preview": cleaned[:4],
            "empty": cleaned == "",
        }

    result = summarize_text("  Python  ")
    print(result["chars"])
    print(result["preview"])
    print(result["empty"])
    ''', '''
    6
    Pyth
    False
    ''', "清理后的 Python 长度为 6，前四字符是 Pyth。把计算与输出分开后，调用者可以只显示 preview，或把整个结果写成 JSON。边界：空白返回 chars=0、preview=''、empty=True；短字符串原样作为预览。本题额外检查空白、短字符串和函数没有打印的约定。",
    tests='''
    f = summarize_text
    assert f("   ") == {"chars": 0, "preview": "", "empty": True}
    assert f("AI") == {"chars": 2, "preview": "AI", "empty": False}
    import contextlib, io
    captured = io.StringIO()
    with contextlib.redirect_stdout(captured):
        f("test")
    assert captured.getvalue() == "", "函数应返回结果，不应打印"
    ''')

    example(chapters[12], "AI / Agent：把会话快照写入 JSON 再读回", '''
    import json
    from pathlib import Path

    messages = [{"role": "user", "content": "学习函数"}]
    path = Path("outputs/ai_chat_demo.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(messages, ensure_ascii=False, indent=2)
    path.write_text(text, encoding="utf-8")
    restored = json.loads(path.read_text(encoding="utf-8"))
    print(type(restored).__name__)
    print(restored[0]["content"])
    print(restored == messages)
    ''', '''
    list
    学习函数
    True
    ''', "messages 是内存列表；dumps 把它变成 JSON 字符串；write_text 把字符串写到当前工作目录下的 outputs/ai_chat_demo.json；read_text 读回字符串；loads 再得到列表。两次转换方向相反，值相等不代表还是同一个内存对象。重复运行会重写这个演示文件；在学习包根目录运行时，可到 outputs 查看内容。这里叫持久化，因为文件在程序退出后仍在；不是训练模型或修改模型权重。",
    "给列表追加一条 assistant 消息再运行，确认文件里出现两条。随后只修改内存列表而不写文件，再读文件，说明为什么文件不会自动跟着改变。")
    exercise(chapters[12], "AI / Agent：读回合法的 JSONL 消息", "场景",
    '实现 parse_messages(text)：输入为多行文本，每个非空行保证是含 role、content 的合法 JSON 对象；跳过空行，返回解析后的字典列表。调用文本为两行 {"role":"user","content":"hi"} 与 {"role":"assistant","content":"hello"}，中间有一空行。输出列表长度和第二条正文。',
    "用 splitlines 遍历行，strip 后为空就 continue；否则 json.loads 后 append。此题只处理合法记录，坏 JSON 留到下一章。",
    '''
    import json

    def parse_messages(text):
        messages = []
        for line in text.splitlines():
            if not line.strip():
                continue
            messages.append(json.loads(line))
        return messages

    text = '{"role":"user","content":"hi"}\\n\\n{"role":"assistant","content":"hello"}'
    messages = parse_messages(text)
    print(len(messages))
    print(messages[1]["content"])
    ''', '''
    2
    hello
    ''', "splitlines 把文本拆成行；空行被跳过；每个非空行独立 loads，而不是把整段 JSONL 当一个 JSON 文档。最后返回列表供调用者使用。尝试末尾换行、Windows 的 CRLF 换行和全空输入；这些都不应多产生一条消息。下一章再区分格式错误和字段错误。",
    tests='''
    f = parse_messages
    assert f("") == []
    assert f(" \\n\\r\\n") == []
    assert f('{"role":"user","content":"a"}\\r\\n') == [{"role":"user","content":"a"}]
    ''')

    example(chapters[13], "AI / Agent：解析、校验、有限次重试", '''
    import json

    def read_answer(text):
        data = json.loads(text)
        if not isinstance(data, dict):
            raise ValueError("最外层必须是对象")
        answer = data.get("answer")
        if not isinstance(answer, str) or not answer.strip():
            raise ValueError("answer 必须是非空字符串")
        return answer.strip()

    replies = ["not-json", '{"answer": 12}', '{"answer": "先学函数"}']
    for attempt, reply in enumerate(replies, start=1):
        try:
            answer = read_answer(reply)
        except ValueError:
            print(f"第 {attempt} 次：格式或内容不合格")
            continue
        print(f"第 {attempt} 次：{answer}")
        break
    else:
        print("已用完预设回复，停止")
    ''', '''
    第 1 次：格式或内容不合格
    第 2 次：格式或内容不合格
    第 3 次：先学函数
    ''', "第 1 条连 JSON 语法都不满足；第 2 条能解析，但 answer 是整数；第 3 条才满足本题结构约定。json.JSONDecodeError 属于 ValueError，因此此处一起捕获；正式调试时可以分别记录原因。try 只包住解析函数，成功后打印并 break。for 的 else 仅在没有 break、正常遍历结束时执行。本例读取三条预设字符串，不会请求模型重试；通过校验也只说明结构合格，不保证答案事实正确。",
    "把第三条改成空字符串字段，确认出现“停止”。再把第二条改为合法答案，确认第三条不会读取。")
    exercise(chapters[13], "AI / Agent：验证工具调用数据", "场景",
    '实现 read_call(text)：解析 JSON，要求最外层为字典、name 恰好为 "char_count"、arguments 为字典且其中 text 为字符串。成功时返回 arguments["text"]；不满足任一条件时 raise ValueError。空字符串允许。调用 {"name":"char_count","arguments":{"text":"Python"}} 并打印返回文本。',
    "分层检查，不要连写 data['arguments']['text'] 后才判断。get 取不到键会得到 None，正好可以进入错误分支。JSON 语法错误本身也是 ValueError 的一种。",
    '''
    import json

    def read_call(text):
        data = json.loads(text)
        if not isinstance(data, dict):
            raise ValueError("调用必须是对象")
        if data.get("name") != "char_count":
            raise ValueError("不支持的工具名")
        arguments = data.get("arguments")
        if not isinstance(arguments, dict):
            raise ValueError("arguments 必须是对象")
        content = arguments.get("text")
        if not isinstance(content, str):
            raise ValueError("text 必须是字符串")
        return content

    request = '{"name":"char_count","arguments":{"text":"Python"}}'
    print(read_call(request))
    ''', "Python",
    "先解析，再按层检查类型和字段，最后才返回允许的数据。本题只负责验证，不执行任何工具。name 的允许值只有 char_count；其他名字应明确拒绝，不能 eval 数据中的文本。空文本是字符串，符合本题约定；数字、null 和缺失字段不符合。额外测试会检查这些分支，并要求错误类型为 ValueError。",
    tests='''
    assert read_call('{"name":"char_count","arguments":{"text":""}}') == ""
    for invalid in [
        "bad-json", "[]", "null",
        '{"name":"unknown","arguments":{"text":"a"}}',
        '{"name":"char_count"}',
        '{"name":"char_count","arguments":[]}',
        '{"name":"char_count","arguments":{"text":12}}',
        '{"name":"char_count","arguments":{}}',
    ]:
        try:
            read_call(invalid)
        except ValueError:
            pass
        else:
            raise AssertionError(f"应拒绝：{invalid}")
    ''')

    example(chapters[14], "AI / Agent：两个会话不能共用消息列表", '''
    class ChatSession:
        def __init__(self, name):
            self.name = name
            self.messages = []

        def add(self, text):
            self.messages.append(text)
            return len(self.messages)

    alice = ChatSession("Alice")
    bob = ChatSession("Bob")
    count = alice.add("我在学习 Python")
    print(alice.name, count)
    print(bob.name, len(bob.messages))
    print(alice.messages is bob.messages)
    ''', '''
    Alice 1
    Bob 0
    False
    ''', "每次 ChatSession(...) 都调用 __init__，其中 [] 各创建一次。alice.add 调用时 self 是 alice，只修改她的 messages；方法把新长度 return 给 count。最后的 is 比较是否为同一对象，不是比较内容是否相等。两个会话当前只在内存保存消息；关闭程序后要靠第 12 章的文件操作恢复。",
    "在临时副本里把 messages = [] 移到类的顶层并删除 self.messages 初始化，重新运行并解释结果变化。随后恢复实例属性写法。")
    exercise(chapters[14], "AI / Agent：有条数上限的会话记忆", "场景",
    '实现 RecentMessages(limit)。limit 必须为大于 0 的 int，bool 不接受，否则 raise ValueError。每个实例有自己的 messages 列表；add(text) 只接受字符串，添加后保留最后 limit 条，返回当前条数。用 limit=2 依次添加 "a"、"b"、"c"，打印 messages。',
    "先完成参数验证，再初始化实例列表。超过上限时可以用切片 self.messages[-self.limit:]。验证应在修改状态之前。",
    '''
    class RecentMessages:
        def __init__(self, limit):
            if type(limit) is not int or limit <= 0:
                raise ValueError("limit 必须为正整数")
            self.limit = limit
            self.messages = []

        def add(self, text):
            if not isinstance(text, str):
                raise ValueError("text 必须为字符串")
            self.messages.append(text)
            self.messages = self.messages[-self.limit:]
            return len(self.messages)

    session = RecentMessages(2)
    session.add("a")
    session.add("b")
    session.add("c")
    print(session.messages)
    ''', "['b', 'c']",
    "前三次添加后的列表依次为 ['a']、['a','b']、['b','c']。切片创建新列表，再绑定给这个实例的属性。两个实例必须分别初始化；非法添加不能先污染已有记录再报错。这里只按消息条数截取，不按 token 总量，也没有保证对话语义完整；真实上下文管理需要另外设计。",
    tests='''
    a, b = RecentMessages(2), RecentMessages(2)
    assert a.add("x") == 1
    assert b.messages == []
    a.add("y")
    assert a.add("z") == 2
    assert a.messages == ["y", "z"]
    for bad in [0, -1, True, 1.5]:
        try:
            RecentMessages(bad)
        except ValueError:
            pass
        else:
            raise AssertionError(f"应拒绝 limit={bad!r}")
    try:
        a.add(None)
    except ValueError:
        pass
    else:
        raise AssertionError("应拒绝非字符串")
    assert a.messages == ["y", "z"], "非法输入不能改坏已有状态"
    ''')

    example(chapters[15], "AI / Agent：用生成器模拟逐段到达的文字", '''
    def simulated_stream():
        yield "先学"
        yield " Python"
        yield "，再做项目。"

    pieces = []
    stream = simulated_stream()
    for piece in stream:
        pieces.append(piece)
        print(f"收到：{piece}")
    print("完整：" + "".join(pieces))
    print(list(stream))
    ''', '''
    收到：先学
    收到： Python
    收到：，再做项目。
    完整：先学 Python，再做项目。
    []
    ''', "调用 simulated_stream 得到生成器，此时还未产出任何片段。for 每次索取下一个值，函数执行到 yield 暂停；下一轮从暂停处继续。遍历结束后，这个 stream 已耗尽，再转成列表是 []；重新调用函数才能得到新的生成器。片段是预设字符串，不是实际模型 token，也没有真实网络延迟。join 用空字符串连接，保留片段自身的空格。",
    "把 join 的分隔符改成一个空格，观察为何会多出空格。再创建一个新的 stream，验证它能重新输出全部片段。")
    exercise(chapters[15], "AI / Agent：从事件流中提取文字片段", "迁移",
    '实现 text_pieces(events) 生成器。events 中每项保证是字典；只 yield kind 为 "text" 且 content 为非空字符串的内容，跳过其他项。用 [{"kind":"start"}, {"kind":"text","content":"Py"}, {"kind":"usage","content":3}, {"kind":"text","content":"thon"}] 生成片段并拼接打印。',
    "先判 kind，再取 content 并检查类型与是否等于空字符串。不要 strip 后再输出，文本片段的空格可能是正文的一部分。",
    '''
    def text_pieces(events):
        for event in events:
            if event.get("kind") != "text":
                continue
            content = event.get("content")
            if isinstance(content, str) and content != "":
                yield content

    events = [
        {"kind": "start"},
        {"kind": "text", "content": "Py"},
        {"kind": "usage", "content": 3},
        {"kind": "text", "content": "thon"},
    ]
    print("".join(text_pieces(events)))
    ''', "Python",
    "start 和 usage 是非文本事件，不能把整个事件字典都拼进答案。生成器只产出 Py 和 thon，join 后得到 Python。额外测试保留单个空格片段、跳过空串和非字符串内容。本题使用自定义事件格式；实际 SDK 的事件名称与字段可能不同。",
    tests='''
    assert list(text_pieces([])) == []
    events = [
        {"kind":"text","content":""},
        {"kind":"text","content":" "},
        {"kind":"text","content":None},
        {"kind":"text"},
        {"kind":"text","content":"A"},
    ]
    assert list(text_pieces(events)) == [" ", "A"]
    stream = text_pieces([{"kind":"text","content":"x"}])
    assert iter(stream) is stream, "请使用生成器而非提前返回列表"
    assert next(stream) == "x"
    assert list(stream) == []
    ''')

    example(chapters[16], "AI / Agent：串起决策、工具、观察和结束", '''
    def search_notes(query):
        notes = [
            {"keyword": "列表", "text": "列表保存有顺序的元素。", "source": "note-01"},
            {"keyword": "函数", "text": "return 把结果交回调用位置。", "source": "note-02"},
        ]
        for note in notes:
            if note["keyword"] in query:
                return {"text": note["text"], "source": note["source"]}
        return {"text": "没有找到相关笔记。", "source": None}

    def decide(state):
        if state["observation"] is None:
            return {"action": "search", "query": state["query"]}
        return {"action": "finish"}

    state = {"query": "怎么理解函数？", "observation": None}
    finished = False
    for step in range(1, 4):
        decision = decide(state)
        print(f"第 {step} 步：{decision['action']}")
        if decision["action"] == "search":
            state["observation"] = search_notes(decision["query"])
        elif decision["action"] == "finish":
            print(state["observation"]["text"])
            print(f"来源：{state['observation']['source']}")
            finished = True
            break
        else:
            raise ValueError("未知动作")
    if not finished:
        print("达到步数上限，尚未完成")
    ''', '''
    第 1 步：search
    第 2 步：finish
    return 把结果交回调用位置。
    来源：note-02
    ''', "输入 query 进入 state；第一次 decide 看见 observation 为 None，提出 search 动作；执行器调用工具 search_notes，把结果写回 observation；第二次 decide 因已有结果而选择 finish；执行器输出结果和来源后结束。决策函数在这里完全由规则实现；没有模型推理、向量检索或生成式回答。检索只返回第一个命中的关键词笔记，能追踪来源不等于覆盖所有问题。固定上限可以限制此循环执行次数，但不能中断某一次已经卡住的工具函数。",
    "把问题改成“什么是张量？”，观察无命中时的结果。把 range(1, 4) 改为 range(1, 2)，确认工具虽执行了但流程还未 finish。最后解释：为什么只把一个函数命名为 agent 并不自动获得规划能力？")
    exercise(chapters[16], "AI / Agent：实现可测试的两步工具流程", "综合",
    '实现 lookup_agent(query, max_steps=2)。query 必须是字符串；max_steps 必须是非负 int（不接受 bool），否则 raise ValueError。固定笔记字典为 {"列表":"有序容器", "函数":"可复用的处理步骤"}，按 query 完全匹配查找。第 1 步保存查找结果；第 2 步返回 {"status":"done", "answer":结果或"未找到", "steps":2}。若步数不够，返回 {"status":"limit", "answer":None, "steps":已执行步数}。只需这两种动作，最多执行两步。调用 "函数" 并依次输出 status、answer、steps。',
    "先验证输入，再用 for 从 1 到 max_steps 迭代。第 1 步查询，第 2 步立即 return。循环正常结束则说明还没完成。max_steps=0 时应执行零步。",
    '''
    def lookup_agent(query, max_steps=2):
        if not isinstance(query, str):
            raise ValueError("query 必须是字符串")
        if type(max_steps) is not int or max_steps < 0:
            raise ValueError("max_steps 必须为非负整数")
        notes = {"列表": "有序容器", "函数": "可复用的处理步骤"}
        observation = None
        steps = 0
        for step in range(1, max_steps + 1):
            steps = step
            if step == 1:
                observation = notes.get(query, "未找到")
            else:
                return {"status": "done", "answer": observation, "steps": steps}
        return {"status": "limit", "answer": None, "steps": steps}

    result = lookup_agent("函数")
    print(result["status"])
    print(result["answer"])
    print(result["steps"])
    ''', '''
    done
    可复用的处理步骤
    2
    ''', "第 1 步只查找，第 2 步才交付结果，因此 max_steps=1 必须报告 limit。max_steps 很大时也在第 2 步提前返回，不能为了用完预算继续循环。未知问题得到 done/未找到，表示流程已结束但没有证据；不能伪造知识补空缺。先画出 max_steps=0、1、2、5 四条执行轨迹，再运行额外测试。本题是离线规则流程，完成它意味着理解了 Python 控制流与状态传递。",
    tests='''
    assert lookup_agent("列表") == {"status":"done","answer":"有序容器","steps":2}
    assert lookup_agent("张量") == {"status":"done","answer":"未找到","steps":2}
    assert lookup_agent("函数", 0) == {"status":"limit","answer":None,"steps":0}
    assert lookup_agent("函数", 1) == {"status":"limit","answer":None,"steps":1}
    assert lookup_agent("函数", 5)["steps"] == 2
    for bad in [-1, True, 1.2]:
        try:
            lookup_agent("函数", bad)
        except ValueError:
            pass
        else:
            raise AssertionError(f"应拒绝 max_steps={bad!r}")
    try:
        lookup_agent(None)
    except ValueError:
        pass
    else:
        raise AssertionError("应拒绝非字符串 query")
    ''')
