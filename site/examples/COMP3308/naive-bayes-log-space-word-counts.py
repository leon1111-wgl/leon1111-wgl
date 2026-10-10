# Leon | Original learning example
# Keep long-text likelihoods in log space
# Python 3.12+ | Run: python naive-bayes-log-space-word-counts.py
from math import exp, log, isclose

vocabulary = ["red", "round", "blue"]
counts = {"A": {"red": 3, "round": 1, "blue": 0},
          "B": {"red": 0, "round": 1, "blue": 3}}

def log_scores(document):
    result = {}
    for label, words in counts.items():
        denominator = sum(words.values()) + len(vocabulary)
        score = log(0.5)
        for word in vocabulary:
            probability = (words[word] + 1) / denominator
            score += document.get(word, 0) * log(probability)
        result[label] = score
    return result

def posterior(scores):
    largest = max(scores.values())
    weights = {label: exp(value - largest) for label, value in scores.items()}
    total = sum(weights.values())
    return {label: value / total for label, value in weights.items()}

short = {"red": 2, "round": 1}
scores = log_scores(short)
probabilities = posterior(scores)
assert isclose(probabilities["A"], 16 / 17)
print(f"short P(A|text): {probabilities['A']:.6f}")
long = {word: count * 1000 for word, count in short.items()}
long_scores = log_scores(long)
print("raw scores underflow:", [exp(x) == 0 for x in long_scores.values()])
print("log-space winner:", max(long_scores, key=long_scores.get))
assert isclose(sum(posterior(long_scores).values()), 1.0)
