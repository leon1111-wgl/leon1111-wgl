# 文本语料清洗与词频

前置：第 00—13 章和第 16 章

把原始 JSONL 清洗成可追踪的小语料：验证 id 与 text，统一英文大小写及空白，去除空文本和重复文本，保留原记录 ID，输出干净 JSONL、错误与重复记录报告和词频。

### 1 定义清洗规则
仅针对本项目英文教学文本：lower 后按空白 split/join。保留标点。去重依据规范化后的完整文本；第一条有效记录保留。输出词频按空白分词，不是模型 tokenizer。

### 2 分离解析与清洗
逐行 JSON 解析可能失败；对象结构和字段类型也可能不对。先确认 dict，再检查 id 与 text 的类型，最后做字符串方法。

### 3 分别记拒绝与重复
坏 JSON、缺字段、非字符串、空文本、重复已保留 ID 计为 rejected；同规范化文本计为 duplicate。两类都记物理行号和原因。不要悄悄消失记录。

### 4 用小样本核对
样本共 9 个非空行，保留 3，重复文本 1，拒绝 5。干净文本为 hello python、learn python、hello world；python 和 hello 各 2 次。

### 5 独立扩展
增加 --min-length 过滤太短文本，给报告增加过滤原因。再测试中文和代码文本，说明为什么当前规则不能直接代表所有语料任务。

### 运行命令

从学习包根目录执行。Windows 用 py，Mac 用 python3，激活环境后可用 python。

```terminal
python projects/03_text_cleaner/app.py
python projects/03_text_cleaner/app.py --help
```

### 预期结果

输出非空行 9、保留 3、重复 1、拒绝 5。outputs/clean.jsonl 保存干净记录；outputs/report.json 保存每个被排除行的原因和排序词频。

### 验收

运行学习包的 python tools/check_projects.py 核验参考实现；自己的实现按上面手算结果和边界逐项验证。
