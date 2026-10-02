# Guoliang | Original learning example
# Find and check the top two
# Python 3.12+ | Run: python image-text-search-search-ranking.py
query = [1.0, 0.0]
images = {"kite": [0.8, 0.6], "umbrella": [1.0, 0.0], "kite-detail": [0.6, 0.8]}
scores = {name: sum(q * x for q, x in zip(query, vector)) for name, vector in images.items()}
ranked = sorted(scores, key=scores.get, reverse=True)
top_two = ranked[:2]
relevant = {"kite", "kite-detail"}
recall = len(set(top_two) & relevant) / len(relevant)
print("ranking:", ranked)
print(f"Recall@2={recall:.2f}")
