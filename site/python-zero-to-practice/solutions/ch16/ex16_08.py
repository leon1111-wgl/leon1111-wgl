# 第 16_08 题 AI / Agent：把乱序结果配回原请求
# 实现 attach_results(requests, results)。输入为列表；每个请求字典有 id、question，每个结果字典有 id、answer。前提：id 是非空字符串，question 与 answer 是字符串（允许空串），所需键都存在；字段类型不属于本题验证范围。两个列表各自的 id 必须唯一，而且两边 id 集合完全相同，否则抛 ValueError。两边都空返回 []。返回新的字典列表，每条只含 id、question、answer，按 requests 原顺序排列；不修改输入，不打印。用请求 r2/今天学什么？、r1/怎么复习？和结果 r1/闭卷重写、r2/练习字典，逐行打印返回的字典。
# 预期程序输出：
# {'id': 'r2', 'question': '今天学什么？', 'answer': '练习字典'}
# {'id': 'r1', 'question': '怎么复习？', 'answer': '闭卷重写'}

def attach_results(requests, results):
    result_by_id = {}
    for row in results:
        request_id = row["id"]
        if request_id in result_by_id:
            raise ValueError("结果 ID 重复")
        result_by_id[request_id] = row["answer"]

    request_ids = set()
    for row in requests:
        request_id = row["id"]
        if request_id in request_ids:
            raise ValueError("请求 ID 重复")
        request_ids.add(request_id)
    if request_ids != set(result_by_id):
        raise ValueError("请求与结果的 ID 不一致")

    joined = []
    for row in requests:
        joined.append({"id": row["id"], "question": row["question"],
                       "answer": result_by_id[row["id"]]})
    return joined

requests = [{"id": "r2", "question": "今天学什么？"},
            {"id": "r1", "question": "怎么复习？"}]
results = [{"id": "r1", "answer": "闭卷重写"},
           {"id": "r2", "answer": "练习字典"}]
for row in attach_results(requests, results):
    print(row)
