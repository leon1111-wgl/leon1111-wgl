# Leon | Original learning example
# Return an answer with its evidence ID
# Python 3.12+ | Run: python multimodal-rag-retrieve-cite.py
query = set("model opening upward".split())
records = [
    {"id": "sheet-A", "terms": "model opening upward arrow", "answer": "arrow-marked opening", "page": 2, "region": "diagram-A"},
    {"id": "sheet-B", "terms": "model paint dry", "answer": None, "page": 3, "region": "paragraph-B"},
]
def overlap(record):
    return len(query & set(record["terms"].split()))
best = max(records, key=overlap)
print("retrieval score:", overlap(best))
if best["answer"] is not None:
    print("answer:", best["answer"])
    print("evidence:", best["id"], "page", best["page"], best["region"])
else:
    print("No checked answer in the retrieved evidence")
