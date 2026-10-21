# 教材维护说明

本项目是面向 GitHub 维护与分发的离线中文 Python 教材。当前 v1.3；学习目标优先于例题数量。仅维护本目录与同级的 Python-Zero-to-Practice.zip。README.md 是仓库入口，修改规模时同步更新统计；GitHub 工作流配置不等于已通过跨平台验证。

用户已确认：补充既有课程，账号 leon1111-wgl，公开并采用 MIT。现有发布位置为 leon1111-wgl/leon1111-wgl 仓库的 site/python-zero-to-practice/，下载包位于 site/downloads/Python-Zero-to-Practice.zip；不要另建同名独立课程仓库。网站原有 Leon 导航、字号、课程网址与进度键需一并保留。更新原仓库时仅同步这套课程、它的入口统计、构建/验证及 CI，避免覆盖其他课程或个人主页内容。

## 来源与范围

- 基础素材：course_data.py、project_data.py、starter_templates.py。
- v1.1 的重难点精讲及 AI / Agent 场景：refinements.py，通过 build.py 接入。
- v1.2 的状态传递、作用域排错与 JSONL 行定位：refinement_v12.py，在 v1.1 增补后接入。
- v1.3 的 CSV 数据校验与三层迁移实操：refinement_v13.py；GitHub 使用与贡献说明在 README.md、CONTRIBUTING.md。
- 本轮参考记录：根目录“开源参考与改编说明.md”，精确查询快照在 qa/open-source-review.json。qa 中的原文只供本地核对，不进入分发包。
- 高星数不是质量结论。每次只选与零基础当前进度相符的概念或练习方式；先看实际文件、许可、提交和前置知识，再用自己的数据和解释重新编写。
- info1110 是用户指定的首页标记；没有课程材料时，不推定官方课程覆盖、作业要求或官方授权。
- 第一阶段只使用标准库；所有当前 AI 例子为离线规则模拟。保留可预测输出，不把关键词匹配称为模型理解或向量检索。

## 保留学习者工作

开始修改前，记录已有 practice/、notes/、各项目 starter.py、TASKS.md 的逐文件 SHA-256。基线文件放 qa/ 并按本轮时间命名；不能一直拿历史基线判断学习者后来的合法改动。

重建会保留这些文件。tools/generated_files.json 记录上次生成文件的校验值；检测到手工修改时 build.py 会在写入前退出。不要删清单或更新校验值来跳过冲突。先复制并保留差异，区分教材生成变化与学习者编辑，再人工合并；需要用户决定时报告具体文件。

旧题号不能重排；新增题接在章末。网页 COURSE、KEY 和进度 schema 保留。旧进度导入后新增题应保持未完成。不要读取或清空用户真实浏览器数据；浏览器验证使用独立临时上下文。

不要覆盖实际运行输出或把它们加入发行包。更新包用于新目录解压；用户有自己的学习副本时，应保留 practice、notes、starter.py、TASKS.md 和导出的进度，再迁移教材版本。

## 修改与验收

1. 每轮选一到两个明确教学问题；先写预期行为和手算结果，再修改源稿。不要只换词、增加数量或更新星数便称为实质精修。
2. 运行 `python3 source/build.py`。Windows 用 `py` 替换 python3。统计数量来自实际数据，不能伪填。
3. 运行 `python3 tools/verify_examples.py`、`python3 tools/check_practice.py --all --solutions`、`python3 tools/check_projects.py`。查看真实退出状态与完整失败信息；只测参考答案不能声称学习者作答已通过。
4. 涉及维护保护或自检提示时运行 `python3 qa/check_refinement_guards.py`。这个脚本只在临时副本里故意修改示例、练习、笔记和项目模板。运行前按本轮的新基线核对真实学习文件，运行后再次核对。
5. 源码或 UI 变化后用用户 Mac 上已安装的 Chrome 做离线检查。qa/browser_check.cjs 使用官方提供的本机 Playwright 运行时，不安装另一套浏览器。例题数量变化时同步浏览器断言。保留旧版本导出样本，检查新题未误标完成。若运行环境缺少可用浏览器，记录限制，不能伪称通过。
6. 只有语法、示例、参考答案、项目及相关界面核验均满足发布要求后，更新“验证说明.md”和“维护记录.md”，再执行 `python3 tools/package.py`。它检查本地链接、ZIP 成员及逐字节一致性，排除 qa、缓存、虚拟环境、outputs、personal、环境密钥和导出的 progress JSON。
7. 需要复核迁移能力时，在临时的含空格/中文路径中解压并运行检查。当前未在真实 Windows 机器上运行，不能把 Mac 的迁移路径测试当成 Windows 实测。

源码核验使用 Python 3.12.2。教材保持 Python 3.10+ 语法，但每轮要如实写明本次实际解释器版本。

## 下一轮候选

- 第 09 / 13 章的状态传递与作用域修复已在 v1.2 完成，后续根据实际学习反馈再补其他边界。
- 第 12—13 章：JSONL 分层校验已在 v1.2 完成，CSV 字段检查与结束行定位已在 v1.3 完成；后续根据实际反馈再扩展，不重复堆题。
- 第 17 章：把一个完整项目拆成可独立运行的中间阶段，逐步展示输入、返回结构和测试；保护原有 TASKS.md 与 starter.py，新增讲解另存文件。

这些是待评审候选，不代表尚未完成的强制范围，也不必一轮全部加入。后续根据实际教材缺口更新。
