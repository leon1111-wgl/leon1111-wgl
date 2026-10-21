# 第 13_08 题 作用域修复：统计工具执行成功次数
# 坏思路是在函数中直接给外部 total += 1。请改为实现 count_successes(results, start=0)：results 保证是布尔列表，start 保证为非负整数。以 start 为起点，只为 True 增加 1，返回新计数，不修改 results，不依赖全局计数，不打印。设 total=10，用 [True, False, True] 调用后保存到 total 并打印。
# 预期程序输出：
# 12

def count_successes(results, start=0):
    count = start
    for succeeded in results:
        if succeeded:
            count += 1
    return count

total = 10
total = count_successes([True, False, True], start=total)
print(total)
