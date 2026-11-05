# AI 数据：同样长度，先按 ID 对齐再计算
predictions = [
    {"id": "s1", "prediction": 1},
    {"id": "s2", "prediction": 0},
    {"id": "s3", "prediction": 1},
]
labels = [
    {"id": "s2", "label": 0},
    {"id": "s3", "label": 1},
    {"id": "s1", "label": 1},
]

positional_correct = 0
for prediction, label in zip(predictions, labels, strict=True):
    if prediction["prediction"] == label["label"]:
        positional_correct += 1
print(f"按位置得到的误算值：{positional_correct / len(predictions):.1%}")

# 本例固定数据已确认 ID 唯一且两边完全一致；迁移题再验证这些前提。
label_by_id = {}
for row in labels:
    label_by_id[row["id"]] = row["label"]

aligned = []
for row in predictions:
    sample_id = row["id"]
    aligned.append({"id": sample_id,
                    "prediction": row["prediction"],
                    "label": label_by_id[sample_id]})

correct = 0
for row in aligned:
    print(row["id"], row["prediction"], row["label"])
    if row["prediction"] == row["label"]:
        correct += 1
print(f"按 ID 对齐后的准确率：{correct / len(aligned):.1%}")
