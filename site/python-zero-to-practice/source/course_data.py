from textwrap import dedent

CHAPTERS = []

def chapter(number, title, subtitle, goals, body, recall, checkpoint):
    c = dict(number=number, title=title, subtitle=subtitle, goals=goals,
             body=dedent(body).strip(), recall=recall, checkpoint=checkpoint,
             examples=[], exercises=[])
    CHAPTERS.append(c)
    return c

def example(c, title, code, output, explain, challenge='', stdin=''):
    eid = f"{c['number']:02d}_{len(c['examples'])+1:02d}"
    c['examples'].append(dict(id=eid,title=title,code=dedent(code).strip()+'\n',
        output=dedent(output).strip()+'\n',explain=explain,challenge=challenge,stdin=stdin))

def exercise(c, title, level, task, hint, code, output, explain, stdin='', tests=''):
    eid = f"{c['number']:02d}_{len(c['exercises'])+1:02d}"
    c['exercises'].append(dict(id=eid,title=title,level=level,task=task,hint=hint,
        code=dedent(code).strip()+'\n',output=dedent(output).strip()+'\n',
        explain=explain,stdin=stdin,tests=dedent(tests).strip()))

c = chapter(0, '从这里开始', '先把第一段程序运行起来，再逐步理解它。',
['区分浏览器、编辑器、终端和 Python 解释器', '在 Windows 与 Mac 上运行同一个文件', '掌握教材、练习、答案和进度的使用方法'], r'''
### 这份教材怎样帮你学会实操
这是给没有编程经验的学习者准备的第一阶段教材。你无需懂数学公式、命令行或英文术语。目标是让你独立完成“接收数据 → 判断与处理 → 保存结果”的小程序，并看懂后续机器学习代码中的常见 Python 写法。它不承诺学完即可训练大模型；模型原理、线性代数、NumPy、PyTorch 是后续阶段。

**先下载并完整解压学习包，再双击 index.html。** 不要在压缩包的预览窗口里运行脚本。网页、代码和示例数据均可离线使用；第一次安装 Python 需要联网，或提前从官方网站准备适合目标电脑的安装文件。网页本身不需要安装任何程序，也不依赖在线字体、CDN 或账号。运行 Python 代码则需要该电脑已安装 Python。

正文中的代码都是 Python；标注为“终端命令”的内容则写在终端里。网页的“复制”只复制代码，不会自动执行。为保证完整离线、避免额外大型运行环境，本教材**不在网页中执行任意 Python**。三个演示器只展示预设语义轨迹，真实练习请在自己的解释器里运行。

### 文件夹地图
- `index.html`：教材入口，双击打开。
- `examples/ch02/ex02_01.py`：第 02 章第 1 个示例，可以直接运行。
- `practice/ch02/ex02_01.py`：第 02 章第 1 道习题，留给你编写代码。
- `solutions/ch02/ex02_01.py`：该题参考答案；先尝试，再查看。
- `projects/`：四个综合项目，每个有分步任务、示例数据和完整实现。
- `tools/check_practice.py`：练习自检器；`tools/verify_examples.py`：全部示例核对器。
- `notes/`：错题本和复习记录模板；`textbook.md`：纯文字备份。

**练习请编辑解压包原位置的 practice 文件。** 网页文件链接会下载副本；若你修改的是“下载”目录中的副本，自检器仍会读取学习包里的原文件。最稳妥的方法是在编辑器里用 File → Open 打开题目注明的 practice 路径，修改并保存。

示例和习题分别编号，所以同一个 `02_01` 在 examples 和 practice 中不是同一段程序。编号的前两位是章节号，后两位是本章顺序。

### 四个工具分别做什么
**编辑器**负责修改文本，例如 Python 自带的 IDLE；**解释器**负责执行 Python 代码；**终端**负责接收启动程序的命令；**浏览器**负责显示教材。可以把编辑器想成写菜谱的纸，解释器想成按菜谱做菜的人，终端想成发出“开始做菜”的入口。类比只帮助入门；代码的准确含义以解释器规则为准。

`hello.py` 是文本文件，`.py` 告诉你这是 Python 源代码。`print("你好")` 的括号是调用，双引号包住字符串，`print` 把内容显示到输出区域。注意使用英文半角括号和引号，不能用中文的 `（ ） “ ”` 替换。

### Windows 安装与首次运行
1. 打开 [Python 官方下载页](https://www.python.org/downloads/)，按照 [Windows 官方安装说明](https://docs.python.org/3/using/windows.html) 安装 Python。官方目前提供 Python install manager；已有正常工作的 Python 3 不必为了本教材重装。安装流程随版本变化，以官方页面为准。
2. 安装完成后，关闭旧终端，再从开始菜单打开 PowerShell 或 Windows Terminal，输入 `py --version`。若 `py` 不可用但 `python --version` 成功，后续把 `py` 换成 `python`。
3. 确认输出是 Python 3.10 或更高。本教材使用的语法按 Python 3.10+ 编写，交付前在 3.12 环境实际验证；不是对所有操作系统组合都做过现场测试。
4. 将整个文件夹放在一个容易找到的位置，例如桌面。打开该文件夹，在文件资源管理器地址栏输入 `powershell` 并回车，通常即可在此目录启动 PowerShell。也可以手动输入 `cd "完整文件夹路径"`。
5. 输入下面的命令，看到文字即成功。命令前面没有要你复制的 `$` 或 `>>>`。

```terminal
py examples/ch01/ex01_01.py
```

### Mac 安装与首次运行
1. 从 [Python 官方下载页](https://www.python.org/downloads/) 获取 macOS 安装包，参考 [macOS 官方说明](https://docs.python.org/3/using/mac.html) 安装。学习用解释器不要依赖系统工具内部使用的 Python。
2. 用 Spotlight 搜索并打开“终端”，输入 `python3 --version`，确认 Python 3.10+。
3. 在终端输入 `cd `（注意末尾有空格），把解压后的学习包文件夹拖入终端，再按回车。拖入操作会帮助你填好带空格的路径。
4. 输入下面的命令：

```terminal
python3 examples/ch01/ex01_01.py
```

之后所有标为 `python ...` 的通用命令，在尚未使用虚拟环境时，Windows 可改成 `py ...`，Mac 可改成 `python3 ...`。第 11 章使用虚拟环境时会给出精确路径。

### 完全不会编辑文件时怎么做
如果安装中包含 IDLE，在开始菜单或应用程序中打开它。选择 File → Open，打开任意 `.py` 文件；修改后按 Ctrl+S（Mac 用 Command+S）保存，再选择 Run → Run Module（常见快捷键 F5）。结果会出现在 IDLE Shell 中。练习也可以用任意纯文本代码编辑器完成。

不要用 Word 编辑 `.py`，也不要保存成 `hello.py.txt`。Windows 可以在文件资源管理器中开启“显示文件扩展名”；Mac 文本编辑器需要先转换为纯文本。使用 IDLE 通常更省事。

遇到 `>>>` 说明进入了 Python 交互模式，可以输入 Python 表达式。此时不能直接输入 `py hello.py`。输入 `exit()` 回到系统终端，再运行终端命令。`...` 是交互模式的续行提示，不是要写进程序里的字符。

### 一次学习的具体流程
每次安排 45—75 分钟，可按自己的时间拆开：5 分钟默写上一节；15 分钟读新知识；20 分钟手敲并改动示例；15 分钟独立做题；5 分钟记录错误。**看懂答案不等于能够独立写出。** 每个例子先写下预计输出，再运行，然后至少改两个输入。

卡住时按顺序做：复述题目 → 写出输入与输出 → 手算一个小例子 → 用中文列步骤 → 把步骤翻译成代码 → 用 print 看中间值。独立尝试 10—15 分钟后可以展开提示；再卡住才看解析。看过答案的题，第二天关掉答案重写。

### 换电脑继续学习
复制整个解压后的文件夹，或者复制压缩包后重新解压。已写好的 practice、projects 和 notes 也要一起带走。网页进度保存在当前浏览器本地，它不会自动同步，也可能因移动文件或浏览器清理而丢失：离开前点击“导出进度”，在另一台电脑点击“导入进度”。导出的 JSON 包含章节勾选和笔记，不包含你的 `.py` 源代码。浏览器禁止本地存储时仍可阅读，应手动导出进度。

### 第一周不要做的额外工作
不需要显卡，不需要注册模型 API，不需要安装 PyTorch，也不需要一次配置多个编辑器。第 00—16 章和四个项目只使用标准库。先把这条最短路径走通：保存一个文件 → 运行 → 修改 → 再运行。
''',
['终端运行命令，解释器运行 Python。', '保存文件后再运行；先预测，再验证。', '跨电脑要带上源码；网页进度单独导出。'],
['我能找到学习包的位置，并从终端进入该目录。','我能运行第 01 章示例，并把输出改成自己的名字。','我知道报错时先读最后一行，而不是马上重装。'])

c = chapter(1, '程序与基本语法', '把想做的事情拆成计算机能执行的小步骤。',
['理解执行顺序、表达式和语句', '会用 print、注释和缩进', '能识别最常见的输入错误'], r'''
### 程序就是一系列明确指令
“帮我统计分数”对人足够，对计算机不够。你要写清楚：分数有哪些、怎样相加、人数怎么算、最后显示什么。通常先确定**输入、处理、输出**。比如输入两科成绩 80 和 90，处理是相加后除以 2，输出是 85.0。

Python 普通脚本从上到下执行；遇到函数定义会先记住函数，遇到调用才执行函数体（第 09 章）；遇到条件和循环会改变执行路径。先把现在的例子当作一行接一行执行。

### 表达式、语句和函数调用
`2 + 3` 是能得到一个值的表达式。在文件里单独写 `2 + 3` 会计算，但通常不会显示结果。`print(2 + 3)` 才会显示。`print` 是函数名，括号里的东西是传给它的参数。多个参数用英文逗号分开，默认用空格连接。

`print("2 + 3")` 输出文字 `2 + 3`；`print(2 + 3)` 输出数字 `5`。引号告诉 Python“里面是文本”，没有引号时则按代码解释。单引号与双引号都可以，开头和结尾必须匹配。

### 空行、注释、缩进
`#` 后直到这一行结束是注释，解释器不把它当作指令执行。注释最好解释“为什么”，例如“先换成分钟，方便比较”，而不是只重复代码。字符串中的 `#` 则是普通文字。

空行帮助人阅读。缩进在 Python 中则参与语法：同一代码块要用一致缩进，建议每层 4 个空格。顶层语句一般从最左边开始。不要混合 Tab 与空格。后面看到 `if`、`for`、`def` 后的冒号，下一层内容通常需要缩进。

### 先读懂一条报错
故意在练习文件里写 `print("你好"`，运行会看到 SyntaxError，意思是结构不符合语法。补上右括号后再运行。报错指向的位置有时是解释器发现问题的位置，真正漏掉的符号可能在上一行。

NameError 常表示名字没定义或拼错，如写成 `pirnt`。`Print` 与 `print` 不同，Python 区分大小写。每次只改一个问题，然后重新运行；不要一次凭感觉改很多行。

### 用中文先写算法
以“给两人平均分一笔钱”为例：得到总金额 → 得到人数 → 总金额除以人数 → 显示结果。暂时用固定数字，等第 02 章再接收键盘输入。写程序不等于背语法；先有步骤，再选择语法。
''',
['引号内是文字，引号外可能是表达式。','print 才负责显示；表达式本身负责求值。','冒号后常有代码块，同一层使用 4 个空格缩进。'],
['我能解释 print("3") 与 print(3) 的相似和不同。','我能从零写出三行介绍自己的程序。','我能修正一处拼写、一处括号和一处引号错误。'])
example(c,'第一段程序',r'''print("你好，Python！")
print("今天开始学编程。")''',r'''你好，Python！
今天开始学编程。''','第 1 行先输出问候，第 2 行再输出计划。每次 print 默认在末尾换行。程序不会自动猜测你想改变什么。','把两句话改成自己的学习目标。')
example(c,'文本与计算',r'''print("2 + 3")
print(2 + 3)
print("结果是", 2 + 3)''',r'''2 + 3
5
结果是 5''','第一行的加号是文本字符。第二行先计算表达式得到 5，再交给 print。第三行传入两个参数，用默认空格连接。','预测 print("2" + "3") 会输出什么，再运行。')
example(c,'控制输出分隔',r'''print("年", "月", "日", sep="/")
print("正在学习", end="：")
print("Python")''',r'''年/月/日
正在学习：Python''','sep 指多个参数之间的分隔符；end 指本次输出结束时追加什么。第二行用中文冒号替代默认换行，所以第三行接在同一行。','把 sep 改成空字符串，把 end 改成换行符。')
example(c,'注释与执行顺序',r'''# 先计算总分，再计算平均分
print(80 + 90)
print((80 + 90) / 2)
print("# 这部分仍会显示")''',r'''170
85.0
# 这部分仍会显示''','括号让加法先执行。除法 / 的结果是浮点数，所以显示 85.0。第一行注释不执行，最后一行引号内的 # 不是注释。','删掉平均分表达式内的小括号，观察结果并解释。')
exercise(c,'学习名片','基础','依次输出两行：我叫小林；我每天学习 45 分钟。标点必须与示例一致。','每行用一个 print，中文文字放在引号里。',r'''print("我叫小林")
print("我每天学习 45 分钟")''',r'''我叫小林
我每天学习 45 分钟''','把自然语言中的两句话对应到两次输出。print 自动换行，无需自己写换行符。')
exercise(c,'先算后显示','基础','输出 12 与 8 的和、差、积，每个结果占一行。','引号中的 12 + 8 不会计算。',r'''print(12 + 8)
print(12 - 8)
print(12 * 8)''',r'''20
4
96''','加减乘分别使用 +、-、*。数学里的乘号 × 不能直接写进 Python 表达式。')
exercise(c,'修复姓名输出','纠错','原程序是 Print(小林)。修好后输出 小林。解释两个错误。','一个错误是函数名大小写，另一个是文字的表示方法。',r'''print("小林")''',r'''小林''','Print 不是内置 print；小林 不加引号会被当作变量名查找。中文变量名技术上可以使用，但教材使用英文变量名以便阅读常见代码。')
exercise(c,'收据一行','场景','用一次 print 输出 苹果|3|12，不要在竖线两侧加入空格。','使用 sep 参数。',r'''print("苹果", 3, 12, sep="|")''',r'''苹果|3|12''','三个参数分别代表品名、数量、金额。sep="|" 替换默认的空格。')
exercise(c,'平均分与优先级','推理','两次测验是 70 和 90，输出平均分 80.0。说明为什么 70 + 90 / 2 不对。','先相加，后除以 2。',r'''print((70 + 90) / 2)''',r'''80.0''','乘除优先于加减；不加括号得到 70 + 45 = 115。括号明确把总分作为除法的左边。')

c = chapter(2, '变量 类型 运算与输入', '先知道手里的数据是什么，再决定怎样处理。',
['会给值命名并更新变量', '区分 int、float、str、bool 与 None', '会把键盘输入转换成需要的类型'], r'''
### 变量是绑定到对象的名字
`age = 20` 不是数学等式，而是把右边的值交给左边的名字。读成“让 age 指向整数 20”。执行 `age = age + 1` 时，先读旧值 20，算出 21，再把 age 绑定到 21。初学可把它想成贴标签；第 07 章会说明为什么两个标签可能指向同一个列表。

名字用字母、数字和下划线组合，不能以数字开头；推荐 `study_minutes` 这种小写下划线风格。`class`、`if` 等关键字不能当变量名。不要把变量起名为 `list`、`str`、`sum`，否则会遮住同名内置工具。

### 类型决定可以做哪些操作
| 类型 | 示例 | 含义与用途 |
|---|---|---|
| int | 3、-8、0 | 整数，人数、次数、索引 |
| float | 3.5、0.01 | 浮点数，近似表示小数 |
| str | "3"、"你好" | 文本，即使看起来像数字 |
| bool | True、False | 真或假，注意首字母大写 |
| NoneType | None | 暂无结果或缺失值的一个标记 |

`type(x)` 查看类型。`3 + 2` 是数值相加；`"3" + "2"` 是拼接；`"3" + 2` 会产生 TypeError。Python 不会替你猜应该拼接还是相加。

### 算术常用符号
`+ - * /` 分别是加减乘除，`//` 是向下取整的除法，`%` 是余数，`**` 是幂。正数场景下 `125 // 60` 得到 2，`125 % 60` 得到 5，常用来把分钟换成小时和分钟。负数时要小心：`-7 // 3` 得到 -3，因为向负无穷取整；`-7 % 3` 得到 2，满足 `a == (a // b) * b + a % b`。

通常先括号，再乘方，再乘除余，再加减；拿不准时用括号表达意图。`-2 ** 2` 是 -4，`(-2) ** 2` 才是 4。`total += 5` 相当于给当前 total 加 5 后赋回；total 必须先有值。

### input 永远先给你字符串
`input("年龄：")` 会显示提示并等待输入，回车后返回字符串，不包含回车本身。输入 18，得到的是 `"18"`。要做整数运算，使用 `int(...)`；小数用 `float(...)`。`int("18.5")` 会报错，而 `int(18.5)` 得到 18，是向零截断，不是四舍五入。

`str(18)` 把数字变成文本。`bool("")` 是 False，而 `bool("False")` 是 True，因为它是非空字符串。不要用 bool 把用户输入的“否”自动转换成 False，要明确比较文本。

### 小数不是总能精确存储
二进制浮点数无法精确表示部分十进制小数。`0.1 + 0.2` 可能显示 `0.30000000000000004`。显示两位小数可以用格式化，比较近似数在第 13 章用 `math.isclose`。学习账本时把金额保存为整数“分”，例如 12.50 元表示为 1250 分。格式化改变显示，不会让底层数值变得精确。

### 把需求翻译成变量
“买 3 本书，每本 25 元，优惠 10 元”可以拆为 price、quantity、discount，再写 `total = price * quantity - discount`。变量名说明数据角色，减少神秘数字。先做固定输入，再加 input，是更容易排错的顺序。
''',
['赋值看右边，算完再绑定左边。','input 得到 str；需要数值时显式转换。','/ 得小数，// 向下取整，% 取余，** 乘方。'],
['我能解释 age = age + 1 的执行过程。','我能让两个键盘输入的数字正确相加。','我能把总秒数拆成分钟和剩余秒数。'])
example(c,'变量更新',r'''minutes = 30
minutes = minutes + 15
minutes += 5
print(minutes)''',r'''50''','先保存 30，第二行用旧值算出 45，第三行再增加 5。变量名不变，绑定的值变了。','增加一行 minutes -= 10，预测新结果。')
example(c,'检查类型',r'''print(type(3).__name__)
print(type(3.0).__name__)
print(type("3").__name__)
print(type(True).__name__)
print(type(None).__name__)''',r'''int
float
str
bool
NoneType''','type 返回类型对象，.__name__ 取该类型的名字。现在只需知道这套写法用于观察，不必提前掌握类。','分别对 0、""、False 使用 type。')
example(c,'分钟拆分',r'''total_minutes = 125
hours = total_minutes // 60
minutes = total_minutes % 60
print(hours, "小时", minutes, "分钟")''',r'''2 小时 5 分钟''','整除计算装满了几个 60，取余计算不足一个 60 的部分。用 2 * 60 + 5 可以还原总数。','换成 59、60、61，检查边界。')
example(c,'从输入到数值',r'''text = input("请输入本周学习天数：")
days = int(text)
print("总分钟", days * 45)''',r'''请输入本周学习天数：总分钟 135''','示例自动核验会模拟输入 3。真实终端中你键入的 3 也会显示，但那是键盘回显，不属于程序输出。input 不自动给提示末尾加换行。','输入 0 或 7；再试 abc，观察 ValueError。',stdin='3\n')
example(c,'购物合计',r'''price_fen = 1250
quantity = 3
total_fen = price_fen * quantity
print(total_fen)
print(f"应付 {total_fen / 100:.2f} 元")''',r'''3750
应付 37.50 元''','运算在整数分上完成，显示时除以 100 并保留两位。f 开头的字符串允许在花括号里填表达式，第 03 章展开。','把数量改成 0，说明它是否符合你的业务规则。')
example(c,'交换变量',r'''a = 10
b = 20
a, b = b, a
print(a, b)
print(-7 // 3, -7 % 3)''',r'''20 10
-3 2''','交换时先求右侧旧的 b 和 a，再给左边两个名字赋值。第二个输出提醒你：负数整除不是简单删掉小数位。','用第三个临时变量完成同样的交换。')
exercise(c,'摄氏转华氏','基础','已有 celsius = 25，按 F = C × 9 / 5 + 32 计算并输出 77.0。','乘号写 *，不要写 ×。',r'''celsius = 25
fahrenheit = celsius * 9 / 5 + 32
print(fahrenheit)''','77.0','按公式依次运算。用 0 摄氏度手算应为 32，可额外验证。')
exercise(c,'时间拆分','场景','把 3671 秒拆成小时、分钟、秒，并用空格分隔输出 1 1 11。','先整除 3600；剩余秒数再拆成 60。',r'''seconds = 3671
hours = seconds // 3600
minutes = (seconds % 3600) // 60
remaining = seconds % 60
print(hours, minutes, remaining)''','1 1 11','先取整小时，余数 71 秒含 1 分 11 秒。验算 1*3600+1*60+11=3671。')
exercise(c,'两次输入相加','基础','程序读入两行整数，不打印提示。输入 12 和 8 时输出 20。','每次 input 后调用 int。',r'''a = int(input())
b = int(input())
print(a + b)''','20','如果忘记 int，字符串相加会得到 128。先决定需要的运算，再决定数据类型。',stdin='12\n8\n')
exercise(c,'修复记账类型','纠错','price = "19.5"，count = 2，输出总价 39.0；解释为什么 price * count 得不到总价。','字符串乘整数是重复文本。',r'''price = "19.5"
count = 2
print(float(price) * count)''','39.0','原式会得到 19.519.5，因为字符串重复两次。转换为 float 后才是数值乘法；正式账本建议整数分。')
exercise(c,'整箱装书','场景','53 本书，每箱最多 12 本。输出完整箱数 4、剩余本数 5、实际需要箱数 5，每个一行。','最后不足一箱也占一箱；可用 (数量 + 容量 - 1) // 容量。',r'''books = 53
capacity = 12
print(books // capacity)
print(books % capacity)
print((books + capacity - 1) // capacity)''',r'''4
5
5''','向上取整公式适用于非负整数数量和正整数容量。用 0、12、13 验证，得到 0、1、2 箱。')
exercise(c,'平均速度','迁移','跑了 5 千米，用时 1500 秒。输出平均速度 12.0，单位千米每小时。','先把秒换成小时；别把分钟当小时。',r'''distance_km = 5
time_seconds = 1500
time_hours = time_seconds / 3600
print(distance_km / time_hours)''','12.0','变量名带单位能减少错误。速度=路程/时间；现实程序还要保证用时大于 0，第 04 章学习判断。')

