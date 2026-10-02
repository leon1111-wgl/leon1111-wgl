# Guoliang | Original learning example
# Inspect rounding and total delay
# Python 3.12+ | Run: python inference-pipelines-pipeline-budget.py
values = [0.12, 0.26, 0.91]
step = 0.1
encoded = [round(value / step) for value in values]
restored = [number * step for number in encoded]
errors = [abs(a - b) for a, b in zip(values, restored)]
print("encoded:", encoded)
print("restored:", [round(x, 2) for x in restored])
print(f"largest error={max(errors):.2f}")
print("serial latency ms:", sum([4, 7, 2]))
