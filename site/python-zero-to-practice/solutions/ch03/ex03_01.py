# 第 03_01 题 邮箱清洗
# 把 "  Learner@Example.COM  " 去两端空白并转小写，输出 learner@example.com。
# 预期程序输出：
# learner@example.com

email = "  Learner@Example.COM  "
print(email.strip().lower())