c = chapter(3, '字符串与文本处理', '从姓名、句子和日志中提取真正需要的信息。',
['会索引、切片、清理和拆分文本','能用 f-string 组织清晰输出','理解不可变对象与返回新值'], r'''
### 字符串是有顺序的文本
`text = "Python"` 包含 6 个字符，`len(text)` 得到 6。索引从 0 开始：`text[0]` 是 P，`text[1]` 是 y；负索引从末尾数，`text[-1]` 是 n。长度为 n 的非空字符串，正索引范围是 0 到 n-1。空字符串 `""` 的长度为 0，没有第一个字符。

`"你好"` 的长度是 2；但有些 emoji 和组合字符由多个 Unicode 码点组成，len 不等于所有场景下肉眼看到的图形数。普通中英文练习先按常见字符理解即可。

### 切片的左闭右开
`text[start:stop:step]` 从 start 开始，到 stop 之前停止，按 step 跨步取。`text[1:4]` 取索引 1、2、3。省略 start 通常从开头，省略 stop 通常到结尾。`text[:3]` 是前三个，`text[3:]` 是从索引 3 到末尾，`text[::-1]` 是倒序。

记忆方法：“**开始要，结束不要**”。先在纸上写索引，再圈出实际取到的位置。普通正向切片中，取几个常可用 stop-start 理解；遇到负步长要重新沿步长方向数。步长不能是 0。单个索引越界报 IndexError，切片超出边界通常会自动截到可用范围。

### 方法调用读成“对这个对象做什么”
`text.strip()` 是调用字符串对象的方法，返回去掉两端空白的新字符串；不会删除中间空格。`lower()` 变小写，`upper()` 变大写，`replace(old, new)` 替换文本，`split()` 按连续空白拆分，`split(",")` 按逗号拆分，`"-".join(parts)` 用连字符把多个字符串连接。

`" a  b ".split()` 得到两个词；`"a,,b".split(",")` 中间会保留空字符串。CSV 含引号或逗号时不要自己 split，第 12 章用 csv 模块。

### 字符串不能就地修改
`name[0] = "L"` 会失败，因为 str 不可变。`name.upper()` 返回新字符串；如果没有保存它，旧变量仍指向原字符串。写 `name = name.upper()` 才让 name 指向转换结果。不可变不等于变量不能重新赋值。

### 格式化输出
`f"你好，{name}"` 会把 name 的值放入文本；f 必须紧贴开头引号。`f"{score:.2f}"` 显示两位小数，`f"{rate:.1%}"` 将比例显示为一位小数的百分数。格式化常用于报告，不应把显示后的字符串重新拿来做数值运算。

转义符 `\n` 表示换行，`\t` 表示制表符，`\\` 表示一个反斜杠。`r"C:\notes"` 是原始字符串的一种写法，但以单个反斜杠结尾仍有语法限制。处理路径优先用第 12 章的 pathlib，少手写反斜杠。三引号可以书写多行字符串，里面的缩进也可能成为文本的一部分。

### 一个实用的文本清洗流程
用户输入账号 → 去掉两端空白 → 统一大小写 → 检查是否为空 → 保存。每一步都先打印 repr(text)，就能看到看不见的空格和换行。例如 `repr(" hi\n")` 会显示带引号和转义符的表示。不要为了“清洗”随意删除有意义的内部空格或符号。
''', ['索引从 0 开始；切片开始要、结束不要。','strip 去两端，split 拆开，join 拼起来。','字符串方法返回新值，想保留就重新赋值。'],
['我能手算 "Python"[1:5:2]。','我能清洗用户输入后生成一句格式化问候。','我能解释为什么 text.upper() 不会改变原字符串。'])
example(c,'读字符与切片',r'''word = "Python"
print(word[0], word[-1])
print(word[1:4])
print(word[:2], word[2:])
print(word[::-1])''',r'''P n
yth
Py thon
nohtyP''','索引 1 到 3 是 y、t、h。反向切片从最后一个字符向前走。','预测 word[1:5:2] 和 word[99:]，再运行。')
example(c,'清理姓名',r'''raw = "  Alice\n"
clean = raw.strip().lower()
print(repr(raw))
print(clean)
print(len(clean))''',r''' '  Alice\n'
alice
5'''.strip(),'先 strip 再 lower，链式调用从左向右。repr 明确显示末尾换行，普通 print 不容易看出它。','把输入改成全空格，观察 clean 是否为空。')
example(c,'分词与拼接',r'''sentence = "  learn   python today  "
words = sentence.split()
print(words)
print("-".join(words))''',r'''['learn', 'python', 'today']
learn-python-today''','split 无参数时把连续空白当分隔。结果是列表，第 07 章详细学习。join 的接收者是分隔字符串，参数是字符串序列。','把 split() 改成 split(" ")，比较连续空格的处理。')
example(c,'报告格式',r'''name = "小林"
score = 86.456
rate = 0.875
print(f"{name}的分数：{score:.2f}")
print(f"完成率：{rate:.1%}")
print(f"编号：{7:03d}")''',r'''小林的分数：86.46
完成率：87.5%
编号：007''','.2f 是小数点后两位；.1% 会乘 100 并添加百分号；03d 将整数补齐为至少三位，不足用 0 填充。','将完成率改成 1 与 0，解释输出。')
example(c,'方法返回新文本',r'''text = "python is fun"
text.replace("fun", "useful")
print(text)
text = text.replace("fun", "useful")
print(text)
print("python" in text)''',r'''python is fun
python is useful
True''','第一次 replace 的返回值被丢弃。第二次赋回 text 才改变名字指向的对象。in 判断子串是否出现，返回布尔值。','检查大小写不同的 "Python" 是否在 text 中。')
exercise(c,'邮箱清洗','基础','把 "  Learner@Example.COM  " 去两端空白并转小写，输出 learner@example.com。','链式调用 strip 和 lower。',r'''email = "  Learner@Example.COM  "
print(email.strip().lower())''','learner@example.com','只去两端，不改变内部结构。这里是字符串操作练习，不是完整的邮箱有效性验证。')
exercise(c,'遮盖号码','场景','给定 phone = "13812345678"，保留前 3 位和后 4 位，中间用 4 个星号，输出 138****5678。','切片 [:3] 和 [-4:]。',r'''phone = "13812345678"
print(phone[:3] + "****" + phone[-4:])''','138****5678','先确认本题假定长度为 11。真实输入还需检查长度和内容，不能把遮盖当作完整隐私保护。')
exercise(c,'提取文件扩展名','基础','给定 filename = "report.final.csv"，按点拆分，输出最后一部分 csv。','split 返回列表，[-1] 取最后一项。',r'''filename = "report.final.csv"
print(filename.split(".")[-1])''','csv','这里练 split 与负索引。处理真实路径更适合 Path.suffix，尤其要注意隐藏文件和没有扩展名的文件。')
exercise(c,'清理多余空格','场景','把 "  I   love  Python  " 转成单个空格分隔的 "I love Python"。','split() 后使用一个空格 join。',r'''text = "  I   love  Python  "
print(" ".join(text.split()))''','I love Python','strip 只能去两端，无法合并内部重复空格。先拆成词，再以统一分隔符拼接。')
exercise(c,'切片推理','推理','给定 s = "abcdef"，依次输出 bdf、fedcba、abc，各一行。','选择不同起点和步长；反向步长为 -1。',r'''s = "abcdef"
print(s[1::2])
print(s[::-1])
print(s[:3])''',r'''bdf
fedcba
abc''','第一个索引序列是 1、3、5。第二个是 5、4、3、2、1、0。第三个是 0、1、2。')
exercise(c,'学习进度百分比','迁移','完成 7 节，共 20 节。输出 已完成 35.0%。','先算比例，再用 .1% 格式。',r'''completed = 7
total = 20
print(f"已完成 {completed / total:.1%}")''','已完成 35.0%','比例是 0.35；百分号格式自己乘以 100。不要先乘 100 再用 %，否则会显示 3500.0%。')

c = chapter(4, '比较 条件与分支', '让程序根据具体情况做出不同选择。',
['使用比较和逻辑运算','正确组织 if、elif、else','检查边界、空值和短路行为'], r'''
### 从比较得到真假
`==` 判断相等，`!=` 判断不等，`>`、`<`、`>=`、`<=` 比较大小。赋值 `=` 与比较 `==` 完全不同。`18 <= age < 60` 是合法链式比较，表示年龄同时落在这个区间。

`and` 要两边条件都成立，`or` 至少一边成立，`not` 取反。判断是否周末应写 `day == "周六" or day == "周日"`，不能写 `day == "周六" or "周日"`；后一项非空字符串总为真。

### if 是选一条路径
基本结构是 `if 条件:`，下一行缩进写条件为真时做的事。`elif` 是前面没有选中时继续检查，`else` 是前面全部没有选中时兜底。一条 if/elif/else 链只会执行最多一个分支。多个独立 if 则会分别检查，有可能都执行。

成绩分级如果先判断 `score >= 60`，90 分也会先进入这个分支；高等级通常从高到低写。缩进结束代表这个分支结束。程序随后继续执行分支后面的语句。

### 真值不是只有 True 和 False
`0`、`0.0`、空字符串、空列表、空字典、空集合和 None 常被当作假；非空容器通常为真。`if items:` 常用来表示“有元素”。`"0"` 和 `"False"` 都是非空字符串，是真。

`None` 经常表示缺失值，判断它用 `is None` 或 `is not None`。值相等通常用 `==`；`is` 判断是否为同一个对象，不要用它比较普通字符串或整数的数值相等。

### 短路能避免无意义运算
`and` 左边为假就不看右边；`or` 左边为真就不看右边。例如 `count > 0 and total / count > 60`，count 为 0 时不会执行除法，避免除零。技术上 and/or 返回某个操作数，而不保证一定返回 bool；刚开始尽量让两边都是明确条件。

### 用边界检查自己的判断
判断“满 100 减 10”，最有价值的测试不是只测 200，而是测 99、100、101。判断合法成绩，至少测 -1、0、60、100、101。先验证输入范围，再做业务分级，能避免把不可能的值分成正常等级。

### 把复杂判断拆成有意义的名字
不要把所有逻辑塞进一个长 if。可以先算 `has_ticket`、`is_open`，再判断 `if has_ticket and is_open:`。表达式很长时加括号，明确逻辑关系。条件中的布尔变量不必写 `== True`。
''', ['一条 if 链选一个分支；多个 if 各自判断。','等级从高到低，边界围着临界值测。','相等用 ==，缺失用 is None。'],
['我能为满减活动写出 99、100、101 三个测试。','我能解释两个独立 if 和 if/elif 的区别。','我能修正 day == "周六" or "周日"。'])
example(c,'判断是否通过',r'''score = 59
if score >= 60:
    print("通过")
else:
    print("继续练习")
print("记录完成")''',r'''继续练习
记录完成''','59 >= 60 为假，走 else。最后一行没有缩进，因此不论哪条路径都会执行。','把 score 换成 60、100、-1；最后一个提醒你还没验证范围。')
example(c,'成绩等级',r'''score = 85
if not 0 <= score <= 100:
    print("成绩无效")
elif score >= 90:
    print("优秀")
elif score >= 60:
    print("通过")
else:
    print("待加强")''','通过','先挡住不合法数据，然后从最高阈值往下判断。85 不满足 90，但满足 60。','验证 -1、0、59、60、89、90、100、101。')
example(c,'同时满足两个条件',r'''age = 20
has_ticket = True
if age >= 18 and has_ticket:
    print("允许进入")
else:
    print("条件未满足")''','允许进入','and 要求年龄和票据条件都成立。用四种真假组合做真值表，可以检查逻辑。','把 has_ticket 改为 False，再把 age 改为 17。')
example(c,'短路避免除零',r'''count = 0
total = 80
if count > 0 and total / count >= 60:
    print("平均分通过")
else:
    print("人数不足或平均分未通过")''','人数不足或平均分未通过','第一个条件为假，第二个除法不执行。短路可以用来保护操作，但别让重要的副作用藏在条件右边。','改成 count = 2，手算第二个条件。')
example(c,'缺失与零分',r'''score = 0
if score is None:
    print("尚未提交")
else:
    print(f"已提交，成绩 {score}")
print(bool("False"), bool(""))''',r'''已提交，成绩 0
True False''','零分仍是已提交的有效成绩。若使用 if not score，会把 0 和缺失混在一起。','把 score 改成 None，观察分支改变。')
exercise(c,'奇偶判断','基础','给定 n = 17，如果能被 2 整除输出 偶数，否则输出 奇数。','余数等于 0 才是整除。',r'''n = 17
if n % 2 == 0:
    print("偶数")
else:
    print("奇数")''','奇数','17 除以 2 余 1。补测 0 和负数，0 也属于偶数。')
exercise(c,'运费规则','场景','订单金额 99 元，满 100 元免运费，否则运费 8 元。输出应付总额 107。','临界值 100 属于免运费。',r'''amount = 99
if amount >= 100:
    shipping = 0
else:
    shipping = 8
print(amount + shipping)''','107','先决定运费，再统一计算合计，避免在每个分支重复相同输出。')
exercise(c,'合法分数','纠错','score = 105。若不在 0 到 100 内输出 无效，否则达到 60 输出 通过，未达到输出 未通过。','合法性判断放在等级判断之前。',r'''score = 105
if not 0 <= score <= 100:
    print("无效")
elif score >= 60:
    print("通过")
else:
    print("未通过")''','无效','错误写法先判断 score >= 60，会把 105 判通过。必须先限定问题域。')
exercise(c,'周末判断修复','纠错','day = "周一"。修复 if day == "周六" or "周日" 的错误，输出 工作日。','or 两边都要完整比较，也可使用 in。',r'''day = "周一"
if day == "周六" or day == "周日":
    print("周末")
else:
    print("工作日")''','工作日','"周日" 作为独立非空字符串是真；修复后左右两项均为 False。')
exercise(c,'找三个数最大值','迁移','a=7，b=12，c=9，不用 max，输出最大值 12。','先把 a 当作当前最大值，再依次比较。',r'''a, b, c = 7, 12, 9
largest = a
if b > largest:
    largest = b
if c > largest:
    largest = c
print(largest)''','12','这里用两个独立 if，因为两次比较都需要执行。相等时无需更新，结果仍正确。')
exercise(c,'区分未填和零','场景','value = 0，None 表示未填，其他数值包括 0 都算已填。输出 已填。','用 is None，而不是 if not value。',r'''value = 0
if value is None:
    print("未填")
else:
    print("已填")''','已填','业务含义决定判断方式。零值和没有值是两个不同状态。')

c = chapter(5, 'for 循环与逐项处理', '同样的动作做很多次，用循环描述规则。',
['理解遍历、循环变量和 range','会累计、计数、筛选与查找','能手工追踪每一次迭代'], r'''
### 为什么需要循环
三个分数可以手写三次相加，三千个就不行。`for score in scores:` 的含义是从 scores 中依次取一个元素，把它绑定给 score，然后执行缩进块。块执行完再取下一个，取完就结束。每一次重复称为一次“迭代”。

本章先把 `[70, 85, 60]` 理解成一串有顺序的数据，叫列表。第 07 章再系统学习增删改查。循环变量可以任意起名，但 `score` 比 `x` 更容易理解。

### range 生成整数序列
`range(5)` 对应 0、1、2、3、4；`range(1, 6)` 对应 1、2、3、4、5；`range(2, 10, 2)` 对应 2、4、6、8。与切片一样，终点不包含。`range(5, 0, -1)` 是 5、4、3、2、1。步长必须非零，方向与边界不匹配时可能一个数都没有。

range 本身不是列表，一般不用为了遍历把它转成 list。要观察全部内容时可以 `print(list(range(5)))`。range 使用整数边界，不接受 0.5 作为步长。

### 累计与计数模板
累计先设 `total = 0`，每次执行 `total += value`。计数先设 `count = 0`，满足条件时执行 `count += 1`。初始值写在循环前；如果写在循环体里，每次都会清零。

“及格人数”累加的是 1；“及格分数总和”累加的是 score。两个题目只差一句话，代码里的更新对象却不同。每次写循环都要问：本轮取到什么？保留什么状态？状态怎么变？什么时候结束？

### 手工追踪表
对 `[2, 4, 1]` 求和：初始 total=0；第 1 轮 value=2，更新为 2；第 2 轮 value=4，更新为 6；第 3 轮 value=1，更新为 7。不要只看最后输出，要能解释中间过程。网页的循环演示器可以逐步显示同样的状态变化。

### 空数据也要考虑
空列表的 for 一次也不执行，因此 total 保留 0。这是合理的空和，但平均值不能直接写 total/len(values)，因为人数为 0。先检查长度再除。求最大值时也要明确空数据怎么处理；第 09 章用函数返回 None 或抛异常表达约定。

### 循环之后变量还在吗
for 不会创建独立作用域。非空循环结束后，循环变量通常仍绑定最后一个值；如果循环一次未执行，这个名字可能根本没定义。不要依赖“最后的循环变量”作为结果；建立明确的结果变量更可靠。
''', ['for 是逐项取，不是自动同时处理所有项。','初始化放循环外，更新放循环内。','求和加数值，计数加 1，平均先防空。'],
['我能逐行追踪 total 在三轮循环中的值。','我能输出 1 到 10，而不是 0 到 9。','我能把筛选条件加入累计程序。'])
example(c,'遍历分数',r'''scores = [70, 85, 60]
for score in scores:
    print("分数", score)
print("遍历结束")''',r'''分数 70
分数 85
分数 60
遍历结束''','循环每次只取一个分数。最后的 print 在循环外，因此只执行一次。','把最后的 print 缩进到循环体，预测区别。')
example(c,'累计过程',r'''total = 0
for value in [2, 4, 1]:
    total += value
    print(value, total)
print("总和", total)''',r'''2 2
4 6
1 7
总和 7''','total 跨越各轮保存累计状态。输出中的左列是本轮输入，右列是更新后的累计值。','把 total = 0 移入循环，解释为什么结果变成 1。')
example(c,'统计通过人数',r'''count = 0
for score in [59, 60, 80, 40]:
    if score >= 60:
        count += 1
print(count)''','2','for 里面嵌套 if，因此 if 内再多缩进一层。只在 60 和 80 两轮更新 count。','再添加 total，只累计通过者分数。')
example(c,'范围与倒计时',r'''for number in range(1, 4):
    print(number)
print("倒数")
for number in range(3, 0, -1):
    print(number)''',r'''1
2
3
倒数
3
2
1''','range 的第二个参数是停止边界，不是最后一个必含元素。负步长使数值递减。','改成 range(3, 0)，解释为什么没有输出。')
example(c,'带序号遍历',r'''names = ["小林", "小陈", "小王"]
for number, name in enumerate(names, start=1):
    print(number, name)''',r'''1 小林
2 小陈
3 小王''','enumerate 把每项配上序号，左边两个名字分别接收序号与内容。start=1 改的是显示序号，不是原列表索引规则。','删除 start=1，观察序号从哪里开始。')
example(c,'空列表平均值',r'''scores = []
total = 0
for score in scores:
    total += score
if len(scores) == 0:
    print("没有成绩")
else:
    print(total / len(scores))''','没有成绩','空列表跳过循环，再由 if 避免除零。程序要为“什么都没有”设计明确输出。','填入两个分数，再测试只有一个分数。')
