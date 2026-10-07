# 第 09_05 题 统计通过率
# 实现 pass_rate(scores, threshold=60)，返回通过人数/总人数，空列表返回 None。打印 pass_rate([50,60,90])，用 .1% 显示为 66.7%。
# 预期程序输出：
# 66.7%

def pass_rate(scores, threshold=60):
    if not scores:
        return None
    count = 0
    for score in scores:
        if score >= threshold:
            count += 1
    return count / len(scores)

print(f"{pass_rate([50, 60, 90]):.1%}")
