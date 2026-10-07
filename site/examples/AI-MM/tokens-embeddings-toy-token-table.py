# Leon | Original learning example
# Look up and pool two tokens
# Python 3.12+ | Run: python tokens-embeddings-toy-token-table.py
text = "red kite"
tokens = text.split()
vocabulary = {"red": 0, "kite": 1}
embedding_table = [[1.0, 0.0], [0.0, 2.0]]
ids = [vocabulary[token] for token in tokens]
vectors = [embedding_table[token_id] for token_id in ids]
pooled = [sum(vector[j] for vector in vectors) / len(vectors) for j in range(2)]
print("tokens:", tokens)
print("IDs:", ids)
print("pooled:", pooled)
