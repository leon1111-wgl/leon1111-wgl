# 学习打卡与统计

前置：第 00—13 章

写一个命令行学习记录本：添加日期、学习分钟和主题；下次打开仍可读取；汇总次数、总分钟和平均分钟。分钟必须为非负整数，主题不能为空。文件损坏时报告问题，不把坏文件当空记录覆盖。

### 1 先写核心函数
先对内存中的记录列表写 summarize(records)，输入 30、60 分钟时总量为 90、平均 45.0。空列表返回平均 None。此时完全不需要文件或命令行。

### 2 加入文件持久化
用 JSON 保存记录列表。文件不存在视作首次使用，返回空列表；文件存在但内容错误则抛出清楚异常。分清这两种情况，避免误覆盖用户数据。

### 3 检查输入再修改
用 date.fromisoformat 验证日期，并保存 isoformat() 的结果，统一为 YYYY-MM-DD（3.11 起它也接受 20261007 这样的写法）；分钟用整数且非负检查；主题 strip 后检查非空。所有检查通过后才 append。

### 4 加入命令行入口
argparse 是标准库命令行参数解析器。add 子命令收 minutes 与 topic；summary 子命令显示统计；--store 指定记录位置。看不懂时先运行 --help，再按已给命令练习。

### 5 独立扩展
增加按主题汇总，不直接改现有统计函数；给新函数写 3 个例子。进一步可做删除记录，但先为每条记录设计稳定 ID，并明确删除规则。

### 6 给命令找位置：参数属于谁
下面是原项目的补充实操，先读完第 11—13 章再做。所有命令都从学习包根目录运行；Windows 将 python 换成 py，macOS 换成 python3。已有 TASKS.md 和 starter.py 留给你作答，新增说明以这里和项目 README.md 为准。

先读两层帮助，它们只显示说明，不添加记录：

```terminal
python projects/01_study_log/app.py --help
python projects/01_study_log/app.py add --help
```

第一层声明 --store 和 add / summary 两个子命令；第二层只解释 add 的 minutes、topic 和 --date。**本程序的 --store 必须写在 add 或 summary 之前，--date 写在 add 后面。** 这是本项目的参数定义，不是所有命令行程序通用的固定顺序。

把下面的命令按片段读一遍，先不要执行：

```terminal
python projects/01_study_log/app.py --store "personal/打卡 练习/round1.json" add 30 "Python 循环" --date 2026-10-07
```

| 命令片段 | 交给哪一层 | 本次意义 |
| --- | --- | --- |
| python | 操作系统启动解释器 | Windows / Mac 按前文替换 |
| projects/01_study_log/app.py | Python | 要执行的脚本 |
| --store "personal/打卡 练习/round1.json" | 主解析器 | 选择本次读写的文件 |
| add | 子命令选择 | 本次要添加 |
| 30 | add 的 minutes | argparse 用 int 转换，再检查非负 |
| "Python 循环" | add 的 topic | 引号让含空格主题作为一个参数传入 |
| --date 2026-10-07 | add 的日期选项 | 固定日期，便于复现 |

引号用于划分终端参数，不会作为双引号字符存入主题。先用完整选项名；不需要背 argparse 的全部功能。记忆顺序：**选文件 → 选动作 → 给动作的数据。**

### 7 追踪持久化：关闭程序后，文件还在
请先在文件管理器确认 personal/打卡 练习/round1.json 不存在；若已有同名文件，给下面每条命令统一换一个新名字，例如 round2.json。不要清空旧文件来凑预期结果。首次有效 add 会自动创建需要的目录。

逐条运行，每运行一条就停下来核对对应表格。每条命令启动一次新的 Python 进程，程序通过同一个 JSON 文件衔接记录。

```terminal
python projects/01_study_log/app.py --store "personal/打卡 练习/round1.json" summary
python projects/01_study_log/app.py --store "personal/打卡 练习/round1.json" add 30 "Python 循环" --date 2026-10-07
python projects/01_study_log/app.py --store "personal/打卡 练习/round1.json" add 0 "复习记录" --date 2026-10-08
python projects/01_study_log/app.py --store "personal/打卡 练习/round1.json" summary
python projects/01_study_log/app.py --store "personal/打卡 练习/round1.json" add 30 "Python 循环" --date 2026-10-07
python projects/01_study_log/app.py --store "personal/打卡 练习/round1.json" summary
```

| 步骤 | 读入的分钟列表 | 本次动作与中间值 | 文件中的分钟列表 | 精确输出（分号表示换行） |
| --- | --- | --- | --- | --- |
| 1 summary | 文件不存在，视作 [] | count=0，total=0，mean=None | 仍不存在 | 记录数：0；总分钟：0；平均分钟：暂无 |
| 2 add 30 | [] | 验证 → append → 保存 | [30] | 已保存 1 条记录 |
| 3 add 0 | [30] | 0 合法，追加第二条 | [30, 0] | 已保存 2 条记录 |
| 4 summary | [30, 0] | count=2，total=30，mean=15.0 | [30, 0]，不重写 | 记录数：2；总分钟：30；平均分钟：15.0 |
| 5 再次 add 30 | [30, 0] | 同日期、同主题也会追加 | [30, 0, 30] | 已保存 3 条记录 |
| 6 summary | [30, 0, 30] | count=3，total=60，mean=20.0 | [30, 0, 30]，不重写 | 记录数：3；总分钟：60；平均分钟：20.0 |

