# 第 04_08 题 AI / Agent：输出长度约定
# 给定 reply = "  hello  "、limit = 5。清理首尾空白后：空内容输出 empty；字符数超过 limit 输出 too_long；否则输出 ok。条件按此顺序组织。
# 预期程序输出：
# ok

reply = "  hello  "
limit = 5
cleaned = reply.strip()
if cleaned == "":
    print("empty")
elif len(cleaned) > limit:
    print("too_long")
else:
    print("ok")
