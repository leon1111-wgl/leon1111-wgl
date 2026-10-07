# 数据集划分 编码与分批

前置：第 00—16 章

读取小型带标签文本数据集，验证记录、ID 与规范化文本唯一性；可复现地划分训练测试；只用训练文本建词表；把各批编码、补齐并生成掩码；保存配置与输出。此项目不训练模型，专门练 Python 数据流。

### 1 先写四个纯函数
normalize、split_records、build_vocab、pad_batch。每个先用 2—3 条手造数据检查。把数据处理和文件输出分开，错误更容易定位。

### 2 约定保留比例
train_ratio 满足 0<ratio<1，至少 2 条数据；n_train=int(n*ratio)，再限制到 1 到 n-1，保证两边非空。小数据可能导致实际比例不同，报告实际条数。

### 3 一次打乱完整记录
复制外层记录列表，用 random.Random(seed).shuffle。ID、text、label 一起移动，避免标签错配。样本按规范化文本完全重复时直接拒绝；相近内容或同源分组需要更复杂检查。

### 4 训练侧建立词表
保留 <PAD>=0、<UNK>=1，只看 train。测试中的未知词映射为 1。保存 vocab.json，让下一次编码使用相同映射。

### 5 切批与补齐
每批独立算最大长度；保存 ids、labels、input_ids、attention_mask。最后不足 batch_size 的批保留。让你能检查每个维度与记录对齐。

### 6 验收与扩展
检查训练测试 ID 无交集、样本数守恒、每批 labels 数与 input_ids 行数相等、每行掩码长度与 ID 长度相等。自行加入分层划分或按来源分组，先写清规则再实现。

### 运行命令

从学习包根目录执行。Windows 用 py，Mac 用 python3，激活环境后可用 python。

```terminal
python projects/04_dataset_pipeline/app.py
python projects/04_dataset_pipeline/app.py --seed 7 --batch-size 3 --train-ratio 0.75
```

### 预期结果

默认 8 条数据，训练 6、测试 2；批大小 2 时训练 3 批、测试 1 批。outputs/ 中有 train.jsonl、test.jsonl、vocab.json、batches.json、manifest.json。默认重复运行应得到相同输出（同一运行环境）。

### 验收

运行学习包的 python tools/check_projects.py 核验参考实现；自己的实现按上面手算结果和边界逐项验证。


## 独立实现记录

- 输入约定：
- 输出约定：
- 最小样例手算：
- 空数据测试：
- 边界测试：
- 错误输入测试：
- 我的新增功能：
