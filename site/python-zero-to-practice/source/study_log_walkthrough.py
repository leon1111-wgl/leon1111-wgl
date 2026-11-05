"""学习打卡项目的命令行与文件状态实操；保留原实现和学习者任务书。"""
from textwrap import dedent

STEPS = [
    ('给命令找位置：参数属于谁', r'''
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
'''),
    ('追踪持久化：关闭程序后，文件还在', r'''
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
'''),
    ('分层实操：预测、定位错误、迁移到 Agent 日志', r'''
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
'''),
]

CLI_CHECKS = r'''
# 使用复制到临时目录的实际 app.py 检查命令行，绝不触碰学习者默认记录。
import os
import shutil
import subprocess
import sys
cli_dir = temp / "打卡 命令行"
cli_dir.mkdir()
cli_app = cli_dir / "app.py"
shutil.copyfile(project_dir / "app.py", cli_app)
cli_cwd = temp / "开始 目录"
cli_cwd.mkdir()
cli_other = temp / "另一 目录"
cli_other.mkdir()
cli_env = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8")
def cli_run(*args, cwd=cli_cwd, status=0):
    result = subprocess.run([sys.executable, "-X", "utf8", str(cli_app), *args],
        cwd=cwd, env=cli_env, capture_output=True, text=True, encoding="utf-8", timeout=3)
    assert result.returncode == status, (args, result.stdout, result.stderr)
    if status == 0:
        assert result.stderr == "", result.stderr
    else:
        assert result.stdout == "", result.stdout
    return result

assert "--store" in cli_run("--help").stdout
cli_help = cli_run("add", "--help").stdout
assert "--date" in cli_help and "--store" not in cli_help
cli_relative = "personal/打卡 练习/round1.json"
cli_path = cli_cwd / cli_relative
cli_empty = "记录数：0\n总分钟：0\n平均分钟：暂无\n"
assert cli_run("--store", cli_relative, "summary").stdout == cli_empty
assert not cli_path.exists()
cli_inputs = [("30", "Python 循环", "2026-10-07"), ("0", "复习记录", "2026-10-08")]
for cli_index, cli_values in enumerate(cli_inputs, start=1):
    assert cli_run("--store", cli_relative, "add", *cli_values[:2], "--date", cli_values[2]).stdout == f"已保存 {cli_index} 条记录\n"
cli_expected = [{"date": day, "minutes": int(minutes), "topic": topic} for minutes, topic, day in cli_inputs]
assert json.loads(cli_path.read_text(encoding="utf-8")) == cli_expected
cli_before = cli_path.read_bytes()
assert cli_run("--store", cli_relative, "summary").stdout == "记录数：2\n总分钟：30\n平均分钟：15.0\n"
assert cli_path.read_bytes() == cli_before
assert cli_run("--store", cli_relative, "add", "30", "Python 循环", "--date", "2026-10-07").stdout == "已保存 3 条记录\n"
cli_expected.append(dict(cli_expected[0]))
assert json.loads(cli_path.read_text(encoding="utf-8")) == cli_expected
cli_summary = "记录数：3\n总分钟：60\n平均分钟：20.0\n"
cli_before = cli_path.read_bytes()
assert cli_run("--store", cli_relative, "summary").stdout == cli_summary
assert cli_run("--store", cli_relative, "summary").stdout == cli_summary
assert cli_path.read_bytes() == cli_before

# 参数顺序、转换、业务校验分别失败；每次都检查已有字节未变。
cli_bad = [
    (["add", "30", "Python 循环", "--store", cli_relative], 2, "unrecognized arguments"),
    (["--store", cli_relative, "add", "abc", "X"], 2, "invalid int value"),
    (["--store", cli_relative, "add", "30.5", "X"], 2, "invalid int value"),
    (["--store", cli_relative, "add", "-1", "X"], 1, "分钟必须是非负整数"),
    (["--store", cli_relative, "add", "1", "   "], 1, "主题不能为空"),
    (["--store", cli_relative, "add", "1", "X", "--date", "2026-02-30"], 1, "无法完成："),
]
for cli_args, cli_status, cli_error in cli_bad:
    assert cli_error in cli_run(*cli_args, status=cli_status).stderr
    assert cli_path.read_bytes() == cli_before

# 同相对路径在不同 cwd 指向不同文件；绝对路径仍指回原文件。
assert cli_run("--store", cli_relative, "summary", cwd=cli_other).stdout == cli_empty
assert not (cli_other / cli_relative).exists()
assert cli_run("--store", str(cli_path), "summary", cwd=cli_other).stdout == cli_summary
assert cli_run("summary", cwd=cli_other).stdout == cli_empty
assert not (cli_dir / "outputs").exists()
cli_run("add", "0", "  默认记录  ", "--date", "2026-10-07", cwd=cli_other)
assert cli_run("summary", cwd=cli_cwd).stdout == "记录数：1\n总分钟：0\n平均分钟：0.0\n"
assert json.loads((cli_dir / "outputs/study_log.json").read_text(encoding="utf-8"))[0]["topic"] == "默认记录"
assert cli_path.read_bytes() == cli_before

# 分层练习的追加结果与单零记录。
cli_run("--store", cli_relative, "add", "60", "预测", "--date", "2026-10-09")
assert cli_run("--store", cli_relative, "summary").stdout == "记录数：4\n总分钟：120\n平均分钟：30.0\n"
cli_round2 = "personal/打卡 练习/round2.json"
cli_run("--store", cli_round2, "add", "0", "预测", "--date", "2026-10-09")
assert cli_run("--store", cli_round2, "summary").stdout == "记录数：1\n总分钟：0\n平均分钟：0.0\n"
cli_broken = cli_cwd / "broken-lab.json"
for cli_content in ["broken", "{}"]:
    cli_broken.write_text(cli_content, encoding="utf-8")
    for cli_action in [("summary",), ("add", "1", "X")]:
        assert "无法完成：" in cli_run("--store", str(cli_broken), *cli_action, status=1).stderr
        assert cli_broken.read_bytes() == cli_content.encode("utf-8")
'''


def attach_study_log_walkthrough(projects):
    project = next(p for p in projects if p['folder'] == '01_study_log')
    project['steps'].extend((title, dedent(body).strip()) for title, body in STEPS)
    project['checks'] += '\n' + dedent(CLI_CHECKS).strip() + '\n'
