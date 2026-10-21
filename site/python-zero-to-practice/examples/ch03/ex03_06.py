# AI / Agent：用字符串组织提示词
topic = "  Python 列表  "
level = "零基础"
clean_topic = topic.strip()
prompt = f"请面向{level}读者解释：{clean_topic}。"
print(prompt)
print(f"主题字符数：{len(clean_topic)}")