exercise(c,'一到十求和','基础','用 for 循环计算 1 到 10（包含 10）的总和，输出 55。','range 的终点要写 11。',r'''total = 0
for number in range(1, 11):
    total += number
print(total)''','55','10 轮分别累加 1 至 10。不要在循环内部重新初始化 total。')
exercise(c,'偶数总和','基础','计算 1 到 20 之间所有偶数的和，输出 110。','可用步长 2，也可用 if 判断。',r'''total = 0
for number in range(2, 21, 2):
    total += number
print(total)''','110','从 2 开始每次加 2，包含 20。另一种写法遍历全部整数后检查 % 2 == 0。')
exercise(c,'学习打卡统计','场景','学习分钟数 [0, 30, 45, 0, 60]，分别输出学习过的天数 3 和总分钟 135。','计数累加 1，总量累加分钟。',r'''days = 0
total = 0
for minutes in [0, 30, 45, 0, 60]:
    if minutes > 0:
        days += 1
    total += minutes
print(days)
print(total)''',r'''3
135''','总和可以对所有项累加，因为 0 不影响结果；有效天数只在大于 0 时增加。')
exercise(c,'单词长度报告','场景','对 ["cat", "python", "AI"] 输出 cat:3、python:6、AI:2，各占一行。','每次处理一个词，len 得到长度。',r'''for word in ["cat", "python", "AI"]:
    print(f"{word}:{len(word)}")''',r'''cat:3
python:6
AI:2''','把“单个词怎样处理”写好后，再用 for 应用到整个列表，这正是批量处理的基本模式。')
exercise(c,'找最大值','迁移','不用 max，求非空列表 [-5, -2, -9] 的最大值，输出 -2。','初始最大值不能设为 0，全部为负会出错。',r'''numbers = [-5, -2, -9]
largest = numbers[0]
for number in numbers[1:]:
    if number > largest:
        largest = number
print(largest)''','-2','用第一个真实元素初始化，之后逐项更新。此实现约定列表非空，空列表需另行处理。')
exercise(c,'统计元音','迁移','统计 "Education" 中英文字母元音 a e i o u 的数量，忽略大小写，输出 5。','先 lower，再用 in 判断字符是否属于元音字符串。',r'''count = 0
for char in "Education".lower():
    if char in "aeiou":
        count += 1
print(count)''','5','依次命中 e、u、a、i、o。这里只统计指定英文字母，不是一般语言的语音分析。')

c = chapter(6, 'while 循环与流程控制', '知道重复的终止条件，才能让程序可靠结束。',
['根据条件重复执行','区分 break、continue 与 return','理解嵌套循环和循环边界'], r'''
### for 与 while 怎样选
有一串现成数据需要逐项处理，优先 for；需要“持续做，直到某个条件改变”，常用 while。例如反复请求输入直到合法、持续显示菜单直到用户选择退出。不要为了用 while 把简单遍历写得更复杂。

`while 条件:` 每次进入循环前都会重新检查条件。先检查，再执行，所以条件一开始为假时执行零次。构成一个可控 while 的三个部分是：初始状态、继续条件、状态更新。遗漏更新可能产生无限循环。

### 手工走一遍计数器
`n = 3`；检查 n>0 为真，输出 3，然后 n-=1；再检查 2>0，输出 2；再检查 1>0，输出 1；最后 n=0，条件为假，退出。条件不是进入时检查一次就永远不变，每轮都会重新计算。

### break 与 continue
`break` 立即结束它所在的最内层循环；`continue` 跳过本轮剩余语句，开始下一轮。嵌套循环里的 break 通常只退出内层。函数里的 `return` 则结束整个当前函数，第 09 章会讲。

while 中如果把计数器更新放在 continue 之后，某些路径可能永远跳过更新。解决方法是确保每条继续执行的路径都推进状态，或者直接用 for 遍历。

### 哨兵输入与菜单
哨兵是约定的结束标记，例如输入 q 就结束录入。先检查是不是 q，再把其他输入转换成数字，否则 int("q") 会直接报错。数据值可能本身为 0 时，别把 0 随意当结束信号；选不会与有效输入冲突的标记。

### 嵌套循环怎样执行
外层走一步，内层通常完整走一遍。两组实验学习率 × 三个批大小，会有 2×3=6 种组合。把外层看成行、内层看成列有助于理解，但它不必真是二维表。不要把“两个顺序排列的循环”误认为“两个嵌套循环”。

### 从错误中退出
终端里的长时间循环通常可以用 Ctrl+C 中断；IDLE 可用 Shell 中断或 Restart Shell。Ctrl+C 是恢复控制的方法，不是正确终止条件的替代品。调试时先限制最大次数，例如最多 5 轮，再观察状态。

Python 还有 for/while 的 else：仅在循环正常耗尽或条件变假、没有由 break 退出时执行。初学阶段用 found 变量更直白；阅读别人代码遇到循环 else 时记住“没有 break 才执行”，它不属于内部 if。
''', ['while 看条件，for 看序列。','break 退出循环；continue 跳过本轮后半段。','状态必须推进，才能走向结束条件。'],
['我能指出一个 while 的初始值、条件和更新。','我能写出输入 q 退出的程序。','我能解释两层循环的真实执行顺序。'])
example(c,'有限倒计时',r'''remaining = 3
while remaining > 0:
    print(remaining)
    remaining -= 1
print("开始")''',r'''3
2
1
开始''','remaining 每轮减少，最终使条件变假。最后的输出在循环之外。','把初值改成 0，观察循环体是否执行。')
example(c,'遇到目标就停止',r'''for value in [4, 8, 15, 16]:
    if value > 10:
        print("首个大于 10 的数", value)
        break
    print("检查过", value)''',r'''检查过 4
检查过 8
首个大于 10 的数 15''','15 命中后 break，连本轮后面的输出也跳过，16 不再访问。','把条件改成 > 100，观察没有命中的路径。')
example(c,'跳过无效项',r'''total = 0
for value in [10, -1, 20, -5, 30]:
    if value < 0:
        continue
    total += value
print(total)''','60','负数轮次直接进入下一轮，正数被累计。continue 不结束整个遍历。','改成 break，解释为什么只得到 10。')
example(c,'读取直到 q',r'''total = 0
while True:
    text = input().strip()
    if text == "q":
        break
    total += int(text)
print(total)''','30','模拟输入 10、20、q。while True 靠显式 break 终止；先判 q，再转整数。非数字输入的恢复在第 13 章学习。','增加一行数字 0，确认它是有效数据而不是退出标记。',stdin='10\n20\nq\n')
example(c,'嵌套组合',r'''for model in ["A", "B"]:
    for batch_size in [2, 4]:
        print(model, batch_size)''',r'''A 2
A 4
B 2
B 4''','外层 A 固定时，内层先完成 2 和 4；再换 B 并重新遍历内层。','增加一个批大小 8，先预测输出行数。')
example(c,'无命中的处理',r'''found = False
for value in [1, 3, 5]:
    if value % 2 == 0:
        found = True
        print(value)
        break
if not found:
    print("没有偶数")''','没有偶数','found 记录有没有找到，循环结束后统一检查。把初始化放在循环外，才能跨轮保留结果。','在中间加入 4，确认只打印第一个偶数。')
exercise(c,'while 求和','基础','用 while 求 1 到 5 的和，输出 15。','计数器从 1 开始，每轮递增。',r'''number = 1
total = 0
while number <= 5:
    total += number
    number += 1
print(total)''','15','条件用 <= 包含 5；循环后 number 为 6。不递增会一直累加同一个数。')
exercise(c,'首次及格','场景','在 [40, 55, 72, 90] 中找到第一个及格成绩，输出 72 后停止。','条件成立后 print，再 break。',r'''for score in [40, 55, 72, 90]:
    if score >= 60:
        print(score)
        break''','72','“第一个”意味着后面的 90 不应再输出。若题目改成“所有”，就不该 break。')
exercise(c,'排除缺测值','场景','[-1, 30, 0, 45, -1] 中 -1 表示缺测，0 有效。输出有效条数 3 与总量 75，各一行。','只跳过 == -1 的项，不要写 if not value。',r'''count = 0
total = 0
for value in [-1, 30, 0, 45, -1]:
    if value == -1:
        continue
    count += 1
    total += value
print(count)
print(total)''',r'''3
75''','缺失标记与 0 的业务含义不同。统计有效条数时必须保留 0。')
exercise(c,'限次查找','推理','给定 guesses = [2, 4, 7, 9]，目标是 7，输出第几次猜中：3。','enumerate 从 1 开始，命中后 break。',r'''for attempt, guess in enumerate([2, 4, 7, 9], start=1):
    if guess == 7:
        print(attempt)
        break''','3','序号表示尝试次数，元素表示猜测值。这两个概念不要混淆。')
exercise(c,'二维坐标','迁移','输出两行三列的所有坐标，行与列都从 0 开始，顺序为 0 0 到 1 2，每对一行。','外层行号 range(2)，内层列号 range(3)。',r'''for row in range(2):
    for column in range(3):
        print(row, column)''',r'''0 0
0 1
0 2
1 0
1 1
1 2''','外层 2 次，每次内层 3 次，一共 6 对。日后张量维度也需要先辨认每一轴表示什么。')
exercise(c,'修复 continue 死循环','纠错','写 while 输出 1 到 5 中的奇数，每个一行；确保遇到偶数也会推进计数器。','一种简单方法是先递增，再决定是否 continue。',r'''n = 0
while n < 5:
    n += 1
    if n % 2 == 0:
        continue
    print(n)''',r'''1
3
5''','更新放在 continue 前，所有轮次都能推进。若从 n=1 开始并把更新写在末尾，n=2 时可能永远跳过更新。')

c = chapter(7, '列表 元组与对象关系', '这是后续数据处理最常用、也最容易产生隐蔽错误的一章。',
['会对列表增删改查和切片','区分修改原对象与返回新对象','理解别名、浅拷贝与嵌套列表'], r'''
### 列表解决一组数据的问题
`values = [10, 20, 30]` 把多个对象放在有顺序的容器中，可按索引取元素，也可以遍历。列表可以混合类型，但同一业务列表尽量保持结构一致，便于处理。`len(values)` 是元素个数；嵌套列表的长度只数外层元素，不自动数所有叶子。

单项赋值 `values[1] = 99` 改变原列表。`append(x)` 在末尾加入一个对象；`extend(xs)` 逐项加入另一个可迭代对象中的内容；`insert(i, x)` 插入；`pop()` 删除并返回末尾元素；`pop(i)` 按索引删除并返回；`remove(x)` 删除第一个相等的值，找不到会报 ValueError。`del values[i]` 也能按索引删除。

### append 与 extend 的区别
对 `[1, 2]` 执行 append([3,4]) 得到 `[1,2,[3,4]]`，因为加入的是一个列表对象；extend([3,4]) 得到 `[1,2,3,4]`，因为逐项加入。初学可记：“append 装一个，extend 逐个装”。append("ab") 装入一个字符串，extend("ab") 会装入 a 和 b 两个字符。

### sort 与 sorted 的区别
`values.sort()` 修改原列表，并返回 None；`sorted(values)` 返回新的排序列表，原对象不变。不要写 `values = values.sort()`，否则 values 会变成 None。`reverse()` 也是就地修改并返回 None。降序可用 `sorted(values, reverse=True)`。

### 两个名字可能指向同一个对象
`b = a` 没有复制列表，只是让 b 也指向 a 指向的对象。因此 `b.append(3)` 后，通过 a 也会看到变化。与之不同，`b = [9]` 只是让 b 改绑到另一个列表，不会修改 a 指向的旧列表。

读代码时问两个问题：“这是在修改对象，还是在改变名字的绑定？” 列表方法、元素赋值经常修改对象；普通 `=` 给名字重新绑定。列表上的 `+=` 通常会就地扩展，不能简单把所有类型上的 += 都理解为创建新对象。

### 浅拷贝复制外壳
`b = a.copy()` 或 `b = a[:]` 创建新外层列表。如果元素是整数等不可变对象，通常足够；若元素本身是列表，内层仍可能共享。`copy.deepcopy(a)` 会递归复制常见嵌套结构，但不是所有对象都适合或需要深拷贝。

`grid = [[0] * 3] * 2` 的两行指向同一个内层列表，改一行会影响另一行。用循环每次新建 `[0] * 3`，或第 10 章的 `[[0] * 3 for _ in range(2)]`，让每行独立。

### 不要一边遍历一边删同一列表
删除会让后面的元素向前移动，迭代位置却继续推进，容易跳过元素。更直白的方法是建立新列表，只把要保留的元素 append 进去。第 10 章可写成列表推导式。

### 元组是不可变的序列
`point = (3, 4)` 常表示一组固定结构的数据。`x, y = point` 是解包，元素数量要匹配。单元素元组写 `(3,)`，逗号不能省；`(3)` 只是整数外加括号。元组的槽位不能重新赋值，但若里面放了可变列表，那个列表仍能改变，所以“元组不可变”并非内部所有东西都永远不变。
''', ['append 加一个，extend 逐个加。','sort 改原地并返回 None，sorted 给新列表。','赋值不等于复制；浅拷贝只复制外层。'],
['我能画出 a、b 与列表对象之间的指向。','我能独立建立两行互不影响的网格。','我能在不修改原列表的情况下筛选与排序。'])
example(c,'基本增删改查',r'''tasks = ["阅读", "练习"]
tasks.append("复习")
tasks[0] = "读第 7 章"
last = tasks.pop()
print(tasks)
print(last)''',r'''['读第 7 章', '练习']
复习''','append 加末尾，索引赋值改首项，pop 同时执行删除并返回被删内容。','用 insert 在最前面插入 "预习"。')
example(c,'append 和 extend',r'''a = [1, 2]
a.append([3, 4])
b = [1, 2]
b.extend([3, 4])
print(a)
print(b)''',r'''[1, 2, [3, 4]]
[1, 2, 3, 4]''','a 外层长度为 3，b 长度为 4。嵌套结构不同，后面的遍历方式也不同。','分别打印 len(a)、len(b)、a[-1][0]。')
example(c,'排序与返回值',r'''scores = [80, 60, 90]
ordered = sorted(scores)
print(scores)
print(ordered)
result = scores.sort()
print(scores)
print(result)''',r'''[80, 60, 90]
[60, 80, 90]
[60, 80, 90]
None''','sorted 没改 scores。sort 随后改变 scores，但它的返回值是 None。不要把“执行效果”与“返回值”混在一起。','用 reverse=True 做降序，并确保原数据保留。')
example(c,'共享与重新绑定',r'''a = [1, 2]
b = a
b.append(3)
print(a)
b = [9]
print(a)
print(b)''',r'''[1, 2, 3]
[1, 2, 3]
[9]''','append 改共享对象；b = [9] 创建并改绑到另一个对象。重新绑定 b 不会沿着旧关系去修改 a。','把 b = a 换成 b = a.copy()，比较第一条输出。')
example(c,'浅拷贝的边界',r'''import copy
a = [[1], [2]]
b = a.copy()
c = copy.deepcopy(a)
b[0].append(9)
print(a)
print(b)
print(c)''',r'''[[1, 9], [2]]
[[1, 9], [2]]
[[1], [2]]''','b 外层独立，b[0] 却和 a[0] 共享内层列表；c 的常见嵌套列表被递归复制。import 的语法第 11 章系统学习。','尝试 b.append([3])，观察为什么不会给 a 增加第三项。')
example(c,'二维列表共享陷阱',r'''bad = [[0] * 2] * 2
bad[0][0] = 9
print(bad)
good = []
for _ in range(2):
    good.append([0] * 2)
good[0][0] = 9
print(good)''',r'''[[9, 0], [9, 0]]
[[9, 0], [0, 0]]''','重复的是内层对象的引用，不是重新创建两行。循环每轮产生新列表，因此 good 的两行彼此独立。下划线表示这个循环值本身不重要。','把网格变成 3 行 4 列，只修改最后一格。')
example(c,'元组与解包',r'''point = (3, 4)
x, y = point
print(x, y)
print(type((3,)).__name__)
print(type((3)).__name__)''',r'''3 4
tuple
int''','逗号建立元组结构。解包按位置赋值，变量个数与元素个数不匹配会报错。','尝试 a, b, c = point，读懂错误后恢复。')
exercise(c,'保留合格成绩','场景','从 [30, 60, 85, 59] 中生成新列表 [60, 85]，并输出。不要修改遍历中的原列表。','建立空列表，满足条件就 append。',r'''passed = []
for score in [30, 60, 85, 59]:
    if score >= 60:
        passed.append(score)
print(passed)''','[60, 85]','筛选模式保留原顺序，也避开边遍历边删除导致的跳项。')
exercise(c,'最高三个分数','场景','scores = [70, 95, 80, 60, 90]，输出降序前三名 [95, 90, 80]，再输出原列表。','sorted 返回新列表，然后 [:3]。',r'''scores = [70, 95, 80, 60, 90]
print(sorted(scores, reverse=True)[:3])
print(scores)''',r'''[95, 90, 80]
[70, 95, 80, 60, 90]''','两步分别做排序和取前缀。若不足三项，切片返回全部已有项，不会越界。')
exercise(c,'修复复制错误','纠错','a = [1,2]，复制给 b 后给 b 加入 3。要求输出 a 为 [1, 2]，b 为 [1, 2, 3]。','用 copy，而不是仅赋值。',r'''a = [1, 2]
b = a.copy()
b.append(3)
print(a)
print(b)''',r'''[1, 2]
[1, 2, 3]''','此题元素是不可变整数，浅拷贝足够。嵌套可变元素需要进一步考虑共享关系。')
exercise(c,'移动末尾任务','迁移','tasks = ["A", "B", "C"]，把最后一个移动到最前，输出 ["C", "A", "B"] 对应的 Python 列表表示。','pop 返回被删项，再 insert 到索引 0。',r'''tasks = ["A", "B", "C"]
last = tasks.pop()
tasks.insert(0, last)
print(tasks)''',"['C', 'A', 'B']",'题目默认列表非空。空列表调用 pop 会失败，真实函数可先判断 tasks。')
exercise(c,'二维求和','迁移','grid = [[1,2,3],[4,5,6]]，输出所有数字的总和 21。','外层取一行，内层取该行的一个数。',r'''grid = [[1, 2, 3], [4, 5, 6]]
total = 0
for row in grid:
    for value in row:
        total += value
print(total)''','21','len(grid) 是 2，不是 6。两层循环逐个访问叶子数值。')
exercise(c,'按顺序去重','挑战','对 ["a","b","a","c","b"] 去重并保留首次出现顺序，输出 ["a","b","c"] 的列表表示。','若元素不在结果列表中，再 append。',r'''unique = []
for item in ["a", "b", "a", "c", "b"]:
    if item not in unique:
        unique.append(item)
print(unique)''',"['a', 'b', 'c']",'本章用列表即可表达算法。大数据中反复做列表成员判断会较慢，第 08 章可增加 seen 集合提升通常的查找效率。')

