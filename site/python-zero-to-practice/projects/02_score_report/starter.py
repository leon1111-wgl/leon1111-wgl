"""先验证一行，再读取整张表。完整参考在 app.py。"""
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
