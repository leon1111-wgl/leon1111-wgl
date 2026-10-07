"""先清洗文本，再处理 JSONL。完整参考在 app.py。"""
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
