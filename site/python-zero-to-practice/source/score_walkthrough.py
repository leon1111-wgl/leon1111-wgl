"""成绩项目的原创分步讲解；单独生成文件，保留学习者骨架与任务书。"""
from html import escape
from textwrap import dedent

FOLDER = 'projects/02_score_report'
INTRO = '''
### 从一个函数走到一个项目
你已经见过 strip、int、for、字典和 return；现在要练的是让它们各负责一层，再把上一层的返回值交给下一层。先不同时面对文件、命令行和报告保存。

这四阶段沿用原成绩项目的约定。原 app.py 的 analyze 把清洗和统计写在一个函数里；下面把同样的行为拆成小函数，便于你实现自己的 starter.py。它们是教学参考文件，原项目不会自动调用这些新文件。

前置：第 03 章字符串、第 04—05 章条件与循环、第 08—09 章记录与函数、第 10 章排序、第 11—13 章模块、CSV 与异常。卡在一个知识点时，先回图谱看关联例子。

### 开始前：文件放在一起，函数逐层接好
完整解压学习包，再在根目录运行命令。Windows 把 python 换成 py；macOS 换成 python3。四个阶段文件放在 projects/02_score_report/guided 中，后面的文件会 import 前面的函数；单独下载一个阶段文件会缺少依赖。

每张预期输出都对应未修改的参考文件。改写前，先把 guided 与 data 两个文件夹复制到自己新建的 personal/score-lab 中，保持同级关系。进入下一阶段前恢复副本中的基准数据和规则，或另用新副本：后续会 import 前面的函数与样本；如果保留改动，后续结果也可能变化，需要重新手算。

每个阶段的 main 都给出一个固定小实验，运行时先预测再核对。导入文件时只取得函数，不执行 main 里的演示；这就是第 11 章 __name__ 入口判断的用途。所有阶段把结果打印到终端，第 4 阶段读取项目自带的 CSV。

| 阶段 | 输入 | 返回给下一层 | 暂时不用考虑 |
| --- | --- | --- | --- |
| 1 parse_row | 一条字符串字段字典 | 一个含整数 score 的新字典 | 一整张表、重复 ID |
| 2 collect_rows | 多条原始字典 | (valid, errors) 两个列表 | 文件从哪里读取 |
| 3 summarize | 通过校验的记录列表 | 统计结果字典 | 重新清洗原始字符串 |
| 4 read_valid_rows / analyze | CSV 文件路径 | 有效与错误列表 / 完整报告 | 命令行参数和保存报告 |

### 输入约定先说清楚
本组 parse_row 接受 csv.DictReader 产生的字典：字段值通常是字符串，缺列可能是 None，超出表头列数的字段会收在 None 键下。练习中的内存样例遵循同一约定；任意 JSON 里的布尔值、列表或嵌套对象不属于这个函数的输入范围，应先按第 13 章检查类型。

项目必需列是 student_id、name、score；表头允许声明额外列，清洗结果只保留三个必需字段。分数用 int 转换，再检查 0—100；不是用字符串字典序比较，也不是把非零都当成合格。姓名与学号去掉首尾空白，学号按原大小写精确比较。
'''.strip()

STAGES = []
def stage(key, title, filename, body, code, output, task, hint, answer):
    STAGES.append(dict(key=key,title=title,file=filename,body=dedent(body).strip(),
                       code=dedent(code).strip()+'\n',output=dedent(output).strip()+'\n',
                       task=task,hint=hint,answer=answer))

