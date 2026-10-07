# 第 10_02 题 单词按长度排序
# 实现 sort_words(words)，长度升序，同长度字母升序，不改输入。打印对 ["dog","a","cat","python"] 的结果。
# 预期程序输出：
# ['a', 'cat', 'dog', 'python']

def sort_words(words):
    return sorted(words, key=lambda word: (len(word), word))

print(sort_words(["dog", "a", "cat", "python"]))
