# 第 08_06 题 按城市分组
# 记录 [{"name":"A","city":"台北"},{"name":"B","city":"高雄"},{"name":"C","city":"台北"}]，构建城市到姓名列表的字典并输出。
# 预期程序输出：
# {'台北': ['A', 'C'], '高雄': ['B']}

records = [
    {"name": "A", "city": "台北"},
    {"name": "B", "city": "高雄"},
    {"name": "C", "city": "台北"},
]
groups = {}
for record in records:
    city = record["city"]
    if city not in groups:
        groups[city] = []
    groups[city].append(record["name"])
print(groups)