stage('stage1','阶段 1：先把一条记录变正确','step01_parse.py',r'''
### 逐句追踪：字符串怎样变成数字
给 parse_row 一条记录，它只决定这条记录是否合法，并返回一个新字典。检查失败时 raise ValueError 结束本次调用，由调用者决定怎样记录错误。

| 执行位置 | 中间值 | 为什么需要它 |
| --- | --- | --- |
| raw["name"] | " 小林 " | 这是原始文本，包含空白 |
| name = (...).strip() | "小林" | 返回新字符串，保存到局部名字 |
| raw["score"] | "60" | 这是 str，还没转成数字 |
| score = int(...) | 60 | 得到可比较、可累计的 int |
| 0 <= score <= 100 | True | 转换成功后仍要检查范围 |
| return {...} | 一个新字典 | 外层 record 接住清洗结果 |

(row.get("score") or "") 中的 or 把缺列的 None 转成空字符串，再由 int 明确报错。这里原始零分是字符串 "0"，不是整数 0，因此不会被 or 丢掉。不要把这句机械套到已经是整数的字典上。

演示输出中的 !r 会显示字符串引号，方便看见空白；type(...).__name__ 只用于显示 int 这样的类型名称。先关注原值与返回值如何变化，不需要在第一遍记住这些显示写法。

try 只包住整数转换；分数范围另行判断。abc 是转换失败，101 是范围失败，0 是有效边界。函数不负责记错误列表，也不负责判断重复学号。
''',r'''
"""阶段 1：一条 CSV 字段字典 -> 一条清洗后的记录。"""

def parse_row(row):
    """仅接受 DictReader 形式的字段；不修改输入字典。"""
    if None in row:
        raise ValueError("字段数超过表头列数")
    student_id = (row.get("student_id") or "").strip()
    name = (row.get("name") or "").strip()
    if not student_id or not name:
        raise ValueError("ID 或姓名为空")
    try:
        score = int(row.get("score") or "")
    except ValueError:
        raise ValueError("分数不是整数") from None
    if not 0 <= score <= 100:
        raise ValueError("分数超出 0 到 100")
    return {"student_id": student_id, "name": name, "score": score}


def main():
    raw = {"student_id": "s1", "name": " 小林 ", "score": "60"}
    record = parse_row(raw)
    print(f"原始：name={raw['name']!r}，score={raw['score']!r}")
    print(f"清洗后：name={record['name']!r}，score={record['score']}，类型={type(record['score']).__name__}")
    for value in ["0", "abc", "101"]:
        try:
            result = parse_row({"student_id": "s2", "name": "小安", "score": value})
            print(f"{value!r} -> 保留 {result['score']}")
        except ValueError as error:
            print(f"{value!r} -> 拒绝：{error}")


if __name__ == "__main__":
    main()
''',r'''
原始：name=' 小林 '，score='60'
清洗后：name='小林'，score=60，类型=int
'0' -> 保留 0
'abc' -> 拒绝：分数不是整数
'101' -> 拒绝：分数超出 0 到 100
''',
'先不运行：分别把 score 改为 "100"、"-1"、"60.5"、None，预测是返回还是报错。再说明为什么 raw 中的姓名仍有空格。',
'先看 int 能否完成，再看范围；return 创建了新的字典。',
'100 返回整数 100；-1 转换成功但超范围；60.5 不是可由 int 直接解析的整数字符串；None 被替换为 "" 后转换失败。strip 返回的新字符串只放进新字典，没有给 raw["name"] 重新赋值。')

stage('stage2','阶段 2：连接循环、错误列表与去重','step02_collect.py',r'''
### 循环的状态放在哪里
valid 保存已保留的记录，errors 保存被拒记录的原因，seen 保存已保留的学号。三个容器都在函数内部、循环之前新建：每次调用重新开始，每轮则继续使用同一份状态。

下面固定输入的分数依次是 60、abc、0、90、90；第 2、3 条是同一学号 s2，第 1、4 条是同一学号 s1。

| 记录号 | 当前输入 | 本轮动作 | 本轮后有效数 / 错误数 |
| --- | --- | --- | --- |
| 1 | s1 / 60 | 清洗成功，登记 s1 | 1 / 0 |
| 2 | s2 / abc | 转换失败，只记录错误，不登记 s2 | 1 / 1 |
| 3 | s2 / 0 | s2 尚未保留，合法零分进入 valid | 2 / 1 |
| 4 | s1 / 90 | 清洗成功，但 s1 已保留，记重复 | 2 / 2 |
| 5 | s3 / 90 | 清洗成功，登记 s3 | 3 / 2 |

except 中的 continue 立即开始下一轮，所以失败记录不会进入下面的 seen.add 和 valid.append。错误发生在 parse_row 时，外层 try 也能捕获它；函数调用是正常执行过程的一部分。

return valid, errors 实际返回一个二元组。外层 valid, errors = collect_rows(...) 按位置接住两个列表；这与函数内部局部名字恰好同名无关。此处的 record 是从 1 开始的逻辑记录号，不是 CSV 文件物理行号。
''',r'''
"""阶段 2：内存中的原始记录 -> 有效记录和错误列表。"""
from step01_parse import parse_row


def collect_rows(rows):
    valid = []
    errors = []
    seen = set()
    for record_number, row in enumerate(rows, start=1):
        try:
            record = parse_row(row)
            if record["student_id"] in seen:
                raise ValueError("重复 ID")
        except ValueError as error:
            errors.append({"record": record_number, "reason": str(error)})
            continue
        seen.add(record["student_id"])
        valid.append(record)
    return valid, errors


def sample_rows():
    return [
        {"student_id": "s1", "name": " 小林 ", "score": "60"},
        {"student_id": "s2", "name": "小安", "score": "abc"},
        {"student_id": "s2", "name": "小安", "score": "0"},
        {"student_id": "s1", "name": "小林", "score": "90"},
        {"student_id": "s3", "name": "小周", "score": "90"},
    ]


def main():
    valid, errors = collect_rows(sample_rows())
    print("有效学号：", [row["student_id"] for row in valid])
    print("有效分数：", [row["score"] for row in valid])
    for error in errors:
        print(f"记录 {error['record']}：{error['reason']}")


if __name__ == "__main__":
    main()
''',r'''
有效学号： ['s1', 's2', 's3']
有效分数： [60, 0, 90]
记录 2：分数不是整数
记录 4：重复 ID
''',
'把第二条 s2/abc 改成 s2/80，其他数据不变，先预测新的有效分数和错误记录号；再预测连续调用 collect_rows 两次是否会累积重复错误。',
'每个学号保留第一条有效记录；seen 在函数内何时新建？',
'有效分数变成 [60, 80, 90]。第三条 s2/0 变为重复，第四条 s1/90 仍重复，错误记录号是 3、4。每次调用都新建 seen，因此第二次结果与第一次相同；把 seen 写成共享的默认参数会破坏这个约定。')

