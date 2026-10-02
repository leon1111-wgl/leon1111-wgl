# Guoliang | Original learning example
# Probability: choose the denominator
# Python 3.12+ | Run: python probability-counts-first-steps.py
all_days = 10
rainy_days = 4
alerted_days = 5
rainy_alerted_days = 3
print("rain:", rainy_days / all_days)
print("rain given alert:", rainy_alerted_days / alerted_days)
print("alert given rain:", rainy_alerted_days / rainy_days)
