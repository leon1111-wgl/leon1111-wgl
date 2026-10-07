"""先写纯函数，再连接成完整数据管道。参考在 app.py。"""
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