stage('stage3','阶段 3：让返回值进入统计函数','step03_summary.py',r'''
### 两个函数怎样接起来
collect_rows 接收原始字符串字典；summarize 接收清洗后的有效字典，它依赖 score 已是 0—100 的整数。这是函数之间约定好的接口，不能把错误列表或原始 rows 传进去凑数。

| 顺序 | count | total | passed | 原因 |
| --- | --- | --- | --- | --- |
| 开始 | 3 | 0 | 0 | valid 有三条记录 |
| 读到 60 | 3 | 60 | 1 | 恰好达到及格线 |
| 读到 0 | 3 | 60 | 1 | 有效，但没有及格 |
| 读到 90 | 3 | 150 | 2 | 又有一人及格 |
| 循环结束 | 3 | 150 | 2 | 平均 150/3=50，及格率 2/3 |

分母必须是有效人数 3，不是输入行数 5，也不是去掉零分后剩下的 2。没有有效记录时，平均分和及格率都用 None 表示没有可计算的值；0.0 会误导为已观察到零平均分。

ranking_key 为每条记录返回 (-score, student_id)。负号让高分排前面；分数相同时比较学号。传给 sorted 的是函数名字 ranking_key，排序时 Python 才对每条记录调用它。sorted 创建新的列表，不改变 valid 的顺序。
''',r'''
"""阶段 3：有效记录 -> 可继续使用的统计结果。"""
from step02_collect import collect_rows, sample_rows


def ranking_key(row):
    return (-row["score"], row["student_id"])


def summarize(records):
    """前置：records 已清洗，每条 score 是 0—100 的整数。"""
    count = len(records)
    total = 0
    passed = 0
    for row in records:
        total += row["score"]
        if row["score"] >= 60:
            passed += 1
    return {
        "valid_count": count,
        "total": total,
        "mean": total / count if count else None,
        "pass_rate": passed / count if count else None,
        "ranking": sorted(records, key=ranking_key),
    }


def main():
    valid, errors = collect_rows(sample_rows())
    report = summarize(valid)
    print(f"有效 {report['valid_count']} 条，无效 {len(errors)} 条")
    print(f"总分 {report['total']}，平均分 {report['mean']:.1f}")
    print(f"通过率 {report['pass_rate']:.1%}")
    print("排名：", [row["student_id"] for row in report["ranking"]])
    empty = summarize([])
    print(f"空列表：人数 {empty['valid_count']}，平均分 {empty['mean']}，通过率 {empty['pass_rate']}")


if __name__ == "__main__":
    main()
''',r'''
有效 3 条，无效 2 条
总分 150，平均分 50.0
通过率 66.7%
排名： ['s3', 's1', 's2']
空列表：人数 0，平均分 None，通过率 None
''',
'在自己的学习副本中，把及格线从 60 改为 70。预测人数、总分、平均分、及格率和排名中，哪些应该变化？不要同时改合法分数的范围。',
'及格线决定 passed，合法范围决定 valid；它们分别属于哪一层？',
'只改 summarize 中的 if row["score"] >= 70。三条仍有效，总分仍 150，均值仍 50.0，排名不变；只有 90 及格，比例从 2/3 变为 1/3，显示 33.3%。修改 parse_row 的 0—100 范围会改变样本集合，是另一种需求。')

