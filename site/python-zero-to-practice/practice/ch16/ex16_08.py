# 第 16_08 题 AI / Agent：把乱序结果配回原请求
# 实现 attach_results(requests, results)。输入为列表；每个请求字典有 id、question，每个结果字典有 id、answer。前提：id 是非空字符串，question 与 answer 是字符串（允许空串），所需键都存在；字段类型不属于本题验证范围。两个列表各自的 id 必须唯一，而且两边 id 集合完全相同，否则抛 ValueError。两边都空返回 []。返回新的字典列表，每条只含 id、question、answer，按 requests 原顺序排列；不修改输入，不打印。用请求 r2/今天学什么？、r1/怎么复习？和结果 r1/闭卷重写、r2/练习字典，逐行打印返回的字典。
# 预期程序输出：
# {'id': 'r2', 'question': '今天学什么？', 'answer': '练习字典'}
# {'id': 'r1', 'question': '怎么复习？', 'answer': '闭卷重写'}

# 请在下面独立作答。先保存，再运行。