c = chapter(8, '字典 集合与嵌套数据', '从一串数，走向现实中的一条条记录。',
['用键组织有名字的字段','用字典做计数和分组','选择合适容器并处理嵌套结构'], r'''
### 字典是键到值的映射
`student = {"name": "小林", "score": 85}` 用字段名取值：`student["score"]`。键必须可哈希，常见字符串和整数可以作为键，列表不行。相同键只能保存一个当前值，再赋值会覆盖旧值。

`student["city"]` 在键不存在时抛 KeyError；`student.get("city", "未知")` 返回默认值但不把它写入字典。判断键是否存在可以用 `"city" in student`，字典上的 in 默认检查键，不检查值。

### 遍历方式要明确
`for key in data` 遍历键，`data.values()` 提供值，`data.items()` 提供键值对。常用 `for key, value in data.items():`。现代 Python 字典保留插入顺序，但这不代表按键的大小排序；需要排序就显式调用 sorted。

不要遍历字典时添加或删除键。可以先生成要删除的键列表，再进行删除；或创建新字典。只更新已有键的值是另一回事，但初学仍建议保持流程清楚。

### 计数的核心公式
`counts[word] = counts.get(word, 0) + 1` 的意思：先读旧次数，没有就视作 0，再加 1，最后写回。get 本身不负责更新。这种“读旧值 → 计算 → 写回”的模式与变量累计相同，只是状态按键分开保存。

### 一条记录与多条记录
字典表示一个学生，字典列表表示多个学生：`[{"name":"A","score":80}, ...]`。先用 for 取一个 record，再用 record["score"] 取该记录字段。不要对整个 records 直接写 records["score"]，外层是列表，索引需要整数或切片。

面对复杂结构，先逐层问 type 和 len，再用一个很小的数据例子。很多所谓“AI 数据问题”本质是把列表、字典、字符串层次搞错。

### 集合用于去重和成员判断
`set([1,1,2])` 得到只含 1 与 2 的集合。空集合写 `set()`，`{}` 是空字典。集合元素也需要可哈希；集合不提供索引，迭代顺序不作为程序结果约定。想稳定展示可排序元素，用 sorted。

交集 `a & b` 是两边都有；并集 `a | b` 是任一边有；差集 `a - b` 是只在 a；对称差 `a ^ b` 是只在一边。set 去重不保留你想要的原列表顺序；保序去重可组合 seen 集合与结果列表。

### 怎样选容器
| 需求 | 优先考虑 | 原因 |
|---|---|---|
| 有顺序、可增删的一组数据 | list | 按位置遍历和修改 |
| 固定结构的一组值 | tuple | 明确槽位结构且槽位不可改 |
| 字段名到字段值、词到次数 | dict | 通过键访问 |
| 唯一元素、快速成员判断 | set | 去重与集合运算 |

不要为了显得高级强行选择复杂结构。先画出一条数据，再决定“一条用什么、多条用什么”。
''', ['一条记录用字典，多条记录常用列表套字典。','get 读默认值，赋值才写回。','集合无索引，稳定展示先 sorted。'],
['我能从学生记录列表中提取所有及格者姓名。','我能从零写一个词频统计循环。','我能解释 {} 和 set() 的区别。'])
example(c,'读取与默认值',r'''student = {"name": "小林", "score": 85}
student["score"] = 90
print(student["name"], student["score"])
print(student.get("city", "未知"))
print("city" in student)''',r'''小林 90
未知
False''','get 返回默认值没有修改字典，所以最后仍为 False。','使用 student["city"] 读取，观察 KeyError。')
example(c,'词频统计',r'''counts = {}
for word in "python is fun python is useful".split():
    counts[word] = counts.get(word, 0) + 1
for word, count in counts.items():
    print(word, count)''',r'''python 2
is 2
fun 1
useful 1''','每个词有独立计数器。插入顺序是首次见到这些词的顺序。','加上大小写和逗号，分析当前清洗规则还缺什么。')
example(c,'记录列表',r'''students = [
    {"name": "A", "score": 55},
    {"name": "B", "score": 80},
]
for student in students:
    if student["score"] >= 60:
        print(student["name"])''','B','外层先取字典，内层再按键取字段。列表与字典各自承担一层组织任务。','给每条记录添加 city，再筛选城市与分数双条件。')
example(c,'集合关系',r'''train_ids = {1, 2, 3}
test_ids = {3, 4}
print(sorted(train_ids & test_ids))
print(sorted(train_ids | test_ids))
print(sorted(train_ids - test_ids))''',r'''[3]
[1, 2, 3, 4]
[1, 2]''','交集发现 ID 3 重复出现在两组数据中。用于训练测试分离时，ID 检查只是第一层，还需考虑同源内容或同一用户泄漏。','让两组完全无交集，观察空交集的输出。')
example(c,'按类别累计',r'''records = [("书", 30), ("餐饮", 20), ("书", 50)]
totals = {}
for category, amount in records:
    totals[category] = totals.get(category, 0) + amount
print(totals)''',"{'书': 80, '餐饮': 20}",'先按类别找到对应累计值，再加本次金额。计数和金额累计只在“加 1 还是加 amount”上不同。','改成按类别统计笔数。')
example(c,'保序去重与 seen',r'''seen = set()
unique = []
for word in ["a", "b", "a", "c"]:
    if word not in seen:
        seen.add(word)
        unique.append(word)
print(unique)''',"['a', 'b', 'c']",'seen 用于判断见没见过，unique 用于保存顺序。两个结构服务不同需求；不要直接输出集合当成有序结果。','解释为什么 seen.add 后仍需要 unique.append。')
exercise(c,'库存更新','基础','stock = {"apple":3,"pear":2}，苹果补货 5 个，新增 banana 4 个，输出 stock 的 Python 表示。','已有键重新赋值，新键直接赋值。',r'''stock = {"apple": 3, "pear": 2}
stock["apple"] += 5
stock["banana"] = 4
print(stock)''',"{'apple': 8, 'pear': 2, 'banana': 4}",'+= 在这里先取出整数再加回；字典的键顺序由首次插入决定。')
exercise(c,'字母次数','场景','统计 banana 每个字母出现次数，输出字典 {"b":1,"a":3,"n":2} 对应的 Python 表示。','遍历字符串，每个字符作为键。',r'''counts = {}
for char in "banana":
    counts[char] = counts.get(char, 0) + 1
print(counts)''',"{'b': 1, 'a': 3, 'n': 2}",'首次出现按 0 起步，后续读取已有次数。插入顺序 b、a、n 与出现次数大小无关。')
exercise(c,'读取可选配置','基础','config = {"batch_size":16}。读取缺失的 epochs，默认 3，输出 3；再输出字典，证明没有新增键。','get 的第二个参数是默认值。',r'''config = {"batch_size": 16}
print(config.get("epochs", 3))
print(config)''',r'''3
{'batch_size': 16}''','默认值只是本次读取结果。如果要存入字典，需要显式赋值或学习 setdefault。')
exercise(c,'检测重复 ID','场景','ids = ["s1","s2","s1","s3"]。若有重复输出 True，否则 False。','比较原列表长度与集合长度。',r'''ids = ["s1", "s2", "s1", "s3"]
print(len(ids) != len(set(ids)))''','True','集合合并重复元素，长度变小意味着至少有一个重复。此方法只回答有没有，不能列出具体重复项及次数。')
exercise(c,'两班共同选课','场景','a={"python","math"}，b={"python","english"}，输出共同课程的排序列表 ["python"]。','求交集后 sorted。',r'''a = {"python", "math"}
b = {"python", "english"}
print(sorted(a & b))''',"['python']",'排序是为了稳定展示，不是集合本身有顺序。')
exercise(c,'按城市分组','挑战','记录 [{"name":"A","city":"台北"},{"name":"B","city":"高雄"},{"name":"C","city":"台北"}]，构建城市到姓名列表的字典并输出。','遇到新城市先创建空列表，再 append。',r'''records = [
    {"name": "A", "city": "台北"},
    {"name": "B", "city": "高雄"},
    {"name": "C", "city": "台北"},
]
groups = {}
for record in records:
    city = record["city"]
    if city not in groups:
        groups[city] = []
    groups[city].append(record["name"])
print(groups)''',"{'台北': ['A', 'C'], '高雄': ['B']}",'每个新城市得到自己独立的列表。不要把同一个预建列表反复赋给多个城市，否则它们会共享内容。')

c = chapter(9, '函数 参数 返回值与作用域', '把会重复的处理步骤变成能独立检查的小工具。',
['定义并调用函数，写清输入输出约定','区分 print、return 和 None','理解作用域、参数传递与默认参数陷阱'], r'''
### 为什么需要函数
同一段“清洗文本、计算平均分、检查范围”的代码如果复制三次，改规则时就要改三处。函数把一个明确任务装进有名字的代码块，调用时传入数据，再得到结果。好函数名通常是动词，例如 clean_text、calculate_total。

基本形式是 `def 函数名(参数):`，缩进部分叫函数体。def 执行时创建函数，并不立即跑函数体；写 `函数名(实际值)` 才是调用。形参是定义中的名字，实参是调用时传入的值。例如 `def double(number)` 里的 number 是形参，`double(5)` 里的 5 是实参。

### 从调用到返回的四步
看到 `answer = add(2, 3)`：先求实参得到 2 和 3；进入函数，把它们分别绑定给 a 和 b；执行函数体并求出 5；return 把 5 交回调用位置，最后 answer 绑定 5。把函数调用想成表达式中的一个可求值步骤，而不只是“跳到另一段代码”。

### print 与 return 必须分清
print 把内容显示到屏幕，便于人看；return 把对象交还给调用者，便于后续程序继续使用。一个只 print 没有 return 的函数，调用结果默认是 None。`print(add(2, 3))` 先由 add 返回值，再让 print 显示它。

执行 return 后，当前函数立即结束，后面的函数体语句不执行。所有需要结果的路径都应有明确返回，否则有些输入会意外得到 None。返回多个值时常用 `return total, count`，实际返回的是一个元组，调用者可以解包。

### 参数的几种写法
位置参数按顺序对应；关键字参数按名字对应。`power(3, exponent=2)` 更容易看出第二项含义。`def power(base, exponent=2)` 给了默认值，调用者可以省略 exponent。普通调用中位置参数放在关键字参数前面，避免给同一个参数赋值两次。

默认值在函数定义时求值，不是每次调用重新创建。不要使用 `items=[]` 作为想要“每次一个新列表”的默认值，改为 `items=None`，进入后 `if items is None: items=[]`。这个检查必须用 is None，不能简单 if not items，否则调用者传入的空列表也会被替换。

### 作用域决定去哪里找名字
函数内部赋值创建的名字通常是局部变量，外面不能直接使用。函数可以读取外层可见名字，但把所有输入写成参数更容易理解和测试。不要一开始就依赖 global 修改全局变量。

如果函数里给 x 赋值，Python 通常把该函数中的 x 当作局部名字，即使你在赋值之前试图读外部 x，也可能得到 UnboundLocalError。改为传参和返回值，比到处加 global 更清楚。

### 传入列表会不会被修改
函数参数获得的是对象引用的绑定。函数内执行 `items.append(x)` 会修改调用者共享的列表；执行 `items = []` 只改变局部参数的绑定，不会替换调用者的名字。不能简单说“Python 都是值传递”或“所有赋值都修改外部”。要看是否修改了同一个对象。

若希望函数不改输入，可先建立新列表再处理。题目应声明是否允许修改输入，测试也应检查这一点。

### 写函数前的输入输出约定
先用一句话描述职责；列出输入类型、合法范围、返回值；决定空输入怎么办；给出至少三个样例。平均分函数可约定空列表返回 None，也可约定抛 ValueError，两种都可能合理，关键在于调用者知道并处理。不要让约定靠读函数内部猜。

本章开始的部分习题附带额外函数测试。你除了打印展示结果，还要按指定函数名与参数实现功能；自检器会用其他输入调用函数，检查边界和是否修改了输入。
''', ['def 先定义，括号才调用。','print 给人看，return 给程序用。','参数获得对象绑定；修改对象与重新绑定不同。','默认列表用 None 创建，别让多次调用共用一个。'],
['我能让函数返回结果后继续参与乘法。','我能解释为什么显示了 5，外面却收到 None。','我能写一个不修改输入列表的清洗函数并测空输入。'])
example(c,'定义与调用',r'''def add(a, b):
    return a + b

result = add(2, 3)
print(result)
print(add(10, 20) * 2)''',r'''5
60''','第一处先计算 2+3 再给 result。第二处先得到 30，再在调用处乘 2。函数体不依赖特定数字，可用于不同输入。','改写成 subtract(a,b)，说明参数顺序为何重要。')
example(c,'打印不等于返回',r'''def show_double(number):
    print(number * 2)

result = show_double(3)
print(result)''',r'''6
None''','函数先显示 6；没有 return，所以调用表达式的值是 None，第二个 print 显示它。','改成 return number * 2，再由外部显示结果。')
example(c,'提前返回处理空输入',r'''def mean(values):
    if not values:
        return None
    return sum(values) / len(values)

print(mean([80, 100]))
print(mean([]))''',r'''90.0
None''','sum 是内置求和函数。空输入路径提前返回，后面的除法不会执行；调用者必须理解 None 表示没有平均值。','将空输入约定改成抛 ValueError，并在第 13 章练习捕获。')
example(c,'默认参数与关键字',r'''def greet(name, prefix="你好"):
    return f"{prefix}，{name}"

print(greet("小林"))
print(greet(prefix="晚上好", name="小陈"))''',r'''你好，小林
晚上好，小陈''','第一调用省略 prefix，用默认值。第二调用按名字对应，书写次序不影响参数绑定。','调用 greet("小林", name="小陈")，观察重复赋值错误。')
example(c,'作用域与返回',r'''score = 60

def improve(value):
    value = value + 10
    return value

new_score = improve(score)
print(score, new_score)''','60 70','局部 value 重新绑定到 70，不会把外部 score 改成 70。想更新外部名字可显式写 score = improve(score)。','删除 return，观察 new_score。')
example(c,'修改对象与改绑参数',r'''def add_item(items):
    items.append("B")

def replace_items(items):
    items = ["C"]

tasks = ["A"]
add_item(tasks)
replace_items(tasks)
print(tasks)''',"['A', 'B']",'add_item 对共享列表追加 B；replace_items 只把局部 items 改绑到新列表。函数返回后这个局部绑定消失。','让 replace_items 返回新列表，并由外面 tasks = replace_items(tasks)。')
example(c,'默认列表陷阱与修复',r'''def bad_add(value, items=[]):
    items.append(value)
    return items

print(bad_add("A"))
print(bad_add("B"))

def good_add(value, items=None):
    if items is None:
        items = []
    items.append(value)
    return items

print(good_add("A"))
print(good_add("B"))''',r'''['A']
['A', 'B']
['A']
['B']''','bad_add 的默认列表在定义时创建一次，多次调用共享。good_add 在每次省略 items 时创建新列表；若显式传入列表，仍会修改那个列表。','显式传入 items=[]，验证 good_add 保留对该列表的修改。')
example(c,'多个结果与文档字符串',r'''def summarize(values):
    """返回数值列表的总和与项数。"""
    return sum(values), len(values)

total, count = summarize([2, 4, 6])
print(total, count)''','12 3','函数体第一条字符串常作为文档字符串，可用 help(summarize) 查看。return 的逗号把两个值组成元组。','再返回最大值，并为无元素情况写约定。')
exercise(c,'温度转换函数','基础','实现 to_fahrenheit(celsius)，返回摄氏转华氏的值。展示 print(to_fahrenheit(25)) 输出 77.0。','函数负责返回，外面负责显示。',r'''def to_fahrenheit(celsius):
    return celsius * 9 / 5 + 32

print(to_fahrenheit(25))''','77.0','把第 02 章公式放进函数，调用者可以多次使用不同输入。',tests=r'''assert to_fahrenheit(0) == 32
assert to_fahrenheit(-40) == -40
assert to_fahrenheit(100) == 212''')
exercise(c,'安全平均值','场景','实现 mean(values)，非空返回平均值，空列表返回 None，不修改输入。依次打印 mean([60,90]) 与 mean([])。','先检查空，再除以长度。',r'''def mean(values):
    if not values:
        return None
    return sum(values) / len(values)

print(mean([60, 90]))
print(mean([]))''',r'''75.0
None''','空平均没有本题定义下的数值。用 None 表达缺失，而非用 0 冒充。',tests=r'''assert mean([]) is None
assert mean([0]) == 0
assert mean([-2, 2]) == 0
values = [1, 3]
assert mean(values) == 2
assert values == [1, 3]''')
exercise(c,'限制范围','迁移','实现 clamp(value, low, high)，假定 low<=high：低于 low 返回 low，高于 high 返回 high，否则原样返回。打印 clamp(120,0,100)。','依次判断上下界。',r'''def clamp(value, low, high):
    if value < low:
        return low
    if value > high:
        return high
    return value

print(clamp(120, 0, 100))''','100','最后 return 覆盖区间内部与两个端点。别漏掉“都不越界”这条路径。',tests=r'''assert clamp(-1, 0, 100) == 0
assert clamp(0, 0, 100) == 0
assert clamp(100, 0, 100) == 100
assert clamp(42, 0, 100) == 42''')
exercise(c,'清洗一组姓名','场景','实现 clean_names(names)，去每项两端空白，丢弃空结果，保留其余顺序且不修改输入。打印对 [" A ","  ","B"] 的结果。','每轮先 strip，再判断 clean 是否非空。',r'''def clean_names(names):
    result = []
    for name in names:
        clean = name.strip()
        if clean:
            result.append(clean)
    return result

print(clean_names([" A ", "  ", "B"]))''',"['A', 'B']",'结果建立在新列表中。空白字符串经 strip 变空后再过滤，否则会保留无内容项。',tests=r'''assert clean_names([]) == []
assert clean_names(["  ", "\n"]) == []
original = [" C ", "D"]
assert clean_names(original) == ["C", "D"]
assert original == [" C ", "D"]''')
exercise(c,'统计通过率','挑战','实现 pass_rate(scores, threshold=60)，返回通过人数/总人数，空列表返回 None。打印 pass_rate([50,60,90])，用 .1% 显示为 66.7%。','把计数和平均逻辑结合；结果是 0 到 1 的比例。',r'''def pass_rate(scores, threshold=60):
    if not scores:
        return None
    count = 0
    for score in scores:
        if score >= threshold:
            count += 1
    return count / len(scores)

print(f"{pass_rate([50, 60, 90]):.1%}")''','66.7%','threshold 可以通过关键字修改。显示百分比放在外部，函数返回数值便于后续运算。',tests=r'''assert pass_rate([]) is None
assert pass_rate([60]) == 1
assert pass_rate([59]) == 0
assert pass_rate([70, 80], threshold=80) == 0.5''')
exercise(c,'无共享默认值','纠错','实现 append_new(value, items=None)，未传 items 时每次建立独立列表；传入列表时追加到该列表。依次打印 append_new("A") 与 append_new("B")。','必须检查 is None。',r'''def append_new(value, items=None):
    if items is None:
        items = []
    items.append(value)
    return items

print(append_new("A"))
print(append_new("B"))''',r'''['A']
['B']''','默认值只用不可变的 None 作标记。显式提供空列表时仍保留该对象，因此测试也检查对象身份。',tests=r'''a = append_new(1)
b = append_new(2)
assert a == [1] and b == [2]
assert a is not b
items = []
assert append_new(3, items) is items
assert items == [3]''')

