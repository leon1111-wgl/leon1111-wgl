from textwrap import dedent
PROJECTS = []
def project(folder, title, prerequisites, task, steps, commands, expected, code, data, checks):
    PROJECTS.append(dict(folder=folder,title=title,prerequisites=prerequisites,task=task,
        steps=steps,commands=commands,expected=expected,code=dedent(code).strip()+'\n',data=data,checks=dedent(checks).strip()))

project('01_study_log','学习打卡与统计','第 00—13 章',
'写一个命令行学习记录本：添加日期、学习分钟和主题；下次打开仍可读取；汇总次数、总分钟和平均分钟。分钟必须为非负整数，主题不能为空。文件损坏时报告问题，不把坏文件当空记录覆盖。',
[
('先写核心函数','先对内存中的记录列表写 summarize(records)，输入 30、60 分钟时总量为 90、平均 45.0。空列表返回平均 None。此时完全不需要文件或命令行。'),
('加入文件持久化','用 JSON 保存记录列表。文件不存在视作首次使用，返回空列表；文件存在但内容错误则抛出清楚异常。分清这两种情况，避免误覆盖用户数据。'),
('检查输入再修改','将日期用 date.fromisoformat 验证；分钟用整数且非负检查；主题 strip 后检查非空。所有检查通过后才 append。'),
('加入命令行入口','argparse 是标准库命令行参数解析器。add 子命令收 minutes 与 topic；summary 子命令显示统计；--store 指定记录位置。看不懂时先运行 --help，再按已给命令练习。'),
('独立扩展','增加按主题汇总，不直接改现有统计函数；给新函数写 3 个例子。进一步可做删除记录，但先为每条记录设计稳定 ID，并明确删除规则。')
],
r'''python projects/01_study_log/app.py add 30 "变量与类型" --date 2026-10-07
python projects/01_study_log/app.py add 60 "循环练习" --date 2026-10-08
python projects/01_study_log/app.py summary''',
'初始无记录时执行两次 add，分别显示已保存 1 条和 2 条；summary 显示记录数 2、总分钟 90、平均分钟 45.0。反复 add 会继续追加，所以重复练习前可使用 --store 指向另一个新的练习文件。',
r'''
"""学习记录本。先运行 python app.py --help 查看命令。"""
import argparse
import json
from datetime import date
from pathlib import Path

BASE = Path(__file__).resolve().parent

def validate_record(record):
    if not isinstance(record, dict):
        raise ValueError("记录必须是对象")
    if not isinstance(record.get("date"), str):
        raise ValueError("记录日期必须是字符串")
    date.fromisoformat(record["date"])
    minutes = record.get("minutes")
    if type(minutes) is not int or minutes < 0:
        raise ValueError("分钟必须是非负整数")
    topic = record.get("topic")
    if not isinstance(topic, str) or not topic.strip():
        raise ValueError("主题不能为空")

def load_records(path):
    if not path.exists():
        return []
    records = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(records, list):
        raise ValueError("记录文件最外层必须是列表")
    for record in records:
        validate_record(record)
    return records

def summarize(records):
    total = sum(record["minutes"] for record in records)
    count = len(records)
    return {"count": count, "total": total, "mean": total / count if count else None}

def add_record(path, minutes, topic, day):
    record = {"date": day, "minutes": minutes, "topic": topic.strip()}
    validate_record(record)
    records = load_records(path)
    records.append(record)
    path.parent.mkdir(parents=True, exist_ok=True)
    # 先写临时文件，再替换本项目自己的记录文件，降低中途写坏的机会。
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    temporary.replace(path)
    return len(records)

def main():
    parser = argparse.ArgumentParser(description="学习打卡记录本")
    parser.add_argument("--store", type=Path, default=BASE / "outputs" / "study_log.json")
    sub = parser.add_subparsers(dest="command", required=True)
    add = sub.add_parser("add", help="添加一条记录")
    add.add_argument("minutes", type=int)
    add.add_argument("topic")
    add.add_argument("--date", default=date.today().isoformat())
    sub.add_parser("summary", help="查看汇总")
    args = parser.parse_args()
    try:
        if args.command == "add":
            count = add_record(args.store, args.minutes, args.topic, args.date)
            print(f"已保存 {count} 条记录")
        else:
            stats = summarize(load_records(args.store))
            print(f"记录数：{stats['count']}")
            print(f"总分钟：{stats['total']}")
            print("平均分钟：暂无" if stats["mean"] is None else f"平均分钟：{stats['mean']:.1f}")
    except (ValueError, OSError) as error:
        parser.exit(1, f"无法完成：{error}\n")

if __name__ == "__main__":
    main()
''',{},
r'''
assert module.summarize([]) == {"count": 0, "total": 0, "mean": None}
path = temp / "log.json"
assert module.add_record(path, 30, "  Python ", "2026-10-07") == 1
assert module.add_record(path, 60, "循环", "2026-10-08") == 2
assert module.summarize(module.load_records(path))["mean"] == 45
before = path.read_text(encoding="utf-8")
for value in [-1, True]:
    try:
        module.add_record(path, value, "X", "2026-10-07")
    except ValueError:
        pass
    else:
        raise AssertionError("非法分钟未拒绝")
assert path.read_text(encoding="utf-8") == before
path.write_text("broken", encoding="utf-8")
try:
    module.add_record(path, 1, "X", "2026-10-07")
except ValueError:
    pass
else:
    raise AssertionError("损坏文件未被拒绝")
assert path.read_text(encoding="utf-8") == "broken"
''')