表格仅列 minutes 方便手算；真实 JSON 每条记录还含 date 和 topic。可以用编辑器只读查看文件：应有三条记录，前后两条内容相同。这个项目没有去重规则，所以“同一条 add 再执行一次”会继续增加次数，不能当作无影响的重试。summary 只读取并计算，不创建缺失的记录文件，也不把已有记录归零。

相对路径从**终端当前工作目录**算起。上面从学习包根目录运行，文件就在根目录的 personal 下。如果进入 projects/01_study_log 再运行 python app.py，同样的 --store "personal/打卡 练习/round1.json" 会指向项目目录下另一份文件。可先运行以下命令查看当前位置；其中 -c 表示直接执行引号内的这段 Python。

```terminal
python -c "from pathlib import Path; print(Path.cwd())"
```

本程序有三种路径情况：显式传入的相对 --store 跟随当前工作目录；显式传入的绝对 --store 指向给定位置；完全省略 --store 时，默认用 app.py 所在目录的 outputs/study_log.json，因为源码用 __file__ 构建默认路径。每条 add 和 summary 都要选同一份文件，参数不会跨进程自动记住。换电脑后绝对路径通常需要修改，练习时优先完整复制学习目录并从根目录启动。

### 8 分层实操：预测、定位错误、迁移到 Agent 日志
**预测练习。** 接着上表的三条记录，再执行一次 summary，再添加 60 分钟，分别预测记录数、总分钟与平均分钟。然后在新的 round2.json 中只添加 0 分钟并汇总。先写答案，再在你自己的练习文件中验证。

解析：summary 仍是 3、60、20.0；追加 60 后汇总为 4、120、30.0。新文件仅一条 0 时为 1、0、0.0，不是暂无。None 表示没有记录；0.0 表示存在记录且平均值为零。反复运行预测练习前需要重新确认起始文件状态。

**纠错练习。** 以下命令故意把 --store 放错位置，它会报告 unrecognized arguments（无法识别的参数），退出状态为 2，不会保存记录。把 --store 及路径一起移到 add 前面才是本项目的正确写法；修正后会真的追加，先确认选择的是练习文件。

```terminal
python projects/01_study_log/app.py add 30 "Python 循环" --store "personal/打卡 练习/round1.json" --date 2026-10-07
```

错误可以发生在不同层。终端通常不会直接显示退出状态数字，先看错误内容；自检脚本会同时检查退出状态与文件内容。

| 改动或文件状态 | 停在哪一层 | 本项目的结果 |
| --- | --- | --- |
| 分钟填 abc 或 30.5 | argparse 的 int 转换 | 退出状态 2，记录文件不变 |
| 分钟填 -1 | validate_record 的非负规则 | 显示 无法完成：分钟必须是非负整数，状态 1，文件不变 |
| 主题填 "   " | strip 后检查空主题 | 显示 无法完成：主题不能为空，状态 1，文件不变 |
| 日期填 2026-02-30 | 日历日期验证 | 显示 无法完成 和日期错误，状态 1，文件不变 |
| 记录文件含 broken | JSON 解析 | 显示 无法完成 和解析错误，状态 1，保留损坏内容 |
| 记录文件含 {} | 最外层结构检查 | 显示 无法完成：记录文件最外层必须是列表，状态 1，保留内容 |

想试坏文件时，另建 personal/打卡 练习/broken-lab.json，只把这份实验文件的内容设为 broken，再用 --store 指向它运行 summary 或 add。不要改自己的打卡文件。文件不存在可以表示首次使用；已有文件损坏可能装着待恢复的学习记录，不能把解析异常一概改成 return [] 后覆盖。具体英文错误文字可能随 Python 版本变化，重点是错误层级及原字节是否保留。

**迁移练习。** 假设 Agent 的本地日志保存了 request_id、action、status：同一个请求是否只能执行一次？可以只按主题删除重复记录吗？这里只画三条字典记录并写判断，不连接模型或执行工具。

解析：先区分“一个请求”与“它的某次尝试”。同名 action 可以属于不同请求；同一 request_id 又可能有多次尝试，应另记 attempt。像本项目一样重复运行有写入动作的命令，会再次产生记录；仅靠日志字段还不能保证工具没有重复执行。保存成功说明记录写入成功，仍需分别判断工具执行结果和任务答案是否正确。分钟、日志条数与 token 数也不能互换。

知识链路：第 09 章把数据交给函数，第 11 章理解启动脚本，第 12 章定位与读写文件，第 13 章分层处理错误，再到第 16 章跟踪 Agent 的观察与结束条件。可在知识图谱中沿“路径与文件 → CSV / JSON / JSONL → 综合项目与验收”回查对应知识。

### 运行命令

从学习包根目录执行。Windows 用 py，Mac 用 python3，激活环境后可用 python。

```terminal
python projects/01_study_log/app.py add 30 "变量与类型" --date 2026-10-07
python projects/01_study_log/app.py add 60 "循环练习" --date 2026-10-08
python projects/01_study_log/app.py summary
```

### 预期结果

初始无记录时执行两次 add，分别显示已保存 1 条和 2 条；summary 显示记录数 2、总分钟 90、平均分钟 45.0。反复 add 会继续追加，所以重复练习前可使用 --store 指向另一个新的练习文件。

### 验收

运行学习包的 python tools/check_projects.py 核验参考实现；自己的实现按上面手算结果和边界逐项验证。
