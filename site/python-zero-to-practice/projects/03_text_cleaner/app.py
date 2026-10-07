"""英文教学语料清洗器，空白分词不是大模型 tokenizer。"""
import argparse
import json
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parent

def normalize(text):
    return " ".join(text.lower().split())

def clean_file(path):
    kept = []
    rejected = []
    duplicates = []
    seen_text = set()
    seen_ids = set()
    input_count = 0
    with path.open(encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue
            input_count += 1
            try:
                record = json.loads(line)
                if not isinstance(record, dict):
                    raise ValueError("记录必须是 JSON 对象")
                if not isinstance(record.get("id"), str) or not record["id"].strip():
                    raise ValueError("id 必须为非空字符串")
                if not isinstance(record.get("text"), str):
                    raise ValueError("text 必须为字符串")
                record_id = record["id"].strip()
                text = normalize(record["text"])
                if not text:
                    raise ValueError("清洗后文本为空")
                if record_id in seen_ids:
                    raise ValueError("与已保留记录的 ID 重复")
            except (ValueError, json.JSONDecodeError) as error:
                rejected.append({"line": line_number, "reason": str(error)})
                continue
            if text in seen_text:
                duplicates.append({"line": line_number, "reason": "规范化文本重复"})
                continue
            seen_text.add(text)
            seen_ids.add(record_id)
            kept.append({"id": record_id, "text": text})
    counts = Counter(word for record in kept for word in record["text"].split())
    frequencies = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    report = {"input_count": input_count, "kept_count": len(kept),
              "duplicate_count": len(duplicates), "rejected_count": len(rejected),
              "duplicates": duplicates, "rejected": rejected, "word_counts": frequencies}
    return kept, report

def save_outputs(records, report, folder):
    folder.mkdir(parents=True, exist_ok=True)
    with (folder / "clean.jsonl").open("w", encoding="utf-8") as file:
        for record in records:
            file.write(json.dumps(record, ensure_ascii=False) + "\n")
    (folder / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

def main():
    parser = argparse.ArgumentParser(description="清洗英文教学 JSONL 语料")
    parser.add_argument("--input", type=Path, default=BASE / "data" / "raw.jsonl")
    parser.add_argument("--out", type=Path, default=BASE / "outputs")
    args = parser.parse_args()
    try:
        records, report = clean_file(args.input)
        save_outputs(records, report, args.out)
    except (OSError, UnicodeError) as error:
        parser.exit(1, f"处理失败：{error}\n")
    print(f"非空行 {report['input_count']}，保留 {report['kept_count']}，重复 {report['duplicate_count']}，拒绝 {report['rejected_count']}")

if __name__ == "__main__":
    main()
