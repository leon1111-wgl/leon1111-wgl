# Guoliang | Original learning example
# Test three known colours
# Python 3.12+ | Run: python colour-channels-red-channel-rule.py
pixels = {"marker": (200, 40, 30), "paper": (220, 220, 220), "shade": (60, 20, 20)}
for name, (red, green, blue) in pixels.items():
    margin = red - max(green, blue)
    print(name, "margin:", margin, "selected:", margin > 50)
