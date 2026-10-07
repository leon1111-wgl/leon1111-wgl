"""项目练习骨架。NotImplementedError 是留给学习者填空，不是参考实现。"""
STARTERS = {
'01_study_log': '''"""先完成 summarize，再加入文件。完整参考在 app.py。"""
import json
from pathlib import Path


def summarize(records):
    """输入记录列表，返回 count、total、mean；空列表 mean 为 None。"""
    # TODO: 用循环或 sum 计算总分钟，然后处理空列表。
    raise NotImplementedError("请先完成 summarize")


def load_records(path):
    """Path -> 记录列表。不存在返回 []；损坏文件应报错。"""
    # TODO: exists 检查，再 read_text + json.loads。
    raise NotImplementedError("请完成 load_records")


def save_records(path, records):
    """把自己的练习记录写入专用路径；注意覆盖规则。"""
    # TODO: 建立父目录，再序列化写出。之后可尝试临时文件替换。
    raise NotImplementedError("请完成 save_records")


if __name__ == "__main__":
    sample = [{"minutes": 30}, {"minutes": 60}]
    print(summarize(sample))  # 应包含 count=2、total=90、mean=45.0
    print(summarize([]))      # mean 应为 None
''',
'02_score_report': '''"""先验证一行，再读取整张表。完整参考在 app.py。"""
import csv
from pathlib import Path


def parse_row(row):
    """字符串字典 -> 含整数 score 的记录；非法则抛 ValueError。"""
    # TODO: 去空白、检查 ID 与姓名、转换分数并检查 0—100。
    raise NotImplementedError("请先完成 parse_row")


def summarize(records):
    """有效记录列表 -> 人数、总分、平均分与通过率。"""
    # TODO: 明确空列表的平均值与通过率为 None。
    raise NotImplementedError("请完成 summarize")


def read_valid_rows(path):
    """返回 (valid, errors)，errors 保存记录号与原因。"""
    # TODO: DictReader + enumerate；调用 parse_row；检测重复 ID。
    raise NotImplementedError("请完成 read_valid_rows")


if __name__ == "__main__":
    print(parse_row({"student_id": "s1", "name": " A ", "score": "80"}))
    # 第一步成功后，再取消下面的注释：
    # source = Path(__file__).resolve().parent / "data" / "scores.csv"
    # valid, errors = read_valid_rows(source)
    # print(summarize(valid))
    # print(errors)
''',
'03_text_cleaner': '''"""先清洗文本，再处理 JSONL。完整参考在 app.py。"""
import json
from pathlib import Path


def normalize(text):
    """英文教学规则：小写化、合并空白、去两端空白。"""
    raise NotImplementedError("请先完成 normalize")


def deduplicate(records):
    """记录含 id/text；按规范化文本保序去重，返回保留记录。"""
    # TODO: seen 集合 + 输出列表；不要覆盖原始记录。
    raise NotImplementedError("请完成 deduplicate")


def count_words(records):
    """按空白分词，返回词到次数的字典。"""
    # TODO: 先用手写 get 计数，之后可改成 Counter。
    raise NotImplementedError("请完成 count_words")


def clean_file(path):
    """逐行解析并验证，再清洗；返回保留记录和错误报告。"""
    # TODO: 参考 TASKS.md 的 9 行数据手算结果。
    raise NotImplementedError("请完成 clean_file")


if __name__ == "__main__":
    print(normalize("  Hello   Python "))  # 预期 hello python
    # 完成更多函数后，把自己的内存样例加在这里。
''',
'04_dataset_pipeline': '''"""先写纯函数，再连接成完整数据管道。参考在 app.py。"""
import random


def split_records(records, train_ratio=0.75, seed=42):
    """复制、打乱、切分；输入至少 2 条；比例在 0 与 1 之间。"""
    raise NotImplementedError("请完成 split_records")


def build_vocab(records):
    """只使用训练记录；PAD=0、UNK=1，其余按首次出现分配。"""
    raise NotImplementedError("请完成 build_vocab")


def encode(text, vocab):
    """按空白拆词，未知词为 1；不得扩充已有词表。"""
    raise NotImplementedError("请先完成 encode")


def pad_batch(sequences):
    """返回 (padded,masks)，空输入返回 ([],[])，不改输入。"""
    raise NotImplementedError("请完成 pad_batch")


def make_batches(records, vocab, size):
    """保留末尾不足一批的数据；每批包含 ID、标签、编码和掩码。"""
    raise NotImplementedError("请完成 make_batches")


if __name__ == "__main__":
    print(encode("known unknown", {"<PAD>": 0, "<UNK>": 1, "known": 2}))
    # 预期 [2, 1]。完成 encode 后再分别测试其他函数。
'''
}
