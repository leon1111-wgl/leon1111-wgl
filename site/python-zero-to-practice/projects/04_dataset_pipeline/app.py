"""仅用标准库的数据管道；toy 词表不能替代预训练模型 tokenizer。"""
import argparse
import json
import random
from pathlib import Path

BASE = Path(__file__).resolve().parent

def normalize(text):
    return " ".join(text.lower().split())

def load_records(path):
    records = []
    ids = set()
    texts = set()
    with path.open(encoding="utf-8") as file:
        for number, line in enumerate(file, start=1):
            if not line.strip():
                continue
            row = json.loads(line)
            if not isinstance(row, dict):
                raise ValueError(f"第 {number} 行不是对象")
            if not isinstance(row.get("id"), str) or not row["id"].strip():
                raise ValueError(f"第 {number} 行 ID 非法")
            if not isinstance(row.get("text"), str):
                raise ValueError(f"第 {number} 行 text 非字符串")
            if type(row.get("label")) is not int or row["label"] not in (0, 1):
                raise ValueError(f"第 {number} 行 label 必须是整数 0 或 1")
            record_id = row["id"].strip()
            text = normalize(row["text"])
            if not text or record_id in ids or text in texts:
                raise ValueError(f"第 {number} 行为空文本、重复 ID 或重复文本")
            ids.add(record_id)
            texts.add(text)
            records.append({"id": record_id, "text": text, "label": row["label"]})
    return records

def split_records(records, train_ratio=0.75, seed=42):
    if not 0 < train_ratio < 1:
        raise ValueError("train_ratio 必须在 0 与 1 之间")
    if len(records) < 2:
        raise ValueError("至少需要 2 条有效记录")
    shuffled = list(records)
    random.Random(seed).shuffle(shuffled)
    cut = max(1, min(len(records) - 1, int(len(records) * train_ratio)))
    return shuffled[:cut], shuffled[cut:]

def build_vocab(records):
    vocab = {"<PAD>": 0, "<UNK>": 1}
    for row in records:
        for word in row["text"].split():
            if word not in vocab:
                vocab[word] = len(vocab)
    return vocab

def pad_batch(sequences):
    width = max((len(sequence) for sequence in sequences), default=0)
    padded = [sequence + [0] * (width - len(sequence)) for sequence in sequences]
    masks = [[1] * len(sequence) + [0] * (width - len(sequence)) for sequence in sequences]
    return padded, masks

def make_batches(records, vocab, size):
    if size <= 0:
        raise ValueError("batch_size 必须为正整数")
    result = []
    for start in range(0, len(records), size):
        rows = records[start:start + size]
        sequences = [[vocab.get(word, 1) for word in row["text"].split()] for row in rows]
        padded, masks = pad_batch(sequences)
        result.append({"ids": [row["id"] for row in rows],
                       "labels": [row["label"] for row in rows],
                       "input_ids": padded, "attention_mask": masks})
    return result

def write_jsonl(path, rows):
    with path.open("w", encoding="utf-8") as file:
        for row in rows:
            file.write(json.dumps(row, ensure_ascii=False) + "\n")

def run(input_path, output_dir, train_ratio=0.75, seed=42, batch_size=2):
    records = load_records(input_path)
    train, test = split_records(records, train_ratio, seed)
    vocab = build_vocab(train)
    batches = {"train": make_batches(train, vocab, batch_size),
               "test": make_batches(test, vocab, batch_size)}
    manifest = {"seed": seed, "requested_train_ratio": train_ratio, "batch_size": batch_size,
                "total": len(records), "train_count": len(train), "test_count": len(test),
                "vocab_size": len(vocab), "normalization": "lower + whitespace split/join",
                "tokenizer": "teaching-only whitespace tokenizer"}
    output_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(output_dir / "train.jsonl", train)
    write_jsonl(output_dir / "test.jsonl", test)
    for name, value in [("vocab.json", vocab), ("batches.json", batches), ("manifest.json", manifest)]:
        (output_dir / name).write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")
    return manifest

def main():
    parser = argparse.ArgumentParser(description="教学文本数据集管道")
    parser.add_argument("--input", type=Path, default=BASE / "data" / "samples.jsonl")
    parser.add_argument("--out", type=Path, default=BASE / "outputs")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--batch-size", type=int, default=2)
    parser.add_argument("--train-ratio", type=float, default=0.75)
    args = parser.parse_args()
    try:
        result = run(args.input, args.out, args.train_ratio, args.seed, args.batch_size)
    except (ValueError, OSError) as error:
        parser.exit(1, f"处理失败：{error}\n")
    print(f"共 {result['total']} 条，训练 {result['train_count']}，测试 {result['test_count']}")
    print(f"词表 {result['vocab_size']} 项，批大小 {result['batch_size']}")

if __name__ == "__main__":
    main()
