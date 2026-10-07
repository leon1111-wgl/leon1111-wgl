# 第 09_04 题 清洗一组姓名
# 实现 clean_names(names)，去每项两端空白，丢弃空结果，保留其余顺序且不修改输入。打印对 [" A ","  ","B"] 的结果。
# 预期程序输出：
# ['A', 'B']

def clean_names(names):
    result = []
    for name in names:
        clean = name.strip()
        if clean:
            result.append(clean)
    return result

print(clean_names([" A ", "  ", "B"]))
