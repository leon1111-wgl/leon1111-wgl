Leon · Python 零基础实操教程 v1.0

1. 完整解压，再双击 index.html，在浏览器阅读。
2. 第 00 章包含 Windows 与 Mac 的 Python 安装、编辑、运行步骤。
3. 阅读不需网络；运行 .py 需要 Python 3.10+。本教材只用标准库。
4. examples 是可运行示例；practice 是作答区；solutions 是参考答案。
5. projects 包含四个完整项目，先读各项目的 TASKS.md。
6. 换电脑：复制整个文件夹，另行导出并导入网页进度；.venv 应重建。
7. 不要在 ZIP 预览中编辑或运行文件，先解压。不要用 Word 编辑 .py。

教材规模：19 个单元，91 个示例，100 道习题，4 个项目。
从学习包根目录运行（Windows 用 py，Mac 用 python3 替换 python）：
  python examples/ch01/ex01_01.py
  python tools/check_practice.py 01_01
  python tools/check_practice.py --chapter 09
  python tools/verify_examples.py
  python tools/check_projects.py

练习自检会执行你自己编写的本地练习文件，每题限时 5 秒，防止常见无限循环持续卡住。
它不是隔离运行未知代码的安全沙箱；只检查你自己可信的练习。
网页不运行任意 Python，代码复制后需在编辑器保存并运行。
自检输出中不含你在终端键入字符的键盘回显。

开始建议：今天完成第 00—01 章并独立做前 3 题，次日关掉答案重写。
文字备份：textbook.md。编辑源稿：source/；source/build.py 可重新生成教材，保留已有练习文件。