project('02_score_report','成绩 CSV 清洗与报告','第 00—13 章',
'读取含坏数据的成绩表。逐条检查 ID、姓名、分数和重复 ID，保留有效记录，把无效行及原因写入错误报告，输出人数、平均分、通过率与排名。CSV 的逻辑记录可能跨物理行，因此报告记录号不伪称绝对物理行号。',
[
('列出数据约定','必需列为 student_id、name、score；ID 和姓名非空；score 是 0—100 的整数字符串；相同 ID 首条有效记录保留，后续重复记错。'),
('手算样本','先查看 data/scores.csv。有效分数为 80、60、100、59、0，总分 299，平均 59.8；达到 60 有 3 人，通过率 60%。有 4 条错误记录。'),
('一条一条验证','先处理字段缺失，再转整数，再检查范围，最后检测已保留 ID 是否重复。错误放入列表并继续，不让一条坏数据阻止所有正常记录。'),
('统计与排序','只对有效数据计算。空数据平均分与通过率为 None，排名为空。sorted 用负分数与 ID 组成 key，保证同分顺序稳定可说明。'),
('保存并核验','写 report.json 和 errors.csv，读回来确认 valid_count+invalid_count 等于输入数据记录数。修改一条坏记录后重跑，确认计数相应变化。')
],
r'''python projects/02_score_report/app.py
python projects/02_score_report/app.py --help''',
'显示：有效 5 条，无效 4 条；平均分 59.8；通过率 60.0%。outputs/report.json 保存完整结果，outputs/errors.csv 保存记录号与错误原因。重复运行覆盖这两个专用输出文件。',
r'''
"""成绩清洗报告；只覆盖 --out 指定目录中的本项目输出文件。"""
import argparse
import csv
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent

def analyze(path):
    valid = []
    errors = []
    seen = set()
    with path.open(encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        required = {"student_id", "name", "score"}
        if not required.issubset(set(reader.fieldnames or [])):
            raise ValueError("缺少必需列 student_id、name、score")
        for record_number, row in enumerate(reader, start=1):
            try:
                if None in row:
                    raise ValueError("字段数超过表头列数")
                student_id = (row.get("student_id") or "").strip()
                name = (row.get("name") or "").strip()
                if not student_id or not name:
                    raise ValueError("ID 或姓名为空")
                try:
                    score = int(row.get("score") or "")
                except ValueError:
                    raise ValueError("分数不是整数") from None
                if not 0 <= score <= 100:
                    raise ValueError("分数超出 0 到 100")
                if student_id in seen:
                    raise ValueError("重复 ID")
            except ValueError as error:
                errors.append({"record": record_number, "reason": str(error)})
                continue
            seen.add(student_id)
            valid.append({"student_id": student_id, "name": name, "score": score})
    count = len(valid)
    total = sum(row["score"] for row in valid)
    passed = sum(row["score"] >= 60 for row in valid)
    return {
        "valid_count": count,
        "invalid_count": len(errors),
        "total": total,
        "mean": total / count if count else None,
        "pass_rate": passed / count if count else None,
        "ranking": sorted(valid, key=lambda row: (-row["score"], row["student_id"])),
        "errors": errors,
    }

def save_report(report, folder):
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    with (folder / "errors.csv").open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["record", "reason"])
        writer.writeheader()
        writer.writerows(report["errors"])

def main():
    parser = argparse.ArgumentParser(description="成绩表清洗与统计")
    parser.add_argument("--input", type=Path, default=BASE / "data" / "scores.csv")
    parser.add_argument("--out", type=Path, default=BASE / "outputs")
    args = parser.parse_args()
    try:
        report = analyze(args.input)
        save_report(report, args.out)
    except (OSError, ValueError, csv.Error) as error:
        parser.exit(1, f"处理失败：{error}\n")
    print(f"有效 {report['valid_count']} 条，无效 {report['invalid_count']} 条")
    if report["mean"] is None:
        print("没有有效分数，无法计算平均分与通过率")
    else:
        print(f"平均分 {report['mean']:.1f}")
        print(f"通过率 {report['pass_rate']:.1%}")

if __name__ == "__main__":
    main()
''',{'data/scores.csv':'student_id,name,score\ns1,小林,80\ns2,小陈,60\ns3,小王,100\ns4,小李,59\ns5,小周,0\ns6,小吴,abc\ns7,,75\ns2,重复记录,90\ns8,小赵,110\n'},
r'''
report = module.analyze(project_dir / "data" / "scores.csv")
assert report["valid_count"] == 5 and report["invalid_count"] == 4
assert report["total"] == 299 and report["mean"] == 59.8
assert report["pass_rate"] == 0.6
assert [row["student_id"] for row in report["ranking"]] == ["s3", "s1", "s2", "s4", "s5"]
module.save_report(report, temp)
assert json.loads((temp / "report.json").read_text(encoding="utf-8"))["total"] == 299
empty = temp / "empty.csv"
empty.write_text("student_id,name,score\n", encoding="utf-8")
assert module.analyze(empty)["mean"] is None
empty.write_text("wrong\n", encoding="utf-8")
try:
    module.analyze(empty)
except ValueError:
    pass
else:
    raise AssertionError("缺失表头未拒绝")
''')