c = chapter(10, '推导式 排序与常见组合', '先会写清楚的循环，再读懂更紧凑的写法。',
['将简单循环转成推导式','用 key 指定排序依据','使用 enumerate、zip、any 与 all'], r'''
### 列表推导式按“结果 遍历 条件”读
`[x * x for x in numbers if x > 0]`：遍历 numbers；只保留大于 0 的 x；对每个保留项计算 x*x；收集到新列表。写法里结果在前，执行时仍先从遍历中拿到 x。

初学先展开成四行：result=[]；for；if；append。展开后理解了再缩写。列表推导式会一次生成完整列表；并非更省内存。多个嵌套 for 可以表达展开矩阵，但可读性差时普通循环更好。

### 两种 if 写法的区别
`[x for x in nums if x > 0]` 是筛选，会减少元素数量；`[x if x > 0 else 0 for x in nums]` 是逐项选择结果，每个输入都有一个输出。前者的 if 在 for 后；后者的 if/else 属于前面的结果表达式。

字典推导式如 `{word: len(word) for word in words}`；集合推导式如 `{word.lower() for word in words}`。字典若产生重复键，后面的值覆盖前面。

### 排序的 key 是“拿什么来比”
`sorted(records, key=...)` 默认会用 key 返回的值排序。可以先定义普通函数 `def get_score(record): return record["score"]`。`lambda record: record["score"]` 是只含一个表达式的小函数，不是必须掌握的炫技写法。

多条件排序可返回元组，例如 `key=lambda r: (-r["score"], r["name"])` 表示分数降序，同分姓名升序。先比较第一项，相同再看第二项。Python 排序是稳定的，键相等时保留输入相对顺序。

### zip 把多个序列并排配对
`zip(names, scores)` 每次给一个姓名和一个分数。默认遇到较短序列结束，较长序列余下元素会被忽略。需要一一对应时，先检查长度，或在本教材支持的 Python 3.10+ 中使用 `zip(..., strict=True)`，不等长会报 ValueError。

enumerate 给单个序列配索引；zip 把多个序列配成行。zip 和 enumerate 返回可迭代工具对象，要观察所有结果可 list(...)，但遍历时不必先转列表。

### any 与 all
`any(条件序列)` 问是否至少一个为真；`all(条件序列)` 问是否全部为真。空输入时 any 返回 False，all 返回 True。这是逻辑约定，不能用 all([]) 推断“有数据而且合格”，业务上还要检查非空。

### 先保证正确，再追求简洁
一行代码不一定更容易维护。清洗文本、解析数字、记录错误同时发生时，普通 for 更清楚。函数职责明确、变量名直白、测试覆盖边界，通常比把所有代码缩成一行重要。
''', ['推导式先拿元素，再过滤，再计算结果。','key 返回比较依据，不是返回排序后的对象。','zip 默认以短的为准；严格对应要检查。'],
['我能把一个推导式展开成普通 for。','我能给记录按分数和姓名排序。','我能解释 zip 不等长时发生什么。'])
example(c,'循环与推导式等价',r'''numbers = [-2, 0, 3, 4]
result = []
for number in numbers:
    if number > 0:
        result.append(number ** 2)
print(result)
print([number ** 2 for number in numbers if number > 0])''',r'''[9, 16]
[9, 16]''','两种写法都先筛正数，再平方。不是对所有数平方后再筛正数，否则 -2 也会留下。','写一个只保留长度至少 3 的单词的推导式。')
example(c,'过滤与替换',r'''numbers = [-2, 0, 3]
print([x for x in numbers if x > 0])
print([x if x > 0 else 0 for x in numbers])''',r'''[3]
[0, 0, 3]''','第一行长度变为 1；第二行长度仍为 3，负数与零都按规则映射到 0。','把替换值改成 None，说明缺失标记和数值零的区别。')
example(c,'按记录字段排序',r'''records = [
    {"name": "B", "score": 90},
    {"name": "A", "score": 90},
    {"name": "C", "score": 80},
]
ordered = sorted(records, key=lambda row: (-row["score"], row["name"]))
print([row["name"] for row in ordered])''',"['A', 'B', 'C']",'分数取负实现第一项降序，姓名保持升序。同为 90 时 A 排在 B 前。','改成分数升序、同分姓名升序。')
example(c,'配对与序号',r'''names = ["A", "B"]
scores = [80, 90]
for index, (name, score) in enumerate(zip(names, scores, strict=True), start=1):
    print(index, name, score)''',r'''1 A 80
2 B 90''','zip 先产生 (name,score) 对，enumerate 再在外面配序号。左侧嵌套解包与右侧结构匹配。','给 scores 多加一个元素，观察 strict 的错误。')
example(c,'全部与至少一个',r'''scores = [50, 80, 90]
print(any(score >= 60 for score in scores))
print(all(score >= 60 for score in scores))
print(any([]), all([]))''',r'''True
False
False True''','这里括号内是生成器表达式，第 15 章详细解释。any 找到真就可停止，all 找到假就可停止。','把 scores 换成空列表，补上非空判断表达“所有已有学生均通过且确实有学生”。')
example(c,'字典推导式',r'''words = ["cat", "python", "AI"]
lengths = {word: len(word) for word in words}
print(lengths)''',"{'cat': 3, 'python': 6, 'AI': 2}",'每个输入生成一个键值对。重复单词会覆盖同一键，因此结果不一定与输入长度相等。','用 lower 生成集合，给重复大小写单词去重。')
exercise(c,'平方正数','基础','实现 positive_squares(values)，返回正数的平方列表，保持顺序；打印对 [-2,0,3] 的结果。','只保留 >0 的元素。',r'''def positive_squares(values):
    return [value ** 2 for value in values if value > 0]

print(positive_squares([-2, 0, 3]))''','[9]','先筛再算；负数的平方虽为正，但原输入不符合条件。',tests=r'''assert positive_squares([]) == []
assert positive_squares([-3, -1]) == []
assert positive_squares([2, 1]) == [4, 1]''')
exercise(c,'单词按长度排序','场景','实现 sort_words(words)，长度升序，同长度字母升序，不改输入。打印对 ["dog","a","cat","python"] 的结果。','key 返回 (len(word), word)。',r'''def sort_words(words):
    return sorted(words, key=lambda word: (len(word), word))

print(sort_words(["dog", "a", "cat", "python"]))''',"['a', 'cat', 'dog', 'python']",'长度先决定分组，字母顺序决定同长词的先后。',tests=r'''assert sort_words([]) == []
assert sort_words(["bb", "aa", "c"]) == ["c", "aa", "bb"]
source = ["zz", "a"]
assert sort_words(source) == ["a", "zz"]
assert source == ["zz", "a"]''')
exercise(c,'负值截为零','迁移','实现 replace_negative(values)，负数变 0，其他数不变。打印对 [-2,0,5] 的结果。','这里是替换，不是过滤。',r'''def replace_negative(values):
    return [0 if value < 0 else value for value in values]

print(replace_negative([-2, 0, 5]))''','[0, 0, 5]','输入输出长度相等。筛掉负数会改变位置对应关系，可能损坏样本与标签的配对。',tests=r'''assert replace_negative([]) == []
assert replace_negative([-1, -2]) == [0, 0]
assert replace_negative([3]) == [3]''')
exercise(c,'建立姓名成绩映射','场景','实现 make_scores(names, scores)，同长度且姓名唯一时返回字典；长度不同抛 ValueError。打印 ["A","B"] 与 [80,90] 的结果。','zip 使用 strict=True。',r'''def make_scores(names, scores):
    return dict(zip(names, scores, strict=True))

print(make_scores(["A", "B"], [80, 90]))''',"{'A': 80, 'B': 90}",'strict 捕获长度不一致。姓名唯一是本题前提；若重复需要另行确定覆盖、报错或分组的业务规则。',tests=r'''assert make_scores([], []) == {}
assert make_scores(["C"], [0]) == {"C": 0}
try:
    make_scores(["A"], [])
except ValueError:
    pass
else:
    raise AssertionError("长度不同应抛 ValueError")''')
exercise(c,'所有项均有效','推理','实现 all_positive(values)，必须非空且每个数字大于 0 才返回 True。依次打印对 [1,2] 和 [] 的结果。','bool(values) 与 all 组合。',r'''def all_positive(values):
    return bool(values) and all(value > 0 for value in values)

print(all_positive([1, 2]))
print(all_positive([]))''',r'''True
False''','单独 all([]) 是 True，不符合本题业务约定。显式的非空条件解决这一差异。',tests=r'''assert all_positive([]) is False
assert all_positive([0]) is False
assert all_positive([-1, 2]) is False
assert all_positive([1]) is True''')
exercise(c,'展开二维列表','挑战','实现 flatten(rows)，按行展开一层二维列表。打印 [[1,2],[],[3]] 的结果 [1,2,3]。','先 for row，再 for value in row。',r'''def flatten(rows):
    return [value for row in rows for value in row]

print(flatten([[1, 2], [], [3]]))''','[1, 2, 3]','多个 for 的顺序与普通嵌套循环一致。此函数只展开一层，不递归展开任意深度结构。',tests=r'''assert flatten([]) == []
assert flatten([[], []]) == []
assert flatten([[0], [1, 2]]) == [0, 1, 2]''')

c = chapter(11, '模块 标准库与环境', '学会组织自己的代码，也能读懂别人项目的启动方式。',
['理解 import 和模块边界','会使用常见标准库','知道解释器、pip 与虚拟环境的对应关系'], r'''
### 模块就是组织代码的文件
一个 `.py` 文件可以作为模块。`import math` 导入模块，然后 `math.sqrt(9)` 使用其中的函数。`from math import sqrt` 直接导入名字，调用时写 sqrt(9)。前者来源清晰，后者更短；避免 `from module import *`，它会让名字来源难以追踪。

Python 首次导入模块时会执行模块顶层代码，然后通常缓存模块。因此不要在工具模块顶层直接开启交互输入、训练过程或大量文件写入。函数定义放顶层可以，真正运行的入口放在 main 保护下。

### 入口保护是什么意思
`if __name__ == "__main__":` 判断这个文件是否作为入口直接运行。如果直接 `python app.py`，条件为真；如果另一个文件 `import app`，条件通常为假。常见结构是定义 main()，然后在这条 if 中调用 main()。

这让同一个文件既可直接运行，也可被测试或其他文件导入复用。入口保护不是防止别人使用代码的安全机制，它只是运行方式判断。

### 两个文件怎样合作
建立同一文件夹中的 `helpers.py`，定义 `def double(x): return x*2`；另一个 `main.py` 写 `from helpers import double`，再调用它。从该文件夹启动 main.py。不要把你的文件命名为 `random.py`、`json.py`、`csv.py` 或 `math.py`，否则可能遮住标准库并造成看起来奇怪的导入错误。

模块搜索与解释器路径有关。发生 ModuleNotFoundError 时，先检查名称、当前使用的解释器和项目结构，不要反复随机安装。`import sys; print(sys.executable)` 可显示当前解释器路径。

### 标准库与第三方包
标准库随正常的 Python 安装提供，例如 math、random、pathlib、json、csv、collections、datetime、statistics、unittest。第三方包需要额外安装，例如 NumPy 和 PyTorch。本教材第一阶段只用标准库，你无需联网安装这些库才能完成作业。

`pip` 是安装 Python 包的工具。优先 `python -m pip ...`，意思是让“这个 Python”运行 pip，减少包装到另一个解释器里的问题。包名和导入名不一定相同，要看包的官方文档。

### 虚拟环境为什么有用
不同项目可能需要不同版本依赖。venv 为每个项目建立独立的解释器入口和包目录。它不是虚拟机，也不需要给每个练习建一个环境；整个学习包用一个即可。第一阶段没有第三方包，虚拟环境是操作练习，不是运行基础示例的硬性条件。

在学习包根目录打开终端，Windows 执行：

```terminal
py -m venv .venv
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\python.exe examples/ch01/ex01_01.py
.\.venv\Scripts\python.exe -m pip --version
```

Mac 执行：

```terminal
python3 -m venv .venv
./.venv/bin/python --version
./.venv/bin/python examples/ch01/ex01_01.py
./.venv/bin/python -m pip --version
```

上面使用精确路径，无需先激活。可选激活方式：Windows PowerShell 为 `.\.venv\Scripts\Activate.ps1`，Mac 为 `source .venv/bin/activate`，激活后可用 `python`，退出用 `deactivate`。若 PowerShell 阻止激活脚本，直接使用上面的解释器完整路径即可，不必为了课程放宽系统执行策略。

换电脑时复制源代码和依赖清单，**重新创建 .venv，不要搬运旧 .venv**。不同操作系统路径和二进制依赖不通用。后续有第三方依赖时，可在旧环境用 `python -m pip freeze > requirements.txt` 保存安装快照，在新环境用 `python -m pip install -r requirements.txt` 安装；跨系统或新版本仍可能需要调整。当前教材无需安装第三方依赖。

### 随机数与实验记录
`random.Random(42)` 建立局部随机数生成器，可帮助在相同环境与调用顺序下复现实验。不要把固定 seed 理解为跨所有库、硬件、版本的绝对一致保证。后续学习 PyTorch 时还需要记录版本、硬件和确定性设置。

环境操作依据 [Python Packaging 官方指南](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/)；具体安装选项变化时请以官方页面为准。
''', ['import 找工具，模块名避免撞上标准库。','入口保护让文件可运行也可导入。','用哪个 Python，就用哪个 Python -m pip。','换电脑重建环境，源代码和数据一起带走。'],
['我能解释 import 为什么可能执行顶层语句。','我能创建虚拟环境并用其中解释器运行文件。','我能定位当前解释器，而不是只看编辑器按钮。'])
example(c,'数学工具',r'''import math
print(math.sqrt(81))
print(math.ceil(2.1))
print(math.floor(-2.1))
print(math.isclose(0.1 + 0.2, 0.3))''',r'''9.0
3
-3
True''','ceil 向上取整，floor 向下取整，isclose 判断浮点近似相等。金融等精确十进制需求还需更合适的数据表示。','预测 floor(2.9) 与 ceil(-2.9)。')
example(c,'Counter 计数',r'''from collections import Counter
counts = Counter("a b a c b a".split())
print(counts["a"])
print(counts["missing"])
print(counts.most_common(2))''',r'''3
0
[('a', 3), ('b', 2)]''','Counter 封装了第 08 章的常见计数逻辑。先理解手写版本，再用标准库减少重复。','用 Counter 统计一段英文文本，先统一大小写。')
example(c,'日期间隔',r'''from datetime import date
start = date(2026, 1, 1)
end = date(2026, 1, 8)
print((end - start).days)''','7','这里使用固定日期而非“今天”，确保你在不同日期运行也得到相同输出。结果表示间隔天数，不把两端各算一次。','计算同一天之间的间隔。')
example(c,'局部随机性',r'''import random
first = random.Random(42)
second = random.Random(42)
a = [first.random() for _ in range(3)]
b = [second.random() for _ in range(3)]
print(a == b)
print(all(0 <= value < 1 for value in a))''',r'''True
True''','两个生成器在当前环境里使用相同 seed 和调用序列，得到一致序列。random() 返回 [0,1) 的值。','只让一个生成器先多调用一次，观察序列是否仍相同。')
example(c,'可导入的入口',r'''def double(value):
    return value * 2

def main():
    print(double(5))

if __name__ == "__main__":
    main()''','10','直接运行时 main 被调用；导入时只定义函数，不执行 main。综合项目都会使用这个结构。','在同目录新建文件导入这个示例模块并调用 double。')
exercise(c,'均值与中位数','场景','用 statistics 模块计算 [1,2,100] 的 mean 和 median，分别输出并把均值格式化为两位小数。','中位数是排序后的中间值，不等于平均值。',r'''import statistics
values = [1, 2, 100]
print(f"{statistics.mean(values):.2f}")
print(statistics.median(values))''',r'''34.33
2''','异常大值显著影响均值，中位数在这里仍为 2。这里只练库函数，不作完整统计推断。')
exercise(c,'词频最多者','基础','用 Counter 统计 "red blue red green red blue"，输出 most_common(1) 的结果。','先 split。',r'''from collections import Counter
counts = Counter("red blue red green red blue".split())
print(counts.most_common(1))''',"[('red', 3)]",'most_common 返回列表，其中元素是词和次数组成的元组，即使只取一个也是列表。')
exercise(c,'向上取整批次数','迁移','23 条数据，每批最多 8 条，用 math.ceil 输出需要几批：3。','先做除法再向上取整。',r'''import math
print(math.ceil(23 / 8))''','3','前两批各 8 条，最后 7 条。对大整数计数可优先使用整数公式避免浮点精度问题。')
exercise(c,'十进制精确相加','拓展','用 decimal.Decimal 从字符串构造 0.1 和 0.2，相加并输出 0.3。','从字符串构造，而非先构造二进制 float。',r'''from decimal import Decimal
print(Decimal("0.1") + Decimal("0.2"))''','0.3','Decimal(0.1) 会带入浮点近似值。先从精确文本表示构造，才符合此例目的。')
exercise(c,'复现实验打乱','场景','列表 range(5)，分别复制两份并用两个 random.Random(7) 打乱，输出两份是否相同 True，再输出原列表。','shuffle 原地修改，所以先 copy。',r'''import random
original = list(range(5))
a = original.copy()
b = original.copy()
random.Random(7).shuffle(a)
random.Random(7).shuffle(b)
print(a == b)
print(original)''',r'''True
[0, 1, 2, 3, 4]''','不要写 a = rng.shuffle(a)，shuffle 返回 None。复制保护原始顺序。')

c = chapter(12, '路径 文件 CSV 与 JSON', '让程序的结果在关闭窗口后仍然存在。',
['理解工作目录与脚本目录','用 with 安全读写 UTF-8 文本','选择 CSV、JSON、JSONL 表示结构化数据'], r'''
### 相对路径相对于哪里
`Path("data.txt")` 默认相对于**当前工作目录**，不一定是代码文件所在目录。你从不同目录启动脚本，可能读到不同地方。终端先 cd 到学习包根目录可以减少混乱。

需要固定相对脚本位置时用 `BASE = Path(__file__).resolve().parent`，再写 `BASE / "data" / "scores.csv"`。`__file__` 通常在脚本中存在，但交互窗口和某些 notebook 环境中没有。Path 的 `/` 在这里是拼接路径，不是数值除法；它会按操作系统处理分隔符。

### 文本读写与覆盖
`path.read_text(encoding="utf-8")` 返回整个文件字符串；`path.write_text(text, encoding="utf-8")` 写入文本，**已有同名文件会被覆盖**。父目录不存在时先 `mkdir(parents=True, exist_ok=True)`。本章示例将演示文件写入当前工作目录下的 `outputs/`，可反复运行并覆盖这些专用示例文件；不要替换成你自己的重要文件路径。

用 `with path.open("r", encoding="utf-8") as file:` 打开文件，离开 with 块后自动关闭。`"r"` 读取，`"w"` 覆盖写，`"a"` 追加，`"x"` 只在文件不存在时新建。二进制模式如 rb 面向字节，本阶段先专注文本。

### 一行一行处理
`for line in file` 可以逐行处理，避免一次把大文件读进内存。line 通常保留行末换行符。若只想去掉行末换行，用 rstrip("\n")；strip() 会连两端其他空白一起删除，是否合适取决于数据。`splitlines()` 把完整字符串拆成行，适合小文件。

### CSV 是表格，不是随便按逗号拆
CSV 一行一条记录，通常第一行是列名。字段里可能包含逗号、引号甚至换行，所以使用 csv.DictReader / DictWriter。打开 CSV 时加 `newline=""`，让 csv 模块正确处理换行。

CSV 读取的字段默认是字符串，"80" 要 int 后才能计算。不要把表头拼错或空字符串当成正常分数；第 13 章学习识别与记录错误。Excel 导出的文件可能含 BOM，可尝试 `encoding="utf-8-sig"` 读取 UTF-8 BOM 文件，不要对所有编码问题盲目使用 errors="ignore"。

### JSON 保存嵌套结构
JSON 能表示对象、数组、字符串、数字、布尔值和 null。读入 Python 后对应 dict、list、str、int/float、bool、None。JSON 文本里是 true/false/null，Python 源码里是 True/False/None。JSON 要求对象键为字符串；集合等类型不能直接序列化。

`json.dumps(obj)` 返回 JSON 字符串，`json.loads(text)` 把字符串解析为对象。`json.dump(obj,file)` 和 `json.load(file)` 面向文件对象。`ensure_ascii=False` 保留中文便于阅读，`indent=2` 让缩进清晰。数据不合法时会报 JSONDecodeError；不要使用 eval 读取 JSON。

### JSONL 是每行一个 JSON 对象
每行独立解析，适合逐条流式处理记录。空行怎么处理、坏行是跳过还是终止，都要制定约定。AI 数据集常见这种格式；文本中的换行应由 JSON 转义，而不是直接破坏一行一条记录的结构。

### 跨电脑可靠性
使用 UTF-8、pathlib、明确的相对脚本路径，避免硬编码 `C:\Users\你的名字` 或 `/Users/你的名字`。把数据和代码一起打包。文件写出后读回来核对条数和关键字段，比“没有报错”更有说服力。
''', ['工作目录不等于脚本目录；固定位置用 __file__。','w 会覆盖，a 会追加，x 防止覆盖。','CSV 字段通常是 str；JSON 可保存嵌套结构。','小文件整体读，大文件逐行读。'],
['我能从任意工作目录运行一个用脚本目录定位数据的程序。','我能将记录写入 JSON 再读回验证。','我能解释为什么 CSV 不能总是直接 split(",")。'])
example(c,'写入与读回文本',r'''from pathlib import Path
folder = Path("outputs")
folder.mkdir(exist_ok=True)
path = folder / "example12_01.txt"
path.write_text("第一天：变量\n第二天：循环\n", encoding="utf-8")
text = path.read_text(encoding="utf-8")
print(text, end="")''',r'''第一天：变量
第二天：循环''','目录先建立，再写固定演示文件。读取结果末尾已有换行，所以 print 用 end="" 避免多一行。','追加第三天内容，再读回确认没有覆盖前两天。')
example(c,'逐行读取与清理',r'''from pathlib import Path
folder = Path("outputs")
folder.mkdir(exist_ok=True)
path = folder / "example12_02.txt"
path.write_text(" Python \n\n AI \n", encoding="utf-8")
with path.open(encoding="utf-8") as file:
    for line in file:
        clean = line.strip()
        if clean:
            print(clean)''',r'''Python
AI''','with 管理文件关闭；for 提供一行；strip 和非空检查完成简单清洗。这是第 16 章文本管道的基础。','保留行内空格，确认 strip 不会删掉中间空格。')
example(c,'CSV 写读转换',r'''import csv
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
print(sum(int(row["score"]) for row in rows))''',r'''str
170''','写时是整数，CSV 文本再读回来是字符串。列名由表头决定。数值转换放在明确处理步骤里。','把名字改成带英文逗号的文本，确认 csv 模块能正确读写。')
example(c,'JSON 往返',r'''import json
config = {"name": "练习", "batch_size": 8, "enabled": True}
text = json.dumps(config, ensure_ascii=False)
restored = json.loads(text)
print(text)
print(restored == config)''',r'''{"name": "练习", "batch_size": 8, "enabled": true}
True''','JSON true 与 Python True 的拼写不同。dumps/loads 在内存字符串间转换，配合 Path 就可以持久化。','加一个 None 字段，观察 JSON 中变成什么。')
example(c,'逐行 JSONL',r'''import json
from pathlib import Path
folder = Path("outputs")
folder.mkdir(exist_ok=True)
path = folder / "example12_05.jsonl"
records = [{"id": 1, "text": "你好"}, {"id": 2, "text": "Python"}]
with path.open("w", encoding="utf-8") as file:
    for record in records:
        file.write(json.dumps(record, ensure_ascii=False) + "\n")
with path.open(encoding="utf-8") as file:
    for line in file:
        record = json.loads(line)
        print(record["id"], record["text"])''',r'''1 你好
2 Python''','每次 dumps 生成一个 JSON 文本，再追加真实换行。读取时每行都是独立 JSON。','让 text 含换行，查看文件中的转义后再读回。')
example(c,'仅解析路径',r'''from pathlib import Path
path = Path("data") / "train.jsonl"
print(path.name)
print(path.stem)
print(path.suffix)''',r'''train.jsonl
train
.jsonl''','name 是最后一部分文件名，stem 去最后一个扩展名，suffix 带点。构造 Path 不会自动创建文件。','尝试 report.final.csv，观察 stem。')
exercise(c,'提取非空行','场景','实现 nonempty_lines(text)，去各行两端空白，丢弃空行。打印对 " A \\n\\n B " 的结果。','先 splitlines，再 strip。',r'''def nonempty_lines(text):
    result = []
    for line in text.splitlines():
        clean = line.strip()
        if clean:
            result.append(clean)
    return result

print(nonempty_lines(" A \n\n B "))''',"['A', 'B']",'函数先只负责文本转换，文件读写留给外部，这样容易独立验证。',tests=r'''assert nonempty_lines("") == []
assert nonempty_lines(" \n\t") == []
assert nonempty_lines("a\r\nb") == ["a", "b"]''')
exercise(c,'配置解析','基础','实现 read_batch_size(text)，解析 JSON 字符串并读取 batch_size，缺失默认 8。打印对 {"name":"demo"} 的结果。假定输入 JSON 对象合法。','json.loads 后 get。',r'''import json

def read_batch_size(text):
    config = json.loads(text)
    return config.get("batch_size", 8)

print(read_batch_size('{"name":"demo"}'))''','8','此题聚焦解析和默认值。真实应用还需要验证 batch_size 是正整数，不能接受任意字段类型。',tests=r'''assert read_batch_size('{}') == 8
assert read_batch_size('{"batch_size":16}') == 16
assert read_batch_size('{"batch_size":1}') == 1''')
exercise(c,'CSV 字符串求和','场景','实现 csv_total(text)，CSV 含 amount 列，内容为整数字符串；返回合计。打印对 "amount\\n10\\n20\\n" 的结果 30。','io.StringIO 可以把内存字符串当文本文件使用。',r'''import csv
import io

def csv_total(text):
    reader = csv.DictReader(io.StringIO(text))
    return sum(int(row["amount"]) for row in reader)

print(csv_total("amount\n10\n20\n"))''','30','StringIO 免去测试中创建实体文件，但 csv 解析规则相同。空数据只有表头时 sum 得到 0。',tests=r'''assert csv_total("amount\n") == 0
assert csv_total("amount\n-2\n5\n") == 3
assert csv_total("amount\n0\n") == 0''')
exercise(c,'JSONL 有效记录','迁移','实现 parse_jsonl(text)，跳过空行，解析其余每行 JSON，返回列表。假定非空行都是合法 JSON。打印两条 {"id":1}、{"id":2} 的结果。','逐行 strip，非空才 loads。',r'''import json

def parse_jsonl(text):
    records = []
    for line in text.splitlines():
        if line.strip():
            records.append(json.loads(line))
    return records

print(parse_jsonl('{"id":1}\n\n{"id":2}\n'))''',"[{'id': 1}, {'id': 2}]",'空行不是合法 JSON，所以应先按约定跳过。坏行处理会在下一章增加。',tests=r'''assert parse_jsonl("") == []
assert parse_jsonl(" \n") == []
assert parse_jsonl('{"text":"你好"}\n') == [{"text":"你好"}]''')
exercise(c,'扩展名清单','基础','实现 suffixes(names)，用 Path.suffix 返回各文件扩展名的列表；打印 ["a.txt","b.tar.gz","README"] 的结果。','suffix 只取最后一个扩展名，没有则为空字符串。',r'''from pathlib import Path

def suffixes(names):
    return [Path(name).suffix for name in names]

print(suffixes(["a.txt", "b.tar.gz", "README"]))''',"['.txt', '.gz', '']",'要所有扩展名可查看 suffixes 属性；本题只要最后一个。此函数不要求文件实际存在。',tests=r'''assert suffixes([]) == []
assert suffixes(["x.jsonl"]) == [".jsonl"]
assert suffixes(["notes"]) == [""]''')

