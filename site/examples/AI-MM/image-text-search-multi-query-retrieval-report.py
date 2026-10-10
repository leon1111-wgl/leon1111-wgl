# Leon | Original learning example
# Evaluate retrieval with several relevant results per query
# Python 3.12+ | Run: python image-text-search-multi-query-retrieval-report.py
from math import isclose

def retrieval_report(queries, k):
    if k <= 0:
        raise ValueError("positive k required")
    recalls, hits, reciprocal = [], [], []
    found_total = relevant_total = unscored = 0
    for ranked, relevant in queries:
        ranked = list(dict.fromkeys(ranked))  # Preserve the first occurrence.
        relevant = set(relevant)
        if not relevant:
            unscored += 1
            continue
        found = len(set(ranked[:k]) & relevant)
        recalls.append(found / len(relevant))
        hits.append(int(found > 0))
        first = next((i for i, item in enumerate(ranked, 1) if item in relevant), None)
        reciprocal.append(1 / first if first is not None else 0.0)
        found_total += found
        relevant_total += len(relevant)
    count = len(recalls)
    if not count:
        return {"scored": 0, "unscored": unscored, "macro_recall": None,
                "micro_recall": None, "hit_rate": None, "mrr": None}
    return {"scored": count, "unscored": unscored,
            "macro_recall": sum(recalls) / count,
            "micro_recall": found_total / relevant_total,
            "hit_rate": sum(hits) / count,
            "mrr": sum(reciprocal) / count}

queries = [(["a", "a", "x", "b"], {"a", "b"}),
           (["z", "c", "d"], {"c"}),
           (["x", "z"], set())]
report = retrieval_report(queries, 2)
assert isclose(report["macro_recall"], 0.75)
assert isclose(report["micro_recall"], 2 / 3)
assert report["hit_rate"] == 1.0 and report["mrr"] == 0.75
assert retrieval_report([([], {"a"})], 2)["mrr"] == 0.0
assert retrieval_report([([], set())], 2)["macro_recall"] is None
print(f"scored: {report['scored']}; unscored: {report['unscored']}")
for metric in ["macro_recall", "micro_recall", "hit_rate", "mrr"]:
    print(f"{metric}: {report[metric]:.6f}")
