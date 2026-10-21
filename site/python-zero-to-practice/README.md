# Python 零基础实操教程

**部分内容为info1110课程**

从第一行 `print` 到独立完成数据处理小项目的中文教材。面向没有编程经验的学习者，先补足 Python 基础，再用大模型与 Agent 的小场景解释这些基础将来怎样用。

本教材继续维护于 [Leon 的原有课程目录](https://github.com/leon1111-wgl/leon1111-wgl/tree/main/site/python-zero-to-practice)，沿用 [原在线阅读地址](https://leon1111-wgl.github.io/leon1111-wgl/python-zero-to-practice/index.html)。这是原课程的增补版，保留旧章节、题号和进度存储格式。

当前 v1.3：**19 个单元 · 105 个可运行示例 · 114 道分层练习 · 4 个项目**。阅读完全离线，第一阶段代码只使用 Python 标准库，无需 API Key、付费服务或第三方框架。

## 现在开始

1. [下载完整 Python 学习包](https://leon1111-wgl.github.io/leon1111-wgl/downloads/Python-Zero-to-Practice.zip)，完整解压到自己的学习文件夹。也可下载整个 GitHub 仓库，然后进入 `site/python-zero-to-practice/`。不要在 ZIP 预览窗口内运行代码。
2. 双击解压后的 **index.html**。第 00 章包含 Windows / macOS 的安装、编辑和运行步骤。GitHub 文件页面只显示 HTML 源码，下载后才能使用完整网页。
3. 安装官网仍受支持的 Python 3。教材使用 Python 3.10+ 语法；本轮本机验证解释器为 3.12.2。
4. 在终端进入解压目录，运行第一个示例，再编辑 `practice/ch01/ex01_01.py` 独立作答。

| 操作 | Windows | macOS |
| --- | --- | --- |
| 查看解释器 | `py --version` | `python3 --version` |
| 运行示例 | `py examples/ch01/ex01_01.py` | `python3 examples/ch01/ex01_01.py` |
| 检查自己的第 01_01 题 | `py tools/check_practice.py 01_01` | `python3 tools/check_practice.py 01_01` |
| 检查自己第 09 章的作答 | `py tools/check_practice.py --chapter 09` | `python3 tools/check_practice.py --chapter 09` |

刚下载的作答文件是空模板，自检不通过是正常的。网页负责阅读、记录与预设演示；实际 Python 代码在本机解释器运行。纯文字版本见 [textbook.md](textbook.md)。

## 每课怎样学

**读懂输入 → 手写预测 → 运行对照 → 每次改一个条件 → 独立作答 → 次日关掉答案重写。**

每章都有学习目标、逐步解释、可运行例子、预期输出、改写任务、练习提示与参考解析。不要把“看懂答案”勾成“独立完成”。例如第 13 章的 CSV 清洗先追踪字符串如何变成数字，再练习空行、缺列、零值与错误定位，最后迁移到工具日志汇总。

## 学习路线

| 单元 | 重点 | 能独立完成什么 |
| --- | --- | --- |
| 00—03 | 安装、输出、变量、类型、字符串 | 从终端运行文件，处理输入和文本 |
| 04—06 | 条件、for、while | 做选择、累计数据、限制重复步骤 |
| 07—10 | 列表、字典、函数、推导式与排序 | 看懂嵌套数据，明确参数与返回值 |
| 11—13 | 模块、环境、文件、异常、验证 | 读写 CSV / JSON / JSONL，定位坏数据 |
| 14—16 | 类、迭代、数据处理与 AI 场景 | 管理独立状态，跟踪批次和工具流程 |
| 17 | 四个完整项目 | 打卡本、成绩清洗、文本清洗、数据集流水线 |
| 18 | 八周路线、复习与综合自测 | 发现基础缺口，准备下一阶段学习 |

大模型 / Agent 场景包括消息列表、提示词字符串、工具参数、返回字典、会话状态、模拟流式片段、循环预算和数据校验。它们均为**固定规则和本地数据模拟**。字符不等于 token，格式合法不等于内容正确，流程跑完不等于任务完成。

## 文件放在哪里

| 路径 | 用途 |
| --- | --- |
| `index.html` | 可搜索、可折叠答案的离线网页，支持笔记和进度导入导出 |
| `examples/` | 与正文对应的运行示例 |
| `practice/` | 留给你独立作答的文件 |
| `solutions/` | 配套参考答案 |
| `projects/` | 四个项目的任务书、骨架、数据和参考实现 |
| `notes/` | 空白错题本、学习记录与迁移清单 |
| `source/` | 教材源稿、网页样式与生成程序 |
| `tools/` | 作答自检、项目验收和打包工具 |

## 换电脑与更新

复制整个学习文件夹，并在网页点击“导出进度”；另一台电脑打开教材后再“导入进度”。浏览器进度不会随 GitHub 自动同步。导入前先导出备份，因为导入会替换当前网页进度。

更新教材时解压到**新目录**，备份并迁移自己的 `practice/`、`notes/`、项目 `starter.py`、`TASKS.md`、运行输出与进度文件。维护仓库中的这些文件是初始模板；最省心的做法是把作答留在单独的学习副本。若用 Git 提交贡献，检查差异，避免将私人笔记和作答误推到公共仓库。

## 参考项目与来源

| 项目 | 借鉴方向 | 本教材中的落实 |
| --- | --- | --- |
| [Python-100-Days](https://github.com/jackfrued/Python-100-Days) | 基础到实践的组织方式 | 按先修知识安排章节；未复制文字或题目 |
| [30-Days-Of-Python](https://github.com/Asabeneh/30-Days-Of-Python) | 分阶段学习与分层练习 | CSV 的读懂、改写、迁移三层实操；未复制代码或题目 |
| [ai-agents-for-beginners](https://github.com/microsoft/ai-agents-for-beginners) | 工具调用与反馈流程 | 函数、校验和执行轨迹 |
| [LLMs-from-scratch](https://github.com/rasbt/LLMs-from-scratch) | 文本到模型输入的概念链条 | 字符、token、编码和批次的边界 |
| [smolagents](https://github.com/huggingface/smolagents) | 有限步骤与完成状态 | 将步数预算和完成条件分别记录 |

高星数只用来寻找候选，不代表内容适合零基础。精确提交、核对日期、具体文件、许可边界和原创改写记录见 [开源参考与改编说明.md](开源参考与改编说明.md)。首页 info1110 标记来自本项目的学习需求，不代表官方课程材料、考试覆盖或官方背书。

## 维护与验证

修改 `source/` 后重建，不直接修改生成的 HTML、示例或答案；生成器会在检测到生成文件被手改时停止。现有作答与笔记不会被重建覆盖。

```bash
python3 source/build.py
python3 tools/verify_examples.py
python3 tools/check_practice.py --all --solutions
python3 tools/check_projects.py
python3 tools/package.py
```

Windows 将 `python3` 替换为 `py`。`--solutions` 验证教材参考答案，不代表学习者已通过。打包输出位于仓库的上一级目录，文件名为 `Python-Zero-to-Practice.zip`。

GitHub Actions 已在 Windows、macOS、Linux 上完成本版本检查，包含 Python 3.10、3.12、3.14 的五组组合，具体证据见 [通过的工作流](https://github.com/leon1111-wgl/leon1111-wgl/actions/runs/39623640001)。每次后续发布仍以对应提交的实际结果为准。环境与验证范围见 [验证说明.md](验证说明.md)，改动见 [维护记录.md](维护记录.md)。

欢迎报告看不懂的讲解、无法复现的输出或欠缺的边界情况。请附题号、操作系统、Python 版本、最小输入、预期与实际结果；提交教学修改前先阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 许可证

本目录中的原创教材文字、代码和练习采用 [MIT License](LICENSE)，版权所有 © 2026 Leon Wang（leon1111-wgl）。所引用的外部项目和材料仍遵循各自许可；本许可证不为外部链接内容或个人主页仓库的其他目录重新授权。具体来源范围见“开源参考与改编说明.md”。