stage('stage4','阶段 4：接入 CSV，保持前三层不变','step04_file.py',r'''
### 文件层只负责把记录交出去
前面三步已在内存小样例上验证。现在 read_valid_rows 用 DictReader 从文件中逐条提供字典，交给 collect_rows；它不重写清洗逻辑。analyze 再把 valid 交给 summarize，并把 errors 放进最终报告。

调用链：analyze(path) → read_valid_rows(path) → collect_rows(reader) → 每轮 parse_row(row)；拿到 valid 后再 summarize(valid)。箭头表示调用顺序，返回时结果会沿调用位置交回去。

return collect_rows(reader) 必须留在 with 内。reader 按需读取文件；如果离开 with 后才遍历，文件已经关闭。collect_rows 在文件仍打开时完成读取，返回的是两个普通列表，因此离开 with 后继续统计没有问题。

encoding="utf-8-sig" 可读取带或不带 UTF-8 BOM 的文件；newline="" 让 csv 处理记录换行。这个项目按逻辑记录编号，带引号的姓名跨两行仍算一条记录。第 13 章 13_09 则刻意记录结束物理行号，两种字段含义不要混用。

默认数据路径相对脚本文件定位：从 guided/step04_file.py 的父目录再上一级，就到 02_score_report，然后读取 data/scores.csv。更换终端工作目录不会改变这个默认文件位置。

### 与完整 app.py 对齐
这一步用原项目九条记录，应得到有效 5、无效 4、总分 299、均值 59.8、及格率 60.0%。analyze 返回的整个报告与原 app.py 相同；只有函数拆分方式不同。之后再读原项目的 save_report 与 argparse 入口，理解怎样把已经验证过的报告保存到指定目录。

缺失必需表头、找不到文件或 csv 解析器报错会向调用处传播。只有针对某条记录的 ValueError 才由 collect_rows 转成错误记录。不要包住整个项目后静默返回空列表，否则会把失败伪装成“没有成绩”。
''',r'''
"""阶段 4：读取项目 CSV，复用前三层，只把报告打印到终端。"""
import csv
from pathlib import Path
from step02_collect import collect_rows
from step03_summary import summarize


def read_valid_rows(path):
    with path.open(encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        required = {"student_id", "name", "score"}
        if not required.issubset(set(reader.fieldnames or [])):
            raise ValueError("缺少必需列 student_id、name、score")
        return collect_rows(reader)


def analyze(path):
    valid, errors = read_valid_rows(path)
    report = summarize(valid)
    report["invalid_count"] = len(errors)
    report["errors"] = errors
    return report


def main():
    source = Path(__file__).resolve().parent.parent / "data" / "scores.csv"
    report = analyze(source)
    print(f"有效 {report['valid_count']} 条，无效 {report['invalid_count']} 条")
    print(f"总分 {report['total']}")
    if report["mean"] is None:
        print("没有有效分数，无法计算平均分与通过率")
    else:
        print(f"平均分 {report['mean']:.1f}")
        print(f"通过率 {report['pass_rate']:.1%}")
    print("错误记录号：", [error["record"] for error in report["errors"]])


if __name__ == "__main__":
    main()
''',r'''
有效 5 条，无效 4 条
总分 299
平均分 59.8
通过率 60.0%
错误记录号： [6, 7, 8, 9]
''',
'先在自己的练习目录准备只有表头的 CSV，再准备缺少 score 表头的 CSV。分别预测 analyze 应返回什么，或应该报什么错。',
'有完整表头但无记录，是合法空输入；缺必需表头，是数据格式约定失败。',
'只有完整表头：valid_count=0、invalid_count=0、total=0、mean=None、pass_rate=None，ranking/errors 为空列表。缺少 score 表头：抛 ValueError("缺少必需列 student_id、name、score")；不能把它算成零个有效成绩。')

