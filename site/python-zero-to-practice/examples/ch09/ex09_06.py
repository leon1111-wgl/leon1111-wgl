# 修改对象与改绑参数
def add_item(items):
    items.append("B")

def replace_items(items):
    items = ["C"]

tasks = ["A"]
add_item(tasks)
replace_items(tasks)
print(tasks)