project('03_text_cleaner','文本语料清洗与词频','第 00—13 章和第 16 章',
'把原始 JSONL 清洗成可追踪的小语料：验证 id 与 text，统一英文大小写及空白，去除空文本和重复文本，保留原记录 ID，输出干净 JSONL、错误与重复记录报告和词频。',
[
('定义清洗规则','仅针对本项目英文教学文本：lower 后按空白 split/join。保留标点。去重依据规范化后的完整文本；第一条有效记录保留。输出词频按空白分词，不是模型 tokenizer。'),
('分离解析与清洗','逐行 JSON 解析可能失败；对象结构和字段类型也可能不对。先确认 dict，再检查 id 与 text 的类型，最后做字符串方法。'),
('分别记拒绝与重复','坏 JSON、缺字段、非字符串、空文本、重复已保留 ID 计为 rejected；同规范化文本计为 duplicate。两类都记物理行号和原因。不要悄悄消失记录。'),
('用小样本核对','样本共 9 个非空行，保留 3，重复文本 1，拒绝 5。干净文本为 hello python、learn python、hello world；python 和 hello 各 2 次。'),
('独立扩展','增加 --min-length 过滤太短文本，给报告增加过滤原因。再测试中文和代码文本，说明为什么当前规则不能直接代表所有语料任务。')
],
r'''python projects/03_text_cleaner/app.py
python projects/03_text_cleaner/app.py --help''',
'输出非空行 9、保留 3、重复 1、拒绝 5。outputs/clean.jsonl 保存干净记录；outputs/report.json 保存每个被排除行的原因和排序词频。',
r'''
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
''',{'data/raw.jsonl':'{"id":"a","text":"  Hello   Python "}\n{"id":"b","text":"Learn Python"}\n{"id":"c","text":"hello python"}\n{"id":"d","text":"  "}\n{"id":"e","text":42}\nnot valid json\n{"id":"f"}\n{"id":"g","text":"Hello world"}\n{"id":"a","text":"different text"}\n'},
r'''
records, report = module.clean_file(project_dir / "data" / "raw.jsonl")
assert [row["id"] for row in records] == ["a", "b", "g"]
assert report["input_count"] == 9
assert report["kept_count"] == 3 and report["duplicate_count"] == 1 and report["rejected_count"] == 5
assert report["input_count"] == sum(report[key] for key in ["kept_count", "duplicate_count", "rejected_count"])
assert dict(report["word_counts"])["python"] == 2
module.save_outputs(records, report, temp)
assert len((temp / "clean.jsonl").read_text(encoding="utf-8").splitlines()) == 3
empty = temp / "empty.jsonl"
empty.write_text("\n", encoding="utf-8")
assert module.clean_file(empty)[1]["input_count"] == 0
''')

