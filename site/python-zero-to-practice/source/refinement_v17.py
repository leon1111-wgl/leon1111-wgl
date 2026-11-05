"""v1.7：按位置配对与按身份对齐；原创数据、场景和解析。"""
from course_data import example, exercise
from refinements import add_body


def apply_v17(chapters):
    add_body(chapters, 10, '''
### 配对精修：两列能配起来，不代表每一项都配上了
前置是第 05 章循环、第 07 章列表与本章 zip。把 `names = ["小青", "小岩"]` 与 `scores = [72]` 写成两列，按同一个位置取值：

| 位置 | names 的当前项 | scores 的当前项 | 默认 zip 的结果 |
| --- | --- | --- | --- |
| 0 | 小青 | 72 | 产生 ('小青', 72) |
| 1 | 小岩 | 已经没有元素 | 停止，不再产生一对 |

`list(zip(names, scores))` 是 `[('小青', 72)]`。它不会自动补出小岩的成绩，也不会说明谁被漏掉。如果再用 `dict(...)`，同样只剩一条记录；姓名有重复时还可能发生字典覆盖。因此“字典创建成功”不能代表数据完整。

示例 10_07 先展示这个反例，再检查两个**列表**的长度。已知它们应当逐项对应时，不等长就先停下来修数据。不要为了让程序运行而随意补 0：缺少成绩与实际得了 0 分是两件事。两列长度相同后，还要确认顺序确实表达同一批对象，第 16 章示例 16_08 会专门演示这种错误。

### strict=True 检查的是长度，不是身份
`zip(names, scores, strict=True)` 仍按第 0 项配第 0 项、第 1 项配第 1 项；它不会识别姓名或自动查 ID。strict 也不是创建对象时就扫完输入：要在 for 或 list 消费到长度不一致的位置才会抛 ValueError。对上面的数据，严格遍历仍可先给出 ('小青', 72)，再在尝试下一对时失败。

第 13 章学异常、第 15 章学迭代器后，再完整验证这个执行顺序。现在记住：不要把 `pairs = zip(...)` 没报错当作“已检查全部”，也不要把严格循环看成自动撤销已执行操作的机制。示例只使用内存列表，没有写文件或调用外部工具。

### 三步实操：先数行，再看谁与谁对应
1. **预测：** 遮住 10_07 的输出，写出原两列条数、配对后的条数和漏掉的姓名，然后运行核对。
2. **改写：** 在分数末尾补上真实已知的 88，预测两对数据。接着将两列都改成空列表：长度相同，得到 []；只有一列为空时则拒绝继续处理。每次只改一种情况。
3. **迁移：** 回到习题 10_04，解释“姓名唯一”这个前提为什么必要。之后去第 16 章，将身份保留在每条字典里，用 ID 对齐乱序返回的数据。

不要为了观察 zip 内容而先 list 一次、再遍历同一个 zip 对象；第一次已消耗它。要复用配对结果，就保存刚生成的列表，或从原列表重新创建 zip。两种选择的内存与执行时机在第 15 章继续学习。
''')
    example(chapters[10], '配对追踪：默认 zip 漏掉了谁', '''
    names = ["小青", "小岩"]
    scores = [72]
    pairs = list(zip(names, scores))
    print("默认配对：", pairs)
    print("原条数与配对数：", len(names), len(scores), len(pairs))
    if len(names) != len(scores):
        print("拒绝继续：姓名与分数条数不同")
    else:
        print("条数一致：", list(zip(names, scores, strict=True)))
    ''', '''
    默认配对： [('小青', 72)]
    原条数与配对数： 2 1 1
    拒绝继续：姓名与分数条数不同
    ''', '默认 zip 只走到分数列表的末尾，所以没有小岩。上面的 pairs 专门用于观察反例，后续遇到长度错误就不把它作为完整成绩表继续处理。len 检查适用于当前两个列表；不要对生成器直接套 len。',
    '将 scores 改为 [72, 88]，预测 2 2 2 和两对记录。随后试两个空列表，以及只让其中一列为空。最后只调换两个分数的位置，解释为什么长度检查已无法发现身份错配。')
    chapters[10]['checkpoint'].append('我能区分 zip 的截短、严格长度检查和按身份对齐。')

    add_body(chapters, 16, '''
### 数据对齐：长度相同，准确率为什么仍会算错
前置：第 08 章字典与集合、第 10 章 zip、第 13 章异常。这里的 predictions 与 labels 都是手写的本地数据，不是实际模型输出。标签是预先给定的正确类别；prediction 是要拿来比较的预测类别，0 和 1 只是类别编号，不代表分数或 token。

第 10 章解决“有没有漏项”；现在还要检查“这两项是不是同一个样本”。示例 16_08 的两组记录各有三条，但排列顺序不同：

| 按位置配对 | 预测所属 ID / 类别 | 标签所属 ID / 类别 | 类别比较结果 | 是否同一条样本 |
| --- | --- | --- | --- | --- |
| 第 1 对 | s1 / 1 | s2 / 0 | 不相等 | 否 |
| 第 2 对 | s2 / 0 | s3 / 1 | 不相等 | 否 |
| 第 3 对 | s3 / 1 | s1 / 1 | 相等 | 否 |

这三对即使用 strict=True 也不会因长度报错。按位置算出来的 1/3、显示为 33.3%，**不能作为这批样本的准确率**：连最后相等的一对也比较错了对象。不要把“数值相等”与“属于同一条样本”混为一谈。

### 建立查找表，再按原请求顺序取回数据
示例中已知两边 ID 唯一且完全一致。先按标签的 id 建立 `label_by_id`：s2 对应 0，s3 对应 1，s1 对应 1。字典提供按键查找，不需要你先把两列分别排序。

| 当前预测记录 | 用于查找的键 | 查到的标签 | 合并后的信息 |
| --- | --- | --- | --- |
| {'id': 's1', 'prediction': 1} | s1 | 1 | s1：预测 1，标签 1 |
| {'id': 's2', 'prediction': 0} | s2 | 0 | s2：预测 0，标签 0 |
| {'id': 's3', 'prediction': 1} | s3 | 1 | s3：预测 1，标签 1 |

对齐后三条都相等，结果 3/3，显示为 100.0%。这只是同一组人为数据在正确对应下的算术结果，不是模型能力证据。打印 ID、预测和标签，比只看最后一个百分比更容易定位错配。

示例分三层：读标签记录建立查找表 → 按预测列表顺序生成 aligned → 只用 aligned 计算比例。它为观察核心过程使用固定且已核对的数据；迁移题再补重复与缺失检查。示例假定非空，空数据下的指标约定仍看习题 16_04。

### 身份校验不能省：重复、缺失与多余分别看
真实输入先约定 ID 的含义。下面迁移题要求两个列表各自 ID 唯一，而且 ID 集合完全相同：每个请求必须有且仅有一条结果，没有额外结果。重复 ID 必须在放进字典前拒绝，否则后值覆盖前值后就看不出重复了。

| 情况 | 本题要求 | 原因 |
| --- | --- | --- |
| 同一请求 ID 出现两次 | ValueError | 无法区分两次请求的身份 |
| 同一结果 ID 出现两次 | ValueError，即使答案相同 | 没有约定采用哪一次 |
| 有请求缺少结果 | ValueError | 不能悄悄漏掉未返回的请求 |
| 结果出现陌生 ID | ValueError | 不能把它配给别的请求 |
| 两边都是空列表 | 返回 [] | 没有请求需要关联 |
| 两条问题文字相同、ID 不同 | 分别保留 | 问题内容不等于请求身份 |

两边长度相同也可能一边缺 r2、另一边多出 r9。用集合检查“有哪些 ID”，用列表保留“按什么顺序输出”；不要遍历集合决定输出顺序。若任务允许重试或多次结果，要另行设计请求 ID、尝试编号和选择规则，本题不默选最后一条。ID 校验只核对数据关联，不能证明标签真实或答案正确。

### 分层实操：同样三条数据，先解释再改写
1. **读懂：** 预测示例 16_08 的两个百分比，逐项写出 aligned。区分“坏配对产生的数字”与“本题正确指标”。
2. **改写：** 只调换 labels 的顺序。按 ID 对齐后的行与比例应不变；按位置得到的数字可能变。恢复后，只将 s2 的预测从 0 改成 1，正确比例应变为 2/3，即 66.7%。
3. **迁移：** 独立做习题 16_08，给乱序结果配回原请求。先手画查找表，再写代码。代码跑通后必须试重复 ID、缺失 ID、同长度但 ID 不同、空输入，以及相同问题对应不同 ID。

把这个联系接回知识图谱：列表表示顺序，字典按身份查找，集合比较覆盖范围，异常阻止有问题的数据继续，最后才计算或展示结果。即使工具流程执行成功，也需要核对结果属于哪个请求，再检查内容是否满足任务。
''')
    example(chapters[16], 'AI 数据：同样长度，先按 ID 对齐再计算', '''
    predictions = [
        {"id": "s1", "prediction": 1},
        {"id": "s2", "prediction": 0},
        {"id": "s3", "prediction": 1},
    ]
    labels = [
        {"id": "s2", "label": 0},
        {"id": "s3", "label": 1},
        {"id": "s1", "label": 1},
    ]

    positional_correct = 0
    for prediction, label in zip(predictions, labels, strict=True):
        if prediction["prediction"] == label["label"]:
            positional_correct += 1
    print(f"按位置得到的误算值：{positional_correct / len(predictions):.1%}")

    # 本例固定数据已确认 ID 唯一且两边完全一致；迁移题再验证这些前提。
    label_by_id = {}
    for row in labels:
        label_by_id[row["id"]] = row["label"]

    aligned = []
    for row in predictions:
        sample_id = row["id"]
        aligned.append({"id": sample_id,
                        "prediction": row["prediction"],
                        "label": label_by_id[sample_id]})

    correct = 0
    for row in aligned:
        print(row["id"], row["prediction"], row["label"])
        if row["prediction"] == row["label"]:
            correct += 1
    print(f"按 ID 对齐后的准确率：{correct / len(aligned):.1%}")
    ''', '''
    按位置得到的误算值：33.3%
    s1 1 1
    s2 0 0
    s3 1 1
    按 ID 对齐后的准确率：100.0%
    ''', '第一段故意演示错误关联，zip 的 strict 只检查长度。label_by_id 将 ID 与标签绑定，再遍历 predictions 保持原顺序；数值 0 也是有效类别。最后只在 aligned 上统计。整个示例仅处理内存中的模拟数据，不训练或调用模型。',
    '先做正文的顺序与单项改写。随后思考：若 labels 多出一个重复 s2，这个固定数据演示为何不能检测它？先不要沿用字典覆盖，转到习题写出重复检查。')
    chapters[16]['checkpoint'].append('我能在长度相同但顺序不同的数据中，按唯一 ID 对齐并拒绝缺失或重复。')
    exercise(chapters[16], 'AI / Agent：把乱序结果配回原请求', '迁移',
    '实现 attach_results(requests, results)。输入为列表；每个请求字典有 id、question，每个结果字典有 id、answer。前提：id 是非空字符串，question 与 answer 是字符串（允许空串），所需键都存在；字段类型不属于本题验证范围。两个列表各自的 id 必须唯一，而且两边 id 集合完全相同，否则抛 ValueError。两边都空返回 []。返回新的字典列表，每条只含 id、question、answer，按 requests 原顺序排列；不修改输入，不打印。用请求 r2/今天学什么？、r1/怎么复习？和结果 r1/闭卷重写、r2/练习字典，逐行打印返回的字典。',
    '先检查结果 ID 是否重复，再建立 result_by_id。另用集合收集请求 ID 并拒绝重复；用 set(result_by_id) 与请求 ID 集合比较。全部通过后，按 requests 遍历，用 ID 查答案并新建一条字典。', '''
    def attach_results(requests, results):
        result_by_id = {}
        for row in results:
            request_id = row["id"]
            if request_id in result_by_id:
                raise ValueError("结果 ID 重复")
            result_by_id[request_id] = row["answer"]

        request_ids = set()
        for row in requests:
            request_id = row["id"]
            if request_id in request_ids:
                raise ValueError("请求 ID 重复")
            request_ids.add(request_id)
        if request_ids != set(result_by_id):
            raise ValueError("请求与结果的 ID 不一致")

        joined = []
        for row in requests:
            joined.append({"id": row["id"], "question": row["question"],
                           "answer": result_by_id[row["id"]]})
        return joined

    requests = [{"id": "r2", "question": "今天学什么？"},
                {"id": "r1", "question": "怎么复习？"}]
    results = [{"id": "r1", "answer": "闭卷重写"},
               {"id": "r2", "answer": "练习字典"}]
    for row in attach_results(requests, results):
        print(row)
    ''', '''
    {'id': 'r2', 'question': '今天学什么？', 'answer': '练习字典'}
    {'id': 'r1', 'question': '怎么复习？', 'answer': '闭卷重写'}
    ''', '查找表是 r1→闭卷重写、r2→练习字典；请求遍历顺序是 r2、r1，所以先输出 r2。不能按结果的到达顺序配，也不能把字典强行排序后当作原请求顺序。set(result_by_id) 取键集合；先拒绝重复，避免集合去重把错误藏起来。相同问题可以有不同 ID，仍是两条请求。空答案在题设中允许，它只表示返回了空字符串，不能据此宣布任务完成。这是本地关联模拟，不会发送请求或调用 Agent。',
    tests='''
    import copy
    requests = [{"id": "b", "question": "同一个问题"}, {"id": "a", "question": "同一个问题"}]
    results = [{"id": "a", "answer": "A"}, {"id": "b", "answer": "B"}]
    expected = [{"id": "b", "question": "同一个问题", "answer": "B"},
                {"id": "a", "question": "同一个问题", "answer": "A"}]
    before = copy.deepcopy((requests, results))
    joined = attach_results(requests, results)
    assert joined == expected, "按请求顺序查 ID，不能按位置或 ID 排序"
    assert attach_results(requests, results[::-1]) == expected
    assert attach_results([], []) == []
    assert attach_results([{"id": "x", "question": ""}], [{"id": "x", "answer": ""}]) == [{"id": "x", "question": "", "answer": ""}]
    assert attach_results([{"id": "x", "question": "Q", "source": "local"}], [{"id": "x", "answer": "A", "ms": 0}]) == [{"id": "x", "question": "Q", "answer": "A"}]
    assert (requests, results) == before
    joined[0]["answer"] = "只改返回字典"
    joined[1]["question"] = "只改返回问题"
    joined.append({"id": "extra"})
    assert (requests, results) == before, "返回的新字典与列表不能改动输入"
    assert attach_results(requests, results) == expected, "调用间不能保留上次状态"
    bad_pairs = [
        (requests, results[:1]),
        (requests[:1], results),
        (requests, [{"id": "a", "answer": "A"}, {"id": "z", "answer": "Z"}]),
        (requests + [requests[0].copy()], results),
        (requests, results + [results[0].copy()]),
        (requests, [{"id": "a", "answer": "A"}, {"id": "a", "answer": "别的答案"}]),
        ([], results), (requests, []),
    ]
    for left, right in bad_pairs:
        original = copy.deepcopy((left, right))
        try:
            attach_results(left, right)
        except ValueError:
            pass
        else:
            raise AssertionError("重复或不一致的 ID 必须拒绝")
        assert (left, right) == original, "失败也不能污染输入"
    import contextlib, io
    capture = io.StringIO()
    with contextlib.redirect_stdout(capture):
        attach_results(requests, results)
    assert capture.getvalue() == "", "返回数据，打印交给调用者"
    ''')
