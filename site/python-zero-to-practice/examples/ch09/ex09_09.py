# AI / Agent：工具函数把结果交回调用者
def count_words(text):
    words = text.split()
    return {"count": len(words), "empty": len(words) == 0}

result = count_words("  learn Python   today ")
print(result["count"])
print(result["empty"])
print(count_words("")["count"])