project('04_dataset_pipeline','数据集划分 编码与分批','第 00—16 章',
'读取小型带标签文本数据集，验证记录、ID 与规范化文本唯一性；可复现地划分训练测试；只用训练文本建词表；把各批编码、补齐并生成掩码；保存配置与输出。此项目不训练模型，专门练 Python 数据流。',
[
('先写四个纯函数','normalize、split_records、build_vocab、pad_batch。每个先用 2—3 条手造数据检查。把数据处理和文件输出分开，错误更容易定位。'),
('约定保留比例','train_ratio 满足 0<ratio<1，至少 2 条数据；n_train=int(n*ratio)，再限制到 1 到 n-1，保证两边非空。小数据可能导致实际比例不同，报告实际条数。'),
('一次打乱完整记录','复制外层记录列表，用 random.Random(seed).shuffle。ID、text、label 一起移动，避免标签错配。样本按规范化文本完全重复时直接拒绝；相近内容或同源分组需要更复杂检查。'),
('训练侧建立词表','保留 <PAD>=0、<UNK>=1，只看 train。测试中的未知词映射为 1。保存 vocab.json，让下一次编码使用相同映射。'),
('切批与补齐','每批独立算最大长度；保存 ids、labels、input_ids、attention_mask。最后不足 batch_size 的批保留。让你能检查每个维度与记录对齐。'),
('验收与扩展','检查训练测试 ID 无交集、样本数守恒、每批 labels 数与 input_ids 行数相等、每行掩码长度与 ID 长度相等。自行加入分层划分或按来源分组，先写清规则再实现。')
],
r'''python projects/04_dataset_pipeline/app.py
python projects/04_dataset_pipeline/app.py --seed 7 --batch-size 3 --train-ratio 0.75''',
'默认 8 条数据，训练 6、测试 2；批大小 2 时训练 3 批、测试 1 批。outputs/ 中有 train.jsonl、test.jsonl、vocab.json、batches.json、manifest.json。默认重复运行应得到相同输出（同一运行环境）。',
r'''
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
''',{'data/samples.jsonl':'{"id":"s1","text":"I love python","label":1}\n{"id":"s2","text":"This lesson is useful","label":1}\n{"id":"s3","text":"I dislike bugs","label":0}\n{"id":"s4","text":"The code is confusing","label":0}\n{"id":"s5","text":"Learning is fun","label":1}\n{"id":"s6","text":"The file is missing","label":0}\n{"id":"s7","text":"Practice helps me","label":1}\n{"id":"s8","text":"This error is annoying","label":0}\n'},
r'''
source = project_dir / "data" / "samples.jsonl"
records = module.load_records(source)
original = list(records)
train, test = module.split_records(records)
assert len(train) == 6 and len(test) == 2
assert records == original
assert {row["id"] for row in train}.isdisjoint({row["id"] for row in test})
assert module.split_records(records) == (train, test)
vocab = module.build_vocab([{"text": "known"}])
batches = module.make_batches([{"id": "a", "text": "unknown known", "label": 0}], vocab, 2)
assert batches[0]["input_ids"] == [[1, 2]]
assert batches[0]["attention_mask"] == [[1, 1]]
assert "unknown" not in vocab
assert module.pad_batch([]) == ([], [])
manifest = module.run(source, temp)
assert manifest["total"] == 8
saved = json.loads((temp / "batches.json").read_text(encoding="utf-8"))
assert len(saved["train"]) == 3 and len(saved["test"]) == 1
for split in saved.values():
    for batch in split:
        assert len(batch["ids"]) == len(batch["labels"]) == len(batch["input_ids"])
        for row, mask in zip(batch["input_ids"], batch["attention_mask"]):
            assert len(row) == len(mask)
for size in [0, -1]:
    try:
        module.make_batches(records, vocab, size)
    except ValueError:
        pass
    else:
        raise AssertionError("非法批大小未拒绝")
''')