TRANSFER_BODY = r'''
### 迁移练习：把成绩清洗改成工具耗时日志
先关闭答案，新建自己的 .py 文件实现 clean_tool_rows(rows)。输入仍是类似 CSV 解析结果的字符串字段字典，但字段改为 id、tool、ms。id 与 tool 去首尾空白后非空；ms 可转换成非负整数，0 有效且没有 100 的上限。保留每个 id 的第一条有效记录，不修改原输入。

返回 (valid, errors)。valid 每项只保留 id、tool、ms，其中 ms 为 int。errors 每项用 record（从 1 开始的逻辑记录号）与 reason；按输入顺序记录。错误检查顺序与精确文字如下：

| 检查 | reason |
| --- | --- |
| 存在 None 键，表示超出表头列数 | 字段数超过表头列数 |
| id 或 tool 为空 | ID 或工具名为空 |
| ms 转整数失败或缺失 | 耗时不是整数 |
| ms 小于 0 | 耗时不能为负数 |
| id 已保留 | 重复 ID |

手算以下五条：t1/search/0，t2/fetch/250，t3/search/bad，t3/search/30，t1/fetch/8。预期保留 t1、t2、t3，耗时 [0, 250, 30]，合计 280 毫秒；第 3 条转整数失败，第 5 条重复。再测试空列表，以及同一 ID 的第一条负耗时、第二条 1000 毫秒。

这里是本地日志整理，不调用模型或工具服务。毫秒不是 token 数；耗时能解析也不代表工具执行成功，更不能证明用户任务答对了。真正分析任务正确性时，需要额外的任务结果与评估规则，不能从 ms 推出来。
'''

stage('transfer','迁移：工具耗时日志','transfer_tool_rows.py',TRANSFER_BODY,r'''
"""迁移参考：只整理固定日志，不调用模型或外部工具。"""

def clean_tool_rows(rows):
    valid = []
    errors = []
    seen = set()
    for record_number, row in enumerate(rows, start=1):
        try:
            if None in row:
                raise ValueError("字段数超过表头列数")
            task_id = (row.get("id") or "").strip()
            tool = (row.get("tool") or "").strip()
            if not task_id or not tool:
                raise ValueError("ID 或工具名为空")
            try:
                milliseconds = int(row.get("ms") or "")
            except ValueError:
                raise ValueError("耗时不是整数") from None
            if milliseconds < 0:
                raise ValueError("耗时不能为负数")
            if task_id in seen:
                raise ValueError("重复 ID")
        except ValueError as error:
            errors.append({"record": record_number, "reason": str(error)})
            continue
        seen.add(task_id)
        valid.append({"id": task_id, "tool": tool, "ms": milliseconds})
    return valid, errors


def sample_logs():
    return [
        {"id": "t1", "tool": "search", "ms": "0"},
        {"id": "t2", "tool": "fetch", "ms": "250"},
        {"id": "t3", "tool": "search", "ms": "bad"},
        {"id": "t3", "tool": "search", "ms": "30"},
        {"id": "t1", "tool": "fetch", "ms": "8"},
    ]


def main():
    valid, errors = clean_tool_rows(sample_logs())
    print("保留 ID：", [row["id"] for row in valid])
    print("耗时：", [row["ms"] for row in valid])
    print("总耗时：", sum(row["ms"] for row in valid), "毫秒")
    for error in errors:
        print(f"记录 {error['record']}：{error['reason']}")


if __name__ == "__main__":
    main()
''',r'''
保留 ID： ['t1', 't2', 't3']
耗时： [0, 250, 30]
总耗时： 280 毫秒
记录 3：耗时不是整数
记录 5：重复 ID
''',
'独立写完 clean_tool_rows 后，向一个空列表输入调用两次；再试同一 ID 的 -1 与 1000 毫秒。说明哪些成绩规则能够复用，哪些必须修改。',
'可以复用字段清洗、错误列表、第一条有效记录保留；重新审视数值字段与合法范围。',
'两次空输入均返回 ([], [])。-1 记录错误但不登记 ID，1000 被保留。把 score 换成 ms 还不够：必须去掉 100 上限，删去成绩及格率的含义，并把错误原因改成日志领域的用词；不要用耗时推断任务成功。')

