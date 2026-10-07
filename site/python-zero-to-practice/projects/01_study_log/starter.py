"""先完成 summarize，再加入文件。完整参考在 app.py。"""
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