c = chapter(13, '错误 调试与验证', '报错是定位线索，能解释错误比只会复制正确代码更有价值。',
['按顺序阅读 traceback','只捕获预期异常并保留诊断信息','用正常、边界和错误输入验证函数'], r'''
### 三种不同的问题
语法错误让代码无法按语法解析，例如少冒号；运行时错误发生在执行到某一步时，例如 int("abc")；逻辑错误可能完全不报错，却给出错误结果，例如平均分除以固定 3 而不是实际人数。第三种尤其需要测试发现。

### 读 traceback 的步骤
先看最后一行的异常类型和消息，再往上找到你自己文件的行号，打开那一行，检查参与操作的变量类型和值。若这个值来自上一步，再追到它的来源。长报错栈不意味着有很多独立错误；它经常是在描述同一个错误的调用路径。

| 异常 | 常见含义 | 首先检查 |
|---|---|---|
| SyntaxError / IndentationError | 语法或缩进不对 | 冒号、括号、引号、缩进 |
| NameError | 名字不存在 | 拼写、是否先赋值 |
| TypeError | 类型或调用方式不匹配 | type、参数数目 |
| ValueError | 类型可用但内容不合法 | int 的输入、范围 |
| IndexError / KeyError | 位置或键不存在 | 长度、键集合 |
| FileNotFoundError | 找不到文件 | 当前目录、路径、是否解压 |
| ModuleNotFoundError | 找不到模块 | 解释器、文件名、环境 |
| ZeroDivisionError | 除数为零 | 空数据、计数初始化 |

### 最小化问题
把大程序缩成还能复现错误的最小例子。打印 `repr(value)` 看不可见字符，打印 type(value) 看字符串还是数字，打印 len(values) 看是否为空。用小数据手算结果，避免一开始在上万条数据里找错。

### try 与 except
把“确实可能失败的一小段”放入 try。`except ValueError as error:` 处理特定错误并获取消息。不要用裸 except 吞掉所有异常，不然 Ctrl+C 等中断也可能被拦截；也不要 `except Exception: pass` 把错误静默丢掉。

多个错误可以分别处理，例如文件不存在与 JSON 格式错误。`else` 可放 try 成功后执行的代码，`finally` 常用于不论成功失败都要执行的清理。文件关闭优先使用 with，减少手写 finally。

### 什么时候主动 raise
输入不符合函数约定时，可以 `raise ValueError("batch_size 必须大于 0")`。清晰消息比后来意外除零好。交互层可以捕获并让用户重试；核心处理函数通常报告错误，让调用者决定如何处理。

### assert 与正式输入校验
`assert actual == expected` 常用在开发和测试中核对内部预期。它失败会抛 AssertionError。不要用 assert 替代处理外部输入的验证，因为 Python 优化模式可能移除 assert；用户输入校验应使用 if 和 raise。

浮点测试用 `math.isclose(actual, expected, rel_tol=..., abs_tol=...)`，容差应由问题精度决定。接近 0 时绝对容差尤其有用。不要不加思考地对所有问题套同一个容差。

### 为一个函数设计测试
以 mean 为例：正常输入 [2,4] →3；单元素 [5] →5；空输入 [] →None；负数 [-2,2] →0；输入不被修改。不要只选“好看的输入”。测试通过说明满足这些检查，不证明对所有可能输入绝对正确。

### 怎样用本教材自检器
先编辑 `practice/ch09/ex09_02.py` 并保存。在学习包根目录执行：

```terminal
python tools/check_practice.py 09_02
python tools/check_practice.py --chapter 09
```

Windows 无虚拟环境时把 python 换成 py；Mac 换成 python3。自检先比较示例输出，再对部分函数题使用其他输入。它只运行学习包中的指定题目文件，不会替你保存编辑器里尚未保存的内容。未完成题显示未通过是正常的。不要用 `--solutions` 代替作答；该选项仅用于核验参考答案。

失败时按报告找到：运行报错、输出不同，或函数额外测试失败。先看题目函数名是否一致、return 是否遗漏、空数据是否处理，再看格式。若靠硬编码示例输出过关，并没有达到学习目的；至少自己再换两个输入。
''', ['先看最后一行，再找自己的代码行号。','抓具体异常，记录原因，不静默吞错。','测试正常、空、边界、错误输入和副作用。'],
['我能区分 SyntaxError、TypeError 和 ValueError。','我能写出一个合法输入和一个非法输入测试。','我能根据自检失败结果定位到自己的实现。'])
example(c,'具体捕获转换错误',r'''texts = ["10", "bad", "20"]
values = []
for text in texts:
    try:
        value = int(text)
    except ValueError:
        print("跳过无效值", repr(text))
    else:
        values.append(value)
print(sum(values))''',r'''跳过无效值 'bad'
30''','只捕获 int 可能产生的 ValueError，失败记录原因；成功才加入数值列表。不要把 int 后所有业务逻辑都塞进一个宽泛 try。','加上空字符串和 "2.5"，观察 int 的规则。')
example(c,'主动验证约定',r'''def divide(total, count):
    if count <= 0:
        raise ValueError("count 必须为正数")
    return total / count

try:
    divide(10, 0)
except ValueError as error:
    print(error)''','count 必须为正数','在执行除法之前验证数据。调用处决定怎样显示错误，核心函数不强行 print。','用 count=-1 与 count=2 测试。')
example(c,'测试浮点结果',r'''import math
result = 0.1 + 0.2
print(result == 0.3)
print(math.isclose(result, 0.3, rel_tol=1e-9, abs_tol=1e-12))''',r'''False
True''','直接相等对二进制浮点近似可能不合适。给出容差后比较数值接近程度。','对 0 与 1e-13 比较，观察 abs_tol 的作用。')
example(c,'小型回归检查',r'''def clamp(value, low, high):
    return min(max(value, low), high)

assert clamp(-1, 0, 10) == 0
assert clamp(5, 0, 10) == 5
assert clamp(11, 0, 10) == 10
print("3 个检查通过")''','3 个检查通过','每个断言对应区间的一种区域。修改函数后再运行这些检查，可以发现旧行为是否被破坏。','补上恰好等于 0 和 10 的检查。')
example(c,'带行号记录坏数据',r'''lines = ["80", "oops", "90"]
for line_number, text in enumerate(lines, start=1):
    try:
        score = int(text)
    except ValueError:
        print(f"第 {line_number} 行不是整数：{text}")
        continue
    if not 0 <= score <= 100:
        print(f"第 {line_number} 行超出范围")
        continue
    print("保留", score)''',r'''保留 80
第 2 行不是整数：oops
保留 90''','语法可解析与业务合法是两层检查。能 int 转换不代表分数一定在 0—100 内。','加一条 120，验证范围检查。')
exercise(c,'容错转整数','基础','实现 parse_int(text)，转换成功返回整数，ValueError 时返回 None。依次打印对 "12" 和 "abc" 的结果。输入约定为字符串。','只捕获 ValueError。',r'''def parse_int(text):
    try:
        return int(text)
    except ValueError:
        return None

print(parse_int("12"))
print(parse_int("abc"))''',r'''12
None''','默认 None 表示解析失败，但 0 是有效返回值；调用者应使用 is None 判断。',tests=r'''assert parse_int("0") == 0
assert parse_int("-2") == -2
assert parse_int(" 5 ") == 5
assert parse_int("2.5") is None''')
exercise(c,'分数合法性','场景','实现 valid_score(text)，字符串可转整数且在 0—100 内返回该整数，否则返回 None。打印对 "101" 和 "60" 的结果。','先转换，再检查范围。',r'''def valid_score(text):
    try:
        value = int(text)
    except ValueError:
        return None
    if not 0 <= value <= 100:
        return None
    return value

print(valid_score("101"))
print(valid_score("60"))''',r'''None
60''','两阶段防止可解析但业务无效的数据进入后续统计。',tests=r'''assert valid_score("0") == 0
assert valid_score("100") == 100
assert valid_score("-1") is None
assert valid_score("oops") is None''')
exercise(c,'正批大小','迁移','实现 batch_count(total, size)，假定 total 为非负整数，size 为整数；size<=0 抛 ValueError，否则向上取整计算批次数。打印 batch_count(17,8)。','先验证 size，再使用整数公式。',r'''def batch_count(total, size):
    if size <= 0:
        raise ValueError("size 必须为正数")
    return (total + size - 1) // size

print(batch_count(17, 8))''','3','明确 total 的输入前提，不把本题测试范围误当作任意类型都能自动处理。',tests=r'''assert batch_count(0, 8) == 0
assert batch_count(16, 8) == 2
for size in [0, -1]:
    try:
        batch_count(10, size)
    except ValueError:
        pass
    else:
        raise AssertionError("size<=0 应抛 ValueError")''')
exercise(c,'保留坏行位置','场景','实现 parse_numbers(lines)，返回 (values, bad_lines)，有效整数字符串进 values，解析失败的 1 起始行号进 bad_lines。打印对 ["1","x","3"] 的结果。','用 enumerate，并分别累计两个列表。',r'''def parse_numbers(lines):
    values = []
    bad_lines = []
    for number, line in enumerate(lines, start=1):
        try:
            values.append(int(line))
        except ValueError:
            bad_lines.append(number)
    return values, bad_lines

print(parse_numbers(["1", "x", "3"]))''','([1, 3], [2])','错误位置也是输出的一部分，用户才能回到原数据修复；不要只说“有错误”。',tests=r'''assert parse_numbers([]) == ([], [])
assert parse_numbers(["x", ""]) == ([], [1, 2])
assert parse_numbers(["0", "-1"]) == ([0, -1], [])''')
exercise(c,'防止空字符串输入','纠错','实现 require_name(text)，strip 后为空则抛 ValueError，否则返回清理后的姓名。打印对 " A " 的结果。','检查的是清理后的字符串。',r'''def require_name(text):
    name = text.strip()
    if not name:
        raise ValueError("姓名不能为空")
    return name

print(require_name(" A "))''','A','仅检查原字符串是否非空会放过全空格；先规范化再验证。',tests=r'''assert require_name("B") == "B"
for text in ["", "  ", "\n"]:
    try:
        require_name(text)
    except ValueError:
        pass
    else:
        raise AssertionError("空姓名应抛 ValueError")''')

c = chapter(14, '类 对象与方法', '为读懂数据集、模型和训练器代码建立基础。',
['区分类与实例','理解 __init__、self 和实例属性','知道何时简单函数已经足够'], r'''
### 先从熟悉对象出发
你已经用过 `names.append(...)` 和 `text.strip()`：数据与可执行操作放在对象上。类定义一类对象的结构与行为，实例是按这个类创建出的具体对象。例如 StudyRecord 是类，“小林今天学了 45 分钟”的记录是一个实例。

不要因为学了类就把所有函数都改写成类。没有持续状态、只做一次输入到输出转换时，普通函数通常足够。多个操作围绕同一份状态协作时，类比较自然。

### __init__ 与 self
`class Counter:` 定义类。`def __init__(self, start=0): self.value = start` 在实例初始化时设置状态。`counter = Counter(3)` 创建实例并初始化为 3；你不手动传 self，Python 的方法调用机制会提供当前实例。

`counter.add(2)` 可理解为让 Counter.add 接收 counter 作为 self，再接收 2。self 是约定俗成的参数名，应保持这个惯例。`self.value` 是实例上的属性；局部变量 value 与 self.value 不是同一个名字。

### 各实例应有各自的可变状态
在 __init__ 里写 `self.items = []`，每次创建对象都会新建列表。若直接在 class 缩进下写 `items = []`，它是类属性，可能被多个实例共享。这个陷阱与函数可变默认参数类似：你以为每个对象新建了一份，实际上只创建了一次。

类属性适合共享常量等状态，例如课程名称；实例属性适合个人进度、账户余额、单个数据集记录。

### 方法也要有明确约定
`add(minutes)` 可以检查分钟数是否为非负整数，合法才更新状态；`average()` 可以在没有记录时返回 None。类内部也会遇到空数据、输入验证与副作用问题，不能因为包了一层 class 就省略这些思考。

### 阅读特殊方法
`__len__` 支持 len(obj)，`__repr__` 返回开发者友好的字符串表示，`__getitem__` 支持 obj[index]。后续 PyTorch 数据集常使用 `__len__` 和 `__getitem__`；这一章只学习对应的 Python 机制，不需要安装深度学习库。

### 继承先会读就够
`class Dog(Animal):` 表示 Dog 从 Animal 继承可用行为，子类也可以定义同名方法覆盖它。`super()` 常用于调用父类相关实现。第一阶段重心是对象状态、方法调用和组合，复杂继承、多重继承与元类暂时不用展开。

组合是“一个对象持有另一个对象或数据”，例如一个 StudyTracker 持有 records 列表。真实程序中它通常比构造很深的继承树更直白。
''', ['类是定义，实例是具体对象。','self 指当前实例，self.x 是它的属性。','每个实例自己的列表放进 __init__ 创建。'],
['我能建立两个互不影响的计数器对象。','我能解释为什么方法定义有 self，调用时却不传它。','我能读懂一个实现 __len__ 与 __getitem__ 的数据集类。'])
example(c,'最小计数器',r'''class Counter:
    def __init__(self, start=0):
        self.value = start

    def add(self, amount=1):
        self.value += amount

counter = Counter(3)
counter.add()
counter.add(2)
print(counter.value)''','6','初始化 3，默认加 1，再加 2。value 是这个实例保存的状态；方法本身没有 return，调用结果为 None。','创建第二个 Counter，验证它不受第一个影响。')
example(c,'实例各自保存记录',r'''class StudyLog:
    def __init__(self):
        self.minutes = []

    def add(self, value):
        self.minutes.append(value)

    def total(self):
        return sum(self.minutes)

a = StudyLog()
b = StudyLog()
a.add(30)
print(a.total(), b.total())''','30 0','两个 __init__ 分别创建列表，因此 a 的追加不会进入 b。','把 minutes=[] 移成类属性，观察共享问题后恢复。')
example(c,'方法中的校验',r'''class Wallet:
    def __init__(self):
        self.balance_fen = 0

    def deposit(self, amount_fen):
        if amount_fen < 0:
            raise ValueError("存入金额不能为负")
        self.balance_fen += amount_fen

wallet = Wallet()
wallet.deposit(1500)
print(wallet.balance_fen)''','1500','金额使用整数分。验证发生在修改前，避免非法输入已经改变状态后才报错。','传入 -1 并捕获错误，再确认余额不变。')
example(c,'数据集接口预习',r'''class TextDataset:
    def __init__(self, texts):
        self.texts = list(texts)

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, index):
        return self.texts[index]

dataset = TextDataset(["hello", "python"])
print(len(dataset))
print(dataset[1])''',r'''2
python''','len 会调用 __len__，索引访问会调用 __getitem__。这里仅保存文本，未涉及 token 化或模型张量。','传入一个原列表后修改原列表，观察 list(texts) 的浅复制效果。')
example(c,'简单继承',r'''class Reporter:
    def describe(self):
        return "普通报告"

class StudyReporter(Reporter):
    def describe(self):
        return "学习报告"

print(Reporter().describe())
print(StudyReporter().describe())''',r'''普通报告
学习报告''','子类覆盖同名方法。调用时看具体对象所属类型提供的实现。','给父类加另一个方法，观察子类未覆盖时是否能调用。')
exercise(c,'步数计数器','基础','实现 StepCounter 类，初始 steps=0，add(count) 累加步数；本题 count 约定非负整数。创建对象加 100 再加 50，打印 steps。','状态放在 self.steps。',r'''class StepCounter:
    def __init__(self):
        self.steps = 0

    def add(self, count):
        self.steps += count

counter = StepCounter()
counter.add(100)
counter.add(50)
print(counter.steps)''','150','用两个实例测试状态隔离；仅打印一个对象无法发现所有共享状态问题。',tests=r'''a = StepCounter()
b = StepCounter()
a.add(2)
assert a.steps == 2 and b.steps == 0
b.add(0)
assert b.steps == 0''')
exercise(c,'学习记录平均值','场景','实现 StudyLog 类，实例 minutes 为空列表，add(value) 追加，mean() 空时 None，否则平均值。添加 30、60 后打印 mean()。','每个对象在 __init__ 创建自己的列表。',r'''class StudyLog:
    def __init__(self):
        self.minutes = []

    def add(self, value):
        self.minutes.append(value)

    def mean(self):
        if not self.minutes:
            return None
        return sum(self.minutes) / len(self.minutes)

log = StudyLog()
log.add(30)
log.add(60)
print(log.mean())''','45.0','方法组合前面学过的列表追加和安全平均值。类新增的是状态归属，不是全新的运算规则。',tests=r'''a = StudyLog()
b = StudyLog()
assert a.mean() is None
a.add(0)
assert a.mean() == 0
assert b.mean() is None''')
exercise(c,'可索引的记录集','迁移','实现 NumberDataset 类，构造时复制 values 到实例，支持 len 和 [index]。用 [10,20] 创建后依次打印长度与索引 0 的值。','实现 __len__、__getitem__。',r'''class NumberDataset:
    def __init__(self, values):
        self.values = list(values)

    def __len__(self):
        return len(self.values)

    def __getitem__(self, index):
        return self.values[index]

data = NumberDataset([10, 20])
print(len(data))
print(data[0])''',r'''2
10''','复制外层列表避免调用者后来 append 改变数据集长度；嵌套对象仍是浅复制。',tests=r'''source = [1, 2]
data = NumberDataset(source)
source.append(3)
assert len(data) == 2
assert data[-1] == 2
assert len(NumberDataset([])) == 0''')
exercise(c,'只接受有效分数','场景','实现 GradeBook，实例 scores=[]，add(score) 接受 0—100 的整数，越界抛 ValueError 且不修改状态。这里只要求范围验证。添加 80 后打印 scores。','检查应在 append 前面。',r'''class GradeBook:
    def __init__(self):
        self.scores = []

    def add(self, score):
        if not 0 <= score <= 100:
            raise ValueError("分数超出范围")
        self.scores.append(score)

book = GradeBook()
book.add(80)
print(book.scores)''','[80]','本题输入类型约定为整数，所以只做范围校验。若对外部 JSON 开放，还需额外验证类型。',tests=r'''book = GradeBook()
book.add(0)
book.add(100)
try:
    book.add(101)
except ValueError:
    pass
else:
    raise AssertionError("越界应抛异常")
assert book.scores == [0, 100]''')