OUTRO = '''
### 把参考文件里的思路带回自己的骨架
先打开你已有的 starter.py，只完成 parse_row，用三条手写字典验证；再实现 summarize，验证空列表、0 分、刚好 60 分；最后实现 read_valid_rows，把文件读取、循环收集和重复检查连接起来。

你可以把 collect_rows 作为新辅助函数写入自己的骨架，也可以把同样逻辑放进 read_valid_rows；重点是输入、输出与错误约定一致。不要把这些函数写成只 print 不 return，否则下一层接到的是 None。

改写练习先新建 personal/score-lab，把原项目的 guided 和 data 两个文件夹完整复制进去，形成 personal/score-lab/guided 与 personal/score-lab/data。这样既保留同级模块，也保留第 4 阶段依赖的数据位置。然后运行、修改副本中的文件，例如 python personal/score-lab/guided/step03_summary.py。若同名练习目录已存在，请另取新名字。personal 中的个人练习不会进入维护者发行包。

### 自己验收的顺序
先单独运行五个参考文件对照预期输出；再从学习包根目录运行 python tools/check_score_walkthrough.py，它只检查本教材的分步参考。python tools/check_projects.py 也包含这些检查，但不会替你运行或判定个人 starter.py。

自己的代码先用手算样例核对，再分别测：空输入、全部无效、零分、60、100、-1、101、缺字段、超列、同分排序、无效记录后出现有效同 ID、重复调用。错误列表也要检查记录号和原因，不能只看最终平均数。

遇到多文件错误时，先看 traceback 最后一行的异常类型，再沿文件名找出调用来自哪一层。ModuleNotFoundError 先检查是否完整解压、同级阶段文件是否齐全；ValueError 先检查对应数据；不要遇到任何错误都重新安装 Python。
'''.strip()


def walkthrough_text():
    parts=['# 成绩项目：四阶段实操与工具日志迁移',INTRO]
    for s in STAGES:
        command='python '+FOLDER+'/guided/'+s['file']
        parts += ['## '+s['title'],s['body'],'运行：\n```terminal\n'+command+'\n```',
                  '预期输出：\n```text\n'+s['output']+'```',
                  '练习：'+s['task'],'提示：'+s['hint'],'解析：'+s['answer'],
                  '参考实现：\n```python\n'+s['code']+'```']
    parts.append(OUTRO)
    return '\n\n'.join(parts)+'\n'


def walkthrough_html(md, codeblock):
    out=['<section class="score-walkthrough" id="c17-score-walkthrough"><div class="eyebrow">STEP BY STEP · 从函数到项目</div><h4>成绩项目：四阶段实操</h4>',md(INTRO,'c17-score-intro')]
    out.append('<p><a href="'+FOLDER+'/GUIDE.md" download>保存分步讲义与解析</a> · <a href="#c00-map-project" data-map-node="project">回到知识图谱</a></p>')
    for s in STAGES:
        target='c17-score-'+s['key']
        command='python '+FOLDER+'/guided/'+s['file']
        out += [f'<section class="walkthrough-step" id="{target}"><h4>{escape(s["title"])}</h4>',md(s['body'],target),
                '<h5>运行本阶段</h5>',codeblock(command,'终端命令'),
                '<details class="walkthrough-output"><summary>先预测，再查看预期输出</summary>'+codeblock(s['output'],'程序输出',False)+'</details>',
                '<p class="try"><b>动手练习：</b>'+escape(s['task'])+'</p>',
                '<details><summary>一点提示</summary><p>'+escape(s['hint'])+'</p></details>',
                '<details class="walkthrough-answer"><summary>改写结果与解析</summary><p>'+escape(s['answer'])+'</p></details>',
                '<details class="walkthrough-code"><summary>展开本阶段参考代码</summary>'+codeblock(s['code'])+'</details>',
                '<p class="fileline">文件：<a href="'+FOLDER+'/guided/'+s['file']+'" download>'+s['file']+'</a>；请保持完整包中的同级文件。</p></section>']
    out += [md(OUTRO,'c17-score-outro'),'</section>']
    return ''.join(out)


def attach_checks(projects):
    score=next(p for p in projects if p['folder']=='02_score_report')
    score['checks']+='\n\n# 同一项目门槛同时验证分步参考与迁移练习。\nimport runpy\nwalkthrough = runpy.run_path(str(project_dir.parents[1] / "tools/check_score_walkthrough.py"))\nwalkthrough["check"](project_dir)\n'
