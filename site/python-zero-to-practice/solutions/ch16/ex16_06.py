# 第 16_06 题 验证记录 ID 唯一
# 实现 unique_ids(records)，如果各字典的 id 唯一返回 True，重复则 False；空列表返回 True。打印 [{"id":1},{"id":1}] 的结果。
# 预期程序输出：
# False

def unique_ids(records):
    ids = [record["id"] for record in records]
    return len(ids) == len(set(ids))

print(unique_ids([{"id": 1}, {"id": 1}]))