c = chapter(15, '读懂进阶 Python 写法', '这一章先练阅读能力，暂时不追求所有写法都背下来。',
['理解迭代器与生成器的一次性消费','读懂类型标注、星号解包和参数收集','能把紧凑代码还原成执行步骤'], r'''
### 可迭代对象与迭代器
列表、字符串、字典等能被 for 遍历，叫可迭代对象。`iter(values)` 取得迭代器，`next(iterator)` 取下一个元素；取完再取会抛 StopIteration。for 会自动处理这个终止信号。

列表通常可以多次遍历，每次重新获得迭代器；同一个迭代器消费过的内容不会自动恢复。`zip`、`enumerate`、生成器也有类似的一次性消费特征。调试时先 `list(iterator)` 看内容，可能已经把后续循环要用的数据消费完了。

### yield 一次给一个
函数中出现 yield，它就成为生成器函数。调用生成器函数通常先得到生成器对象，代码在迭代取值时逐步执行。执行到 yield 暂停并交出当前值，下次继续从暂停处往后走，局部状态得以保留。

`return` 结束普通函数并给出最终结果；生成器中的 return 结束迭代。yield 是“这次先给一个，后面还可能有”。它避免一次保存全部输出，但输入本身是否已经全部在内存、内部是否保留大量状态，仍影响内存使用。

### 列表推导式与生成器表达式
`[x*x for x in values]` 立刻生成完整列表；`(x*x for x in values)` 产生按需计算的生成器。sum、any、all 等可以逐个消费生成器，通常无需额外列表。生成器不能直接 len，也不能普通索引访问。

### 星号在不同位置含义不同
赋值里的 `first, *middle, last = values` 收集剩余项；调用里的 `func(*args)` 把可迭代对象展开为位置参数，`func(**kwargs)` 把映射展开为关键字参数；定义里的 `def func(*args, **kwargs)` 收集额外参数为元组和字典。不要把这些星号与数字乘法混为一谈。

默认参数、位置参数、关键字参数的复杂组合以后可以继续学。当前目标是读懂训练代码中 `model(**batch)` 表示按批次字典的键把值作为命名参数传入，具体键必须符合函数接口。

### 类型标注是说明，不是自动转换
`def mean(values: list[float]) -> float | None:` 表明希望接收浮点列表，返回浮点或 None。Python 默认不会因为标注自动检查或转换输入；`"3"` 不会自动变成 3.0。实际验证需要 if/raise，静态类型检查则是额外工具。

本教材使用的 `list[...]` 与 `| None` 写法要求相应现代 Python 版本，整体学习包按 Python 3.10+ 编写。类型标注可以逐步添加，先保证函数的实际行为正确。

### with 与装饰器先会辨认
with 把一段需要进入和退出管理的工作包起来，例如打开与关闭文件。后续可能看到禁用梯度等上下文，其行为由具体库定义，不是所有 with 都在处理文件。

函数上方的 `@something` 是装饰器语法，可理解为函数定义完成后再交给 something 包装并绑定回来。第一阶段不必自己构造复杂装饰器；先查具体装饰器的官方说明，别凭 @ 符号猜它做什么。

### 暂时可以放后的主题
异步编程、并发、复杂正则、元类、多重继承、描述符和性能优化不是本阶段通关要求。看到陌生语法先确认输入、输出和调用路径；一个可运行的 10 行实验比一次背完语言参考更有效。
''', ['列表可反复遍历，同一迭代器会被消费。','yield 给一次结果并暂停，return 结束。','标注是约定，不会自动转换或验证。'],
['我能解释为什么 list(generator) 第二次为空。','我能把 **config 看成关键字参数展开。','我能写一个每次产生一批数据的生成器。'])
example(c,'迭代器逐项取值',r'''iterator = iter([10, 20, 30])
print(next(iterator))
print(list(iterator))
print(list(iterator))''',r'''10
[20, 30]
[]''','第一个元素已由 next 消费；第一次 list 消费剩余两项；最后再消费已无内容。','重新对原列表调用 iter，确认可以重新开始。')
example(c,'生成器暂停',r'''def countdown(start):
    while start > 0:
        yield start
        start -= 1

numbers = countdown(3)
print(next(numbers))
print(list(numbers))''',r'''3
[2, 1]''','第一次 next 运行到 yield 3；下一次从后面的 start -= 1 继续，不会从函数第一行重来。','在 yield 前后各加 print，观察真实执行时机。')
example(c,'星号解包',r'''first, *middle, last = [1, 2, 3, 4]
print(first, middle, last)

def add(a, b):
    return a + b

print(add(*[2, 3]))
print(add(**{"a": 5, "b": 6}))''',r'''1 [2, 3] 4
5
11''','赋值时收集到 middle 列表；调用时 * 展开位置，** 展开键值为命名参数。','尝试给 ** 字典增加不存在的键，阅读调用错误。')
example(c,'收集可变参数',r'''def describe(*args, **kwargs):
    print(args)
    print(kwargs)

describe("A", "B", score=90)''',r'''('A', 'B')
{'score': 90}''','args 是元组，kwargs 是字典。名字可更改，但这两个名称是常用惯例。','将位置参数变成 0 个，观察空元组。')
example(c,'带标注的函数',r'''def average(values: list[float]) -> float | None:
    if not values:
        return None
    return sum(values) / len(values)

print(average([1.0, 3.0]))
print(average([]))''',r'''2.0
None''','标注让接口更容易阅读，函数体仍需要自己处理空列表。标注也不会强制每项自动变成 float。','自己用错误类型调用，确认真正失败发生在哪个操作。')
exercise(c,'偶数生成器','基础','实现 even_numbers(stop)，使用 yield 产生 0 到 stop 之前的偶数，stop 为非负整数。打印 list(even_numbers(7))。','range 的步长用 2。',r'''def even_numbers(stop):
    for number in range(0, stop, 2):
        yield number

print(list(even_numbers(7)))''','[0, 2, 4, 6]','函数返回生成器，list 在展示时消费它。空范围自然产生空列表。',tests=r'''assert list(even_numbers(0)) == []
assert list(even_numbers(1)) == [0]
assert list(even_numbers(6)) == [0, 2, 4]
g = even_numbers(4)
assert iter(g) is g''')
exercise(c,'按批产生列表','场景','实现 batches(values,size)，size 是整数，<=0 时在消费时抛 ValueError；每次 yield 一个至多 size 项的切片，保留最后不足一批的数据。打印对 [1,2,3,4,5] 与 2 的结果。','range(0,len(values),size)，再切 [start:start+size]。',r'''def batches(values, size):
    if size <= 0:
        raise ValueError("size 必须为正数")
    for start in range(0, len(values), size):
        yield values[start:start + size]

print(list(batches([1, 2, 3, 4, 5], 2)))''','[[1, 2], [3, 4], [5]]','最后切片自动截到结尾。生成器中的验证在迭代开始时执行，而不是仅调用函数拿到对象时执行。',tests=r'''assert list(batches([], 2)) == []
assert list(batches([1], 4)) == [[1]]
assert list(batches([1, 2], 2)) == [[1, 2]]
try:
    list(batches([1], 0))
except ValueError:
    pass
else:
    raise AssertionError("size=0 应抛 ValueError")''')
exercise(c,'配置展开调用','迁移','实现 format_run(name,epochs)，返回 "名称:轮数"。用 config={"name":"demo","epochs":3} 的 ** 展开调用并打印。','字典键必须与形参名匹配。',r'''def format_run(name, epochs):
    return f"{name}:{epochs}"

config = {"name": "demo", "epochs": 3}
print(format_run(**config))''','demo:3','函数不知道参数是否来自字典展开，它收到的只是相应绑定。',tests=r'''assert format_run("x", 1) == "x:1"
assert format_run(**{"epochs": 0, "name": "empty"}) == "empty:0"''')
exercise(c,'生成器消费观察','推理','建立 (x*x for x in range(3))，连续两次 print(list(g))，写出结果并解释。','第一次 list 取走所有元素。',r'''g = (x * x for x in range(3))
print(list(g))
print(list(g))''',r'''[0, 1, 4]
[]''','想重新得到数据需要新建生成器，或第一次就保留生成的列表。不要把已经被日志打印消耗的生成器继续当作完整输入。')

c = chapter(16, '面向 AI 的 Python 数据实操', '把前面的语法组合成真实的数据处理步骤。',
['建立清洗、验证、分割、编码与分批的顺序','区分文本、词、token ID 与张量','实现简单指标并识别数据泄漏风险'], r'''
### 先看清数据走过哪些步骤
原始记录 → 检查字段类型 → 文本清洗 → 去空与去重 → 划分数据集 → 仅用训练数据建立统计规则 → 转换为数值表示 → 分批。这个顺序不是所有项目唯一答案，但它能帮助你识别哪些步骤可能把测试信息带入训练。

这一章所有数据都是很小的教学样本，只验证 Python 逻辑。它们不能支持模型效果结论，也不构成完整的深度学习训练系统。

### 文本清洗不要破坏任务信息
空白标准化可以 `" ".join(text.split())`。小写化对英文词频方便，但有时大小写本身有意义。数字、标点、代码缩进、换行对不同任务意义不同，不应统一无脑删除。先写明本次实验的清洗规则，再保存原始数据以便回溯。

### 词频不等于大模型 token 化
这里的 `text.split()` 只是按空白分词。中文一句话可能没有空格，专业 tokenizer 还可能把单词拆成子词、字节或其他单元。字典映射得到的 toy token ID 只供理解，不可直接喂给任意预训练模型；每个模型需要与其配套的 tokenizer 和特殊 token 约定。

### 划分时让记录保持完整
不要把 texts 和 labels 分别随机打乱，否则对应关系可能丢失。把它们放在同一条字典记录内，打乱记录列表，再切分。需要复现时使用局部随机生成器并记录 seed。

随机划分不是所有数据的正确策略。时间序列通常考虑时间先后；同一用户、病人、文档来源产生的相近记录通常要按组隔离；重复文本也可能让训练测试互相泄漏。先定义什么是独立样本，再选划分方式。

### 为什么词表只从训练集建立
假设测试集中出现从未见过的词，模型真实使用时也会遇到这种情况。若提前看全量数据建立词表或统计量，就把测试信息带入了预处理。教学管道中用训练集建词表，验证和测试遇到新词映射到 `<UNK>`。

同样原则适用于基于数据学习的均值、标准差、特征选择等。固定的、与样本无关的字符规则是另一类处理，但仍要明确记录。

### 形状与批大小
列表 `[1,2,3]` 可类比长度为 3 的一维数据；`[[1,2],[3,4]]` 可类比 2×2。Python 嵌套列表不自动保证每行等长，而真实张量的规则由数值库定义。常见文本批次有“批大小 × 序列长度”，之后才可能再有特征维度。先说清每一轴的含义，再谈 shape。

padding 是把短序列补到约定长度，attention mask 常用来标记哪些位置是真实内容；具体 0/1 含义需查所用模型接口。这里把 pad ID 设为 0，真实词 ID 从 2 开始，1 留给未知词，只是本课程自定义规则。

### 指标的分母决定含义
分类准确率是预测等于真实标签的个数除以样本数。长度必须一致；空集合的指标要明确约定。严重类别不平衡时，准确率可能具有误导性，后续还需学习精确率、召回率和 F1。不要把一个简单指标当作模型能力的完整描述。

### 这一阶段到下一阶段的桥
你现在应能读懂列表推导式、字典批次、函数参数、类方法和迭代器。下一阶段再学 NumPy 数组、广播与矩阵乘法，接着 PyTorch 张量、自动求导、Dataset/DataLoader，最后才是 tokenizer、Transformer 和训练/推理流程。新库安装时按其当时的官方兼容矩阵选择 Python 与硬件配置；本教材不预设未来深度学习环境的版本。
''', ['清洗规则先写清，不是删得越多越好。','记录一起打乱，训练数据负责建立统计规则。','空白分词是教学简化，不等于模型 tokenizer。','批大小、序列长度、特征维度分别命名。'],
['我能把原始记录整理成没有空文本和重复 ID 的列表。','我能从训练文本建立词表并处理未知词。','我能检查批次末尾、标签对齐与空指标。'])
example(c,'清洗并保序去重',r'''raw = ["  Hello   Python ", "", "hello python", "Learn AI"]
seen = set()
cleaned = []
for text in raw:
    clean = " ".join(text.lower().split())
    if clean and clean not in seen:
        seen.add(clean)
        cleaned.append(clean)
print(cleaned)''',"['hello python', 'learn ai']",'先规范化，才能识别空白和大小写差异造成的重复。保留第一次出现顺序；原始输入仍保存着。','解释对源代码文本直接使用这个规则会有什么问题。')
example(c,'记录整体划分',r'''import random
records = [{"id": i, "label": i % 2} for i in range(6)]
shuffled = records.copy()
random.Random(42).shuffle(shuffled)
train = shuffled[:4]
test = shuffled[4:]
print(len(train), len(test))
print(set(row["id"] for row in train).isdisjoint(row["id"] for row in test))
print([row["id"] for row in records])''',r'''4 2
True
[0, 1, 2, 3, 4, 5]''','copy 保护原顺序，记录中的 id 与 label 一起移动。这里只检查 ID 无重叠，完整数据泄漏检查还要考虑内容和来源。','让不同 ID 的文本完全相同，解释为什么 ID 检查不够。')
example(c,'训练词表与未知词',r'''train_texts = ["hello python", "hello world"]
vocab = {"<PAD>": 0, "<UNK>": 1}
for text in train_texts:
    for word in text.split():
        if word not in vocab:
            vocab[word] = len(vocab)
encoded = [vocab.get(word, vocab["<UNK>"]) for word in "hello ai".split()]
print(vocab)
print(encoded)''',r'''{'<PAD>': 0, '<UNK>': 1, 'hello': 2, 'python': 3, 'world': 4}
[2, 1]''','ai 不在训练词表，因此映射到 1。词表只从 train_texts 建立。真实模型不能随意使用这个自建词表代替其配套 tokenizer。','添加一个训练词后重新建表，观察 ID 是否受顺序影响。')
example(c,'补齐与掩码',r'''sequences = [[2, 3, 4], [2]]
width = max(len(sequence) for sequence in sequences)
padded = []
masks = []
for sequence in sequences:
    padding = width - len(sequence)
    padded.append(sequence + [0] * padding)
    masks.append([1] * len(sequence) + [0] * padding)
print(padded)
print(masks)''',r'''[[2, 3, 4], [2, 0, 0]]
[[1, 1, 1], [1, 0, 0]]''','每行长度变成批内最大长度。mask=1 表示本例真实位置，0 表示补齐位置。此例假定批次非空，练习中处理空输入。','加入空序列，确认该行全部为 padding。')
example(c,'准确率与对齐',r'''def accuracy(predictions, labels):
    if len(predictions) != len(labels):
        raise ValueError("长度不一致")
    if not labels:
        return None
    correct = sum(pred == label for pred, label in zip(predictions, labels))
    return correct / len(labels)

print(f"{accuracy([1, 0, 1, 1], [1, 1, 1, 0]):.1%}")''','50.0%','布尔值参与 sum 时 True 当作 1，False 当作 0。先检查长度，避免 zip 的截短悄悄忽略样本。','构造全部猜主要类别但准确率很高的例子，说明指标局限。')
example(c,'二维形状检查',r'''rows = [[1, 2], [3, 4], [5, 6]]
width = len(rows[0]) if rows else 0
is_rectangular = all(len(row) == width for row in rows)
print(len(rows), width)
print(is_rectangular)''',r'''3 2
True''','外层长度是行数，内层长度是列数；所有行等长才符合本例矩形结构。Python 列表本身不会强制这一规则。','把最后一行改为 [5]，确认检查能发现不齐。')
exercise(c,'文本清洗函数','场景','实现 normalize(text)，转小写并将连续空白变成单空格，去两端空白。打印对 "  Hello   AI  " 的结果。','lower、split、join。',r'''def normalize(text):
    return " ".join(text.lower().split())

print(normalize("  Hello   AI  "))''','hello ai','规则应被记录并保持一致。对训练与推理文本使用同一预处理约定，避免流程不一致。',tests=r'''assert normalize("") == ""
assert normalize(" \n\t") == ""
assert normalize("A\nB") == "a b"''')
exercise(c,'训练词表','场景','实现 build_vocab(texts)，初始 {"<PAD>":0,"<UNK>":1}，按首次出现为按空白分出的词分配 ID；文本已预处理。打印 ["a b","a c"] 的结果。','未出现才用当前字典长度分配。',r'''def build_vocab(texts):
    vocab = {"<PAD>": 0, "<UNK>": 1}
    for text in texts:
        for word in text.split():
            if word not in vocab:
                vocab[word] = len(vocab)
    return vocab

print(build_vocab(["a b", "a c"]))''',"{'<PAD>': 0, '<UNK>': 1, 'a': 2, 'b': 3, 'c': 4}",'保留两个特殊 ID；同词再次出现不分配新 ID。只对训练集调用这个建表函数。',tests=r'''assert build_vocab([]) == {"<PAD>": 0, "<UNK>": 1}
assert build_vocab(["a a"])["a"] == 2
assert len(build_vocab(["a a"])) == 3''')
exercise(c,'未知词编码','基础','实现 encode(text,vocab)，按空白拆词，用 vocab["<UNK>"] 处理未知词。打印 "a x" 在 {"<UNK>":1,"a":2} 下的结果。','get 默认未知词 ID。',r'''def encode(text, vocab):
    return [vocab.get(word, vocab["<UNK>"]) for word in text.split()]

print(encode("a x", {"<UNK>": 1, "a": 2}))''','[2, 1]','本题约定词表含 <UNK>。编码不修改词表，尤其不能因为看见测试词就自动扩充训练词表。',tests=r'''vocab = {"<UNK>": 1, "a": 2}
assert encode("", vocab) == []
assert encode("x x", vocab) == [1, 1]
assert vocab == {"<UNK>": 1, "a": 2}''')
exercise(c,'准确率函数','迁移','实现 accuracy(predictions,labels)，等长空列表返回 None，长度不同抛 ValueError，其余返回准确率。打印 [1,0] 对 [1,1] 的结果。','长度检查在 zip 前。',r'''def accuracy(predictions, labels):
    if len(predictions) != len(labels):
        raise ValueError("长度不一致")
    if not labels:
        return None
    correct = sum(pred == label for pred, label in zip(predictions, labels))
    return correct / len(labels)

print(accuracy([1, 0], [1, 1]))''','0.5','先约定空输入行为，再计算分母。不能把空输入默认为 100% 正确。',tests=r'''assert accuracy([], []) is None
assert accuracy([1], [1]) == 1
assert accuracy([0], [1]) == 0
try:
    accuracy([1], [])
except ValueError:
    pass
else:
    raise AssertionError("长度不匹配应报错")''')
