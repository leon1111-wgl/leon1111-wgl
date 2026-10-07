# Leon | Original learning example
# Follow one channel
# Python 3.12+ | Run: python pixels-contracts-pixel-scale.py
bgr = [255, 0, 0]
rgb = list(reversed(bgr))
value = 153
scaled = value / 255
standardized = (scaled - 0.5) / 0.25
print("RGB:", rgb)
print(f"scaled={scaled:.1f}; standardized={standardized:.1f}")
print("stored numbers:", 4 * 6 * 3)
