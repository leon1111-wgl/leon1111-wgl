# CSV 清洗：空行、缺列与零分分别处理
import csv
import io

def clean_scores_csv(text):
    reader = csv.reader(io.StringIO(text, newline=""), strict=True)
    if next(reader, None) != ["name", "score"]:
        raise ValueError("表头必须为 name,score")
    valid, errors = [], []
    for row in reader:
        end_line = reader.line_num
        if not row:
            continue
        if len(row) != 2:
            errors.append((end_line, "columns"))
            continue
        name = row[0].strip()
        if not name:
            errors.append((end_line, "name"))
            continue
        try:
            score = int(row[1].strip())
        except ValueError:
            errors.append((end_line, "integer"))
            continue
        if not 0 <= score <= 100:
            errors.append((end_line, "range"))
            continue
        valid.append({"name": name, "score": score})
    return valid, errors

text = 'name,score\n"林,一",80\n\n小陈,bad\n小周,101\n小李\n小何,0\n'
valid, errors = clean_scores_csv(text)
print(valid)
for end_line, reason in errors:
    print(f"结束行 {end_line}：{reason}")