exercise(c,'补齐批次','挑战','实现 pad_batch(sequences,pad_id=0)，返回 (padded,masks)，补到本批最大长度，空批返回 ([],[])，不修改输入。打印 [[2,3],[4]] 的结果。','空批先返回；每行构建新列表。',r'''def pad_batch(sequences, pad_id=0):
    if not sequences:
        return [], []
    width = max(len(sequence) for sequence in sequences)
    padded = []
    masks = []
    for sequence in sequences:
        extra = width - len(sequence)
        padded.append(sequence + [pad_id] * extra)
        masks.append([1] * len(sequence) + [0] * extra)
    return padded, masks

print(pad_batch([[2, 3], [4]]))''','([[2, 3], [4, 0]], [[1, 1], [1, 0]])','返回两个对齐结构。空序列可以作为批中的一项；全空序列时宽度为 0。',tests=r'''assert pad_batch([]) == ([], [])
assert pad_batch([[], []]) == ([[], []], [[], []])
source = [[1], []]
assert pad_batch(source, 9) == ([[1], [9]], [[1], [0]])
assert source == [[1], []]''')
exercise(c,'验证记录 ID 唯一','场景','实现 unique_ids(records)，如果各字典的 id 唯一返回 True，重复则 False；空列表返回 True。打印 [{"id":1},{"id":1}] 的结果。','取 id 列表再比较集合长度。',r'''def unique_ids(records):
    ids = [record["id"] for record in records]
    return len(ids) == len(set(ids))

print(unique_ids([{"id": 1}, {"id": 1}]))''','False','本题假定 id 字段存在且可哈希。真实导入流程需先验证字段类型，再执行唯一性检查。',tests=r'''assert unique_ids([]) is True
assert unique_ids([{"id": 1}, {"id": 2}]) is True
assert unique_ids([{"id": "a"}, {"id": "a"}]) is False''')

c = chapter(17, '四个综合项目', '从需求开始独立组织程序，再对照参考实现。',
['把需求拆成数据、函数和验证规则','运行完整项目并核对输出文件','在已有程序上独立增加一个功能'], r'''
### 项目练习的正确顺序
先读项目需求和输入数据，不要先打开 app.py。用中文写出 5—8 个步骤，在 `starter.py` 里实现最小版本。先用内存里的三条假数据验证，再加入文件读取，最后才加命令行界面。app.py 是完整参考实现，分步任务并不要求一开始就复刻它的全部结构。starter.py 中的 NotImplementedError 是提醒你填入代码的练习标记；它报错并不表示 Python 安装失败。每次只完成一个函数，再运行底部的小样例检查。

每个项目目录都有 README.md、TASKS.md、starter.py 和 app.py。需要输入数据的项目另有 data/。默认运行会把结果写进该项目 outputs/。这些都是专用练习输出；重跑项目 02—04 会覆盖同名报告，项目 01 的 add 会追加记录。不要将练习输出路径改成自己的重要文件。

### 四次递进练习
1. **学习打卡本**：日期、分钟、主题 → 验证 → JSON 保存 → 汇总。重点是函数边界、文件持久化、错误恢复。
2. **成绩表清洗**：含错误的 CSV → 按字段检查 → 有效记录与错误记录分流 → 排名和统计。重点是字符串转数字、边界和错误报告。
3. **文本语料清洗**：JSONL → 解析 → 规范化 → 去空去重 → 词频。重点是字典、集合和数据可追溯性。
4. **数据集管道**：记录验证 → 划分 → 训练词表 → 编码 → 补齐 → 分批。重点是数据对齐、未知词、形状和复现。

### 把一个任务拆成函数的完整示范
以成绩表为例，输入是路径，不是分数列表。读取后每条 CSV 记录仍是字符串字典。先约定 student_id、name、score 三列必须存在；再对每行去空白、转整数、检查范围。合法记录加入 valid，非法记录加入 errors。两个结果列表形成“验证层”的输出。

统计层只接收 valid，所以不必在每次求平均时重新猜哪些分数可用。最后输出层把统计对象序列化成 JSON，把 errors 写成 CSV。这样如果平均分错了，可以直接测试统计层；如果文件找不到，则看读取层；不必每次从头怀疑全部代码。

### 项目验收的五个问题
- 用最小样本手算，程序结果一致吗？
- 没有数据、只有一条、全是坏数据时会怎样？
- 用户看到的错误能找到对应记录吗？
- 换一个启动目录或另一台电脑，路径是否仍然正确？
- 同样输入再跑一次，哪些文件覆盖、哪些记录追加，行为是否符合说明？

### 新出现的 argparse 不用死记
项目里的 argparse 来自标准库。`ArgumentParser` 建立命令说明，`add_argument` 声明参数，`parse_args` 把终端输入读成对象。`args.input` 对应 `--input`；命令中的带空格主题要加引号。先运行 `python app.py --help`，按照给出的命令执行，再回看源代码中相应定义。

注意运行位置：本章给出的命令从**学习包根目录**执行。如果已进入某个项目目录，命令可以简化为 `python app.py`。Windows/Mac 的解释器名字按第 00 章替换。

### 不看答案的通关挑战
给成绩报告增加“分数区间人数”，区间为 0—59、60—79、80—89、90—100。先手算样例，应为 2、1、1、1。把逻辑写成独立函数，测试 59、60、79、80、89、90、100。再把结果加入输出 JSON。完成后用自己的话解释：为什么区间不能互相重叠，为什么不能把 100 漏掉。

另一个挑战：给学习打卡增加“按主题累计”，清洗主题两端空格但不随意更改中文内容。对 30 分钟 Python、20 分钟 Git、15 分钟 Python，结果应为 Python=45、Git=20。把这题与第 08 章的分类累计联系起来。

### 最后一次自我验收
以下命令核验参考项目，不会替你完成 starter.py：

```terminal
python tools/check_projects.py
```

自己的实现仍要用 TASKS.md 的验收案例检查。工具通过只能证明参考实现通过了已写检查；你能否不看答案重建其中一个项目，才是本阶段最重要的学习证据。
''', ['先内存逻辑，再文件，再命令行。','验证层把坏数据说明白，统计层只接收约定的数据。','完成一个独立扩展，比只运行参考代码更能证明掌握。'],
['我能独立完成至少一个项目的核心逻辑。','我能给项目增加一个小功能并验证边界。','我能解释原始输入如何一步步变成最终报告。'])

c = chapter(18, '复习路线 自测与速查', '按能力前进，不必为了赶进度跳过卡住的知识。',
['安排可执行的复习节奏','通过阶段检查找到薄弱点','知道进入 NumPy 与 PyTorch 前应会什么'], r'''
### 一个可调整的八周路线
这只是安排参考，不是保证八周精通。建议每周 5 天，每天 45—75 分钟；基础薄弱或工作繁忙时，每周内容可以拆成两周。

| 周次 | 重点 | 必须留下的实作成果 |
|---|---|---|
| 1 | 第 00—03 章 | 能独立运行文件，完成输入转换和文本清洗 |
| 2 | 第 04—06 章 | 写成绩分级、累计、菜单退出，手工追踪循环 |
| 3 | 第 07—08 章 | 会列表与字典，解释共享对象，写分组和词频 |
| 4 | 第 09—10 章 | 把旧程序改成函数，处理空数据并完成额外测试 |
| 5 | 第 11—13 章 | 读写 CSV/JSON，创建环境，定位并修复报错 |
| 6 | 第 14—15 章 | 看懂 self、数据集类、生成器与 ** 参数展开 |
| 7 | 第 16—17 章项目 01—03 | 独立写一个有持久化输出的完整程序 |
| 8 | 项目 04 与综合验收 | 画出数据处理路径，增加一个功能，重做错题 |

### 记忆靠提取，不靠反复划线
学完当天合上教材，用空文件写一个同类例子；次日重写错题；第 3 天换输入和场景；第 7 天混合不同章节；第 14 天在项目中复用。这些间隔只是可操作的复习安排，不是对所有人最佳的固定规律。

每张记忆卡只放一个问题，例如“sort 返回什么？”、“空列表的 all 是什么？”、“input 得到什么类型？”、“为什么 b=a 后改 b 会影响 a？”先口头回答，再看背面并运行小例子。不要把十个语法点塞在一张卡里。

### 一页关键记忆表
| 问题 | 记住的核心 | 最小例子 |
|---|---|---|
| = 与 == | 赋值与比较 | x=3；x==3 |
| 索引与切片 | 单点与区间，终点不含 | s[0]；s[:3] |
| input 类型 | 先是字符串 | int(input()) |
| append 与 extend | 加一个与逐个加 | a.append([1,2]) |
| sort 与 sorted | 原地改并返回 None 与新列表 | b=sorted(a) |
| b=a 与 copy | 共享对象与新外层 | b=a.copy() |
| print 与 return | 显示与把值交回 | return total |
| break 与 continue | 结束循环与跳本轮后半段 | if bad: continue |
| in 在 dict 中 | 默认查键 | "name" in row |
| None 与 0 | 缺失与有效数值可能不同 | value is None |
| get 的默认值 | 读取缺失键，不自动写回 | d.get(k,0) |
| CSV 与 JSON | 文本字段表格与嵌套对象 | int(row["score"]) |
| 路径 | 当前目录与脚本目录区别 | Path(__file__).parent |
| yield 与 return | 暂停给一个与结束 | yield batch |

### 常见报错恢复路线
“找不到 Python”：关闭并重开终端，检查安装，分别试 Windows 的 py、Mac 的 python3。

“can't open file”：先确认完整解压，检查当前目录与文件名，路径有空格时加引号。不要把教材里的尖括号占位文字当作真实路径。

“ModuleNotFoundError”：标准库先检查是否拼错和是否用同名文件遮蔽；第三方库检查当前解释器与 pip 对应，不能只看另一个终端是否曾安装。

“TypeError 或 ValueError”：打印 type 和 repr，确认数据内容。字符串 "80" 与整数 80 外观相似，操作规则不同。

“网页勾选丢失”：浏览器本地存储不是跨电脑云同步；导入之前导出的进度 JSON。你的代码保存在 .py 文件，与网页勾选独立。

### 阶段自测 A 语法解释
先口头回答，再在对应章节验证：
1. `print("3"*2)` 与 `print(3*2)` 分别是什么？答案：33 与 6；前者字符串重复。
2. `list(range(2,7,2))` 是什么？答案：[2,4,6]，不包含 7。
3. `a=[1]; b=a; b.append(2)` 后 a 是什么？答案：[1,2]，共享对象。
4. 函数只有 print 没有 return，返回什么？答案：None。
5. `bool("False")` 是什么？答案：True，非空字符串。
6. 空列表可以直接求平均吗？答案：不能直接除以 len；需定义空数据行为。
7. `d.get("x",0)` 会创建 x 键吗？答案：不会。
8. 第二次 list(g) 为什么可能为空？答案：同一个生成器已经消费完。
9. 标注 `x: int` 会自动转型吗？答案：不会。
10. 训练集和测试集标签为什么不能分别打乱？答案：会破坏样本与标签配对。

### 阶段自测 B 独立编程
不给参考代码，按下面案例自己验证：
- 写 summarize_minutes([0,30,45])，返回总分钟 75、学习天数 2、按全部 3 天计算的日均 25.0；空列表日均 None。要求说明“按全部天数”与“只按学习日”的区别。
- 写 top_words("a b a c b a",2)，返回 [("a",3),("b",2)]；同频按词的字母顺序。空文本返回空列表。
- 写 clean_scores(["80","x","101","0"])，返回有效分数 [80,0] 与无效项位置 [2,3]，位置从 1 开始。把它接到 CSV 读取程序。
- 写 chunks([1,2,3,4,5],2)，返回 [[1,2],[3,4],[5]]；size<=0 抛 ValueError；不改变输入列表。

完成标准不是记住这几个答案，而是你能为每个函数换 3 组输入，手算预期，然后解释结果不一致时是哪一步出错。

### 项目自评 100 分
需求与输入输出约定 15 分；核心逻辑正确 30 分；边界与错误处理 20 分；函数拆分与命名 15 分；可重复运行与路径 10 分；能解释并独立扩展 10 分。80 分可作为继续下一阶段的参考线，但若还分不清 return、列表共享或字典列表层次，应先回补，即使总分够也别跳过。

### 进入深度学习前的能力清单
能够独立读写 CSV/JSONL；能解释嵌套列表与字典的层级；能编写带参数、返回值和边界检查的函数；能定位类型、路径和导入错误；能读懂类、迭代器与批次；会建立环境并记录依赖；知道训练测试应保持独立。这些基础比提前背某个模型 API 更耐用。

下一阶段的顺序建议是：NumPy 数组与形状 → 数学中的向量、矩阵和导数直觉 → PyTorch 张量与自动求导 → 小型分类任务完整训练流程 → tokenizer、Transformer 与模型推理 → 根据目标学习微调、评估或检索增强。每一阶段仍然用小数据、可核对输出和独立实现来检验理解。

### 官方资料与核对日期
本教材是为零基础重新组织的原创讲解和练习，并非 Python 官方教程的翻译。安装与环境说明参考官方资料；语法细节有争议时以对应版本文档为准。核对日期：2026-10-07。

- [Python 官方教程](https://docs.python.org/3/tutorial/)：适合完成基础阶段后查阅。
- [Python 内置函数](https://docs.python.org/3/library/functions.html)：查询 print、range、sorted 等。
- [Python 标准类型](https://docs.python.org/3/library/stdtypes.html)：字符串、列表、字典的准确语义。
- [Windows 安装](https://docs.python.org/3/using/windows.html) 与 [macOS 安装](https://docs.python.org/3/using/mac.html)。
- [虚拟环境与 pip](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/)。
- [NumPy 入门](https://numpy.org/doc/stable/user/absolute_beginners.html)、[PyTorch 基础](https://docs.pytorch.org/tutorials/beginner/basics/intro.html)：下一阶段再学，安装前查看当时官方要求。

### 以后向助教提问的模板
“我正在做第 XX 章第 XX 题；我理解目标是……；我的代码是……；输入是……；我预计输出……；实际输出或完整报错是……；我已经试过……。请先提示定位思路，不直接给完整答案。”

能把问题这样说清楚，本身就是一种重要的编程能力。你不需要一次记住所有方法，但要能把数据、步骤和错误描述清楚。
''', ['先独立提取，再核对答案；会背不代表会用。','每个函数至少测正常、空、边界。','看懂数据流，再学习库的接口。'],
['我能在空文件里完成阶段自测 B 的至少三题。','我能不看答案解释一段综合项目代码。','我有自己的错题记录和下一周可执行的练习安排。'])

# 针对重点补充变式，避免只会套用一个例子。
c = CHAPTERS[3]
exercise(c,'确认是否已保存清洗结果','纠错','text="  Python  "。有人调用 text.strip() 后直接打印 text。请修复并输出 Python，再输出长度 6。','方法返回新字符串，要保存返回值。',r'''text = "  Python  "
text = text.strip()
print(text)
print(len(text))''',r'''Python
6''','字符串不可变，strip 不会就地改原对象。长度检查帮助你确认两端空格确实被去掉。')
c = CHAPTERS[4]
exercise(c,'实验启动条件','场景','has_data=True，has_config=True，is_running=False。只有有数据、有配置且当前未运行时输出 可以启动，否则输出 暂不能启动。','三个条件用 and，其中一个要取 not。',r'''has_data = True
has_config = True
is_running = False
if has_data and has_config and not is_running:
    print("可以启动")
else:
    print("暂不能启动")''','可以启动','布尔名字直接放入条件，无需 == True。逐个翻转三个值，应该每次都阻止启动。')
c = CHAPTERS[5]
exercise(c,'最长单词','迁移','在 ["I","study","python","daily"] 中找第一个最长词，输出 python；不用 max。','用当前最长词作状态，只在严格更长时更新。',r'''words = ["I", "study", "python", "daily"]
longest = ""
for word in words:
    if len(word) > len(longest):
        longest = word
print(longest)''','python','使用 > 而不是 >=，同长度时保留先出现的词。本题空列表时结果为空字符串，应在实际需求中明确是否接受。')
c = CHAPTERS[6]
exercise(c,'整数各位求和','挑战','对非负整数 2048，用 while、// 和 % 求各位数字之和，输出 14。','%10 取末位，//10 去末位。',r'''number = 2048
total = 0
while number > 0:
    total += number % 10
    number //= 10
print(total)''','14','逐轮末位为 8、4、0、2；number 变为 204、20、2、0。输入 0 时循环零次，总和仍为 0，符合约定。')
c = CHAPTERS[7]
exercise(c,'修复 sort 赋值','纠错','values=[3,1,2]。修复 values=values.sort() 导致 None 的问题；要求保留 values 的列表并输出升序。','sort 自己修改原列表，不用接收返回值。',r'''values = [3, 1, 2]
values.sort()
print(values)''','[1, 2, 3]','另一种正确方法是 values=sorted(values)。关键是辨认方法的副作用与返回值。')
exercise(c,'复制二维数表','挑战','original=[[1,2],[3,4]]，用逐行 copy 建立新二维列表，修改新表左上角为 9。依次输出原表、新表。','外层新建，每行也新建；本题叶子为整数，复制两层足够。',r'''original = [[1, 2], [3, 4]]
copied = []
for row in original:
    copied.append(row.copy())
copied[0][0] = 9
print(original)
print(copied)''',r'''[[1, 2], [3, 4]]
[[9, 2], [3, 4]]''','只 original.copy() 仍共享内层行。本题逐行 copy 解决两层结构，任意深层结构应重新分析或使用适当深拷贝。')
c = CHAPTERS[8]
exercise(c,'按标签统计','场景','records=[{"label":1},{"label":0},{"label":1}]，输出标签到数量的字典 {1:2,0:1}。','先取 record["label"]，再对该键累计。',r'''records = [{"label": 1}, {"label": 0}, {"label": 1}]
counts = {}
for record in records:
    label = record["label"]
    counts[label] = counts.get(label, 0) + 1
print(counts)''','{1: 2, 0: 1}','这是类别分布的最小统计，有助于发现标签不平衡。JSON 保存这种字典时整数键会变成字符串，读回时不要假定类型不变。')
exercise(c,'读取嵌套配置','迁移','config={"training":{"batch_size":8,"epochs":3}}，输出 batch_size 与 epochs 的乘积 24。','先取 training 得到内层字典。',r'''config = {"training": {"batch_size": 8, "epochs": 3}}
training = config["training"]
print(training["batch_size"] * training["epochs"])''','24','逐层命名帮助观察结构。这里乘积只作语法练习，不代表训练步数，真实步数还取决于数据量和批数。')
c = CHAPTERS[9]
exercise(c,'是否回文','迁移','实现 is_palindrome(text)，按 lower 后 split/join 去除全部空白，再比较正反文本。打印对 "Never odd or even" 的结果。标点本题不删除。','用 "".join(...) 去空白，再与 [::-1] 比较。',r'''def is_palindrome(text):
    cleaned = "".join(text.lower().split())
    return cleaned == cleaned[::-1]

print(is_palindrome("Never odd or even"))''','True','先写清规范化规则。按本题定义空字符串也满足与逆序相等，不同需求可以另作约定。',tests=r'''assert is_palindrome("") is True
assert is_palindrome("A b a") is True
assert is_palindrome("Python") is False''')
exercise(c,'优惠后的新列表','场景','实现 discounted(prices, rate=0.9)，返回每个价格乘 rate 的新列表，不改输入。打印 [100,200] 的默认结果。','用一个新列表收集各价格的折后值。',r'''def discounted(prices, rate=0.9):
    result = []
    for price in prices:
        result.append(price * rate)
    return result

print(discounted([100, 200]))''','[90.0, 180.0]','rate=0.9 表示付原价的 90%，不是减去 90%。此题使用浮点练习，精确金额仍建议整数分或 Decimal。',tests=r'''assert discounted([]) == []
source = [10, 20]
assert discounted(source, 0.5) == [5, 10]
assert source == [10, 20]''')
c = CHAPTERS[12]
exercise(c,'读取数字文件','场景','实现 read_numbers(path)，path 为 pathlib.Path，读 UTF-8 文本，每个非空行是合法整数，返回整数列表。演示时在临时目录建文件，内容 10、20，输出 [10,20]。','复用 splitlines、strip 与 int；临时目录离开 with 后自动清理。',r'''from pathlib import Path
from tempfile import TemporaryDirectory

def read_numbers(path):
    return [int(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]

with TemporaryDirectory() as folder:
    path = Path(folder) / "numbers.txt"
    path.write_text("10\n20\n", encoding="utf-8")
    print(read_numbers(path))''','[10, 20]','临时目录只用于演示和检查，不适合保存你长期需要的学习记录。函数不负责跳过非法数字，本题约定输入合法。',tests=r'''with TemporaryDirectory() as folder:
    path = Path(folder) / "input.txt"
    path.write_text("\n0\n-2\n", encoding="utf-8")
    assert read_numbers(path) == [0, -2]
    path.write_text("", encoding="utf-8")
    assert read_numbers(path) == []''')
c = CHAPTERS[13]
exercise(c,'只捕获预期解析错误','挑战','实现 json_object(text)，JSON 解析失败或解析结果不是字典时返回 None，否则返回字典。分别打印对 {"a":1}、[]、bad 的结果。','json.loads 后检查 isinstance(data, dict)。',r'''import json

def json_object(text):
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return None
    if not isinstance(data, dict):
        return None
    return data

print(json_object('{"a":1}'))
print(json_object('[]'))
print(json_object('bad'))''',r'''{'a': 1}
None
None''','语法合法的 JSON 不一定具有你要求的结构。解析层与结构验证层分别检查，后续才能安全按键访问。',tests=r'''assert json_object('{}') == {}
assert json_object('null') is None
assert json_object('42') is None
assert json_object('{') is None''')
